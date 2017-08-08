import math

class Position:
    def __init__(self, position=(0.0, 0.0)):
        self.x = position[0]
        self.y = position[1]

    def setPos(self, position):
        self.x = position[0]
        self.y = position[1]

    def getPos(self):
        return (self.x, self.y)

    def __str__(self):
        return " ".join((str(self.x), str(self.y)))

class Segmento:
    """docstring for Segmento"""
    def __init__(self, inicio=(0.0,0.0), fin=(0.0,0.0)):
        self.inicio = Position(position = inicio)
        self.fin = Position(position = fin)

    def setInicio(self, pos):
        self.inicio.setPos(position = pos)

    def setFin(self, pos):
        self.fin.setPos(position = fin)

    def getInicio(self):
        return self.inicio.getPos()

    def getFin(self):
        return self.fin.getPos()

    def getModulo(self):
        return math.sqrt((self.inicio.getPos()[0]-self.fin.getPos()[0])**2 + (self.inicio.getPos()[1]-self.fin.getPos()[1])**2)

    def __str__(self):
        return " ".join(("Segmento desde:", str(self.inicio), "hasta:", str(self.fin), "distancia:", str(self.getModulo())))

class Pad:

    def __init__(self, id=0, pos=(0.0,0.0), net="", componente=""):
        self.position = Position()
        self.id = id
        self.position.setPos(pos)
        self.componente = componente
        self.net = net

    def setId(self, id):
        self.id = id

    def setPos(self, pos):
        self.position.setPos(pos)

    def setComponente(self, componente):
        self.componente = componente

    def setNet(self, net):
        self.net = net

    def getId(self):
        return self.id

    def getPos(self):
        return self.position.getPos()

    def getComponente(self):
        return self.componente

    def getNet(self):
        return self.net

    def __str__(self):
        return " ".join(("pad at pos", str(self.position), "conected to net:", self.net))


class Componente():
    """docstring for Componente"""
   
    def __init__(self, pos=(0.0,0.0), nombre=""):
        self.nombre = nombre
        self.position = Position(pos)
        self.pads = []

    def setName(self, nombre):
        self.nombre = nombre

    def getName(self):
        return self.nombre

    def addPad(self, pad):
        self.pads.append(pad)

    def getPads(self):
        return self.pads

    def setPos(self, pos):
        self.position.setPos(pos)

    def getPos(self):
        return self.position.getPos()

    def __str__(self):
        return " ".join(("Component name:",self.nombre, "at pos:", str(self.position)))

class Net:
    def __init__(self):
        self.name = ""
        self.pads = []
        self.longitud = 0
        self.segmentos = []

    def set(self, name, longitud=0):
        self.name = name
        self.longitud = longitud

    def addPad(self, pad):
        self.pads.append(pad)

    def setLongitud(self,longitud):
        self.longitud = longitud

    def getLongitud(self):
        return self.longitud

    def getName(self):
        return self.name

    def getPads(self):
        return self.pads

    def addSegmento(self, seg):
        self.segmentos.append(seg)

    def getSegmentos(self):
        return self.segmentos

    def __str__(self):
        return " ".join(("Net name:",self.name))



class Board:

    def __init__(self):
        self.nets =  []
        self.componentes = []

    def crear(self, fichero):

        try:
            with open(name=fichero, mode='r') as f:
                modulo = False
                for linea in f:
                    # Prepara la lista de redes
                    if "  (net " in linea[:7]:
                        net = Net()
                        valores = linea.split(" ",4)
                        net.set(valores[4][:-2])
                        self.nets.append(net)
                        
                    # Prepara un diccionario con la posicion y una lista de pads con posicion y red para cada modulo
                    elif "  (module " in linea[:10]:
                        modulo = True
                        posicion = False
                        referencia = False
                        pad_found = False
                        componente = Componente()

                    elif modulo == True:    
                        if not posicion:
                            if "at" in linea:
                                valores = linea.split(" ")
                                if len(valores) > 7:
                                    xpos = float(valores[5])
                                    ypos = float(valores[6])
                                else:
                                    xpos = float(valores[5])
                                    ypos = float(valores[6][:-2])

                                posicion = True
                                componente.setPos((xpos,ypos))

                        elif not referencia:
                            if "reference" in linea:
                                ref = linea.split(" ")[6]
                                componente.setName(ref)
                                referencia = True

                        elif not pad_found:
                            # busca el primer pad
                            if "(pad " in linea:                  
                                pad = Pad()
                                valores = linea.split(" ")
                                if ")" in valores[10]:
                                    xpos = float(valores[9]) + componente.getPos()[0]
                                    ypos = float(valores[10][:-1]) + componente.getPos()[1]
                                else:
                                    xpos = float(valores[9]) + componente.getPos()[0]
                                    ypos = float(valores[10]) + componente.getPos()[1]
                                
                                pad.setPos((xpos,ypos))
                                pad.setComponente(componente.getName())
                                pad_found = True
                                
                            elif "  )" in linea[:2]:
                                modulo = False

                        elif pad_found:
                            if "(pad " in linea:
                                pad = Pad()
                                valores = linea.split(" ")
                                
                                if ")" in valores[10]:
                                    xpos = float(valores[9]) + componente.getPos()[0]
                                    ypos = float(valores[10][:-1]) + componente.getPos()[1]
                                else:
                                    xpos = float(valores[9]) + componente.getPos()[0]
                                    ypos = float(valores[10]) + componente.getPos()[1]
                                
                                pad.setPos((xpos,ypos))
                                pad.setComponente(componente.getName())

                            elif "(net" in linea:
                                valores = linea.split(" ", )
                                pad.setNet(valores[7])
                                componente.addPad(pad)
                                self.nets[int(valores[7])].addPad(pad)
                            
                            else:
                                self.componentes.append(componente)
                                modulo = False

                    # prepara el diccionario de longitudes de los nodos
                    elif "  (segment (start " in linea:
                        valores = linea.split(" ")
                        xi = float(valores[4])
                        yi = float(valores[5][:-2])
                        xf = float(valores[7])
                        yf = float(valores[8][:-2])
                        net = int(valores[14][:-3])

                        distancia = math.sqrt((xi-xf)**2 + (yi-yf)**2)

                        segmento = Segmento(inicio = (xi,yi), fin = (xf,yf))
                        self.nets[net].addSegmento(segmento)
                        self.nets[net].setLongitud(self.nets[net].getLongitud() + distancia)
                                
            
        except IOError as e:
            print('Error abrindo {} = {}'.format(fichero, e))
            return False
        
        else:
            f.close()
            return True

    def getNets(self):
        return self.nets

    def getComponents(self):
        return self.componentes

    def printModules(self):

        for componente in self.componentes:
            print componente
            for pad in componente.getPads():
                print "     ", pad
   
    def printNets(self):
        for net in self.nets:
            print net
            for pad in net.getPads():
                print "     with pad at", pad.getPos(), "from component", pad.getComponente()

            for segmento in net.getSegmentos():
                print "    ", segmento

    def __str__(self):
        return "str"
        #return '\n'.join(" = ".join((str(ref),str(valor))) for valor,ref in self.boom.items())
   #     return '\n'.join(" = ".join((str(net),str(legth)))   for net,legth in self.nets_length.items())