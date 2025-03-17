class FileLineCounterModel:
    """Model class responsible for storing and managing file line count."""

    def __init__(self, file_line_counter_controller):
        """
        Initializes the FileLineCounterModel.
        """
        self.__file_line_counter_controller = file_line_counter_controller
        self.__line_count_results = None

    def set_line_count_results(self, line_count_results):
        """
        Sets the line count results and notifies the controller of the update.
        """
        self.__line_count_results = line_count_results
        self.inform_changes_to_controller()

    def get_line_count_results(self):
        """Returns the stored line count results.
        """
        return self.__line_count_results

    def inform_changes_to_controller(self):
        """Notifies the controller that the model's data has changed."""
        self.__file_line_counter_controller.manage_model_changes()
