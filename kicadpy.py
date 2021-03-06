#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pcbnew

ESCALA = 1000000.0

def listaPads(modulo=""):
    """ Imprime por consola la lista de pads de un determinado modulo cuya referencia
        Se pasa como parametro"""
    pcb = pcbnew.GetBoard()
    modules = pcb.GetModules()

    for module in modules:
        if (module.GetReference() == modulo):
            for pad in module.Pads():
                print ("    Pad {} conectado a nodo {}".format(pad.GetPadName(),pad.GetNet().GetNetname()))

def nodosComunes(modulo1="", modulo2=""):
    """ Imprime los nodos comunes entre los dos modulos cuyas referencias se pasan como
        parametro, indicando los pad mediante los que se conectan los modulos """
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
    """ Imprime las dimensiones del la pcb (en revision)"""
    pcb = pcbnew.GetBoard()
    pcbX = pcb.ComputeBoundingBox().GetX()
    pcbY = pcb.ComputeBoundingBox().GetY()
    pcbWidth = pcb.ComputeBoundingBox().GetWidth()
    pcbHeight = pcb.ComputeBoundingBox().GetHeight()

    print ("pcb situada en {},{} de largo {} mm y ancho {} mm".format(pcbX/ESCALA, pcbY/ESCALA, pcbWidth/ESCALA, pcbHeight/ESCALA))

def distancia(modulo1, modulo2, net="ALL"):
    """ Imprime los nodos comunes entre los dos modulos cuyas referencias se pasan como
        parametro, indicando los pad mediante los que se conectan los modulos y la distancia
        del nodo que los interconecta (en reficion) """

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
                print ("    de longitud {}".format(longitud/ESCALA))

def setModuleRefSize(ancho=0, alto=0, grosor=0, all=False, allLikeThis=False):
    """ Fija el tamaño del texto del campo Referencia de los modulos segun los parametros especificados.
        Si algun parametro no se indica, o se indica a 0, no se cambiara. 
        Pasando el parametro all a True se cambiaran en todos los modulos. 
        Pasando el parametro allLikeThis a True se cambiaran todos los modulos iguales al modulo
        seleccionado en la pcb """

    pcb = pcbnew.GetBoard()

    modulos = pcb.GetModules()

    if allLikeThis:
        for modulo in modulos:
            if modulo.IsSelected():
                descripcion = modulo.GetDescription()
                break

    for modulo in modulos:
        if all or modulo.IsSelected() or (allLikeThis and (modulo.GetDescription() == descripcion)):
            ref = modulo.Reference()
            if ancho != 0:
                ref.SetTextWidth(int(ancho * ESCALA))
            if alto != 0:
                ref.SetTextHeight(int(alto * ESCALA))
            if grosor != 0:
                ref.SetThickness(int(grosor * ESCALA))

def setModuleRefPos(xPos=0, yPos=0, all=False, allLikeThis=False):
    """ Fija la posicion del texto del campo Referencia de los modulos segun los parametros especificados.
        Si algun parametro no se indica, o se indica a 0, no se cambiara. 
        Pasando el parametro all a True se cambiaran en todos los modulos. 
        Pasando el parametro allLikeThis a True se cambiaran todos los modulos iguales al modulo
        seleccionado en la pcb """

    pcb = pcbnew.GetBoard()

    modulos = pcb.GetModules()

    if allLikeThis:
        for modulo in modulos:
            if modulo.IsSelected():
                descripcion = modulo.GetDescription()
                break

    for modulo in modulos:
        if all or modulo.IsSelected() or (allLikeThis and (modulo.GetDescription() == descripcion)):
            ref = modulo.Reference().SetPos0(pcbnew.wxPoint(int(xPos*ESCALA),int(yPos*ESCALA)))
            
def getModuleRefParam(modulo="", selected=True):
    """ Obtiene los parametros de configuracion del campo Referencia para un modulo.
        por defecto lo obtendra del modulo seleccionado en la pcb
        Es posible indicar la referencia del modulo a capturar mediante el parametro modulo,
        en cuyo caso habra que indicar el parametro selected a False """
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

def setModuleRefParam(refParam, allLikeThis=False):
    """ Modifica los valores de configuracion del campo Referencia de un modulo con los valores
        capturados previamente con la funcion getModuleRefParam().
        Por defecto modifica todos los modulos seleccionados 
        Si se indica el parametro allLikeThis = True se modificaran todos los modulos iguales 
        que el modulo seleccionado. """

    pcb = pcbnew.GetBoard()

    if allLikeThis:
        for modulo in modulos:
            if modulo.IsSelected():
                descripcion = modulo.GetDescription()
                break

    for modulo in pcb.GetModules():
        if modulo.IsSelected() or (allLikeThis and (modulo.GetDescription() == descripcion)):
            modulo.Reference().SetTextHeight(refParam[0])
            modulo.Reference().SetTextWidth(refParam[1])
            modulo.Reference().SetThickness(refParam[2])
            modulo.Reference().SetPos0(refParam[3])

def setModuleValSize(ancho=0, alto=0, grosor=0, all=False, allLikeThis=False):
    """ Fija el tamaño del texto del campo Valor de los modulos segun los parametros especificados.
        Si algun parametro no se indica, o se indica a 0, no se cambiara. 
        Pasando el parametro all a True se cambiaran en todos los modulos. 
        Pasando el parametro allLikeThis a True se cambiaran todos los modulos iguales al modulo
        seleccionado en la pcb """
    pcb = pcbnew.GetBoard()

    modulos = pcb.GetModules()

    if allLikeThis:
        for modulo in modulos:
            if modulo.IsSelected():
                descripcion = modulo.GetDescription()
                break

    for modulo in modulos:
        if all or modulo.IsSelected() or (allLikeThis and (modulo.GetDescription() == descripcion)):
            value = modulo.Value()
            if ancho != 0:
                value.SetTextWidth(int(ancho * ESCALA))
            if alto != 0:
                value.SetTextHeight(int(alto * ESCALA))
            if grosor != 0:
                value.SetThickness(int(grosor * ESCALA))

def setModuleValPos(xPos=0, yPos=0, all=False, allLikeThis):
    """ Fija la posicion del texto del campo Valor de los modulos segun los parametros especificados.
        Si algun parametro no se indica, o se indica a 0, no se cambiara. 
        Pasando el parametro all a True se cambiaran en todos los modulos. 
        Pasando el parametro allLikeThis a True se cambiaran todos los modulos iguales al modulo
        seleccionado en la pcb """
    pcb = pcbnew.GetBoard()

    modulos = pcb.GetModules()
    
    if allLikeThis:
        for modulo in modulos:
            if modulo.IsSelected():
                descripcion = modulo.GetDescription()
                break

    for modulo in modulos:
        if all or modulo.IsSelected() or (allLikeThis and (modulo.GetDescription() == descripcion)):
            modulo.Value().SetPos0(pcbnew.wxPoint(int(xPos*ESCALA),int(yPos*ESCALA)))    
        
def getModuleValParam(modulo="", selected=True):
    """ Obtiene los parametros de configuracion del campo Valor para un modulo.
        por defecto lo obtendra del modulo seleccionado en la pcb
        Es posible indicar la referencia del modulo a capturar mediante el parametro modulo,
        en cuyo caso habra que indicar el parametro selected a False """
    pcb = pcbnew.GetBoard()
    
    if selected == True:
        for modulo in pcb.GetModules():
            if modulo.IsSelected():
                refHeight = modulo.Value().GetTextHeight()
                refWidth = modulo.Value().GetTextWidth()
                refThick = modulo.Value().GetThickness()
                refPos = modulo.Value().GetPos0()
                return (refHeight,refWidth,refThick,refPos)
    else:
        modulo = pcb.FindModuleByReference(modulo)
        refHeight = modulo.Value().GetTextHeight()
        refWidth = modulo.Value().GetTextWidth()
        refThick = modulo.Value().GetThickness()
        refPos = modulo.Value().GetPos0()
        return (refHeight,refWidth,refThick,refPos)

def setModuleValParam(valParam, allLikeThis=False):
    """ Modifica los valores de configuracion del campo Valor de un modulo con los valores
        capturados previamente con la funcion getModuleValParam().
        Por defecto modifica todos los modulos seleccionados 
        Si se indica el parametro allLikeThis = True se modificaran todos los modulos iguales 
        que el modulo seleccionado. """
    pcb = pcbnew.GetBoard()
    
    if allLikeThis:
        for modulo in modulos:
            if modulo.IsSelected():
                descripcion = modulo.GetDescription()
                break

    for modulo in pcb.GetModules():
        if modulo.IsSelected() or (allLikeThis and (modulo.GetDescription() == descripcion)):
            modulo.Value().SetTextHeight(valParam[0])
            modulo.Value().SetTextWidth(valParam[1])
            modulo.Value().SetThickness(valParam[2])
            modulo.Value().SetPos0(valParam[3])

def lockModules(opcion=True):
    """ Bloquea/desbloquea todos los modulos en la pcb dependiendo del valor pasado como parametro"""
    pcb = pcbnew.GetBoard()

    modulos = pcb.GetModules()

    for modulo in modulos:
        modulo.SetLocked(opcion)

def lockNets(opcion=True):
    """ Bloquea/desbloquea todas las pistas en la pcb dependiendo del valor pasado como parametro (en revision)"""
    pass
