import logging

import customtkinter as ctk

from pathlib import Path
from Utils.Constants import THRESHOLD

logging.basicConfig(level=logging.INFO)

class FileLineCounterView(ctk.CTk):
    """
    A GUI for counting physical lines and methods per class in Python files.

    This class provides an interface for the user to input a file path and
    retrieve metrics about the physical lines and methods per class
    of code in a Python project.
    It renders the necessary UI elements, including a file entry, button,
    and result display.
    """

    def __init__(self, file_line_counter_controller):
        """
        Initializes the FileLineCounterView with the given controller.
        """
        super().__init__()

        self.title("FileLineCounter")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.__create_widgets()
        self.__file_line_counter_controller = file_line_counter_controller

    def __create_widgets(self):
        """
        Creates all the elements of the UI, including:
        - Header text
        - File path entry text box
        - Button to retrieve file metrics
        These elements are placed in the main frame of the window.
        """
        self.header = ctk.CTkLabel(
            self.main_frame,
            text="Enter the paths for the " \
            "previous and current project versions",
            font=("Helvetica", 24, "bold"),
        )
        self.header.pack(pady=(40, 20))

        self.old_path_entry = ctk.CTkEntry(
            self.main_frame,
            width=300,
            height=45,
            placeholder_text="Previous version path...",
        )
        self.old_path_entry.pack(pady=10)
    
        self.new_path_entry = ctk.CTkEntry(
            self.main_frame,
            width=300,
            height=45,
            placeholder_text="Current version path...",
        )
        self.new_path_entry.pack(pady=10)

        self.file_button = ctk.CTkButton(
            self.main_frame,
            text="Compare versions",
            command=self.process_file_path_from_user,
            width=300,
            height=45,
            corner_radius=10,
        )
        self.file_button.pack(pady=10)

    def process_file_path_from_user(self):
        """
        Handles the button click event to process the file path entered
        by the user.

        This method retrieves the file path from the input field and
        calls the controllerto process the file and calculate the metrics.

        If the file path is not valid, it displays an error message.
        """
        new_file_path = self.new_path_entry.get().strip()
        old_file_path = self.old_path_entry.get().strip()

        if new_file_path and old_file_path:
            self.__file_line_counter_controller.process_file_path(
                old_file_path,
                new_file_path
            )
        else:
            self.file_label = ctk.CTkLabel(
                self.main_frame,
                text="No valid files in the folder",
                text_color="red"
            )
            self.file_label.pack()

    def show_metric_results(self, metric_results):
        """
        Displays the metric results in a new window.
        This method generates a new window containing a scrollable table
        displaying the filename along with its physical line and methods 
        counts.
        """
        self.__create_result_window()
        canvas, table_frame = self.__create_scrollable_table()

        self.__populate_table_headers(table_frame)
        self.__populate_table_data(table_frame, metric_results)

        table_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def __create_result_window(self):
        """
        Creates a new window to display the results of the metrics.
        This window contains a table where the results will be shown.
        """
        old_path_name = self.get_folder_name(
            self.old_path_entry.get().strip()
        )
        new_path_name = self.get_folder_name(
            self.new_path_entry.get().strip()
        )
        custom_title = f"{old_path_name} vs {new_path_name}"
        self.result_window = ctk.CTkToplevel(self)
        self.result_window.title(custom_title)
        self.result_window.geometry("600x400")

        title_label = ctk.CTkLabel(
            self.result_window,
            text="Comparing " + custom_title,
            font=("Helvetica", 20, "bold"),
            text_color="white"
        )
        title_label.pack(pady=(20, 10))

    def __create_scrollable_table(self):
        """
        Creates a scrollable table for displaying metric results.
        Adds both vertical and horizontal scrollbars.
        """
        outer_frame = ctk.CTkFrame(self.result_window)
        outer_frame.pack(fill="both", expand=True)

        canvas = ctk.CTkCanvas(outer_frame)
        canvas.pack(side="left", fill="both", expand=True)

        v_scrollbar = ctk.CTkScrollbar(outer_frame, command=canvas.yview)
        v_scrollbar.pack(side="right", fill="y")

        h_scrollbar = ctk.CTkScrollbar(self.result_window, command=canvas.xview, orientation="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")

        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        table_frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=table_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        table_frame.bind("<Configure>", on_frame_configure)

        return canvas, table_frame

    def __populate_table_headers(self, table_frame):
        """
        Adds headers to the result table.

        The table headers include 'Filename', 'Class',
        'Total Methods', 'Physical Lines per Class'
        and 'Total Physical Lines in the Program'.
        """
        headers = ["File", "Class", "Methods", 
                    "Physical Lines", "Deleted Lines",
                    "Added Lines", "Major Changes"
                ]
        row_padding, col_padding = 5, 10

        for col_index, header in enumerate(headers):
            ctk.CTkLabel(
                table_frame,
                text=header,
                font=("Helvetica", 14, "bold"),
            ).grid(row=0, column=col_index, padx=col_padding,
                   pady=row_padding)

    def __populate_table_data(self, table_frame, metric_results):
        """
        Populates the result table with the metric data.

        This method iterates over the metric results and displays
        the filename along with its corresponding physical line counts,
        methods counts and the total number of physical lines
        in the proyect.
        """
        row_padding, col_padding = 5, 10

        for row_index, (file_name, metrics) in enumerate(
                metric_results.items(), start=1
        ):
            logging.info(f"DEBUG - {file_name} -> {metrics}")
            class_name, physical_count, method_count, added_lines, removed_lines = metrics
            has_changes = int(physical_count) * THRESHOLD < (
                int(added_lines) + int(removed_lines)
            )

            ctk.CTkLabel(table_frame, text=file_name).grid(
                row=row_index, column=0, padx=col_padding,
                pady=row_padding
            )
            ctk.CTkLabel(table_frame, text=class_name).grid(
                row=row_index, column=1, padx=col_padding,
                pady=row_padding
            )
            ctk.CTkLabel(table_frame, text=str(method_count)).grid(
                row=row_index, column=2, padx=col_padding,
                pady=row_padding
            )
            ctk.CTkLabel(table_frame, text=str(physical_count)).grid(
                row=row_index, column=3, padx=col_padding,
                pady=row_padding
            )
            ctk.CTkLabel(table_frame, text=str(added_lines)).grid(
                row=row_index, column=4, padx=col_padding,
                pady=row_padding
            )
            ctk.CTkLabel(table_frame, text=str(removed_lines)).grid(
                row=row_index, column=5, padx=col_padding,
                pady=row_padding
            )
            ctk.CTkLabel(table_frame, text=str(has_changes)).grid(
                row=row_index, column=6, padx=col_padding,
                pady=row_padding
            )

    def get_folder_name(self, path: str) -> str:
        """
        Returns the folder name from the given path.
        """
        return Path(path).name
                
    def set_controller(self, controller):
        """
        Sets the controller for handling file path processing
        and metric retrieval.
        """
        self.__file_line_counter_controller = controller