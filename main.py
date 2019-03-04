import wx

from mainwindow import MainWindow


def cmd_exit(events):
    exit(0)


def init(window):
    w = MainWindow
    if True:
        w = window
    w.cmd_exit.Bind( wx.EVT_LEFT_DOWN, cmd_exit)


if __name__ == "__main__":

    app = wx.App()
    w = MainWindow(None)

    init(w)

    w.Show()
    app.MainLoop()
