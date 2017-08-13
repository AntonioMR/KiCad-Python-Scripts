#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pcbnew

ESCALA = 1000000.0

def listaPads(modulo=""):
    
    pcb = pcbnew.GetBoard()
    modules = pcb.GetModules()

    for module in modules:
        if (module.GetReference() == modulo):
            for pad in module.Pads():
                print ("    Pad {} conectado a nodo {}".format(pad.GetPadName(),pad.GetNet().GetNetname()))

def nodosComunes(modulo1="", modulo2=""):
    
    mod1Nets = []
    mod2Nets = []

    pcb = pcbnew.GetBoard()

    mod1 = pcb.FindModuleByReference(modulo1)
    if (type(mod1) != pcbnew.MODULE):
        return False

    mod2 = pcb.FindModuleByReference(modulo2)
    if (type(mod2) != pcbnew.MODULE):
        return False

    for pad1 in mod1.Pads():
        net1 = pad1.GetNet().GetNetname()
        mod1Nets.append(net1)
        for pad2 in mod2.Pads():
            net2 = pad2.GetNet().GetNetname()
            mod2Nets.append(net2)
            if net1 == net2:
                print "modulo:", mod1.GetReference(), "pad:", pad1.GetPadName(), "conectado a modulo:", mod2.GetReference(), "pad:", pad2.GetPadName(), "mediante el nodo:", net1 
 
    nodos = []
    for net in mod1Nets:
        if net in mod2Nets:
            nodos.append(net)

    return nodos

def dimension():
    pcb = pcbnew.GetBoard()
    pcbX = pcb.ComputeBoundingBox().GetX()
    pcbY = pcb.ComputeBoundingBox().GetY()
    pcbWidth = pcb.ComputeBoundingBox().GetWidth()
    pcbHeight = pcb.ComputeBoundingBox().GetHeight()

    print ("pcb situada en {},{} de largo {} mm y ancho {} mm".format(pcbX/ESCALA, pcbY/ESCALA, pcbWidth/ESCALA, pcbHeight/ESCALA))

def distancia(modulo1, modulo2, net="ALL"):

    mod1Nets = []
    mod2Nets = []

    pcb = pcbnew.GetBoard()

    mod1 = pcb.FindModuleByReference(modulo1)
    if (type(mod1) != pcbnew.MODULE):
        return False

    mod2 = pcb.FindModuleByReference(modulo2)
    if (type(mod2) != pcbnew.MODULE):
        return False

    for pad1 in mod1.Pads():
        net1 = pad1.GetNet().GetNetname()
        # print ("analizando net {} en {} de {}".format(net1, pad1.GetPadName(), modulo1))
        for pad2 in mod2.Pads():
            net2 = pad2.GetNet().GetNetname()
           # print ("    analizando net {} en {} de {}".format(net2, pad2.GetPadName(), modulo2))
            if net1 == net2:
                longitud = 0.0
                print ("Encontrado nodo comun en net {} desde {} pad {} hasta {} pad {}".format(net1, modulo1, pad1.GetPadName(), modulo2, pad2.GetPadName()))
                tracks = []
                try:
                    #tracks = pcb.TracksInNetBetweenPoints(pad1.GetPosition(), pad2.GetPosition(), pad1.GetNetCode())
                    tracks = pcb.TracksInNet(pad1.GetNetCode())
                except:
                    print ("fallo")
                    

                for track in tracks:
                    longitud += track.GetLength()
                print ("    de longitud {}".format(longitud))

def setModuleRefSize(ancho=0, alto=0, grosor=0, all=False):
    pcb = pcbnew.GetBoard()

    modulos = pcb.GetModules()

    for modulo in modulos:
        if all or modulo.IsSelected():
            ref = modulo.Reference()
            if ancho != 0:
                ref.SetTextWidth(int(ancho * ESCALA))
            if alto != 0:
                ref.SetTextHeight(int(alto * ESCALA))
            if grosor != 0:
                ref.SetThickness(int(grosor * ESCALA))

def setModuleRefPos(xPos=0, yPos=0, all=False):
    pcb = pcbnew.GetBoard()

    modulos = pcb.GetModules()

    for modulo in modulos:
        if all or modulo.IsSelected():
            ref = modulo.Reference().SetPos0(pcbnew.wxPoint(int(xPos*ESCALA),int(yPos*ESCALA)))
            
        

def getModuleRefParam(modulo="", selected=True):
    pcb = pcbnew.GetBoard()
    
    if selected == True:
        modulos = pcb.GetModules()
        for modulo in modulos:
            if modulo.IsSelected():
                refHeight = modulo.Reference().GetTextHeight()
                refWidth = modulo.Reference().GetTextWidth()
                refThick = modulo.Reference().GetThickness()
                refPos = modulo.Reference().GetPos0()
                return (refHeight,refWidth,refThick,refPos)
    else:
        modulo = pcb.FindModuleByReference(modulo)
        refHeight = modulo.Reference().GetTextHeight()
        refWidth = modulo.Reference().GetTextWidth()
        refThick = modulo.Reference().GetThickness()
        refPos = modulo.Reference().GetPos0()
        return (refHeight,refWidth,refThick,refPos)

def setModuleRefParam(refParam):
    pcb = pcbnew.GetBoard()

    for modulo in pcb.GetModules():
        if modulo.IsSelected:
            modulo.Reference().SetTextHeight(refParam[0])
            modulo.Reference().SetTextWidth(refParam[1])
            modulo.Reference().SetThickness(refParam[2])
            modulo.Reference().SetPos0(refParam[3])

def lockModules(opcion=True):
    pcb = pcbnew.GetBoard()

    modulos = pcb.GetModules()

    for modulo in modulos:
        modulo.SetLocked(opcion)

def lockNets(opcion=True):
    pass
