
# Mentor

## Introducción

Mentor es un programa para convertir documentos *.odt* en un paquete de documentos HTML que puedan ser utilizados en plataformas educacionales. 

El objetivo simplificar la creación de contenidos en formatos interactivos y fácilmente visibles en la WEB, basándonos en un documento en formato *.odt*. Se pretende de esta manera:

* Simplificar la curva de aprendizaje para la creación de contenidos.
* Conseguir una exportación en formato *.pdf* óptima.
* Crear documentación vistosa.
* *Responsive*. Compatible con dispositivos de diferentes tamaños.
* Dotarla por defecto de soporte de accesibillidad

## Funcionamiento
 
El creador de contenidos debe trabajar sobre un procesador de textos que soporte de manera nativa el formato odt ([OpenOffice](https://www.openoffice.org/es/) o [LibreOffice](https://es.libreoffice.org/)). Para ello debe utilizar la plantilla *mentor.es.ott* o *mentor.en.ott* que se encuentra disponible en la carpeta *ott templates*. Estas plantillas aportan estilos y funcionalidades que permiten la exportación vía *Mentor*. La exportación se encarga de obtener el contenido del documento y crear una colección de páginas web aplicándoles una plantilla HTML/CSS.

Por lo tanto Mentor funciona definiendo un documento pensado para formato papel (al cual le aplica los **estilos ott**) y exportándolo a formato HTML (aplicando **estilos CSS**). 

Lo importante de los estilos que proporciona el ott es el nombre, no como tengan definidas sus caracterísitcas. El usuario es libre de poder asignar a cada uno de los estilos las características que le interesen para que la presentación en papel sea lo más óptima y estética posible. Los estilos aplicados en el paquete HTML generado serán los definidos en la plantilla HTML (ficheros .css) que vaya a utilizar, no los definidos en el .ott.

### Estilos ott

*Mentor* utiliza dos tipos de estilos ott: estilos de serie del procesador (como los Encabezados) y estilos Mentor (que son aquellos que permiten la creación de elementos diferentes, como observaciones).

> Los estilos de *Mentor* empiezan con el prefijo MT

*Mentor* divide el documento en lo que denomina **bloques**, que son todas aquellas partes del documento encabezadas por un *Encabezados 1*. Es, por lo tanto, necesario que exista al menos un *Encabezado 1* en el documento. Además todos aquellos elementos ubicados delante del primer *Encabezado 1* no serán tenidos en cuenta.

En el apartado Elementos soportados se indican todos aquellos *estilos ott* y objetos que están soportados por *Mentor* y que por lo tanto son capaces de generar una salida HTML.

## Ejecución

La ejecución de *Mentor* se puede realizar 

Desde consola:

~~~
mentor.py [-h] [-f] filename
~~~

Donde:
    *-h*: muestra la ayuda
    *-f*: fuerza la sobreescritura de la carpeta destino en caso de que ya existiera.
    *filename*: nombre del fichero *.odt* a ser procesado.

## Elementos soportados

### Bloques y apartados

**Estilos**: *Encabezados 1..10*

*Mentor* genera una estructura compuesta por tantas páginas (bloques) como encabezados de nivel 1 (*Encabezado 1*) exitan en el documento *odt*. Los párrafos marcados como *Encabezado 1* pero vacíos son descartados. Para que la generación pueda realizarse, es necesario que exista al menos un *Encabezado 1* y que sea el primero de todos los encabezados (no puede haber ningún encabezado de un nivel inferior por delante en el texto).

Los encabezados 2 al 10 también son generados para la creación de secciones o apartados dentro de cada bloque.

### Observaciones

**Estilos**: *MT Observaciones 1..3*

Las observaciones pretenden ser textos que muestren al lector información que pueda ser interesante, importante, en la que suele comenter errores, etc. La plantilla ott proporciona tres estilos *MT Observaciones 1..3*. El estilo *MT Observaciones* no debe ser usado ya que únicamente se encuentra definido como estilo vinculado del resto. 

### Notas al pie

**Estilos**: *No es necesario aplicar ningún estilo*

Las notas al pie son indicaciones que el autor o el traductor incluye para aclarar algún aspecto o aportar más información. Para su generación no es necesario el uso de ningún estilo, simplemente elegir la inserción de *nota al pie* desde el procresador de textos.

## Plantillas / Templates

Es posible configurar la presentación del paquete generado mediante el uso plantillas desarrolladas en HTML5/JS/CSS3. Las plantillas se almacenan en la carpeta *templates*.

### Plantilla basic

Es la plantilla que por defecto propociona la instalación de *Mentor*

Soporta:

* Encabezados hasta nivel 3.
* 3 tipos de observaciones.
* Notas al pie.

### Como crear una plantilla

Cada plantilla se define en una carpeta con el nombre de la plantilla. En su interior debe existir:

* un fichero *chapter.html*, que define la plantilla para cada uno de los bloques principales.
* *[Opcional]* Una carpeta llamada *css* donde se almacenen los ficheros CSS a aplicar en la plantilla. En ella no se deben incluir los ficheros CSS de Bootstrap.
* *[Opcional]* Una carpeta llamada *js* donde se almacenen los ficheros javascript a aplicar en la plantilla. En ella no se deben incluir los ficheros js de Bootstrap.
* *[Opcional]* Todos aquellos ficheros .html que se vayan a incluir (con *xi:include*) dentro del fichero *chapter.html*.
* *[Opcional]* Una carpeta llamada *python* donde se almacenen los ficheros .py que incluyan funciones a utilizar dentro de la plantilla. Estas funciones se importan dentro de la plantilla y se utilizan mediante (NOMPLANTILLA: nombre de la plantilla, NOMFICHERO: nombre del fichero, NOMFUNCION: nombre de la función)

~~~
<?python import templates.NOMPLANTILLA.python.NOMFICHERO as MGF ?>

${MGF.NOMFUNCION()}
~~~

Las plantillas son creadas mediante [Genshi](https://genshi.edgewall.org/). La manera de crearlas es totalmente libre, con la única condición de que deber existir un fichero llamado *chapter.html*. 

Una recomendación que posibilita la escalabilidad de la plantilla así como la facilidad de adapatación, es la de estructurarla en tres páginas:

* *chapter*. Documento raíz que define las características básicas de la página a generar.
* *content*. Documento que define los elementos contenedores tipo bloque: párrados, cabeceras, observaciones...
* *element*. Documento que define los elementos html de tipo __inline__: span,... . 

Cada uno de estos documentos se inserta mediante *xi:include* otros documentos (normalmente en *chapter* se incluye *content* y en este  *element*). Por otra parte, teniendo en cuenta que es habitual que elementos __inline__ contengan otros elementos __inline__, es recomendable que *element* defina una función que pueda ser llamada recursivamente:

~~~
<div xmlns:py="http://genshi.edgewall.org/" py:def="render_elements(input)" py:strip="">
    ...
    ${render_elements(elementos)}        
    ...
</div>
~~~

Por lo demás cada uno de las páginas lo que hace es procesar los diferentes tipos de elementos y aplicarles la estructura y estilos deseados.

### Variables y funciones

Las variables y funciones descritas como **.nombre* hacen referencia los elementos que podemos encontrar en cada uno de los elementos de la lista definida previamente. Por ejemplo, **.number* hace referencia a la variable number de uno de los blocks.

(v): variable, (f): función

**Generales**

| Propiedad | Tipo  | Definición           | 
| :-------- | :---: | :------------------- | 
| title     |  (v)  | Título de la unidad  |
| lang      |  (v)  | Idioma del documento |
| blocks    |  (v)  | Listado de los títulos de los capítulos (encabezados nivel 1) de toda la unidad |
| content   |  (v)  | Listado del contenido del capítulo que se procesa |
| footnotes |  (v)  | Listado de notas al pie del capítulo que se procesa |

**Capítulos**

| Propiedad      | Tipo  | Definición                | 
| :------------- | :---: |:------------------------ | 
| blocks         |  (v)  | Lista de los capítulos, es decir los bloques de nivel 1 *(Encabezado 1)*, de la unidad  | 
| *.number       |  (v)  | Número de orden del capítulo | 
| *.block        |  (v)  | Contenido xml del encabezado del capítulo | 
| *.content      |  (v)  | Lista de objetos con el contenido de cada capítulo | 
| *.get_string() |  (f)  | Devuelve el texto del encabezado | 

**Contenido**

| Propiedad        | Tipo  | Definición           | 
| :--------        | :---: | :------------------- | 
| *.type           |  (v)  | Tipo de contenido | 
| *.elements       |  (v)  | Lista de elementos hijos | 
| *.element_style  |  (v)  | Estilo del elemento | 
| *.get_raw_text() |  (f)  | Devuelve el texto en crudo (son modificaciones de estilo del contenido | 
  
| Tipo 0   | Tipo  | Headings (Encabezados)     |
| :------- | :---: | :------------------------- | 
| *.level  |  (v)  | Nivel del encabezado 2..10 | 
  
| Tipo 1   | Paragraph (Párrafos)      |
| :------- | :-----------------------  | 
|          | Sin propiedades añadidas  |  

| Tipo 2   | Remarks (Observaciones)  |
| :------- | :----------------------- |  
|          | Sin propiedades añadidas |

| Tipo 3       | Tipo  | Footnote (Nota al pie)           |
| :----------- | :---: | :------------------------------  |  
| *.citation   |  (v)  | Número de nota al pie            | 
| *.body       |  (v)  | Elemento body de la nota al pie (tipo 5) | 
  
| Tipo 4       | Tipo  | Text (Texto)         |
| :----------- | :---: | :------------------- | 
| *.string     |  (v)  | Texto sin formato    | 
  
| Tipo 5       | Footnote.Body (Cuerpo de nota al pie)   |
| :----------- | :-------------------------------------  |  
|              | Sin propiedades añadidas                |
  
| Tipo 6   | Span                     |
| :------- | :----------------------- | 
|          | Sin propiedades añadidas |



## Documentos odt antiguos



## Problemas

¡¡No sandbox!!!

## Author / Autor

Alfredo Oltra (Twitter:  [@aoltra](https://twitter.com/aoltra) / [@uhurulabs](https://twitter.com/uhurulabs))

## Licencia
	
El proyecto está liberado bajo licencia [GPL 3.0](https://www.gnu.org/licenses/gpl-3.0-standalone.html).