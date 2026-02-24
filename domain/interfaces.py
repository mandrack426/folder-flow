from abc import ABC, abstractmethod
from domain.entities import Product


class ProductRepositoryInterface(ABC):

    @abstractmethod
    def get_by_barcode(self, barcode: str) -> Product | None:
        pass


class FolderCreatorInterface(ABC):

    @abstractmethod
    def create_folder(self, path: str) -> None:
        pass