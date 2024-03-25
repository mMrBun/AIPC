from sentence_transformers import SentenceTransformer, util
from .utils import process_retrieval_document


class ToolRetrieverLoader:
    def __init__(self, model_path=""):
        self.model_path = model_path

    def build_retrieval_embedder(self):
        embedder = SentenceTransformer(self.model_path, device="cuda")
        return embedder


class ToolRetrieverEmbedder:
    def __init__(self, model_loader_instance, defined_tools):
        self.embedder = model_loader_instance.build_retrieval_embedder()
        self.tools = defined_tools
        self.corpus, self.corpus2tool = self.build_retrieval_corpus()
        self.corpus_embeddings = self.build_corpus_embeddings()

    def build_retrieval_corpus(self):
        corpus, corpus2tool = process_retrieval_document(self.tools[1])
        corpus_ids = list(corpus.keys())
        corpus = [corpus[cid] for cid in corpus_ids]
        return corpus, corpus2tool

    def build_corpus_embeddings(self):
        corpus_embeddings = self.embedder.encode(self.corpus, convert_to_tensor=True)
        return corpus_embeddings

    def retrieving(self, query, top_k=5):
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(
            query_embedding,
            self.corpus_embeddings,
            top_k=top_k,
            score_function=util.cos_sim,
        )
        retrieved_tools = []
        for rank, hit in enumerate(hits[0]):
            tool = self.corpus2tool[
                self.corpus[hit["corpus_id"]]
            ]
            retrieved_tools.append(tool)
        return retrieved_tools

    def do_retrieve(self, query, top_k):
        result = self.retrieving(query, top_k=top_k)
        return result
