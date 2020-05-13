#!/usr/bin/env python
# coding: utf-8

instrucciones = {
    'validez': '<p>Demuestre que el siguiente argumento es válido o inválido. </p><p>Traduzca los enunciados y demuestre validez o invalidez usando tablas de verdad o deducción natural.</p><p><small>Nota: Si los enunciados contienen cuantificadores, no use tablas de verdad.</small></p>',
    'consistencia': '<p>Demuestre que el siguiente conjunto es consistente o inconsistente. </p><p>Traduzca los enunciados y demuestre consistencia o inconsistencia usando tablas de verdad o deducción natural.</p><p><small>Nota: Si los enunciados contienen cuantificadores, no use tablas de verdad.</small></p>',
    'equivalencia': '<p>Demuestre si los siguientes enunciados son equivalentes. </p><p>Traduzca los enunciados y demuestre su equivalencia (o falta de equivalencia) usando tablas de verdad o deducción natural.</p><p><small>Nota: Si los enunciados contienen cuantificadores, no use tablas de verdad.</small></p>',
    'tautologia-contradiccion': '<p>Demuestre si el siguiente enunciado es una tautología, una contradicción o una contingencia. </p><p>Traduzca los enunciados y demuestre usando tablas de verdad o deducción natural.</p><p><small>Nota: Si los enunciados contienen cuantificadores, no use tablas de verdad.</small></p>'
}

def generarHTML(ejercicio):
    style = 'margin: 1em'
    html = instrucciones[ejercicio['tipo']]

    if ejercicio['tipo'] == 'validez':
        html += '<table style="%s"><tbody>' % style

        for enunciado in ejercicio['premisas']:
            html += '<tr><td>' + enunciado + '</td></tr>'

        html += '<tr><td style="border-top: 1px solid black">' + ejercicio['conclusion'][0] + '</td></tr>'
        html += '</tbody></table>'

    elif ejercicio['tipo'] == 'consistencia':
        html += '<p style="%s">{' % style
        for enunciado in ejercicio['premisas']:
            if enunciado != ejercicio['premisas'][-1]:
                html += enunciado + '; '
            else:
                html += enunciado
        html += '}</p>'

    elif ejercicio['tipo'] == 'equivalencia':
        html += '<p style="%s">' % style
        html += ejercicio['premisas'][0] + ' :: ' + ejercicio['premisas'][1]
        html += '</p>'

    else:
        html += '<p style="%s">' % style
        html += ejercicio['premisas'][0]
        html += '</p>'

    html += '<p>Escriba su respuesta en el campo de texto proporcionado y adjunte el archivo con la tabla de verdad o la deducción correspondiente.</p>'
    return html

def main():
    counter = 1

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>'

    for ejercicio in ejercicios:
        nombre = ejercicio['tipo'] + str(counter)

        xmlPregunta =  '''<question type="category">
    <category>
        <text>$course$/top/Examen final/%s</text>

    </category>
  </question>
  <question type="essay">
    <name>
      <text>%s</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[%s]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text></text>
    </generalfeedback>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.0000000</penalty>
    <hidden>0</hidden>
    <responseformat>plain</responseformat>
    <responserequired>1</responserequired>
    <responsefieldlines>1</responsefieldlines>
    <attachments>1</attachments>
    <attachmentsrequired>1</attachmentsrequired>
    <graderinfo format="html">
      <text></text>
    </graderinfo>
    <responsetemplate format="html">
      <text></text>
    </responsetemplate>
  </question>''' % (ejercicio['tipo'].title(), nombre ,generarHTML(ejercicio))

        counter += 1

        xml += xmlPregunta

    xml += '</quiz>'

    return xml

with open('parcial.json') as f:
    ejercicios = f.read()

with open('examen.xml', 'w') as f:
    f.write(main())
