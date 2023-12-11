# Chat2BI

## Quick Start

Place the retrieval model in the retriever/retriever_model directory.

|      Model       |                                                              Download                                                              |
|:----------------:|:----------------------------------------------------------------------------------------------------------------------------------:|
|   MrBun/ToolRetrieval_IR_bert_based_chinese    |                          [HuggingFace](https://huggingface.co/MrBun/ToolRetrieval_IR_bert_based_chinese)                           |

```bash
git clone https://github.com/mMrBun/Chat2BI.git

conda create -n Chat2BI python=3.10

conda activate Chat2BI

cd Chat2BI

pip install -r requirements.txt

python web_server/web_demo.py
```
view the web demo at http://127.0.0.1:7860
