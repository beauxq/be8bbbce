import abc


class Receiver(abc.ABC):
    @abc.abstractmethod
    def receive_signal(self, code: str, value: int) -> None:
        pass
