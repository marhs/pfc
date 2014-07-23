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

ID_SPLITTER = 300
class MessageList(wx.ListCtrl):
    
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.InsertColumn(0, 'Id')
        self.InsertColumn(1, 'Source')
        self.InsertColumn(2, 'Dest')
        self.InsertColumn(3, 'Data')

        self.SetColumnWidth(0, 50)
        self.SetColumnWidth(1, 75)
        self.SetColumnWidth(2, 75)
        self.SetColumnWidth(3, 300)


class ConfigurationWindow(wx.Panel):
    
    def __init__(self, parent, id, title):
        wx.Panel.__init__(self, parent, id=-1,size=wx.Size(300,200))

            
        self.InitUI()
        
    def InitUI(self):    

        
        # Numero de usuarios
        wx.StaticText(self, label='Numero de usuarios', pos=(25, 26))
        self.spinUsers = wx.SpinCtrl(self, value='2', pos=(165,25), size=(60,-1))
        self.spinUsers.SetRange(2,100)

        # Boton de inicio
        self.cbtn = wx.Button(self, label='Iniciar', pos=(220, 21))


        # Inspector de usuarios
        wx.StaticText(self, label='Informacion:', pos=(25, 66))
        users = []
        self.comboUsers = wx.ComboBox(self, pos=(160,63), choices=users, style=wx.CB_READONLY)
    
            # Text area
        wx.StaticBox(self, label='Inspector', pos=(25,110), size=(290,450))
        self.l1 = wx.StaticText(self, label='Id:', pos=(37,140))
        self.l2 = wx.StaticText(self, label='', pos=(37,165))
        self.l3 = wx.StaticText(self, label='', pos=(37,190))
        self.inspectorId = wx.StaticText(self, label='', pos=(70,140))
        self.inspectorSrc = wx.StaticText(self, label='', pos=(70,165))
        self.inspectorDst = wx.StaticText(self, label='', pos=(70,190))
        self.inspectorKeyText = wx.StaticText(self, label='Clave acordada', pos=(37,220))
        self.inspectorKey = wx.TextCtrl(self, pos=(40,250), size=(263,300), style=wx.TE_MULTILINE)
        self.inspectorKey.SetEditable(False)

    def ClearValues(self):

        self.inspectorId.SetLabel("")
        self.inspectorKey.ChangeValue("")
        self.comboUsers.Clear()

class MainWindow(wx.Frame):

    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,-1,title)
        
        # Objeto comm y kgc

        self.splitter = wx.SplitterWindow(self, ID_SPLITTER)
        self.splitter.SetMinimumPaneSize(300)

        self.p1 = ConfigurationWindow(self.splitter, -1, 'wololo')
        self.p2 = MessageList(self.splitter, -1)
        self.splitter.SplitVertically(self.p1, self.p2,330)

        self.p1.cbtn.Bind(wx.EVT_BUTTON, self.OnButton)
        self.p1.comboUsers.Bind(wx.EVT_COMBOBOX, self.ChangeInspectorUser)

        self.p2.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectList)
        
        self.SetSize((900, 600))
        self.SetTitle('Toolbars')
        self.Centre()
        self.Show(True)

    # Elimina los valores generados anteriormente
    def Reset(self):

        self.p2.DeleteAllItems()
        self.p1.ClearValues()


    def OnButton(self,e):
       
        # Limpiar los valores anteriores
        self.Reset()
        kgc = comm.KeyGenerationCenter()
        self.c = comm.Comm(kgc,self.p1.spinUsers.GetValue())
        self.c.bucle()
        j = 0
        for message in self.c.messages:
            (mId, mSrc, mDst, mData) = message
            self.p2.InsertStringItem(j, str(mId))
            self.p2.SetStringItem(j,1,str(mSrc))
            self.p2.SetStringItem(j,2,str(mDst))
            self.p2.SetStringItem(j,3,str(mData))
            j += 1

        # Fill the inspector
        self.p1.comboUsers.Append('kgc')
        self.p1.comboUsers.AppendItems([x.name for x in self.c.participants])

    def ChangeInspectorUser(self,e):
        self.p1.inspectorSrc.SetLabel("")
        self.p1.inspectorDst.SetLabel("")
        self.p1.l2.SetLabel("")
        self.p1.l3.SetLabel("")
        self.p1.inspectorKeyText.SetLabel("Clave acordada")
        selection = e.GetSelection()
        if selection == 0:
            # KGC
            self.p1.inspectorId.SetLabel('kgc')
            self.p1.inspectorKey.ChangeValue(str(self.c.kgc.k))
        else:
            self.p1.inspectorKey.ChangeValue(str(self.c.participants[selection-1].key))
            self.p1.inspectorId.SetLabel(self.c.participants[selection-1].name)

    def OnSelectList(self, e):

        index = e.GetIndex()
        s = self.c.messages[index]
        if s == -1:
            return 0
        else:
            self.ChangeInspectorList(s[0],s[1],s[2],s[3])
                


    def ChangeInspectorList(self, idn, src, dst, data):

        self.p1.l2.SetLabel("Src:")
        self.p1.l3.SetLabel("Dst:")

        self.p1.inspectorId.SetLabel(str(idn))
        self.p1.inspectorSrc.SetLabel(src)
        self.p1.inspectorDst.SetLabel(dst)

        self.p1.inspectorKeyText.SetLabel("Mensaje")
        self.p1.inspectorKey.ChangeValue(str(data))


def main():
    
    ex = wx.App()
    MainWindow(None,-1,'Main window')
    ex.MainLoop()    


if __name__ == '__main__':
    main()
