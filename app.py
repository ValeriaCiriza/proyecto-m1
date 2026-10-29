# La app de mi proyecto
# Para verla, en la terminal: streamlit run app.py
# Son los mismos pasos que en app_pisos.py y app_titanic.py. Si te atascas, busca el mismo paso allí.



# Paso 1. La página
# 1.1 Importa streamlit y pandas.
# 1.2 Pon el nombre de la pestaña del navegador, la página a todo lo ancho y un título que diga de qué va tu proyecto.
# 1.3 Debajo, una o dos frases con st.write: qué pregunta responde la app y de dónde salen los datos.



# Paso 2. Los datos
# 2.1 La función cargar_datos, con @st.cache_data encima, que lea "datos/datos_limpios.csv" y lo devuelva.
#     La limpieza ya está hecha en el cuaderno, así que la función solo lee y devuelve, como en la carta del bar.
# 2.2 Llama a la función y guarda la tabla en una variable con el nombre de tus datos.



# Paso 3. Los filtros
# 3.1 En la barra de la izquierda (with st.sidebar:), al menos dos filtros:
#     un desplegable o unos botones para una columna de texto, con "Todos" al principio,
#     y una barra para una columna de números.



# Paso 4. Filtrar
# 4.1 Empieza con filtrados = tu tabla, y después aplica un filtro por cada widget, como en los pisos.



# Paso 5. Si no queda nada
# 5.1 Si filtrados está vacía, saca un aviso con st.warning y para el programa con st.stop().



# Paso 6. Las métricas
# 6.1 Tres métricas en columnas, con los números más importantes para tu pregunta.



# Paso 7. Las pestañas
# 7.1 Al menos dos pestañas: una con la tabla filtrada y otra con dos gráficos.
# 7.2 Si tus datos tienen latitud y longitud, otra pestaña con el mapa.



# Paso 8. Una pregunta para el usuario
# 8.1 Una última pestaña con una pregunta, como "¿Cuánto cobrarías por tu piso?" o "¿Te habrías salvado?":
#     el usuario elige algo y la app le contesta con lo que dicen los datos.
