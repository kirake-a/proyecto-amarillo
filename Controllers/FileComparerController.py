from pathlib import Path
from difflib import unified_diff
from difflib import SequenceMatcher

from Utils.Constants import THRESHOLD

class FileComparerController:
    """
    Controller class for comparing two Python
    project directories.
    Identifies added and removed lines
    for each file.
    """

    def compare_files(self, old_version_file: Path, new_version_file: Path):
        if not old_version_file.exists() or not new_version_file.exists():
            raise FileNotFoundError("One or both files do not exist.")

        with old_version_file.open('r') as \
        ovfile, new_version_file.open('r') as nvfile:
            old_lines = ovfile.readlines()
            new_lines = nvfile.readlines()

        num_added_lines = num_removed_lines = 0

        for line in unified_diff(old_lines, new_lines, lineterm=''):
            if line.startswith('+') and not line.startswith('+++'):
                num_added_lines += 1
            elif line.startswith('-') and not line.startswith('---'):
                num_removed_lines += 1

        return num_added_lines, num_removed_lines

    def add_modification_comments(self, old_file: Path, new_file: Path):
        with old_file.open('r') as f1, new_file.open('r') as f2:
            old_lines = f1.readlines()
            new_lines = f2.readlines()

        sm = SequenceMatcher(None, old_lines, new_lines)

        with old_file.open('w') as outf_old, new_file.open('w') as outf_new:
            for tag, i1, i2, j1, j2 in sm.get_opcodes():

                if tag == 'equal':
                    outf_old.writelines(old_lines[i1:i2])
                    outf_new.writelines(new_lines[j1:j2])

                elif tag == 'replace':
                    # Modified Lines: tratamos cada par (vieja, nueva)
                    for old, new in zip(old_lines[i1:i2], new_lines[j1:j2]):
                        outf_old.write('# Deleted Line\n')
                        outf_old.write(old)

                        etiqueta = self.__set_exchange_rate_tags(old, new)
                        outf_new.write(f'# Added Line: {etiqueta}\n')
                        outf_new.write(new)

                    # Si hay desbalance en número de líneas, procesar sobrantes:
                    extra_old = old_lines[i1:i2][len(new_lines[j1:j2]):]
                    extra_new = new_lines[j1:j2][len(old_lines[i1:i2]):]
                    for old in extra_old:
                        outf_old.write('# Deleted Line: Major change\n')
                        outf_old.write(old)
                    for new in extra_new:
                        outf_new.write('# Added Line: Major change\n')
                        outf_new.write(new)

                elif tag == 'delete':
                    # Deleted lines: Solo estaban en old_file
                    for old in old_lines[i1:i2]:
                        outf_old.write('# Deleted Line\n')
                        outf_old.write(old)

                elif tag == 'insert':
                    # Added lines: Solo estaban en new_file
                    for new in new_lines[j1:j2]:
                        outf_new.write('# Added Line\n')
                        outf_new.write(new)
        
    def __set_exchange_rate_tags(
        self,
        old_line: str,
        new_line: str,
    ) -> str:
        ovline = old_line.rstrip('\n')
        nvline = new_line.rstrip('\n')
        
        if not ovline:
            return "  # major change"
        
        avg_length = (len(ovline) + len(nvline)) / 2
        diff = abs(len(nvline) - len(ovline)) / avg_length
        tag = "  # major change" if diff >= THRESHOLD else "  # minor change"

        return tag