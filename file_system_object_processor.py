import pwd
import stat
from pathlib import Path


class FileSystemObjectProcessor:
    # raises ValueError in the case that conformance has been violated
    def process(self, dictionary: dict) -> None:
        name = dictionary['name']
        attributes = dictionary['attributes']

        if attributes.get('path') is not None:
            path = Path(attributes['path'])

            if not path.exists():
                raise ValueError(f'{name}: {path} does not exist')

            # 'owner' and 'mode' require 'path'. if you don't have path ...
            if attributes.get('owner') is not None:
                owner = attributes['owner']
                stat_info = path.stat()
                declared_owner = pwd.getpwuid(stat_info.st_uid).pw_name

                if not declared_owner == owner:
                    raise ValueError(f'{name}: {path} does not belong to {owner}')

            if attributes.get('mode') is not None:
                expected_mode = attributes['mode']
                stat_info = path.stat()
                actual_mode = stat.S_IMODE(stat_info.st_mode)

                try:
                    expected_mode_int = int(expected_mode, 8)

                    if not actual_mode == expected_mode_int:
                        raise ValueError(f'{name}: modes differ: {oct(expected_mode)} != {oct(actual_mode)}')
                except Exception as e:
                    raise ValueError(f'error occurred while converting {expected_mode} to octal: {str(e)}')

        return None
