from abc import ABCMeta, abstractmethod


class QueryClient(metaclass=ABCMeta):

    @abstractmethod
    def query(self, prompt: str) -> str:
        pass
