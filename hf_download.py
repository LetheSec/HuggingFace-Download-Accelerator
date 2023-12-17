"""
@File         :hf_download.py
@Description  :Download huggingface models and datasets from mirror site.
@Author       :Xiaojian Yuan
"""


import argparse
import os
import sys

# Check if huggingface_hub is installed, if not, install it
try:
    import huggingface_hub
except ImportError:
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
    "--include",
    default=None,
    type=str,
    help="Specify the file to be downloaded",
)
parser.add_argument(
    "--exclude",
    default=None,
    type=str,
    help="Files you don't want to download",
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
    default=None,
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
    # Check if hf_transfer is installed, if not, install it
    try:
        import hf_transfer
    except ImportError:
        print("Install hf_transfer.")
        os.system("pip install -U hf-transfer -i https://pypi.org/simple")
    # Enable hf-transfer if specified
    os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
    print("export HF_HUB_ENABLE_HF_TRANSFER=", os.getenv("HF_HUB_ENABLE_HF_TRANSFER"))


if args.model is None and args.dataset is None:
    print(
        "Specify the name of the model or dataset, e.g., --model baichuan-inc/Baichuan2-7B-Chat"
    )
    sys.exit()
elif args.model is not None and args.dataset is not None:
    print("Only one model or dataset can be downloaded at a time.")
    sys.exit()

if args.use_mirror:
    # Set default endpoint to mirror site if specified
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    print("export HF_ENDPOINT=", os.getenv("HF_ENDPOINT"))  # https://hf-mirror.com


if args.token is not None:
    token_option = "--token %s" % args.token
else:
    token_option = ""

if args.include is not None:
    include_option = "--include %s" % args.include
else:
    include_option =  ""
    
if args.exclude is not None:
    exclude_option = "--exclude %s" % args.exclude
else:
    exclude_option = ""
    
    
if args.model is not None:
    model_name = args.model.split("/")
    save_dir_option = ""
    if args.save_dir is not None:
        if len(model_name) > 1:
            save_path = os.path.join(
                args.save_dir, "models--%s--%s" % (model_name[0], model_name[1])
            )
        else:
            save_path = os.path.join(
                args.save_dir, "models--%s" % (model_name[0])
            )
        save_dir_option = "--local-dir %s" % save_path

    download_shell = (
        "huggingface-cli download %s %s %s --local-dir-use-symlinks False --resume-download %s %s"
        % (token_option, include_option, exclude_option, args.model, save_dir_option)
    )
    os.system(download_shell)

elif args.dataset is not None:
    dataset_name = args.dataset.split("/")
    save_dir_option = ""
    if args.save_dir is not None:
        if len(dataset_name) > 1:
            save_path = os.path.join(
                args.save_dir, "datasets--%s--%s" % (dataset_name[0], dataset_name[1])
            )
        else:
            save_path = os.path.join(
                args.save_dir, "datasets--%s" % (dataset_name[0])
            )
        save_dir_option = "--local-dir %s" % save_path

    download_shell = (
        "huggingface-cli download %s %s %s --local-dir-use-symlinks False --resume-download  --repo-type dataset %s %s"
        % (token_option, include_option, exclude_option, args.dataset, save_dir_option)
    )
    os.system(download_shell)
