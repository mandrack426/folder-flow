import os
import tempfile
from infrastructure.file_system import LocalFolderCreator


def test_folder_creation():

    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "teste")

        creator = LocalFolderCreator()
        creator.create_folder(path)

        assert os.path.exists(path)