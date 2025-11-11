import sys
from pathlib import Path

import yaml

from file_system_object_processor import FileSystemObjectProcessor
from directory_processor import DirectoryProcessor
from file_processor import FileProcessor
from service_processor import SystemDServiceProcessor


def load_checks_one_by_one(path):
    buffer = []
    in_check = False

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.lstrip().startswith('- name:'):
                if buffer:
                    result = yaml.safe_load('\n'.join(buffer))
                    yield result[0]
                    buffer = []
                in_check = True
            if in_check:
                buffer.append(line.rstrip())

        if buffer:
            result = yaml.safe_load('\n'.join(buffer))
            yield result[0]

def main():
    path = Path(sys.argv[1])

    # configuration based upon type
    configuration = dict()
    file_system_object_processor = FileSystemObjectProcessor()
    directory_processor = DirectoryProcessor(file_system_object_processor)
    file_processor = FileProcessor(file_system_object_processor)
    configuration['directory'] = directory_processor
    configuration['file'] = file_processor
    service_processor = SystemDServiceProcessor()
    configuration['service'] = service_processor

    for check in load_checks_one_by_one(path):
        # print(f'{type(check)}: {check}')
        if check.get('name') is None:
            raise RuntimeError(f'attribute name is not defined')
        else:
            name = check['name']

            if check.get('type') is None:
                raise RuntimeError(f'{name}: attribute type is not defined')
            else:
                declared_type = check['type']

                if not declared_type in configuration:
                    raise RuntimeError(f'misconfiguration: {name}: type {declared_type} is not configured')
                else:
                    configuration[declared_type].process(check)

if __name__ == '__main__':
    main()
