from pathlib import Path
from difflib import unified_diff
from difflib import SequenceMatcher

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
                    outf_old.writelines(line.rstrip('\n') + '  # Line deleted\n' for line in old_lines[i1:i2])
                    outf_new.writelines(line.rstrip('\n') + '  # Line added\n' for line in new_lines[j1:j2])

                elif tag == 'delete':
                    outf_old.writelines(line.rstrip('\n') + '  # Line deleted\n' for line in old_lines[i1:i2])

                elif tag == 'insert':
                    outf_new.writelines(line.rstrip('\n') + '  # Line added\n' for line in new_lines[j1:j2])
