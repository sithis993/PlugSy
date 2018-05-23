# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jan 23 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"PlugSy - v0.1.0", pos = wx.DefaultPosition, size = wx.Size( 650,450 ), style = wx.DEFAULT_FRAME_STYLE|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.Notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.SdkPanel = wx.Panel( self.Notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer25 = wx.BoxSizer( wx.VERTICAL )
		
		self.PluginsTreeCtrl = wx.TreeCtrl( self.SdkPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.TR_LINES_AT_ROOT )
		bSizer25.Add( self.PluginsTreeCtrl, 88, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer12.Add( bSizer25, 1, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.SdkPanel, wx.ID_ANY, u"Plugin Settings" ), wx.VERTICAL )
		
		self.m_panel22 = wx.Panel( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer56 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer81 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.PluginNameLabel = wx.StaticText( self.m_panel22, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.PluginNameLabel.Wrap( -1 )
		bSizer81.Add( self.PluginNameLabel, 0, wx.ALL, 8 )
		
		
		bSizer81.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.PluginNameTextCtrl = wx.TextCtrl( self.m_panel22, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer81.Add( self.PluginNameTextCtrl, 0, wx.ALL, 5 )
		
		
		bSizer7.Add( bSizer81, 1, wx.EXPAND, 5 )
		
		bSizer811 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.PluginTypeLabel = wx.StaticText( self.m_panel22, wx.ID_ANY, u"Type", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.PluginTypeLabel.Wrap( -1 )
		bSizer811.Add( self.PluginTypeLabel, 0, wx.ALL, 8 )
		
		
		bSizer811.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		PluginTypeComboBoxChoices = [ u"Core", u"Addon" ]
		self.PluginTypeComboBox = wx.ComboBox( self.m_panel22, wx.ID_ANY, u"Core", wx.DefaultPosition, wx.DefaultSize, PluginTypeComboBoxChoices, wx.CB_READONLY )
		self.PluginTypeComboBox.Enable( False )
		
		bSizer811.Add( self.PluginTypeComboBox, 0, wx.ALL, 5 )
		
		
		bSizer7.Add( bSizer811, 1, wx.EXPAND, 5 )
		
		
		bSizer56.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		
		self.m_panel22.SetSizer( bSizer56 )
		self.m_panel22.Layout()
		bSizer56.Fit( self.m_panel22 )
		sbSizer2.Add( self.m_panel22, 1, wx.EXPAND |wx.ALL, 10 )
		
		
		bSizer6.Add( sbSizer2, 3, wx.EXPAND, 5 )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.SdkPanel, wx.ID_ANY, wx.EmptyString ), wx.HORIZONTAL )
		
		
		sbSizer3.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.DeletePluginButton = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Delete Plugin", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.DeletePluginButton.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
		self.DeletePluginButton.Enable( False )
		
		sbSizer3.Add( self.DeletePluginButton, 0, wx.ALL, 5 )
		
		
		sbSizer3.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer6.Add( sbSizer3, 0, wx.EXPAND, 5 )
		
		
		bSizer12.Add( bSizer6, 2, wx.EXPAND, 5 )
		
		
		self.SdkPanel.SetSizer( bSizer12 )
		self.SdkPanel.Layout()
		bSizer12.Fit( self.SdkPanel )
		self.Notebook.AddPage( self.SdkPanel, u"SDK", True )
		
		bSizer8.Add( self.Notebook, 1, wx.EXPAND |wx.ALL, 2 )
		
		
		self.SetSizer( bSizer8 )
		self.Layout()
		self.MenuBar = wx.MenuBar( 0 )
		self.MenuBar.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True, "Arial" ) )
		
		self.FileMenu = wx.Menu()
		self.FileMenu.AppendSeparator()
		
		self.ExitMenuItem = wx.MenuItem( self.FileMenu, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.FileMenu.Append( self.ExitMenuItem )
		
		self.MenuBar.Append( self.FileMenu, u"File" ) 
		
		self.PluginMenu = wx.Menu()
		self.NewPluginMenuItem = wx.MenuItem( self.PluginMenu, wx.ID_ANY, u"New Plugin"+ u"\t" + u"Ctrl + n", wx.EmptyString, wx.ITEM_NORMAL )
		self.PluginMenu.Append( self.NewPluginMenuItem )
		
		self.MenuBar.Append( self.PluginMenu, u"Plugin" ) 
		
		self.SetMenuBar( self.MenuBar )
		
		self.StatusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class PluginsHomeDirDialog
###########################################################################

class PluginsHomeDirDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"PlugSy - SDK", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHints( wx.Size( 400,100 ), wx.DefaultSize )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Plugins Home" ), wx.VERTICAL )
		
		sbSizer1.SetMinSize( wx.Size( 400,100 ) ) 
		self.m_panel10 = wx.Panel( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.PluginsHomeDirPicker = wx.DirPickerCtrl( self.m_panel10, wx.ID_ANY, wx.EmptyString, u"test", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_USE_TEXTCTRL )
		self.PluginsHomeDirPicker.SetToolTip( u"Select the plugins' home directory. This is the location in which plugins are created, loaded and stored" )
		
		bSizer15.Add( self.PluginsHomeDirPicker, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer15, 1, wx.EXPAND, 5 )
		
		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer18.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.LogLevelLabel = wx.StaticText( self.m_panel10, wx.ID_ANY, u"Log Level", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.LogLevelLabel.Wrap( -1 )
		bSizer18.Add( self.LogLevelLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		LogLevelChoiceChoices = [ wx.EmptyString, u"Debug", u"Info", u"Warning", u"Error", u"Critical" ]
		self.LogLevelChoice = wx.Choice( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, LogLevelChoiceChoices, 0 )
		self.LogLevelChoice.SetSelection( 0 )
		bSizer18.Add( self.LogLevelChoice, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.LogFilePathLabel = wx.StaticText( self.m_panel10, wx.ID_ANY, u"Log File Path", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.LogFilePathLabel.Wrap( -1 )
		bSizer18.Add( self.LogFilePathLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.LogFilePathTextCtrl = wx.TextCtrl( self.m_panel10, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.LogFilePathTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer18.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer12.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		
		self.m_panel10.SetSizer( bSizer12 )
		self.m_panel10.Layout()
		bSizer12.Fit( self.m_panel10 )
		sbSizer1.Add( self.m_panel10, 3, wx.EXPAND |wx.ALL, 10 )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		self.StatusLabel = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.StatusLabel.Wrap( -1 )
		self.StatusLabel.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer11.Add( self.StatusLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		OkCancelSizer = wx.StdDialogButtonSizer()
		self.OkCancelSizerOK = wx.Button( sbSizer1.GetStaticBox(), wx.ID_OK )
		OkCancelSizer.AddButton( self.OkCancelSizerOK )
		self.OkCancelSizerCancel = wx.Button( sbSizer1.GetStaticBox(), wx.ID_CANCEL )
		OkCancelSizer.AddButton( self.OkCancelSizerCancel )
		OkCancelSizer.Realize();
		
		bSizer11.Add( OkCancelSizer, 1, wx.EXPAND, 5 )
		
		
		sbSizer1.Add( bSizer11, 2, wx.EXPAND, 5 )
		
		
		self.SetSizer( sbSizer1 )
		self.Layout()
		sbSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class NewPluginDialog
###########################################################################

class NewPluginDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"PlugSy - New Plugin", pos = wx.DefaultPosition, size = wx.Size( 446,160 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"New Plugin" ), wx.VERTICAL )
		
		self.m_panel4 = wx.Panel( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer20 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.PluginNameLabel = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Plugin Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.PluginNameLabel.Wrap( -1 )
		bSizer21.Add( self.PluginNameLabel, 0, wx.ALL, 8 )
		
		
		bSizer21.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.PluginNameTextCtrl = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.PluginNameTextCtrl, 0, wx.ALL, 5 )
		
		
		bSizer22.Add( bSizer21, 1, wx.EXPAND, 5 )
		
		wSizer4 = wx.WrapSizer( wx.HORIZONTAL )
		
		self.PluginTypeLabel = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Plugin Type", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.PluginTypeLabel.Wrap( -1 )
		wSizer4.Add( self.PluginTypeLabel, 0, wx.ALL, 8 )
		
		
		wSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		PluginTypeChoiceChoices = [ u"core", u"addon" ]
		self.PluginTypeChoice = wx.Choice( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, PluginTypeChoiceChoices, 0 )
		self.PluginTypeChoice.SetSelection( 0 )
		wSizer4.Add( self.PluginTypeChoice, 0, wx.ALL, 5 )
		
		
		bSizer22.Add( wSizer4, 1, wx.EXPAND, 5 )
		
		
		bSizer20.Add( bSizer22, 1, wx.EXPAND, 5 )
		
		
		self.m_panel4.SetSizer( bSizer20 )
		self.m_panel4.Layout()
		bSizer20.Fit( self.m_panel4 )
		sbSizer4.Add( self.m_panel4, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer23 = wx.BoxSizer( wx.VERTICAL )
		
		self.StatusLabel = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.StatusLabel.Wrap( -1 )
		self.StatusLabel.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer23.Add( self.StatusLabel, 0, wx.ALL, 5 )
		
		OkCanelSizer = wx.StdDialogButtonSizer()
		self.OkCanelSizerOK = wx.Button( sbSizer4.GetStaticBox(), wx.ID_OK )
		OkCanelSizer.AddButton( self.OkCanelSizerOK )
		self.OkCanelSizerCancel = wx.Button( sbSizer4.GetStaticBox(), wx.ID_CANCEL )
		OkCanelSizer.AddButton( self.OkCanelSizerCancel )
		OkCanelSizer.Realize();
		
		bSizer23.Add( OkCanelSizer, 1, wx.EXPAND, 5 )
		
		
		sbSizer4.Add( bSizer23, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( sbSizer4 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class ConfirmationDialog
###########################################################################

class ConfirmationDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"PlugSy - Are you Sure?", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Confirmation" ), wx.VERTICAL )
		
		sbSizer5.SetMinSize( wx.Size( 320,100 ) ) 
		self.MainPanel = wx.Panel( sbSizer5.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		self.ConfirmationLabel = wx.StaticText( self.MainPanel, wx.ID_ANY, u"Are you sure you want to delete this Plugin?", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.ConfirmationLabel.Wrap( 250 )
		bSizer17.Add( self.ConfirmationLabel, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
		
		self.MainPanel.SetSizer( bSizer17 )
		self.MainPanel.Layout()
		bSizer17.Fit( self.MainPanel )
		sbSizer5.Add( self.MainPanel, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 10 )
		
		OkCancelSizer = wx.StdDialogButtonSizer()
		self.OkCancelSizerOK = wx.Button( sbSizer5.GetStaticBox(), wx.ID_OK )
		OkCancelSizer.AddButton( self.OkCancelSizerOK )
		self.OkCancelSizerCancel = wx.Button( sbSizer5.GetStaticBox(), wx.ID_CANCEL )
		OkCancelSizer.AddButton( self.OkCancelSizerCancel )
		OkCancelSizer.Realize();
		
		sbSizer5.Add( OkCancelSizer, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( sbSizer5 )
		self.Layout()
		sbSizer5.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

