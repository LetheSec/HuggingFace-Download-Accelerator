# 国内用户 HuggingFace 高速下载

利用 HuggingFace 官方的下载工具 [huggingface-cli](https://huggingface.co/docs/huggingface_hub/guides/download#download-from-the-cli) 和 [hf_transfer](https://github.com/huggingface/hf_transfer) 从 [HuggingFace 镜像站](https://hf-mirror.com/)上对模型和数据集进行高速下载。

## Usage

用法如下:

**（1）下载模型**

从HuggingFace上获取到所需模型名，例如 `lmsys/vicuna-7b-v1.5`：

```bash
python hf_download.py --model lmsys/vicuna-7b-v1.5 --save_dir ./hf_hub
```
- 脚本内置通过 pip 自动安装 huggingface-cli 和 hf_transfer，若用户之前更换过pip源，那么可能安装的不是最新版本。
- 默认开启 hf-transfer 进行加速(版本低于0.1.4则会不显示进度条, 可手动更新版本)。此时如需进度条请添加`--use_hf_transfer False`，但可能会降低下载速度。
- 下载过程中文件会先暂存在默认路径`~/.cache/huggingface/hub`中，下载完成后自动移动到`--save_dir`指定对目录下。因此需要在下载前保证 `~/.cache/huggingface/hub` 有足够容量，也可以通过设置 `export HF_HOME=/xxx/xxx/` 变量改变默认路径。
- 使用transformers库加载时需要指定保存后的路径，例如：
```python
from transformers import pipeline
pipe = pipeline("text-generation", model="./hf_hub/models--lmsys--vicuna-7b-v1.5")
```

**（2）下载数据集**

以 `zh-plus/tiny-imagenet` 为例:
```bash
python hf_download.py --dataset zh-plus/tiny-imagenet --save_dir ./hf_hub
```

**（3）参数说明**
 -  `--model`: huggingface上要下载的模型名称，例如 `--model lmsys/vicuna-7b-v1.5`
 - `--dataset`: huggingface上要下载的数据集名称，例如 `--dataset zh-plus/tiny-imagenet`
 - `--save_dir`: 文件下载后实际的存储路径
 - `--token`: 下载需要登录的模型（Gated Model），例如`meta-llama/Llama-2-7b-hf`时，需要指定hugginface的token，格式为`hf_****`
 - `--use_hf_transfer`: 使用 hf-transfer 进行加速下载，默认开启(True), 开启将不显示进度条。
 - `--use_mirror`: 从镜像站 https://hf-mirror.com/ 下载, 默认开启(True), 国内用户建议开启

--- 
**可能的问题：**
- 如果第一次运行出错，可以尝试手动安装huggingface-cli和hf_transfer（若不是官方pip源，可能不是最新版本）：
```bash
pip install -U huggingface_hub
pip install -U hf-transfer
```
- 如果某次下载中断，再次运行脚本时，出现卡住或报错的现象，可以尝试删除`save_dir`和`HF_HOME`中的之前下载的模型文件，然后重新运行脚本进行下载。
