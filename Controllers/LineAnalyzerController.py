class LineAnalyzerController:
    """
    Analyzes a code's content to count physical lines of code.
    """

    def __init__(self, content):
        """
        Initializes the LineAnalyzerController with the code content.
        """
        self.__content = content

    def count_physical_lines(self):
        """
        Counts the number of physical lines of code,
        ignoring blank lines, comments, and docstrings.
        """
        physical_line_count = 0
        in_docstring = False

        for line in self.__content:
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
    
    def count_methods(self):
        """
        Counts the number of methods in a class,
        considering only  method definitions.
        """
        methods_count = 0 

        for line in self.__content:
            stripped_line = line.strip()

            if stripped_line.startswith("def "):
                methods_count += 1
       
        return methods_count   

    def extract_class(self):
        """
        Extract the name class of each file.
        """
        for line in self.__content:
            stripped_line = line.strip()

            if stripped_line.startswith("class "):
                class_name = line[6:-2]
                return class_name
            
        return "No class" 