from abc import ABC, abstractmethod


class Speech2TextInterface(ABC):
    @abstractmethod
    def transcribe(self, local_path: str, return_raw: bool = True):
        ...