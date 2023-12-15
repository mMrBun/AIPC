import json
import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from retriever import (
    standardize,
    standardize_category,
    change_name,
    process_retrieval_ducoment,
)
from core.decorator.class_decorator import singleton


@singleton
class ToolRetrieverLoader:
    def __init__(self, model_path=""):
        self.model_path = model_path

        # self.embedder = self.build_retrieval_embedder()

    def build_retrieval_embedder(self):
        print("Building embedder...")
        embedder = SentenceTransformer(self.model_path, device="cuda")
        return embedder


class ToolRetrieverEmbedder:
    def __init__(self, model_loader_instance, corpus_tsv_path="", tool_root_dir="./core"):
        self.embedder = model_loader_instance.build_retrieval_embedder()
        self.corpus_tsv_path = corpus_tsv_path
        self.corpus, self.corpus2tool = self.build_retrieval_corpus()
        self.corpus_embeddings = self.build_corpus_embeddings()
        self.tool_root_dir = tool_root_dir

    def build_retrieval_corpus(self):
        print("Building corpus...")
        documents_df = pd.read_csv(self.corpus_tsv_path, sep="\t")
        corpus, corpus2tool = process_retrieval_ducoment(documents_df)
        corpus_ids = list(corpus.keys())
        corpus = [corpus[cid] for cid in corpus_ids]
        return corpus, corpus2tool

    def build_corpus_embeddings(self):
        print("Building corpus embeddings with embedder...")
        corpus_embeddings = self.embedder.encode(self.corpus, convert_to_tensor=True)
        return corpus_embeddings

    def retrieving(self, query, top_k=5, excluded_tools={}):
        print("Retrieving...")
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(
            query_embedding,
            self.corpus_embeddings,
            top_k=10 * top_k,
            score_function=util.cos_sim,
        )
        retrieved_tools = []
        for rank, hit in enumerate(hits[0]):
            category, tool_name, api_name = self.corpus2tool[
                self.corpus[hit["corpus_id"]]
            ].split("\t")
            category = standardize_category(category)
            tool_name = standardize(tool_name)  # standardizing
            api_name = change_name(standardize(api_name))  # standardizing
            if category in excluded_tools:
                if tool_name in excluded_tools[category]:
                    top_k += 1
                    continue
            tmp_dict = {
                "category": category,
                "tool_name": tool_name,
                "api_name": api_name,
            }
            retrieved_tools.append(tmp_dict)
        return retrieved_tools

    def retrieve_rapidapi_tools(self, query, top_k):
        retrieved_tools = self.retrieving(query, top_k=top_k)
        query_json = {"api_list": []}
        for tool_dict in retrieved_tools:
            if len(query_json["api_list"]) == top_k:
                break
            category = tool_dict["category"]
            tool_name = tool_dict["tool_name"]
            api_name = tool_dict["api_name"]
            if os.path.exists(self.tool_root_dir):
                if os.path.exists(os.path.join(self.tool_root_dir, category)):
                    if os.path.exists(
                            os.path.join(self.tool_root_dir, category, tool_name + ".json")
                    ):
                        query_json["api_list"].append(
                            {
                                "category_name": category,
                                "tool_name": tool_name,
                                "api_name": api_name,
                            }
                        )
        return query_json

    def fetch_api_json(self, query_json):
        data_dict = {"api_list": []}
        for item in query_json["api_list"]:
            cate_name = item["category_name"]
            tool_name = standardize(item["tool_name"])
            api_name = change_name(standardize(item["api_name"]))
            tool_json = json.load(
                open(
                    os.path.join(self.tool_root_dir, cate_name, tool_name + ".json"),
                    "r",
                    encoding='utf-8'
                )
            )
            append_flag = False
            api_dict_names = []
            for api_dict in tool_json["api_list"]:
                api_dict_names.append(api_dict["name"])
                pure_api_name = change_name(standardize(api_dict["name"]))
                if pure_api_name != api_name:
                    continue
                api_json = {}
                api_json["category_name"] = cate_name
                api_json["api_name"] = api_dict["name"]
                api_json["api_description"] = api_dict["description"]
                api_json["required_parameters"] = api_dict["required_parameters"]
                api_json["optional_parameters"] = api_dict["optional_parameters"]
                api_json["tool_name"] = tool_json["tool_name"]
                data_dict["api_list"].append(api_json)
                append_flag = True
                break
            if not append_flag:
                print(api_name, api_dict_names)
        return data_dict

    def do_retrieve(self, query, top_k):
        result = self.retrieve_rapidapi_tools(
            query=query,
            top_k=top_k,
        )
        data_dict = self.fetch_api_json(result)
        return data_dict
