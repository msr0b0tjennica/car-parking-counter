from abc import ABC, abstractmethod

class BaseVideoSource(ABC):
    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def release(self):
        pass