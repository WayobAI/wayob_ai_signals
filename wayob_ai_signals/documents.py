import os

from elasticsearch import Elasticsearch
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import (
    DocumentCompressorPipeline,
    EmbeddingsFilter,
    LLMChainFilter,
)
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.document_loaders import (
    AsyncHtmlLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_transformers import EmbeddingsRedundantFilter
from langchain_core.prompts import PromptTemplate
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)

from .constants import (
    AI_TOKEN,
    ELASTIC_HOST_DEV,
    ELASTIC_PASSWORD,
    ELASTIC_USER,
    INDEX_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    QUERY_PROMPT_TEMPLATE
)

os.environ["OPENAI_API_KEY"] = AI_TOKEN


def get_vectorstore():
    embeddings = OpenAIEmbeddings(api_key=AI_TOKEN)
    es_store = ElasticsearchStore(
        embedding=embeddings,
        index_name=INDEX_NAME,
        es_user=ELASTIC_USER,
        es_password=ELASTIC_PASSWORD,
        es_url=ELASTIC_HOST_DEV,
    )

    return es_store


def load_urls(urls: list[str]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    loader = AsyncHtmlLoader(urls)
    documents = loader.load_and_split(text_splitter=text_splitter)

    es_store = get_vectorstore()
    es_store.add_documents(documents)

    return None


def load_documents(document_paths: list[str]):
    documents = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    for document_path in document_paths:
        _, ext = os.path.splitext(document_path)
        if ext == ".pdf":
            loader = PyPDFLoader(document_path)
        elif ext == ".csv":
            loader = CSVLoader(document_path)
        elif ext == ".txt":
            loader = TextLoader(document_path)
        else:
            print(f"Unsupported file type: {ext}")
            continue

        docs = loader.load_and_split(text_splitter=text_splitter)

        documents.extend(docs)

    es_store = get_vectorstore()
    es_store.add_documents(documents)

    return None


def multi_query_retriever(es_store: ElasticsearchStore):
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template=QUERY_PROMPT_TEMPLATE,
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    base_retriever = MultiQueryRetriever.from_llm(
        retriever=es_store.as_retriever(),
        prompt=QUERY_PROMPT,
        llm=llm,
        include_original=True,
    )

    # More adavanced code retriever missing

    return base_retriever
