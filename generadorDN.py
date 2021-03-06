#!/usr/bin/env python
# coding: utf-8

import yaml
import re
import random

# CONSTANTES
# Definimos unas constantes para los operadores lógicos...
lenguaje = [
    "~",
    "&",
    "v",
    "→",
    "↔",
    "(",
    ")"
]

# ...y una lista de reglas de inferencia.
reglas = [
    "Simp.",
    "Conj.",
    "Add.",
    "SD",
    "MP",
    "MT",
    "DB",
    "Sust.",
    "Inst.",
    "Gen.",
    "CB",
    "PC",
    "Dil.",
    "RA",
    "Dist.",
    "Asoc.",
    "Conm.",
    "Impl.",
    "PE",
    "Univ.",
    "IC",
    "Export.",
    "Trans.",
    "DN",
    "PI",
    "DeM",
    "R"
]

# FUNCIONES AUXILIARES

# Esta función recibe un ejercicio que contiene premisas y pasos.
# Pasamos por cada uno de los pasos para extraer las proposiciones atómicas.
# Ya que estamos pasando por cada proposición atómica, revisamos la presencia
# de cuantificadores para agregarlos al lenguaje en caso de que sea necesario.
# Hacemos esto por cada ejercicio en caso de que tengamos cuantificadores
# con variables diferentes.


def parseAtomicas(ejercicio):
    lenguaje_local = []
    proposiciones = []

    filas = ejercicio['premisas'] + ejercicio['pasos']

    for paso in filas:
        props = []
        cuantificadores = []

        if type(paso) is dict:
            resultado = parseAtomicas(paso['prueba'])
            props += resultado[0]
            lenguaje_local += resultado[1]

        else:
            if type(paso) is str:
                fila = paso

            elif type(paso) is list:
                fila = paso[0]

            props += re.findall('[A-Z][a-z]+', fila)
            props += re.findall('[a-z]=[a-z]', fila)

            cuantificadores += re.findall('\(∀[a-z]\)', fila)
            cuantificadores += re.findall('\(∃[a-z]\)', fila)

        for prop in props:
            if prop not in proposiciones:
                proposiciones.append(prop)

        for cuantificador in cuantificadores:
            if cuantificador not in lenguaje_local:
                lenguaje_local.append(cuantificador)

        lenguaje_local = list(set(lenguaje_local))

    return proposiciones, lenguaje_local

# Función para extraer reglas del ejercicio. Mejor que sea otra función.


def extraerReglas(prueba):
    reglasLocales = []

    for paso in prueba['pasos']:
        print('\t\t' + str(paso))
        if type(paso) == list:
            reglasLocales += [regla for regla in re.findall(
                '[A-Za-z]+\.?', paso[1]) if regla not in reglasLocales]

        elif type(paso) == dict:
            reglasLocales += extraerReglas(paso['prueba'])

    return reglasLocales

# Definimos una función de reemplazo que va por cada string de cada paso
# y reemplaza cada proposición atómica, cada operador y cada regla de inferencia y número
# por un código [[X]] para moodle. Esto es lo que nos ayuda a formar las casillas.


def reemplazo(paso):
    string = paso

    for item in completo:
        if "*" not in string:
            rem = '(?<!\[\[)' + item.replace('(', '\(').replace(')', '\)') + '(?!\]\])'

            string = re.sub(
                rem, '[[' + str(completo.index(item) + 1) + ']]', string)

    string = string.replace("*", "")

    return string

# Esta función genera la tabla del ejercicio en HTML.
# Esta es la que nos premite presentar el ejercicio en moodle.

# Contamos los niveles de profundidad de las pruebas auxiliares.


def contar_profundidad(prueba):
    niveles = 0
    # si la prueba no contiene diccionarios
    if not any(type(paso) is dict for paso in prueba['pasos']):
        return 0
    else:
        subpruebas = [paso['prueba']
                      for paso in prueba['pasos'] if type(paso) is dict]
        niveles += 1
        for subprueba in subpruebas:
            niveles += contar_profundidad(subprueba)
        return niveles

# Función para contar los pasos incluyendo los pasos en subpruebas


def contarPasos(prueba, contador=0):
    pasos = prueba['pasos'] + prueba['premisas']
    for paso in pasos:
        if type(paso) is str or type(paso) is list:
            contador += 1

        elif type(paso) is dict:
            contador = contarPasos(paso['prueba'], contador)
    return contador

# Produce la columna con los pasos


def columnaPasos(contador):
    columna = '\n\t\t<td style="padding: 5px; border-right: 1px solid black;"> %s </td>\n' % contador
    return columna

# Rellena según el nivel de profundidad del ejercicio


def relleno(nivel):
    # Agregar celdas para profundidad
    relleno = ""
    for x in range(nivel):
        relleno += '<td style="padding: 5px; border-right: 1px solid black;"></td>'
    return relleno

# Arma las celdas de proposiciones y reglas


def armarContenido(texto, regla, profundidad, isLastPremisa=False):
    estilo = "padding: 5px; "

    # Si estamos en la última premisa,
    # agregue un borde abajo.
    if isLastPremisa:
        estilo += "border-bottom: 1px solid black;"

    colTexto = '\t\t<td style="%s" colspan="%s"> %s </td>' % (
        estilo, profundidad, texto)

    colRegla = '\t\t<td>%s</td>\n' % regla

    return colTexto + colRegla

# Genera las filas de la tabla en HTML


def generarFilas(ejercicio, profundidad, nivel=0, contador=1):
    filas = ""

    for premisa in ejercicio['premisas']:
        if premisa == ejercicio['premisas'][-1]:
            isLastPremisa = True
        else:
            isLastPremisa = False

        filas += '\t<tr>' + columnaPasos(contador) + relleno(nivel) + armarContenido(
            reemplazo(premisa), reemplazo('S'), profundidad, isLastPremisa) + '</tr>\n'

        contador += 1

    for paso in ejercicio['pasos']:

        if type(paso) is dict:
            subfilas, contador = generarFilas(
                paso['prueba'], profundidad - 1, nivel + 1, contador)
            filas += subfilas

        else:
            print("\t%s" % paso)

            filas += '\t<tr>' + columnaPasos(contador) + relleno(nivel) + armarContenido(
                reemplazo(paso[0]), reemplazo(paso[1]), profundidad) + '</tr>\n'

            contador += 1

    return filas, contador

# Genera la tabla en HTML


def generarTabla(ejercicio):
    tabla = "<strong>Objetivo: </strong>%s<br>" % ejercicio['objetivo']
    tabla += "<table>"
    # contar profundidad
    profundidad = contar_profundidad(ejercicio) + 1

    filas = generarFilas(ejercicio, profundidad)[0]
    tabla += filas
    tabla += '</table>'
    return tabla


# Esto genera el XML correspondiente al ejercicio.
# Juntamos la tabla generada en HTML con código XML de Moodle para su importación.

def generar_ejercicio(tabla, contador_ejercicios):

    ejercicio_html = """
    <question type="ddwtos">
        <name>
           <text>%s (%s) %s</text>
        </name>
        <questiontext format="html">
            <text><![CDATA[\n""" % (abreviatura, dificultad,  contador_ejercicios)

    contador_ejercicios += 1

    ejercicio_html += tabla

    ejercicio_html += """
        ]]></text>
        </questiontext>
        <generalfeedback format="html">
          <text></text>
        </generalfeedback>
        <defaultgrade>1.0000000</defaultgrade>
        <penalty>0.3333333</penalty>
        <hidden>0</hidden>
        <shuffleanswers>0</shuffleanswers>
        <correctfeedback format="html">
          <text><![CDATA[<p>Respuesta correcta</p>]]></text>
        </correctfeedback>
        <partiallycorrectfeedback format="html">
          <text><![CDATA[<p>Respuesta parcialmente correcta.</p>]]></text>
        </partiallycorrectfeedback>
        <incorrectfeedback format="html">
          <text><![CDATA[<p>Respuesta incorrecta.</p>]]></text>
        </incorrectfeedback>
        <shownumcorrect/>\n"""

    return ejercicio_html

# Generamos las casillas (dragboxes) para cada proposición atómica, operador y regla de inferencia.


def generar_dragboxes(proposiciones, lenguaje_local):
    dragboxes = ""
    for item in completo:
        item_html = "<dragbox>\n"
        item_html += "\t\t\t<text><![CDATA[%s]]></text>\n" % item

        if item in proposiciones:
            grupo = 1
        elif item in lenguaje_local:
            grupo = 1
        elif item in reglas:
            grupo = 3
        else:
            grupo = 4

        item_html += "\t\t\t<group>%s</group>\n" % grupo
        item_html += "\t\t\t<infinite/>\n"
        item_html += "\t\t</dragbox>\n"

        dragboxes += item_html

    return dragboxes


# Constante de comienzo del código html
html = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n'

# Loop principal
contador_ejercicios = 1

# Cargamos los ejercicios en formato JSON
with open('ejercicios.yml') as f:
    ejercicios = yaml.load(f.read(), Loader=yaml.FullLoader)

# Asignamos un nombre y categoría para los ejercicios
categoria = input("Escriba un tema: ")
abreviatura = input("Escriba una abreviatura para el tema: ")
autor = input("Autor/a: ")

for conjunto_por_dificultad in ejercicios:
    dificultad = conjunto_por_dificultad["dificultad"]

    # Comenzamos el html del ejercicio declarando la categoría
    html += """
    <question type="category">
    <category>
    <text>$course$/top/Deducción natural/Autogenerados/%s/%s (%s)</text>

    </category>
    </question>""" % (categoria, dificultad, autor)

    for ejercicio in conjunto_por_dificultad["ejercicios"]:

        # Procesamos el ejercicio
        print("%s: %s" % (contador_ejercicios, ejercicio["objetivo"]))

        # Extraemos las proposiciones atómicas y los cuantificadores si los hay.
        proposiciones, lenguaje_local = parseAtomicas(ejercicio)
        reglasLocales = extraerReglas(ejercicio)

        # Agregamos los cuantificadores al lenguaje general
        lenguaje_local += lenguaje

        # Contamos el total de pasos para armar una lista con los pasos
        # y agregarlos al lenguaje completo.
        total_pasos = contarPasos(ejercicio)
        lista_pasos = [str(x) for x in range(total_pasos, 0, -1)] + ['-']

        # Armamos una lista del lenguaje completo, incluyendo los números
        # de los pasos, cuantificadores, las reglas de inferencia y las
        # proposiciones atómicas.
        reglasEjercicio = random.sample(
            [regla for regla in reglas if regla not in reglasLocales], k=3) + reglasLocales
        random.shuffle(reglasEjercicio)
        reglasEjercicio = list(set(reglasEjercicio))

        # Tenemos que depurar la lista de reglas. Hay que poner las reglas que
        # están en el ejercicio y un par más, pero no todas. De lo contrario,
        # sobrecargamos algunos exploradores.
        completo = lista_pasos + reglasEjercicio + lenguaje_local + proposiciones

        # Generamos una tabla en html para el ejercicio
        tabla = generarTabla(ejercicio)

        # Generamos el xml del ejercicio y subimos el contador de ejercicios.
        ejercicio_html = generar_ejercicio(tabla, contador_ejercicios)
        contador_ejercicios += 1

        # Generamos las casillas de arrastre para el ejercicio.
        ejercicio_html += generar_dragboxes(proposiciones, lenguaje_local)

        # Cerramos el xml del ejercicio y lo agregamos al html general.
        ejercicio_html += '</question>\n'
        html += ejercicio_html

html += '</quiz>'

print("¡Listos!")
print("Ejercicios procesados: %s" % (contador_ejercicios - 1))

with open('ejercicios.xml', 'w') as f:
    f.write(html)
