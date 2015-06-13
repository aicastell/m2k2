<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta charset="UTF-8">
</head>

<body>

<h1>
1. Introducción
</h1>

<p align=justify>
Vamos a seguir todos los pasos necesarios para diseñar e implementar un intérprete. Un intérprete es un programa que recibe como entrada un programa en un lenguaje determinado y que produce como salida el resultado de su ejecución.  El lenguaje aceptado como entrada por el intérprete que vamos a implementar se denomina m2k2. Vamos a describir la especificación formal del lenguaje.</p>


<h1>
2. Tipos de datos
</h1>

<p align=justify>
Las variables que pueden definirse en m2k2 siempre llevan definido un tipo. Los tipos que pueden definirse son dos: el entero y el real. El lenguaje no asume convenios ni rangos de representación concretos, que dependerán de la arquitectura sobre la que se ejecute el interprete. En cuanto a los valores logicos, m2k2 no dispone de un tipo lógico explicito, sino que utiliza variables de tipo entero para representarlos: el cero se asocia al valor falso, y otros enteros, no nulos, se consideran asociados al cierto. El lenguaje no acepta cadenas de caracteres ni vectores.


<h1>
3. Nivel lexico
</h1>

<p align=justify>
Los programas en m2k15 utilizan el juego de caracteres ASCII de 7 bits. A la hora de identificar los diferentes componentes léxicos de un programa m2k15 se sigue siempre una "estrategia avariciosa": procedimiento de izquierda a derecha, el siguiente componente será de la porción de programa pendiente de analizar, el prefijo mas largo que pertenezca al conjunto de componentes léxicos básicos del lenguaje.</p>

<h2>
Blancos
</h2>

<p align=justify>
Los componentes lexicos pueden separarse por cualquier secuencia de espacios en blanco, tabuladores, y saltos de linea. El salto de linea cumple en m2k2 la función de terminador. El lenguaje no admite comentarios.</p>

<h2>
Identificadores
</h2>

<p align=justify>
Los identificadores serán secuencias de caracteres donde pueden intervenir letras, digitos y el caracter subrayado, y que comienzan siempre por letra. Los identificadores harán referencia a las variables. Las letras mayusculas y minusculas no son equivalentes: así por ejemplo "abc", "AbC" y "ABC" hacen referencia a 3 variables diferentes.</p>

<h2>
Literales
</h2>

<p align=justify>
A continuación se presentan los literales que dentro de un programa m2k2 permite especificar valores constantes.</p>

<h3>
Literales enteros
</h3>

<p align=justify>
Los literales enteros pueden ser en notación decimal o en notación hexadecimal. En notación decimal se utilizan secuencias de digitos en base 10 (por ejemplo 123). En notación hexadecimal se emplea el caracter '#' para cambiar a base hexadecimal (por ejemplo #12ac).</p>


<h3>
Literales reales
</h3>

<p align=justify>
Los literales reales han de expresarse en notación cientifica, en formato: entero.decimal[eE][+-]digitos. Observa que aunque la parte "entero.decimal" es obligatoria (y va separada por un punto), la parte del exponente es opcional. La letra 'e' puede ser indistintamente mayuscula o minuscula. Por ejemplo, 2.37, 0.1e-1 o 100.0e+10 son ejemplos validos de literales reales.</p>


<h2>
Operadores
</h2>

<p align=justify>
El lenguaje dispone del siguiente conjunto de operadores:</p>

<pre>
     + - * / % & | ! = != <> < > <= >=
</pre>

Ademas algunos de ellos pueden intervenir como parte de unos componentes léxicos mas complejos llamados operatorios, donde aparecen entre parentesis:

<pre>
    (+) (-) (*) (/) (%) (&) (|)
</pre>


<h2>
Palabras clave
</h2>

<p align=justify>
Las palabras clave que define el lenguaje son:
</p>

<pre>
    ENTER REAL
</pre>

<p align=justify>
Las palabras clave pueden escribirse en mayusculas y en minusculas, indistintamente, o utilizando cualquier combinación de ambas. Son palabras reservadas que por tanto no pueden utilizarse como identificadores.
</p>


<h2>
Otros componentes lexicos
</h2>

<p align=justify>
El nucleo básico del lenguaje también admite los siguientes componentes léxicos:</p>

<pre>
    (   )   <-   ,   ..   :
</pre>


<h1>
4. Expresiones
</h1>

<p align=justify>
Las expresiones mas simples validas en el nucleo básico del lenguaje son los literales y las variables de los tipos numéricos elementales. También son validas aquellas expresiones que pueden construirse a partir de otras utilizando operadores. El lenguaje posee operadores aritmeticos, de comparación y lógicos. Ademas, también posee una construcción especial para expresar la aplicación reiterada de un mismo operador binario, construcción a la que denominaremos expresión "operatorio", por tratarse de una generalización de la notación matemática de sumatorios y productorios.</p>


<h2>
Operadores aritméticos
</h2>

<p align=justify>
Los operadores aritméticos aplicables a operandos de tipos numericos son los siguientes:
</p>

<pre>
    + suma (binario) o sin efecto (unario)
    - resta (binario) o cambio de signo (unario)
    * multiplicación (binario)
    / división (binario)
    % resto (binario)
</pre>

<p align=justify>
La operación de dos valores del mismo tipo siempre devuelve un valor de ese tipo. En particular, cabe señalar que la división de dos valores enteros devuelve el entero resultante de realizar la división entera del primer valor entre el segundo (por ejemplo, 7/3 devuelve 2).
</p>

<p align=justify>
Si se realiza una operación aritmetica entre dos valores numericos de tipos distintos, se somete al operando de tipo menos general, antes de realizar los calculos propios de la operación, a una conversión implicita al tipo mas general (el tipo real es mas general que el tipo entero). Se dice que el operando "promociona", y como consecuencia de ello, el resultado de la operación acaba siendo del tipo mas general.</p>

<p align=justify>
El caso del operador % es especial, ya que requiere obligatoriamente que sus dos operandos sean de tipo entero. El resultado de una operación como a%b, el resto de la división entera de a entre b, puede expresarse entonces como a-b*(a/b).  </p>

<h2>
Operadores de comparación
</h2>

<p align=justify>
Los operadores de comparación son los siguientes:
</p>

<pre>
    =  igual
    != distinto
    <> distinto
    < menor
    > mayor
    <= menor o igual
    >= mayor o igual
</pre>

<p align=justify>
Son todos operadores binarios, y en principio, los valores comparados han de ser del mismo tipo numérico elemental, si bien también se pueden realizar comparaciones en las que intervengan un valor real y uno entero, en cuyo caso se produce una previa conversión implicita del operando entero al tipo real.
</p>

<p align=justify>
El resultado devuelto es siempre de tipo entero: un 0 para representar el valor falso y un 1 para representar el valor cierto.
</p>


<h2>
Operadores logicos
</h2>

<p align=justify>
Los operadores lógicos son:
</p>

<pre>
    & conjunción (binario)
    | disyunción (binario)
    ! negación (unario)
</pre>

<p align=justify>
Los operadores lógicos solo pueden operar sobre operandos de tipo entero (el cero se interpreta como falso y cualquier otro valor, como cierto), y el resultado que devuelven es, también, de tipo entero: 0 para representar falso y 1 para representar cierto.</p>

<p align=justify>
Cabe señalar que, en el caso de los operadores lógicos binarios, el lenguaje no garantiza que, cuando baste el valor del primer operando para determinar el valor del resultado, no intente evaluarse el segundo. Será responsabilidad del interprete del lenguaje optimizar la evaluación de este tipo de expresiones.</p>


<h2>
Reglas de precedencia y asociatividad
</h2>

<p align=justify>
En el lenguaje m2k2 los operadores unarios son prefijos y los binarios son infijos y asociativos por la izquierda. Respecto a los niveles de precedencia, estos son solo tres:</p>

<ul>
<li>MAXIMA: La de los operadors unarios
<li>INTERMEDIA: La de los operadores de multiplicación, división, resto, conjunción y comparación.
<li>MINIMA: La de los operadores de suma, resta y disyunción.
</ul>

<p align=justify>
Se permite el uso de parentesis para especificar la aplicación de operadores en uno orden distinto del que se seguirá de sus reglas de precedencia y asociatividad.</p>


<h2>
La expresión operatorio
</h2>

<p align=justify>
El lenguaje m2k2 ofrece una expresión "operatorio" con la sintaxis:</p>

<pre>
    idop(ident, expr1..expr2,expr3)
</pre>

<p align=justify>
donde "idop" puede ser cualquier identificador de los definidos en la sección que hablamos de los operatorios, "ident" debe ser el identificador de una variable (la variable muda del operatorio), adecuadamente declarada de tipo entero, las expresiones "expr1" y "expr2" han de ser de tipo entero, y expr3 puede ser de cualquier tipo numérico, con la restricción de que en el interior de expr3 no puede aparecer otro "operatorio" que utilice a "ident" también como variable muda.</p>

<p align=justify>
En lo que respecta a la semantica de la expresión, se puede decir, informalmente, que se trata de aplicar reiteradamente el operador binario (aritmetico o logico) que aparece entre parentesis en "idop" a una lista de operandos de la forma expr3, donde la variable "ident" va tomando, sucesivamente y en orden creciente, todos los valores comprendidos entre un limite inferior (el resultado de evaluar expr1) y uno superior (el resultado de evaluar expr2), ambos inclusive. Es responsabilidad del usuario del lenguaje que el limite superior sea mayor o igual que el inferior.</p>

<p align=justify>
Así por ejemplo, el sumatorio de j desde 1 hasta 1000 de j^2 se podría expresar en m2k2 como (+)(j,1..1000,j*j). Mientras que el resultado de evaluar (/)(k,1..3,k+0.5) sería el mismo que el de evaluar 1.5/2.5/3.5</p>


<h1>
Estructura de los programas
</h1>

<p align=justify>
Los programas en m2k2 son secuencias de cero o mas declaraciones de las siguientes clases: declaraciones de variables y sentencias (simples o compuestas).
</p>

<h2>
Declaraciones de variables
</h2>

<p align=justify>
Declarar una variable consiste en asociar un identificador con un determinado tipo de variable (entera o real).
</p>

<p align=justify>
En m2k2 pueden declararse simultáneamente variables de un mismo tipo mediante lo que se denomina una declaración homogenea de variables, consistente en una especificación del tipo de las variables, y una lista de uno o mas identificadores separados por comas.
</p>

<p align=justify>
Todas las variables a las que se haga referencia en el programa deben haber sido explicitamente declaradas previamente. Por otra parte esta prohibido usar el mismo identificador mas de una vez para declarar variables.</p>

<h3>
Variables de tipos elementales
</h3>

<p align=justify>
Para los tipos elementales, la especificación de tipo consiste, simplemente, en la palabra clave que lo identifica: ENTER para el tipo entero y REAL para el tipo real. Asi, por ejemplo, podrían declararse las variables enteras a y esPar y la real X1, de la siguiente manera:
</p>

<pre>
    ENTER a, esPar
    REAL X1
</pre>


<h2>
Sentencias simples
</h2>

<p align=justify>
Las sentencias simples que ofrece el lenguaje son las de asignación y las de expresión.
</p>

<h3>
Sentencias de asignación
</h3>

<p align=justify>
Las sentencias de asignación en m2k2 permiten asignar el valor de una expresión al objeto receptor referenciado por su parte izquierda. Su sintaxis puede expresarse como:
</p>

<pre>
    receptor <- expresion
</pre>

<p align=justify>
donde receptor puede ser únicamente un identificador de una variable de tipo elemental previamente declarada. El tipo de receptor ha de ser el mismo que el de expresión, o bien un tipo mas general, en cuyo caso el valor de la expresión se convierte implicitamente al tipo del receptor antes de realizar la asignación.</p>

<h3>
Sentencias expresión
</h3>

<p align=justify>
Cualquier expresión correcta constituye una sentencia válida en el lenguaje, cuya ejecución consiste, simplemente, en evaluar la expresión. El interprete del lenguaje m2k2 actuará mostrando por la salida estandar el resultado de evaluar las expresiones.
</p>

<h1>
Ejemplo
</h1>

<p align=justify>
Para finalizar con la definición del lenguaje se ofrece a modo de ejemplo un programa en el lenguaje m2k2:
</p>

<pre>
    >>> enter inicio, final
    >>> inicio<-0
    >>> final<-3
    >>>
    >>> real x
    >>> x<-3.5
    >>>
    >>> enter i
    >>> x <- (*)(i,inicio..final,x) + (+)(i,1..10,i)
    >>> x
    205.0625
</pre>

</body>

