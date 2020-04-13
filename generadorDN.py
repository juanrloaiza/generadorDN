#!/usr/bin/env python
# coding: utf-8

import json
import re

## CONSTANTES
# Definimos unas constantes para los operadores lógicos...
lenguaje = [
    "&",
    "v",
    "→",
    "⟷",
    "~",
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
    "Gen."
]

### FUNCIONES AUXILIARES

# Esta función recibe un ejercicio que contiene premisas y pasos.
# Pasamos por cada uno de los pasos para extraer las proposiciones atómicas.
# Ya que estamos pasando por cada proposición atómica, revisamos la presencia
# de cuantificadores para agregarlos al lenguaje en caso de que sea necesario.
# Hacemos esto por cada ejercicio en caso de que tengamos cuantificadores
# con variables diferentes.

def parse_atomicas(ejercicio):
    lenguaje_local = []

    proposiciones = []

    for paso in ejercicio['pasos']:
        props = re.findall('[A-Z][a-z]+', paso[0])
        props += re.findall('[a-z]=[a-z]', paso[0])
        for prop in props:
            if prop not in proposiciones:
                proposiciones.append(prop)

        cuantificadores = re.findall('\(∀[a-z]\)', paso[0])
        cuantificadores += re.findall('\(∃[a-z]\)', paso[0])

        for cuantificador in cuantificadores:
            if cuantificador not in lenguaje_local:
                lenguaje_local.append(cuantificador)

    return proposiciones, lenguaje_local


# Definimos una función de reemplazo que va por cada string de cada paso
# y reemplaza cada proposición atómica, cada operador y cada regla de inferencia y número
# por un código [[X]] para moodle. Esto es lo que nos ayuda a formar las casillas.

def reemplazo(paso):
    string = paso

    for item in completo:
        if "*" not in string:
            #print("Buscando: %s" % item)
            rem = '(?<!\[\[)' + item.replace('(', '\(').replace(')', '\)') + '(?!\]\])'

            string = re.sub(rem, '[[' + str(completo.index(item) + 1) + ']]', string)

    string = string.replace("*", "")

    #print("%s → %s" % (paso, string))
    return string

## Esta función genera la tabla del ejercicio en HTML.
# Esta es la que nos premite presentar el ejercicio en moodle.

def generar_tabla(ejercicio):

    tabla = "<strong>Conclusión:</strong> %s <br>\n<table>\n" % ejercicio['objetivo']
    contador_pasos = 1

    for premisa in ejercicio['premisas']:
        row_tag = '\t<tr>'
        columna_pasos = '\n\t\t<td style="padding: 5px; border-right: 1px solid black;"> %s </td>\n' % contador_pasos
        contador_pasos += 1

        if premisa == ejercicio['premisas'][-1]:
            premisa_html = '\t\t<td style="padding: 5px; border-bottom: 1px solid black;" colspan="2"> %s </td>\n' % premisa

        else:
            premisa_html = '\t\t<td style="padding: 5px;" colspan="2"> %s </td>\n' % premisa

        tabla += '\t<tr>' + columna_pasos + premisa_html + '</tr>\n'


    for paso in ejercicio['pasos']:
        columna_pasos = '\t\t<td style="padding: 5px; border-right: 1px solid black;"> %s </td>\n' % contador_pasos
        contador_pasos += 1

        regla = '\t\t<td>%s</td>\n' % reemplazo(paso[1])

        paso_html = '\t\t<td style="padding: 5px;"> %s </td>\n' % reemplazo(paso[0])

        tabla += '\t<tr>' + columna_pasos + paso_html + regla + '</tr>\n'

    tabla += '</table>\n'

    return tabla

## Esto genera el XML correspondiente al ejercicio.
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
with open('ejercicios.json') as f:
    ejercicios = json.loads(f.read())

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

        proposiciones, lenguaje_local = parse_atomicas(ejercicio)

        lenguaje_local += lenguaje

        total_pasos = len(ejercicio['premisas']) + len(ejercicio['pasos'])

        lista_pasos = [str(x) for x in range(total_pasos + 1, 0, -1)]

        completo = lista_pasos  + lenguaje_local + reglas + proposiciones

        tabla = generar_tabla(ejercicio)

        ejercicio_html = generar_ejercicio(tabla, contador_ejercicios)
        contador_ejercicios += 1

        ejercicio_html += generar_dragboxes(proposiciones, lenguaje_local)

        ejercicio_html += '</question>\n'

        html += ejercicio_html

html += '</quiz>'

print("¡Listos!")
print("Ejercicios procesados: %s" % (contador_ejercicios - 1))

with open('ejercicios.xml', 'w') as f:
    f.write(html)
