import re


class LineAnalyzerController:
    """
    Analyzes a file's content to count physical and logical lines of code.
    """

    def __init__(self, file_content):
        """
        Initializes the LineAnalyzerController with file content.
        """
        self.__file_content = file_content

    def count_physical_file_lines(self):
        """
        Counts the number of physical lines of code in the file,
        ignoring blank lines, comments, and docstrings.
        """
        physical_line_count = 0
        in_docstring = False

        for line in self.__file_content:
            stripped_line = line.strip()

            if not stripped_line or stripped_line.startswith("#"):
                continue

            if (stripped_line.startswith('"""') and
                stripped_line.endswith('"""') and
                    len(stripped_line) > 3):
                continue

            if stripped_line.startswith('"""'):
                in_docstring = not in_docstring
                continue

            if in_docstring:
                continue

            physical_line_count += 1

        return physical_line_count

    def count_logical_file_lines(self):
        """
        Counts the number of logical lines of code in the file,
        considering only control statements, method definitions,
          and class definitions.
        Counts nested control structures (e.g., if inside a for).
        Handles multiple control structures in the same line.
        """
        logical_line_count = 0
        in_docstring = False

        for line in self.__file_content:
            stripped_line = line.strip()

            if not stripped_line or stripped_line.startswith("#"):
                continue

            if (stripped_line.startswith('"""') and
                stripped_line.endswith('"""') and
                    len(stripped_line) > 3):
                continue

            if stripped_line.startswith('"""'):
                in_docstring = not in_docstring
                continue

            if in_docstring:
                continue
            
            if stripped_line.startswith("elif"):
                continue

            if stripped_line.startswith(
                "class ") or stripped_line.startswith("def "):
                logical_line_count += 1
                continue

            control_keywords = ["if ", "for ", "while ","do while ",
                                "try: ", "switch "]
            
            stripped_no_strings = re.sub(
                r'(["\'])(?:\\.|(?!\1).)*\1', '', stripped_line)
    
            for keyword in control_keywords:
                if keyword in stripped_no_strings:
                    logical_line_count += 1

        return logical_line_count
    