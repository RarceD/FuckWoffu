from abc import ABC, abstractmethod


class ISignInManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def sign_in(self) -> bool:
        pass

    @abstractmethod
    def get_holiday(self):
        pass
