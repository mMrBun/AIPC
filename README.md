<div align="center">
<h1>Chat2BI</h1>
</div>



## Changelog

- 2023.12.14 Optimize ECHARTS_PROMPT to improve the success rate of chart rendering. tag:[#5](https://github.com/mMrBun/Chat2BI/issues/5)
- 2023.12.14 Change `model.generate()` to `model.chat()`. tag:[#6](https://github.com/mMrBun/Chat2BI/issues/6)

## Roadmap
- [ ] Support api server [#3](https://github.com/mMrBun/Chat2BI/issues/3)


## Quick Start

Place the retrieval model in the retriever/retriever_model directory.

|      Model       |                                                              Download                                                              |
|:----------------:|:----------------------------------------------------------------------------------------------------------------------------------:|
|   MrBun/ToolRetrieval_IR_bert_based_chinese    |                          [🤗HuggingFace](https://huggingface.co/MrBun/ToolRetrieval_IR_bert_based_chinese)                           |

```bash
git clone https://github.com/mMrBun/Chat2BI.git

conda create -n Chat2BI python=3.10

conda activate Chat2BI

cd Chat2BI

pip install -r requirements.txt

python web_server/web_demo.py
```

view the web demo at http://127.0.0.1:7860
