import logging

from Views.FileLineCounterView import FileLineCounterView
from Controllers.FileLineCounterController import FileLineCounterController
from Models.FileLineCounterModel import FileLineCounterModel

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Starting application...")
    controller = FileLineCounterController()
    view = FileLineCounterView(controller)
    model = FileLineCounterModel(controller)

    controller.set_file_line_counter_view(view)
    controller.set_file_line_counter_model(model)

    view.mainloop()
    logging.info("Application finished...")

if __name__ == "__main__":
    main()
