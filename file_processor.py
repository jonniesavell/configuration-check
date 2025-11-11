from pathlib import Path
from file_system_object_processor import FileSystemObjectProcessor

class FileProcessor:
    def __init__(self, file_system_object_processor: FileSystemObjectProcessor):
        self.file_system_object_processor = file_system_object_processor

    def process(self, dictionary: dict) -> None:
        name = dictionary['name']
        configured_type = dictionary['type']

        if not configured_type == 'file':
            raise RuntimeError(f'configuration error: {name} is not of type file')

        self.file_system_object_processor.process(dictionary)

        attributes = dictionary['attributes']
        path = Path(attributes['path'])

        if not path.is_file():
            raise ValueError(f'{name} is not a file')

        return None
