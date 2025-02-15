from abc import ABC, abstractmethod


class AbstractService(ABC):
    @abstractmethod
    async def add(self, **kwargs):
        pass

    @abstractmethod
    async def update(self, **kwargs):
        pass

    @abstractmethod
    async def delete(self, **kwargs):
        pass

    @abstractmethod
    async def get(self, **kwargs):
        pass
