from PySide2 import QtWidgets
from shiboken2 import wrapInstance

def maya_main_window():
    '''
    Return Maya main window widget as a python object
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr),QtWidgets.QWidget)

class StandAloneWindow(QtWidgets.QWidget):
    wnd_instance = None

    def __init__(self):
        super(StandAloneWindow,self).__init__(parent=None)

        self.setWindowTitle("Stand Alone App")
        self.setMinimumSize(300,400)
        
        self.close_btn = QtWidgets.QPushButton("Close",self)
        self.close_btn.clicked.connect(self.close)

    @classmethod
    def display(cls):
        if not cls.wnd_instance:
            cls.wnd_instance = maya_main_window()

        if cls.isHidden():
            cls.wnd_instance.show()
        else:
            cls.wnd_instance.raise_()
            cls.wnd_instance.activatewindow()

if __name__ == "__main__":
    try:
        test_dialog.close() #pylint: disable=E0601
        test_dialog.deleteLater()
    except:
        pass

    test_dialog = StandAloneWindow()
    test_dialog.show()
