#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import wx
import comm

ID_SPLITTER = 300

class MessageList(wx.ListCtrl):
    
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.InsertColumn(0, 'Tipo')
        self.InsertColumn(1, 'Origen')
        self.InsertColumn(2, 'Destino')
        self.InsertColumn(3, 'Datos')

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
        wx.StaticText(self, label='Número de usuarios', pos=(25, 26))
        self.spinUsers = wx.SpinCtrl(self, value='2', pos=(165,25), size=(60,-1))
        self.spinUsers.SetRange(0,10000)

        # Boton de inicio
        self.cbtn = wx.Button(self, label='Iniciar', pos=(220, 21))

        self.botonRonda = wx.Button(self, label='Ronda', pos=(220, 46))

        # Inspector de usuarios
        wx.StaticText(self, label='Datos usuario:', pos=(25, 86))
        users = []
        self.comboUsers = wx.ComboBox(self, pos=(160,83), choices=users, style=wx.CB_READONLY)
    
        # Text area
        wx.StaticBox(self, label='Inspector', pos=(25,110), size=(290,450))
        self.l1 = wx.StaticText(self, label='Tiempo:', pos=(37,140))
        self.l2 = wx.StaticText(self, label='Número de mensajes intercambiados', pos=(37,165))
        self.l3 = wx.StaticText(self, label='', pos=(37,190))
        self.time = wx.StaticText(self, label='', pos=(100,140))
        self.dataSize = wx.StaticText(self, label='', pos=(70,185))
        self.inspectorDst = wx.StaticText(self, label='', pos=(70,190))
        self.inspectorKeyText = wx.StaticText(self, label='Clave acordada', pos=(37,220))
        self.inspectorKey = wx.TextCtrl(self, pos=(40,250), size=(263,300), style=wx.TE_MULTILINE)
        self.inspectorKey.SetEditable(False)

    def ClearValues(self):

        self.time.SetLabel("")
        self.inspectorKey.ChangeValue("")
        #self.comboUsers.Clear()

    def ClearUsers(self):
        self.comboUsers.Clear()

class MainWindow(wx.Frame):

    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,-1,title)
        

        self.splitter = wx.SplitterWindow(self, ID_SPLITTER)
        self.splitter.SetMinimumPaneSize(300)

        self.p1 = ConfigurationWindow(self.splitter, -1, 'pclass')
        self.p2 = MessageList(self.splitter, -1)
        self.splitter.SplitVertically(self.p1, self.p2,330)

        self.p1.cbtn.Bind(wx.EVT_BUTTON, self.OnButtonRegister)
        self.p1.botonRonda.Bind(wx.EVT_BUTTON, self.OnButtonRound)
        self.p1.botonRonda.Disable()
        self.p1.comboUsers.Bind(wx.EVT_COMBOBOX, self.ChangeInspectorUser)

        self.p2.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnSelectList)
        
        self.SetSize((900, 600))
        self.SetTitle('Intercambio de clave')
        self.Centre()
        self.Show(True)

    # Elimina los valores generados anteriormente
    def Reset(self):

        self.p2.DeleteAllItems()
        self.p1.ClearValues()

    def OnButtonRegister(self,e):
       
        # Limpiar los valores anteriores
        self.Reset()
        self.p1.ClearUsers()
        self.p1.botonRonda.Enable()

        kgc = comm.KeyGenerationCenter()
        if self.p1.spinUsers.GetValue() < 1:
            self.ShowError(e)
            return False
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
        self.p1.comboUsers.AppendItems([x.name for x in self.c.participants])
        self.p1.time.SetLabel(str(self.c.time)[:5]+' segundos')
        self.p1.dataSize.SetLabel(str(len(self.c.messages))+' mensajes')
        self.p1.inspectorKey.ChangeValue(str(self.c.kgc.k))

    def OnButtonRound(self,e):

        self.Reset()
        self.c.messages = []
        self.c.bucle()
        # Limpiar los valores anteriores
        j = 0
        for message in self.c.messages:
            (mId, mSrc, mDst, mData) = message
            self.p2.InsertStringItem(j, str(mId))
            self.p2.SetStringItem(j,1,str(mSrc))
            self.p2.SetStringItem(j,2,str(mDst))
            self.p2.SetStringItem(j,3,str(mData))
            j += 1

        # Fill the inspector
        self.p1.time.SetLabel(str(self.c.time)[:5]+' segundos')
        self.p1.dataSize.SetLabel(str(len(self.c.messages))+' mensajes')
        self.p1.inspectorKey.ChangeValue(str(self.c.kgc.k))

    def ChangeInspectorUser(self,e):
        self.inspectorUser = InspectorUserWindow(None,-1,'Main window') 
        self.inspectorUser.inspectorSrc.SetLabel("")
        self.inspectorUser.inspectorDst.SetLabel("")
        self.inspectorUser.inspectorKeyText.SetLabel("Clave acordada")
        selection = e.GetSelection()
        self.inspectorUser.participant = self.c.participants[selection-2]
        self.inspectorUser.inspectorKey.ChangeValue(str(self.c.participants[selection-2].key))
        self.inspectorUser.inspectorId.SetLabel(self.c.participants[selection-2].name)
            
        # Crea y abre la ventana del inspector de usuarios
        self.inspectorUser.Show(True)

    def OnSelectList(self, e):

        index = e.GetIndex()
        s = self.c.messages[index]
        if s == -1:
            return 0
        else:
            self.ChangeInspectorMsg(s[0],s[1],s[2],s[3])
                


    def ChangeInspectorMsg(self, idn, src, dst, data):


        self.inspectorMsg = InspectorMsgWindow(None,-1,'Main window') 

        self.inspectorMsg.inspectorId.SetLabel(str(idn))
        self.inspectorMsg.inspectorSrc.SetLabel(src)
        self.inspectorMsg.inspectorDst.SetLabel(dst)

        self.inspectorMsg.inspectorKeyText.SetLabel("Mensaje")
        self.inspectorMsg.inspectorKey.ChangeValue(str(data))

        # Crea y abre la ventana del inspector de mensajes
        self.inspectorMsg.Show(True)

    def ShowError(self, event):
        dial = wx.MessageDialog(None, 'Debe existir algún usuario para el acuerdo', 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
class InspectorUserWindow(wx.Frame):

    def __init__(self, parent, id, title):

        wx.Frame.__init__(self,parent,-1,title)
        
        self.participant = 0
        wx.StaticBox(self, label='Mensaje', pos=(25,25), size=(290,450))
        self.l1 = wx.StaticText(self, label='Id:', pos=(37,55))
        self.l2 = wx.StaticText(self, label='Mostrar:', pos=(37,80))
        self.b1 = wx.Button(self, label='Subclave', pos=(33, 100))
        self.b2 = wx.Button(self, label='Clave acordada', pos=(123, 100))
        self.l3 = wx.StaticText(self, label='', pos=(37,105))
        self.inspectorId = wx.StaticText(self, label='', pos=(110,55))
        self.inspectorSrc = wx.StaticText(self, label='', pos=(110,80))
        self.inspectorDst = wx.StaticText(self, label='', pos=(110,105))
        self.inspectorKeyText = wx.StaticText(self, label='Clave acordada', pos=(37,135))
        self.inspectorKey = wx.TextCtrl(self, pos=(40,165), size=(263,300), style=wx.TE_MULTILINE)
        self.inspectorKey.SetEditable(False)


        self.b1.Bind(wx.EVT_BUTTON, self.OnSubClave)
        self.b2.Bind(wx.EVT_BUTTON, self.OnClaveAcordada)
        
        self.SetSize((330, 500))
        self.SetTitle('Inspector')
        self.Centre()
        self.Show(False)

    def OnSubClave(self,e):
        
        self.inspectorKeyText.SetLabel('Subclave')
        self.inspectorKey.ChangeValue(str(self.participant.subkey))

    def OnClaveAcordada(self,e):

        self.inspectorKeyText.SetLabel('Clave acordada')
        self.inspectorKey.ChangeValue(str(self.participant.key))

    def OnClose(self):
        self.Close()

class InspectorMsgWindow(wx.Frame):

    def __init__(self, parent, id, title):

        wx.Frame.__init__(self,parent,-1,title)
        
        wx.StaticBox(self, label='Mensaje', pos=(25,25), size=(290,450))
        self.l1 = wx.StaticText(self, label='Id:', pos=(37,55))
        self.l2 = wx.StaticText(self, label='Origen:', pos=(37,80))
        self.l3 = wx.StaticText(self, label='Destino:', pos=(37,105))
        self.inspectorId = wx.StaticText(self, label='', pos=(110,55))
        self.inspectorSrc = wx.StaticText(self, label='', pos=(110,80))
        self.inspectorDst = wx.StaticText(self, label='', pos=(110,105))
        self.inspectorKeyText = wx.StaticText(self, label='Datos', pos=(37,135))
        self.inspectorKey = wx.TextCtrl(self, pos=(40,165), size=(263,300), style=wx.TE_MULTILINE)
        self.inspectorKey.SetEditable(False)


        self.SetSize((330, 500))
        self.SetTitle('Inspector')
        self.Centre()
        self.Show(False)

def main():
    
    ex = wx.App()
    
    MainWindow(None,-1,'Main window')
    InspectorUserWindow(None,-1,'Main window')
    InspectorMsgWindow(None,-1,'Main window')
    ex.MainLoop()    

if __name__ == '__main__':
    main()
