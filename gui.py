import wx
import wx.grid as grid
import data

class panel1(wx.Panel):
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent = parent)

        # ---------------- Grid section ---------------- #
        mock = data.mock_list
        rows = len(mock);
        print("Mock lenght = " + str(rows))
        myGrid = grid.Grid(self)
        myGrid.CreateGrid(rows, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(myGrid, 1, wx.EXPAND)
        self.SetSizer(sizer)
        # ---------------- End of Grid section ---------------- #

class panel2(wx.Panel):
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent = parent)
        #super(MyPanel, self).__init__(parent)

        self.label = wx.StaticText(self, label = "Target set", pos = (150, 10))

        # Adding label, combobox's and binding methods to eax combo
        for i in range(1, 5):
            self.label = wx.StaticText(self, label = str(i), pos = (5, i * 30))
            self.combo = wx.ComboBox(self, choices = data.cases, pos = (20, i * 30), name = "Combo "+ str(i))
            # self.Bind(wx.EVT_COMBOBOX, self.OnCombo)
        print('end of loop')

        self.button = wx.Button(self, label = "Save target Params", pos = (10, 150), name = "btnSave")
        self.button = wx.Button(self, label = "Reset and Clear", pos = (150, 150), name = "btnReset")

        # Test label
        self.label2 = wx.StaticText(self, label = "", pos = (50,80))

        #OnCombo selected
        def OnCombo(self, event):
            self.label2.SetLabel("You Like " + self.combobox.GetValue())

        # Save frame settings
        def onSave(self, event):
            print("Pending")

        # Clear selected combos and checkboxes
        def onReset(self, event):
            print("Pending")
        

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Graphical User Interface")
 
        splitter = wx.SplitterWindow(self)
        leftP = panel1(splitter)
        rightP = panel2(splitter)
 
        # split the window
        splitter.SplitVertically(leftP, rightP)
        splitter.SetMinimumPaneSize(20)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        

        # ---------- Old MyFrame's constructor ----------- #
        #super(MyFrame, self).__init__(parent, title = title)

        #self.panel = MyPanel(self)
        # ------------------------------------------------ #

#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()