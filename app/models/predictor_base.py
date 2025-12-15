from abc import ABC, abstractmethod


class BasePredictor(ABC):

    @abstractmethod
    def train(self, data, config):
        ...

    @abstractmethod
    def predict(self, data):
        ...


    @abstractmethod
    def save(self, path: str):
        ...


    @classmethod
    @abstractmethod
    def load(cls, path: str):
        ...