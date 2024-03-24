# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 23:12:45 2024

@author: crist
"""

from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Cargar el modelo entrenado
with open('modelo_entrenado.pkl', 'rb') as f:
    model = pickle.load(f)

# Función para convertir la categoría seleccionada en variables dummy
def obtener_variables_dummy(categoria):
    variables_dummy = np.zeros(21)  # Aquí ajusta el tamaño según tu número de categorías
    index = ['A', 'B', 'C','C2', 'D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T'].index(categoria)
    variables_dummy[index] = 1
    return variables_dummy
def obtener_variables_si_no(categoria):
    index = ['A', 'B'].index(categoria)
    value=[1,0]
    #variables_si_no[index] = 1
    return value[index]

@app.route('/')
def home():
    return render_template('formulario.html')

@app.route('/predecir', methods=['POST'])
def predecir():
    # Obtener los valores ingresados en el formulario
    valores_input = [float(request.form['habitaciones']), float(request.form['superficie'])]
    # Obtener la categoría seleccionada y convertirla en variables dummy
    categoria_barrio = request.form['barrio']
    variables_dummy = obtener_variables_dummy(categoria_barrio)
    variable_piscina=obtener_variables_si_no(request.form['piscina'])
    variable_terraza=obtener_variables_si_no(request.form['terraza'])
    variable_reformado=obtener_variables_si_no(request.form['reformado'])
    variable_amueblado=obtener_variables_si_no(request.form['amueblado'])
    # Concatenar los valores de entrada con las variables dummy
    valores_input.extend(variables_dummy)
    valores_input.extend([variable_piscina])
    valores_input.extend([variable_terraza])
    valores_input.extend([variable_reformado])
    valores_input.extend([variable_amueblado])
    
    print("aa")
    print(valores_input)
    # Realizar la predicción utilizando el modelo
    prediccion = model.predict([valores_input])
    print(prediccion)
    # Renderizar una plantilla HTML con la predicción
    return render_template('resultado.html', prediccion=prediccion[0])

if __name__ == '__main__':
    app.run(debug=False)