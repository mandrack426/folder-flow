import os
from domain.interfaces import FolderCreatorInterface


class LocalFolderCreator(FolderCreatorInterface):

    def create_folder(self, path: str) -> None:
        os.makedirs(path, exist_ok=True)