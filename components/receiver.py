import abc


class Receiver(abc.ABC):
    @abc.abstractmethod
    def receive_signal(self, code: str, value: int):
        pass


def test():
    class myR(Receiver):
        def receive_signal(self, code: str, value: int):
            pass

    try:
        myR()
    except TypeError as e:
        print("test success:", e)
    else:
        raise AssertionError("Error should have been raised instantiating")


if __name__ == "__main__":
    test()
