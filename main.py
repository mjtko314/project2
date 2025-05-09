from logic import *

def main():
    """
    Displays the GUI window
    """
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()

if __name__ == '__main__':
    main()