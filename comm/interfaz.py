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

        kgc = comm.KeyGenerationCenter(1024)
        self.c = comm.Comm(kgc,4)
        texto = str(self.c.kgc.k)


        pnl = wx.Panel(self)
        cbtn = wx.Button(pnl, label='Close', pos=(80, 90))
        cbtn.Bind(wx.EVT_BUTTON, self.OnButton)

        wx.StaticText(self, label=texto, pos=(150, 80))

        wx.StaticLine(self, pos=(25, 50), size=(300,1)) 
        wx.StaticText(self, label='Key Agreement', pos=(25, 80))



        self.SetSize((300, 250))
        self.SetTitle('Toolbars')
        self.Centre()
        self.Show(True)
        
    def OnQuit(self, e):
        self.Close()

    def OnButton(self,e):
        self.comm.bucle()
        print self.c.kgc.k

def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()
