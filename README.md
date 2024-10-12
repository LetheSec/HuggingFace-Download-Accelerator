# 国内用户 HuggingFace 高速下载

利用 HuggingFace 官方的下载工具 [huggingface-cli](https://huggingface.co/docs/huggingface_hub/guides/download#download-from-the-cli) 和 [hf_transfer](https://github.com/huggingface/hf_transfer) 从 [HuggingFace 镜像站](https://hf-mirror.com/)上对模型和数据集进行高速下载。

> 此脚本只是对 [huggingface-cli](https://huggingface.co/docs/huggingface_hub/guides/download#download-from-the-cli) 的一个简单封装，本意是方便本人自己的习惯使用，如果有对更高级功能的需求，请参考 [官方文档](https://huggingface.co/docs/huggingface_hub/guides/cli) 自行修改。另外，国内用户也可以参考 [HuggingFace 镜像站](https://hf-mirror.com/) 上提供的下载方式。

---
**12/17/2023 update:** 新增 `--include` 和 `--exlucde`参数，可以指定下载或忽略某些文件。

- 下载指定的文件: `--include "tokenizer.model tokenizer_config.json"`
- 下载某一类文件: `--include "*.bin"`
- 不下载指定文件: `--exclude "*.md"`
- 也可以同时使用: `--include "*.json" --exclude "config.json"`


## Usage


### 下载模型

从HuggingFace上获取到所需模型名，例如 `lmsys/vicuna-7b-v1.5`：

```bash
python hf_download.py --model lmsys/vicuna-7b-v1.5 --save_dir ./hf_hub
```
如果下载需要授权的模型，例如 meta-llama 系列，则需要指定 `--token` 参数为你的 Huggingface Access Token。

**注意事项：**

（1）若指定了 `--save_dir`，下载过程中会将文件先暂存在 transformers 的默认路径`~/.cache/huggingface/hub`中，下载完成后自动移动到`--save_dir`指定目录下，因此需要在下载前保证默认路径下有足够容量。 

下载完成后使用 transformers 库加载时需要指定保存后的路径，例如：
```python
from transformers import pipeline
pipe = pipeline("text-generation", model="./hf_hub/models--lmsys--vicuna-7b-v1.5")
```
**若不指定 `--save_dir` 则会下载到默认路径`~/.cache/huggingface/hub`中，这时调用模型可以直接使用模型名称 `lmsys/vicuna-7b-v1.5`。**

（2）若不想在调用时使用绝对路径，又不希望将所有模型保存在默认路径下，可以通过**软链接**的方式进行设置，步骤如下：
- 先在任意位置创建目录，作为下载文件的真实存储位置，例如：
    ```bash
    mkdir /data/huggingface_cache
    ```
- 若 transforms 已经在默认位置 `~/.cache/huggingface/hub` 创建了目录，需要先删除：
    ```bash
    rm -r ~/.cache/huggingface
    ```
- 创建软链接指向真实存储目录：
    ```bash
    ln -s /data/huggingface_cache ~/.cache/huggingface
    ``` 
- 之后运行下载脚本时**不要指定** `save_dir`，会自动下载至第一步创建的目录下：
    ```bash
    python hf_download.py --model lmsys/vicuna-7b-v1.5
    ```
- 通过这种方式，调用模型时可以直接使用模型名称，而不需要使用存储路径：
    ```bash
    from transformers import pipeline
    pipe = pipeline("text-generation", model="lmsys/vicuna-7b-v1.5")
    ```

（3）脚本内置通过 pip 自动安装 huggingface-cli 和 hf_transfer。如果 hf_transfer 版本低于 0.1.4 则不会显示下载进度条，可以手动更新：
```
pip install -U hf-transfer -i https://pypi.org/simple
```
如出现 `huggingface-cli: error` 问题，尝试重新安装：
```
pip install -U huggingface_hub
```
如出现关于 `hf_transfer`的报错，可以通过`--use_hf_transfer False`参数关闭hf_transfer。


### 下载数据集

和下载模型同理，以 `zh-plus/tiny-imagenet` 为例:
```bash
python hf_download.py --dataset zh-plus/tiny-imagenet --save_dir ./hf_hub
```

### 参数说明
 -  `--model`: huggingface上要下载的模型名称，例如 `--model lmsys/vicuna-7b-v1.5`
 - `--dataset`: huggingface上要下载的数据集名称，例如 `--dataset zh-plus/tiny-imagenet`
 - `--save_dir`: 文件下载后实际的存储路径
 - `--token`: 下载需要登录的模型（Gated Model），例如`meta-llama/Llama-2-7b-hf`时，需要指定hugginface的token，格式为`hf_****`
 - `--use_hf_transfer`: 使用 hf-transfer 进行加速下载，默认开启(True), 若版本低于开启将不显示进度条。
 - `--use_mirror`: 从镜像站 https://hf-mirror.com/ 下载, 默认开启(True), 国内用户建议开启
- `--include`: 下载指定的文件，例如 `--include "tokenizer.model tokenizer_config.json"` 或 `--include "*.bin` 下载
- `--exclude`: 不下载指定的文件，与include用法一致，例如 `--exclude "*.md"`
