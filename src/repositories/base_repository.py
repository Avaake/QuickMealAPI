from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    async def create(self, **kwargs):
        pass

    @abstractmethod
    async def update(self, **kwargs):
        pass

    @abstractmethod
    async def delete(self, **kwargs):
        pass

    @abstractmethod
    async def find_single(self, **kwargs):
        pass
