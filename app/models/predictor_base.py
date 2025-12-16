from abc import ABC, abstractmethod


class BasePredictor(ABC):

    @abstractmethod
    def train(self, data, config):
        """Train the predictor on `data` using `config`.

        Implementations should persist any trained model to `self` so that
        `predict` can be called on the same instance.
        """
        raise NotImplementedError("train must be implemented by subclasses")

    @abstractmethod
    def predict(self, data):
        """Return predictions for `data`.

        The exact return format is predictor-specific (e.g. DataFrame,
        dict with thresholds, etc.).
        """
        raise NotImplementedError("predict must be implemented by subclasses")


    @abstractmethod
    def save(self, path: str):
        """Save model artifacts to `path` so they can be reloaded later."""
        raise NotImplementedError("save must be implemented by subclasses")


    @classmethod
    @abstractmethod
    def load(cls, path: str):
        """Load model artifacts from `path` and return an instance."""
        raise NotImplementedError("load must be implemented by subclasses")