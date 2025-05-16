class LineAnalyzerController:
    """
    Analyzes a code's content to count physical lines of code.
    """

    def count_physical_lines(self, content):
        """
        Counts the number of physical lines of code,
        ignoring blank lines, comments, and docstrings.
        """
        physical_line_count = 0
        in_docstring = False

        for line in content:
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
    
    def count_methods(self, content):
        """
        Counts the number of methods in a class,
        considering only  method definitions.
        """
        methods_count = 0 

        for line in content:
            stripped_line = line.strip()

            if stripped_line.startswith("def "):
                methods_count += 1
       
        return methods_count   

    def extract_class(self, content):
        """
        Extract the name class of each file.
        """
        for line in content:
            stripped_line = line.strip()

            if stripped_line.startswith("class "):
                class_name = line[6:-2]
                return class_name
            
        return "No class" 
    
    def get_all_data(self, content):
        """
        Get all data from the file.
        """
        physical_lines = self.count_physical_lines(content)
        methods = self.count_methods(content)
        class_name = self.extract_class(content)

        return class_name, physical_lines, methods