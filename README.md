## Descripción:
Este repositorio incluye una serie de funciones para realizar acciones no implementadas en el software de diseño de PCB KiCad.

Estas funciones están pensadas para llamarse desde la consola de Python incorporada en el software Pcbnew del EDA KiCad.

Es necesario tener una versión de KiCad que este compilada con el interprete de Python activado. Este interprete de Python puede encontrarse dentro del software Pcbnew dentro del menu Herramientas->Consola de Script.

Dentro de la consola de Python situarse en el directorio donde esté el fichero kicadpy.py e importarlo mediante:
```python
import kicadpy
```
## Funciones incorporadas:
Salvo que se indique lo contrario las medidas indicadas en los parámetros están especificadas en milímetros

**setModuleRefSize(ancho=0, alto=0, grosor=0, all=False, allLikeThis=False)**

Mediante esta función es posible cambiar el tamaño del texto del campo Referencia de los Modulos en la PCB sin tener que recurrir al menú de edición del campo dentro de PcbNew.
Es posible especificar el ancho y alto alto del texto así como el grosor de linea empleada.

Formas de uso:

* Cambiar el tamaño de la referencia en el módulo seleccionado dentro de Pcbnew
```python
kicadpy.setModuleRefSize(ancho=0.8, alto=0.8, grosor=0.15)
```

* Cambiar el tamaño del alto de las referencias de todos los módulos de la PCB
```python
kicadpy.setModuleRefSize(alto=0.8, all=True)
```

* Cambiar el tamaño del ancho y alto de las referencias de todos los módulos de la PCB iguales al modulo seleccionado
```python
kicadpy.setModuleRefSize(ancho=0.8, alto=0.8, allLikeThis=True)
```

**setModuleRefPos(xPos=0, yPos=0, all=False, allLikeThis=False)**

Mediante esta función es posible cambiar la posicion relativa del texto del campo Referencia de los Modulos respecto a la posicion del módulo
Es posible especificar el desplazamiento en el eje X e Y

Formas de uso:

* Cambiar la posición de la referencia en el módulo seleccionado dentro de Pcbnew
```python
kicadpy.setModuleRefPos(xPos=-2.54, yPos=0)
```

* Situar todas las referencias en la posicion 0,0
```python
kicadpy.setModuleRefPos(all=True)
```

* Cambiar la posición de la referencia en el módulo seleccionado y todos los iguales all seleccionado
```python
kicadpy.setModuleRefPos(xPos=-2.54, yPos=5.08, allLikeThis=True)
```

**getModuleRefParam(modulo="", selected=True)**

Devuelve los parametros de configuración del campo Referencia de un módulo para utilizarlo como configuracion de otros módulos. Los parametros devueltos son los parametros de tamaño y posicion del texto.

Formas de uso:

* Obtener los parametros de configuracion del modulo seleccionado en Pcbnew
```python
parametros = kicadpy.getModuleRefParam()
```

* Obtener los parametros de configuracion del modulo con referencia R14
```python
parametros = kicadpy.getModuleRefParam(modulo="R14", selected=False)
```

**setModuleRefParam(refParam, allLikeThis=False)**

Permite configurar los parametros del campo Referencia con los valores obtenidos con la funcion _getModuleRefParam()_

Formas de uso:

* Configurar los parametros del campo Referencia para los modulos seleccionados en Pcbnew
```python
kicadpy.setModuleRefParam(parametros)
```

* Configurar los parametros del campo Referencia para los modulos iguales al seleccionado en Pcbnew
```python
kicadpy.setModuleRefParam(parametros, allLikeThis=True)
```

**setModuleValSize(ancho=0, alto=0, grosor=0, all=False, allLikeThis=False)**

Permite realizar las mismas acciones que _setModuleRefSize()_ pero para el campo Valor del uno o varios modulos

**setModuleValPos(xPos=0, yPos=0, all=False, allLikeThis=False)**

Permite realizar las mismas acciones que _setModuleRefPos()_ pero para el campo Valor del uno o varios modulos

**getModuleValParam(modulo="", selected=True)**

Permite realizar las mismas acciones que _getModuleRefParam()_ pero para el campo Valor del uno o varios modulos

**setModuleValParam(refParam, allLikeThis=False)**

Permite realizar las mismas acciones que _setModuleRefParam()_ pero para el campo Valor del uno o varios modulos
