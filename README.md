# 国内用户 HuggingFace 高速下载

利用 HuggingFace 官方的下载工具 [huggingface-cli](https://huggingface.co/docs/huggingface_hub/guides/download#download-from-the-cli) 和 [hf_transfer](https://github.com/huggingface/hf_transfer) 从[镜像网站](https://hf-mirror.com/)上对HuggingFace上的模型和数据集进行高速下载。

## Usage
推荐先手动安装huggingface-cli和hf_transfer：
```bash
pip install -U huggingface_hub
pip install -U hf-transfer
```

用法如下:

**（1）下载模型**

以 `lmsys/vicuna-7b-v1.5` 模型为例：

```bash
python hf_download.py --model lmsys/vicuna-7b-v1.5 --save_dir ./hf_hub
```
- 默认使用 hf-transfer 进行加速(会导致不显示进度条)，如需进度条请添加`--use_hf_transfer False`，但会降低下载速度。
- 下载后的文件会保存在`--save_dir`指定对目录下，使用transformers库加载时需要指定保存后的路径，例如：
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
 - `--use_hf_transfer`: 使用 hf-transfer 进行加速下载，默认开启(True), 开启将不显示进度条。如果下载报错, 可以尝试设置为False。
 - `--use_mirror`: 从镜像站 https://hf-mirror.com/ 下载, 默认开启(True), 国内用户建议开启


 ## Reference

https://hf-mirror.com/

https://zhuanlan.zhihu.com/p/663712983
