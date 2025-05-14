import os
from typing import Dict, List, Tuple


class FileComparerController:
    """
    Controller class for comparing two Python project directories.
    Identifies added, removed, and unchanged lines for each file.
    """

    def compare_projects(
        self,
        previous_project_path: str,
        new_project_path: str
    ) -> Dict[str, Tuple[int, int]]:
        """
        Compares two project versions and returns a dictionary with
        counts of added and removed lines per file.

        :param previous_project_path: Path to the previous version of the project.
        :param new_project_path: Path to the new version of the project.
        :return: A dictionary where keys are filenames and values are tuples:
                 (added_lines, removed_lines)
        """
        results: Dict[str, Tuple[int, int]] = {}

        for dirpath, _, filenames in os.walk(new_project_path):
            for filename in filenames:
                if not filename.endswith(".py"):
                    continue

                rel_path = os.path.relpath(os.path.join(dirpath, filename), new_project_path)
                prev_file_path = os.path.join(previous_project_path, rel_path)
                new_file_path = os.path.join(new_project_path, rel_path)

                if not os.path.exists(prev_file_path):
                    # New file
                    added_lines = self.__count_lines_in_file(new_file_path)
                    results[rel_path] = (added_lines, 0)
                else:
                    added, removed = self.compare_files(prev_file_path, new_file_path)
                    results[rel_path] = (added, removed)

        # Archivos eliminados
        for dirpath, _, filenames in os.walk(previous_project_path):
            for filename in filenames:
                if not filename.endswith(".py"):
                    continue

                rel_path = os.path.relpath(os.path.join(dirpath, filename), previous_project_path)
                new_file_path = os.path.join(new_project_path, rel_path)

                if not os.path.exists(new_file_path):
                    removed_lines = self.__count_lines_in_file(os.path.join(dirpath, filename))
                    results[rel_path] = (0, removed_lines)

        return results

    def compare_files(self, old_file: str, new_file: str) -> Tuple[int, int]:
        with open(old_file, 'r', encoding='utf-8') as f1:
            old_lines = set(f1.readlines())

        with open(new_file, 'r', encoding='utf-8') as f2:
            new_lines = set(f2.readlines())

        added = len(new_lines - old_lines)
        removed = len(old_lines - new_lines)
        return added, removed

    def __count_lines_in_file(self, path: str) -> int:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return len(f.readlines())
        except Exception:
            return 0
