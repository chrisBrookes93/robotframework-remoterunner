from io import open
import logging
import os
import re
from robot.libraries import STDLIBS
from robot.utils.robotpath import find_file
import six

from rfremoterunner.utils import read_file_from_disk

logger = logging.getLogger(__file__)
IMPORT_LINE_REGEX = '(Resource|Library)([\\s]+)([^[\\n\\r]*)([\\s]+)'


class RobotFileProcessor:

    def __init__(self, source):
        self._modified_file_lines = []

        if isinstance(source, six.string_types):
            self.file_path = source
            self.is_test_suite = False
        else:
            self.file_path = source.source
            self.is_test_suite = True

        with open(self.file_path, 'r', encoding='utf-8') as file_handle:
            self._file_lines = file_handle.readlines()

    def get_updated_file_data(self):
        return ''.join(self._modified_file_lines)

    def process_dependencies(self, dependency_cache):
        self._modified_file_lines = []

        for line in self._file_lines:
            matches = re.search(IMPORT_LINE_REGEX, line)
            if matches and len(matches.groups()) == 4:
                imp_type = matches.group(1)
                whitespace_sep = matches.group(2)
                res_path = matches.group(3)
                filename = os.path.basename(res_path)
                line_ending = matches.group(4)

                self._modified_file_lines.append(imp_type + whitespace_sep + filename + line_ending)

                if filename not in dependency_cache and res_path.strip() not in STDLIBS:
                    # Rebuild with the adjusted path
                    full_path = find_file(res_path, os.path.dirname(self.file_path), imp_type)

                    if imp_type == 'Library':
                        dependency_cache[filename] = read_file_from_disk(full_path)
                    else:
                        RobotFileProcessor(full_path).process_dependencies(dependency_cache)
            else:
                self._modified_file_lines.append(line)

        if not self.is_test_suite:
            dependency_cache[os.path.basename(self.file_path)] = self.get_updated_file_data()
