
# Mentor

## Introducción

Mentor es un programa para convertir documentos *.odt* en un paquete de documentos HTML que puedan ser utilizados en plataformas educacionales. 

El objetivo simplificar la creación de contenidos en formatos interactivos y fácilmente visibles en la WEB, basándonos en un documento en formato *.odt*. Se pretende de esta manera:

* Simplificar la curva de aprendizaje para la creación de contenidos.
* Conseguir una exportación en formato *.pdf* óptima.
* Crear documentación vistosa.
* *Responsive*. Compatible con dispositivos de diferentes tamaños.
* Dotarla por defecto de soporte de accesibillidad

## Ejecución

La ejecución de *mentor* se puede realizar 

Desde consola:

~~~
mentor.py [-h] [-f] filename
~~~

Donde:
    *-h*: muestra la ayuda
    *-f*: fuerza la sobreescritura de la carpeta destino en caso de que ya existiera.
    *filename*: nombre del fichero *.odt* a ser procesado.

## Elementos soportados

#### Bloques y apartados

*Mentor* genera una estructura compuesta por tantas páginas (bloques) como encabezados de nivel 1 (*Encabezado 1*) exitan en el documento *odt*. Los párrafos marcados como *Encabezado 1* pero vacíos son descartados. Para que la generación pueda realizarse, es necesario que exista al menos un *Encabezado 1* y que sea el primero de todos lso encabezados (no puede haber ningún encabezado de un nivel inferior por delante en el texto)

## Plantillas / Templates

Es posible configurar la presentación del paquete generado mediante el uso plantillas desarrolladas en HTML5/JS/CSS3. Las plantillas se almacenan en la carpeta *templates*.

### Como crear una plantilla

Cada plantilla se define en una carpeta con el nombre de la plantilla. En su interior debe existir:

* un fichero *chapter.html*, que define la plantilla para cada uno de los bloques principales.
* *[Opcional]* Una carpeta llamada css donde se almacenen los ficheros CSS a aplicar en la plantilla. En ella no se deben incluir los ficheros CSS de Bootstrap.

### Variables

Las variables descritas como **.nombre* hacen referencia los elementos que podemos encontrar en cada uno de los elementos de la lista definida previamente

**Generales**

| Variable | Definición           | 
| :------- | :------------------- | 
| $title   | Título de la unidad  |
| $lang    | Idioma del documento |

**Encabezados**

| Variable | Definición           | 
| :------- | :------------------- | 
| blocks   | Lista con los bloques de nivel 1 *(Encabezado 1)* de la unidad  | 
| *.string   | Texto del encabezado de nivel 1 | 
| *.number   | Número de orden del encabezado | 


## Author / Autor

Alfredo Oltra (Twitter:  [@aoltra](https://twitter.com/aoltra) / [@uhurulabs](https://twitter.com/uhurulabs))

## Licencia
	
El proyecto está liberado bajo licencia [GPL 3.0](https://www.gnu.org/licenses/gpl-3.0-standalone.html).