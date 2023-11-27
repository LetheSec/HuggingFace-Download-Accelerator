"""
@File         :hf_download.py
@Description  :Download huggingface models and datasets from mirror site.
@Author       :Xiaojian Yuan
"""


import argparse
import importlib
import os
import sys

if importlib.util.find_spec("huggingface_hub") is None:
    print("Install huggingface_hub.")
    os.system("pip install -U huggingface_hub")


parser = argparse.ArgumentParser(description="HuggingFace Download Accelerator Script.")
parser.add_argument(
    "--model",
    "-M",
    default=None,
    type=str,
    help="model name in huggingface, e.g., baichuan-inc/Baichuan2-7B-Chat",
)
parser.add_argument(
    "--token",
    "-T",
    default=None,
    type=str,
    help="hugging face access token for download meta-llama/Llama-2-7b-hf, e.g., hf_***** ",
)
parser.add_argument(
    "--dataset",
    "-D",
    default=None,
    type=str,
    help="dataset name in huggingface, e.g., zh-plus/tiny-imagenet",
)
parser.add_argument(
    "--save_dir",
    "-S",
    default="./hf_hub",
    type=str,
    help="path to be saved after downloading.",
)
parser.add_argument(
    "--use_hf_transfer", default=True, type=eval, help="Use hf-transfer, default: True"
)
parser.add_argument(
    "--use_mirror", default=True, type=eval, help="Download from mirror, default: True"
)

args = parser.parse_args()

if args.use_hf_transfer:
    if importlib.util.find_spec("hf_transfer") is None:
        print("Install hf_transfer.")
        os.system("pip install -U hf-transfer")

    os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
    print("HF_HUB_ENABLE_HF_TRANSFER: ", os.getenv("HF_HUB_ENABLE_HF_TRANSFER"))

if args.model is None and args.dataset is None:
    print(
        "Specify the name of the model or dataset, e.g., --model baichuan-inc/Baichuan2-7B-Chat"
    )
    sys.exit()
elif args.model is not None and args.dataset is not None:
    print("Only one model or dataset can be downloaded at a time.")
    sys.exit()

if args.use_mirror:
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    print("HF_ENDPOINT: ", os.getenv("HF_ENDPOINT"))  # https://hf-mirror.com

if args.model is not None:
    author_name, model_name = args.model.split("/")
    save_path = os.path.join(
        args.save_dir, "models--%s--%s" % (author_name, model_name)
    )
    #
    if args.token is not None:
        download_shell = (
            "huggingface-cli download --token %s --local-dir-use-symlinks False --resume-download %s --local-dir %s"
            % (args.token, args.model, save_path)
        )
    else:
        download_shell = (
            "huggingface-cli download --local-dir-use-symlinks False --resume-download %s --local-dir %s"
            % (args.model, save_path)
        )
    os.system(download_shell)

elif args.dataset is not None:
    author_name, dataset_name = args.dataset.split("/")
    save_path = os.path.join(
        args.save_dir, "datasets--%s--%s" % (author_name, dataset_name)
    )

    download_shell = (
        "huggingface-cli download --local-dir-use-symlinks False --resume-download  --repo-type dataset %s --local-dir %s"
        % (args.dataset, save_path)
    )
    os.system(download_shell)
