import os
from domain.services import build_folder_name


class CreateFolderUseCase:

    def __init__(self, repository, folder_creator):
        self.repository = repository
        self.folder_creator = folder_creator

    def execute(self, barcode: str, base_path: str):

        product = self.repository.get_by_barcode(barcode)

        if not product:
            raise ValueError("Código de barra não encontrado.")

        folder_name = build_folder_name(product)
        full_path = os.path.join(base_path, folder_name)

        self.folder_creator.create_folder(full_path)

        return product, folder_name, full_path