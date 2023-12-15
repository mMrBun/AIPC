from fastapi import Body
from configs import RETRIEVE_MODEL_PATH
from retriever.build_retriever import ToolRetrieverLoader, ToolRetrieverEmbedder
from core import BaseResponse
from core.build_tools.utils import get_tsv_callable_path, get_model_class


def function_calling(
        query: str = Body(..., description="问题", examples=["你好"]),
        top_k: int = Body(..., description="检索api的数量", examples=[5]),
        top_p: float = Body(..., description="", examples=[1]),
        temperature: float = Body(..., description="", examples=[0.9]),
        model_type: str = Body(..., description="模型类型", examples=["ChatGLM3", "Qwen"])
):
    # done 根据tenant_id和project_id获取配置文件路径
    corpus_tsv_path, tool_root_dir = get_tsv_callable_path()
    # done 根据问题使用build_retriever做语义相似查询，返回top_k条记录当作大模型的TOOLS
    retrieve_loader = ToolRetrieverLoader(model_path=RETRIEVE_MODEL_PATH)
    retrieve_embedder = ToolRetrieverEmbedder(tool_root_dir=tool_root_dir,
                                              model_loader_instance=retrieve_loader,
                                              corpus_tsv_path=corpus_tsv_path)
    tools_dict = retrieve_embedder.do_retrieve(query=query, top_k=top_k)

    api_list = tools_dict.get('api_list')
    # done 根据配置文件选择初始化哪个大模型
    model_class = get_model_class(model_type)
    class_instance = model_class()

    response, code, history = class_instance.do_chat(query=query,
                                                     history=[],
                                                     top_p=top_p,
                                                     temperature=temperature,
                                                     tools_description_path=api_list,
                                                     tools_callable_path=tool_root_dir)
    return BaseResponse(code=200,
                        msg="工具初始化成功",
                        data={
                            "response": response,
                            "code": code,
                            "history": history
                        })
