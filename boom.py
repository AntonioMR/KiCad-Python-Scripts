class Boom:
    """ Generacion de listas de componentes para proyectos de KiCad"""
    def __init__(self):
        self.boom = {}

    def crear(self, fichero):
    	""" Crea un diccionario con los valores y referencias del ficher netlist especificado como parametro """
        try:
            f = open(fichero , "r")
        except:
            return False

        while True:
            linea = f.readline()
            if not linea: 
	            break
	
            elif "(comp (ref" in linea:
                finNombre = linea[15:].find(")")
                ref = linea[15:(15+finNombre)]
        
                linea = f.readline()
                finNombre = linea[13:].find(")")
                valor = linea[13:(13+finNombre)]
             
                self.boom.setdefault(valor,[])
                self.boom[valor].append(ref)

        f.close()

        return True


    def imprimir(self):
    	""" Imprime el diccionario """
        elementos = self.boom.items()
        for valor, ref in elementos:
            print ref, ": ", valor

    def __str__(self):
    	return '\n'.join(" = ".join((str(ref),str(valor))) for valor,ref in self.boom.items())
