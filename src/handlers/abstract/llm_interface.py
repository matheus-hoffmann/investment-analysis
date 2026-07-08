from abc import ABC, abstractmethod


class LLMInterface(ABC):
    @abstractmethod
    def set_llm(self):
        ...

    @abstractmethod
    def set_embedding(self, model: str = ''):
        ...
    
    @abstractmethod
    def invoke(self, text: str):
        ...
    
    @abstractmethod
    def embed_query(self, text: str, model: str = ''):
        ...