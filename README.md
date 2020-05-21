# generadorDN
Generador de preguntas de deducción natural para Moodle.

Autores: Juan R. Loaiza y Juliana Gutiérrez

Este código pasa preguntas en formato [YAML](https://yaml.org/) a [preguntas de arrastre](https://docs.moodle.org/all/es/Tipo_de_pregunta_arrastrar_y_soltar_al_texto) con casillas para Moodle en formato XML.

## Instrucciones
En la carpeta misma de generadorDN.py debe haber un archivo llamado "ejercicios.yaml" con la siguiente estructura:

~~~
  - dificultad: Fácil
  - ejercicios:
    - objetivo: Qa & Qb
      premisas:
      - Qa & (Qb v Qc)
      - Qb v ~Qa
      pasos:
      - ['Qa*', 'Simp. 1']
      - ['Qb', 'SD 2 3']
      - ['Qa & Qb', Conj. 3 4]
~~~
Los ejercicios van divididos por dificultad y contienen:
* Objetivo: Conclusión de la deducción
* Premisas: Premisas de la deducción
* Pasos: Cada paso de la deducción como una lista con el paso y la regla de inferencia correspondiente.
  * Si desea que el código no reemplace un paso por una casilla de arrastre (e.g. para desambiguar una deducción), incluya un asterisco en el texto (véase el paso 3 en el ejemplo anterior).

Si se quiere hacer uso de pruebas auxiliares, es posible integrarlas de la siguiente manera:
~~~
- dificultad: Fácil
  ejercicios:
  - objetivo: (Pa & Rb) → Qa
    premisas:
    - "*Pa → Qa"
    pasos:
    - prueba:
        premisas:
        - Pa & Rb
        pasos:
        - [Pa, Simp. 2]
        - [Qa, MP 1 3]
    - [(Pa & Rb) → Qa, PC 2-4]
~~~
En este caso, se incluye como uno de los pasos un ítem llamado "prueba" que contiene nuevamente premisas y pasos. El código generará la prueba auxiliar correspondiente. Es importante aquí el nivel de indentación de cada conjunto de premisas y pasos.

Una vez tenga el archivo con los ejercicios que desee procesar, basta con ejecutar el código en la terminal (`python generadorDN.py`) e introducir:
* Nombre del conjunto de ejercicios.
* Abreviación (que se usará para darle nombre a cada ejercicio)
* Autor/a

Si el código corre con éxito, encontrará un archivo `ejercicios.xml` en la carpeta que podrá importar directamente en Moodle.
