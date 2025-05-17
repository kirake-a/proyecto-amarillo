from pathlib import Path
from difflib import unified_diff
from difflib import SequenceMatcher
import re

from Utils.Constants import THRESHOLD
from Utils.Constants import MAX_LINE_LENGTH

class FileComparerController:
    """
    Controller class for comparing and formatting Python source files.

    This controller provides functionality to:
    - Compare two versions of a file and count added or
        removed lines.
    - Annotate line-level differences between file versions
        with comments.
    - Tag modifications as 'major' or 'minor' based on configurable thresholds.
    - Format files to split overly long lines for better readability.

    Attributes:
        None
    """

    def compare_files(self, old_version_file: Path, new_version_file: Path):
        """
        Compare two files line-by-line and count the number of added and
        removed lines.

        Args:
            old_version_file (Path): The path to the original version of the file.
            new_version_file (Path): The path to the new version of the file.

        Returns:
            tuple[int, int]: A tuple containing the number of added and removed lines.
        """

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
        """
        Add inline comments to highlight modifications between two file versions.

        The old file receives comments indicating deleted lines, while the new file
        is annotated with added lines and a tag indicating the severity of the change
        (major or minor).

        Args:
            old_file (Path): Path to the original file.
            new_file (Path): Path to the new file.
        """
                
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
                    for old, new in zip(old_lines[i1:i2], new_lines[j1:j2]):
                        outf_old.write('# Deleted Line\n')
                        outf_old.write(old)

                        etiqueta = self.__set_exchange_rate_tags(old, new)
                        outf_new.write(f'# Added Line: {etiqueta}\n')
                        outf_new.write(new)

                    extra_old = old_lines[i1:i2][len(new_lines[j1:j2]):]
                    extra_new = new_lines[j1:j2][len(old_lines[i1:i2]):]
                    for old in extra_old:
                        outf_old.write('# Deleted Line: Major change\n')
                        outf_old.write(old)
                    for new in extra_new:
                        outf_new.write('# Added Line: Major change\n')
                        outf_new.write(new)

                elif tag == 'delete':
                    for old in old_lines[i1:i2]:
                        outf_old.write('# Deleted Line\n')
                        outf_old.write(old)

                elif tag == 'insert':
                    for new in new_lines[j1:j2]:
                        outf_new.write('# Added Line\n')
                        outf_new.write(new)
        
    def __set_exchange_rate_tags(
        self,
        old_line: str,
        new_line: str,
    ) -> str:
        """
        Determine the severity tag for a modified line.

        Calculates the difference in length between the old and new line, and compares it
        to a predefined threshold to assign either a 'major' or 'minor' change tag.

        Args:
            old_line (str): The original line.
            new_line (str): The modified line.

        Returns:
            str: A string tag indicating 'major change' or 'minor change'.
        """
        ovline = old_line.rstrip('\n')
        nvline = new_line.rstrip('\n')
        
        if not ovline:
            return "  # major change"
        
        avg_length = (len(ovline) + len(nvline)) / 2
        diff = abs(len(nvline) - len(ovline)) / avg_length
        tag = "  # major change" if diff >= THRESHOLD else "  # minor change"

        return tag

    def format_file_long_lines(self, file_path: Path) -> list[str]:
        """
        Format a file by splitting lines that exceed MAX_LINE_LENGTH.

        Long lines are split at the last space before the limit and continued on the next line
        with indentation preserved. A continuation character (`\\`) is added at the end
        of each broken line.

        Args:
            file_path (Path): Path to the file to be formatted.

        Returns:
            list[str]: The newly formatted lines.
        """

        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} does not exist.")

        with file_path.open("r", encoding="utf-8") as file_read:
            lines = file_read.readlines()

        formatted_lines = []

        for line in lines:
            line = line.rstrip('\n')
            indent = len(line) - len(line.lstrip(' '))
            indent_str = ' ' * indent

            while len(line) > MAX_LINE_LENGTH:
                split_pos = line.rfind(' ', 0, MAX_LINE_LENGTH)

                if split_pos <= indent:
                    split_pos = MAX_LINE_LENGTH

                part = line[:split_pos].rstrip()
                formatted_lines.append(part + ' \\\n')

                next_part = line[split_pos:].lstrip()

                if not next_part or next_part == line:
                    formatted_lines.append(indent_str + next_part + '\n')
                    break

                line = indent_str + next_part

            else:
                formatted_lines.append(line + '\n')

        with file_path.open("w", encoding="utf-8") as file_write:
            file_write.writelines(formatted_lines)

        return formatted_lines
