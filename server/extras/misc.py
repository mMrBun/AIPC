import gc
import os
from typing import Tuple, TYPE_CHECKING

import torch
from transformers import LogitsProcessorList, InfNanRemoveLogitsProcessor, is_torch_xpu_available, \
    is_torch_npu_available
from transformers.utils import is_torch_mps_available, is_torch_cuda_available, is_torch_bf16_gpu_available
from transformers.utils.versions import require_version

from server.extras.logging import get_logger

if TYPE_CHECKING:
    from server.hparams import ModelArguments
logger = get_logger(__name__)

_is_fp16_available = is_torch_npu_available() or is_torch_cuda_available()
try:
    _is_bf16_available = is_torch_bf16_gpu_available()
except Exception:
    _is_bf16_available = False

def torch_gc() -> None:
    r"""
    Collects GPU memory.
    """
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


def get_logits_processor() -> "LogitsProcessorList":
    r"""
    Gets logits processor that removes NaN and Inf logits.
    """
    logits_processor = LogitsProcessorList()
    logits_processor.append(InfNanRemoveLogitsProcessor())
    return logits_processor


def get_device_count() -> int:
    r"""
    Gets the number of available GPU devices.
    """
    if not torch.cuda.is_available():
        return 0

    return torch.cuda.device_count()


def use_modelscope() -> bool:
    return bool(int(os.environ.get("USE_MODELSCOPE_HUB", "0")))


def count_parameters(model: torch.nn.Module) -> Tuple[int, int]:
    r"""
    Returns the number of trainable parameters and number of all parameters in the model.
    """
    trainable_params, all_param = 0, 0
    for param in model.parameters():
        num_params = param.numel()
        # if using DS Zero 3 and the weights are initialized empty
        if num_params == 0 and hasattr(param, "ds_numel"):
            num_params = param.ds_numel

        # Due to the design of 4bit linear layers from bitsandbytes, multiply the number of parameters by 2
        if param.__class__.__name__ == "Params4bit":
            if hasattr(param, "quant_storage") and hasattr(param.quant_storage, "itemsize"):
                num_bytes = param.quant_storage.itemsize
            else:
                num_bytes = 1

            num_params = num_params * 2 * num_bytes

        all_param += num_params
        if param.requires_grad:
            trainable_params += num_params

    return trainable_params, all_param


def get_current_device() -> torch.device:
    r"""
    Gets the current available device.
    """
    if is_torch_xpu_available():
        device = "xpu:{}".format(os.environ.get("LOCAL_RANK", "0"))
    elif is_torch_npu_available():
        device = "npu:{}".format(os.environ.get("LOCAL_RANK", "0"))
    elif is_torch_mps_available():
        device = "mps:{}".format(os.environ.get("LOCAL_RANK", "0"))
    elif is_torch_cuda_available():
        device = "cuda:{}".format(os.environ.get("LOCAL_RANK", "0"))
    else:
        device = "cpu"

    return torch.device(device)


def try_download_model_from_ms(model_args: "ModelArguments") -> None:
    if not use_modelscope() or os.path.exists(model_args.model_name_or_path):
        return

    try:
        from modelscope import snapshot_download

        revision = "master" if model_args.model_revision == "main" else model_args.model_revision
        model_args.model_name_or_path = snapshot_download(
            model_args.model_name_or_path, revision=revision, cache_dir=model_args.cache_dir
        )
    except ImportError:
        raise ImportError("Please install modelscope via `pip install modelscope -U`")


def check_dependencies() -> None:
    if int(os.environ.get("DISABLE_VERSION_CHECK", "0")):
        logger.warning("Version checking has been disabled, may lead to unexpected behaviors.")
    else:
        require_version("transformers>=4.37.2", "To fix: pip install transformers>=4.37.2")
        require_version("datasets>=2.14.3", "To fix: pip install datasets>=2.14.3")
        require_version("accelerate>=0.27.2", "To fix: pip install accelerate>=0.27.2")
        require_version("trl>=0.8.1", "To fix: pip install trl>=0.8.1")


def infer_optim_dtype(model_dtype: torch.dtype) -> torch.dtype:
    r"""
    Infers the optimal dtype according to the model_dtype and device compatibility.
    """
    if _is_bf16_available and model_dtype == torch.bfloat16:
        return torch.bfloat16
    elif _is_fp16_available:
        return torch.float16
    else:
        return torch.float32