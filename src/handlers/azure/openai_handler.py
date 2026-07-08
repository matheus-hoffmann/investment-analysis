import os
from openai import OpenAI
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

from src.handlers.abstract.llm_interface import LLMInterface


class AzureOpenAIHandler(LLMInterface):
    def __init__(self):
        super().__init__()
    
    def set_embedding(self):
        model = model if model != '' else "text-embedding-ada-002"
        return AzureOpenAIEmbeddings(azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
                                     api_key=os.getenv('AZURE_OPENAI_API_KEY'),
                                     model=os.getenv('AZURE_OPENAI_EMBEDDING_NAME', "text-embedding-ada-002"))

    def embed_query(self, text: str):
        return self.set_embedding(model=os.getenv('AZURE_OPENAI_EMBEDDING_NAME', "text-embedding-ada-002")).embed_query(text)
    
    def set_llm(self):
        return OpenAI(
            base_url=os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_key=os.getenv('AZURE_OPENAI_API_KEY')
        )

    def invoke(self, text):
        completion = self.set_llm().chat.completions.create(
        model=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
        messages=[
                {
                    "role": "user",
                    "content": text,
                }
            ],
        )

        return completion.choices[0].message.content
