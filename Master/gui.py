import wx
import wx.xrc

class MainFrame ( wx.Frame ):
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Virus-Master", pos = wx.DefaultPosition, size = wx.Size( 600,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		fgSizer4 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


		fgSizer4.Add( ( 200, 0), 1, wx.EXPAND, 5 )

		self.title_lable = wx.StaticText( self, wx.ID_ANY, u"Virus Master", wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		self.title_lable.Wrap( -1 )

		self.title_lable.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		fgSizer4.Add( self.title_lable, 0, wx.ALL, 5 )


		bSizer1.Add( fgSizer4, 1, wx.EXPAND, 5 )

		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.victims_listChoice = []
		self.victims_list = wx.ListBox( self, wx.ID_ANY, wx.Point( -1,-1 ), wx.Size( 200,400 ), self.victims_listChoice, 0 )
		fgSizer2.Add( self.victims_list, 0, wx.ALL, 5 )
		
		self.Bind(wx.EVT_LISTBOX, self.OnSelect, self.victims_list)

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		chat_listChoices = []
		self.chat_list = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 350,350 ), chat_listChoices, 0 )
		bSizer3.Add( self.chat_list, 0, wx.ALL, 5 )

		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.input_message = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 270,-1 ), 0 )
		fgSizer3.Add( self.input_message, 0, wx.ALL, 5 )

		self.send_btn = wx.Button( self, wx.ID_ANY, u"Send", wx.Point( 0,2 ), wx.DefaultSize, 0 )
		fgSizer3.Add( self.send_btn, 0, wx.ALL, 5 )

		self.send_btn.Bind(wx.EVT_BUTTON, self.OnSendBtn)


		bSizer3.Add( fgSizer3, 1, wx.EXPAND, 5 )


		fgSizer2.Add( bSizer3, 1, wx.EXPAND, 5 )


		bSizer1.Add( fgSizer2, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

	def OnSendBtn(self, event):
		inputMessage = self.input_message.GetValue()
		print(inputMessage)
	def OnSelect(self, event):
		#clear the chat and make sure that we send the message to the right person
		selected = event.GetSelection()
		print(selected)
	
    
	def __del__( self ):
		pass


