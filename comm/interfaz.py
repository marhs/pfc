#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
ZetCode wxPython tutorial

In this example, we create two horizontal 
toolbars. 

author: Jan Bodnar
website: www.zetcode.com
last modified: September 2011
'''

import wx
import comm

class Example(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs) 
            
        self.InitUI()
        
    def InitUI(self):    

        vbox = wx.BoxSizer(wx.VERTICAL)

        toolbar1 = wx.ToolBar(self)
        toolbar1.Realize()

        toolbar2 = wx.ToolBar(self)
        toolbar2.Realize()

        vbox.Add(toolbar1, 0, wx.EXPAND)
        vbox.Add(toolbar2, 0, wx.EXPAND)

        wx.StaticLine(self, pos=(25, 50), size=(300,1)) 
        wx.StaticText(self, label='Key Agreement', pos=(25, 80))

        kgc = comm.KeyGenerationCenter(1024,4)
        c = comm.Comm(kgc,4)
        c.bucle()
        texto = str(c.kgc.k)
        wx.StaticText(self, label=texto, pos=(150, 80))
        self.SetSizer(vbox)

        self.SetSize((300, 250))
        self.SetTitle('Toolbars')
        self.Centre()
        self.Show(True)
        
    def OnQuit(self, e):
        self.Close()

def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()
