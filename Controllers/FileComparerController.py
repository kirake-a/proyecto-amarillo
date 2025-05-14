from pathlib import Path
from difflib import unified_diff

class FileComparerController:
    """
    Controller class for comparing two Python
    project directories.
    Identifies added and removed lines
    for each file.
    """
    def compare_files2(self, old_version_file: Path, new_version_file: Path):
        if old_version_file and new_version_file:
            added_lines = 10
            removed_lines = 5

        return added_lines, removed_lines
    
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
    
    def __add_comments(self, old_version_file: Path, new_version_file: Path):
        if old_version_file and new_version_file:
            added_lines = 10
            removed_lines = 5

        return added_lines, removed_lines