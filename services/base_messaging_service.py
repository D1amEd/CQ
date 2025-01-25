
from abc import ABC, abstractmethod

class BaseMessagingService(ABC):
    @abstractmethod
    def send_message(self, message: str):
        pass