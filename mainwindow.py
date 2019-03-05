# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Dec 17 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class MainWindow
###########################################################################

class MainWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"XaaS Automation Script", pos = wx.DefaultPosition, size = wx.Size( 842,770 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bS_base = wx.BoxSizer( wx.VERTICAL )

		bS_header = wx.BoxSizer( wx.HORIZONTAL )

		self.i_logo = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"logo apct heigh 50.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bS_header.Add( self.i_logo, 0, wx.ALL, 5 )

		self.t_header = wx.StaticText( self, wx.ID_ANY, u"Direct Image Target Tool v 0.1", wx.Point( -1,-1 ), wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.t_header.Wrap( -1 )

		self.t_header.SetFont( wx.Font( 24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		bS_header.Add( self.t_header, 1, wx.EXPAND, 5 )


		bS_base.Add( bS_header, 0, wx.EXPAND, 5 )

		bS_body = wx.BoxSizer( wx.HORIZONTAL )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		bSizer6.SetMinSize( wx.Size( 450,-1 ) )
		self.g_layers = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.g_layers.CreateGrid( 0, 5 )
		self.g_layers.EnableEditing( True )
		self.g_layers.EnableGridLines( True )
		self.g_layers.EnableDragGridSize( False )
		self.g_layers.SetMargins( 0, 0 )

		# Columns
		self.g_layers.SetColSize( 0, 120 )
		self.g_layers.SetColSize( 1, 70 )
		self.g_layers.SetColSize( 2, 70 )
		self.g_layers.SetColSize( 3, 70 )
		self.g_layers.SetColSize( 4, 70 )
		self.g_layers.EnableDragColMove( False )
		self.g_layers.EnableDragColSize( False )
		self.g_layers.SetColLabelSize( 30 )
		self.g_layers.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.g_layers.EnableDragRowSize( True )
		self.g_layers.SetRowLabelSize( 80 )
		self.g_layers.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.g_layers.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		self.g_layers.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )

		bSizer6.Add( self.g_layers, 1, wx.ALL|wx.EXPAND, 3 )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer7.SetMinSize( wx.Size( -1,60 ) )
		self.cmd_save = wx.Button( self, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cmd_save.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )

		bSizer7.Add( self.cmd_save, 1, wx.ALL|wx.EXPAND, 3 )

		self.cmd_restore = wx.Button( self, wx.ID_ANY, u"Restore", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cmd_restore.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )

		bSizer7.Add( self.cmd_restore, 1, wx.ALL|wx.EXPAND, 3 )

		self.cmd_uncheck = wx.Button( self, wx.ID_ANY, u"None", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cmd_uncheck.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )

		bSizer7.Add( self.cmd_uncheck, 1, wx.ALL|wx.EXPAND, 3 )


		bSizer6.Add( bSizer7, 0, wx.EXPAND, 15 )


		bS_body.Add( bSizer6, 1, wx.EXPAND, 5 )

		bS_layers = wx.BoxSizer( wx.VERTICAL )

		self.t_sethead = wx.StaticText( self, wx.ID_ANY, u"Select Target Set", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.t_sethead.Wrap( -1 )

		self.t_sethead.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
		self.t_sethead.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )

		bS_layers.Add( self.t_sethead, 0, wx.ALL|wx.EXPAND, 5 )

		self.t_set1 = wx.StaticText( self, wx.ID_ANY, u"Target Set A", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.t_set1.Wrap( -1 )

		self.t_set1.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )

		bS_layers.Add( self.t_set1, 0, wx.ALL, 5 )

		c_set_aChoices = []
		self.c_set_a = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, c_set_aChoices, 0 )
		self.c_set_a.SetSelection( 0 )
		bS_layers.Add( self.c_set_a, 0, wx.ALL|wx.EXPAND, 5 )

		self.t_set2 = wx.StaticText( self, wx.ID_ANY, u"Target Set B", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.t_set2.Wrap( -1 )

		self.t_set2.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )

		bS_layers.Add( self.t_set2, 0, wx.ALL, 5 )

		c_set_bChoices = []
		self.c_set_b = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, c_set_bChoices, 0 )
		self.c_set_b.SetSelection( 0 )
		bS_layers.Add( self.c_set_b, 0, wx.ALL|wx.EXPAND, 5 )

		self.t_set3 = wx.StaticText( self, wx.ID_ANY, u"Target Set C", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.t_set3.Wrap( -1 )

		self.t_set3.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )

		bS_layers.Add( self.t_set3, 0, wx.ALL, 5 )

		c_set_cChoices = []
		self.c_set_c = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, c_set_cChoices, 0 )
		self.c_set_c.SetSelection( 0 )
		bS_layers.Add( self.c_set_c, 0, wx.ALL|wx.EXPAND, 5 )

		self.t_set4 = wx.StaticText( self, wx.ID_ANY, u"Target Set D", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.t_set4.Wrap( -1 )

		self.t_set4.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )

		bS_layers.Add( self.t_set4, 0, wx.ALL, 5 )

		c_set_dChoices = []
		self.c_set_d = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, c_set_dChoices, 0 )
		self.c_set_d.SetSelection( 0 )
		bS_layers.Add( self.c_set_d, 0, wx.ALL|wx.EXPAND, 5 )


		bS_layers.Add( ( 0, 50), 0, 0, 5 )

		bS_layer_commands = wx.BoxSizer( wx.HORIZONTAL )

		bS_layer_commands.SetMinSize( wx.Size( -1,60 ) )
		self.cmd_apply = wx.Button( self, wx.ID_ANY, u"Apply Targets", wx.DefaultPosition, wx.DefaultSize, 0 )
		bS_layer_commands.Add( self.cmd_apply, 1, wx.ALL|wx.EXPAND, 3 )

		self.cmd_clear = wx.Button( self, wx.ID_ANY, u"Remove All DI targets", wx.DefaultPosition, wx.DefaultSize, 0 )
		bS_layer_commands.Add( self.cmd_clear, 1, wx.ALL|wx.EXPAND, 3 )


		bS_layers.Add( bS_layer_commands, 0, wx.EXPAND, 5 )


		bS_body.Add( bS_layers, 1, wx.EXPAND, 15 )


		bS_base.Add( bS_body, 1, wx.EXPAND, 5 )

		bS_footer = wx.BoxSizer( wx.HORIZONTAL )

		self.t_status = wx.StaticText( self, wx.ID_ANY, u"Ready", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.t_status.Wrap( -1 )

		self.t_status.SetFont( wx.Font( 16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		bS_footer.Add( self.t_status, 1, wx.ALL|wx.EXPAND, 5 )

		self.cmd_save_job = wx.Button( self, wx.ID_ANY, u"Save Job", wx.DefaultPosition, wx.DefaultSize, 0 )
		bS_footer.Add( self.cmd_save_job, 0, wx.ALL, 5 )

		self.m_button4 = wx.Button( self, wx.ID_ANY, u"Feedback", wx.DefaultPosition, wx.DefaultSize, 0 )
		bS_footer.Add( self.m_button4, 0, wx.ALL, 5 )

		self.cmd_exit = wx.Button( self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		bS_footer.Add( self.cmd_exit, 0, wx.ALL, 5 )


		bS_base.Add( bS_footer, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )


		self.SetSizer( bS_base )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


