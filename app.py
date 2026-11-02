# La app de mi proyecto
# Para verla, en la terminal: streamlit run app.py
# Son los mismos pasos que en app_pisos.py y app_titanic.py. Si te atascas, busca el mismo paso allí.



# Paso 1. La página
# 1.1 Importa streamlit y pandas.
# 1.2 Pon el nombre de la pestaña del navegador, la página a todo lo ancho y un título que diga de qué va tu proyecto.
# 1.3 Debajo, una o dos frases con st.write: qué pregunta responde la app y de dónde salen los datos.
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lead Scoring", layout="wide")
st.title("¿A quién llamamos primero?")

st.write("Esta app ayuda al equipo de ventas a ver qué contactos tienen más probabilidad de comprar un curso y qué canales traen clientes de verdad.")
st.write("Los datos son contactos de X Education, una empresa de cursos online, y salen de Kaggle (Leads Dataset).")


# Paso 2. Los datos
# 2.1 La función cargar_datos, con @st.cache_data encima, que lea "datos/datos_limpios.csv" y lo devuelva.
#     La limpieza ya está hecha en el cuaderno, así que la función solo lee y devuelve, como en la carta del bar.
# 2.2 Llama a la función y guarda la tabla en una variable con el nombre de tus datos.

@st.cache_data
def cargar_datos():
    leads = pd.read_csv("datos/datos_limpios.csv")
    # Pongo la ocupación en español, como el sexo y la clase en la app del Titanic
    leads["ocupacion"] = leads["ocupacion"].replace({
        "Unemployed": "Desempleado",
        "Working Professional": "Trabajando",
        "Student": "Estudiante",
        "Housewife": "Ama de casa",
        "Businessman": "Empresario",
        "Other": "Otra",
    })
    return leads

leads = cargar_datos()
st.write("Tenemos", len(leads), "contactos.")

# Paso 3. Los filtros
# 3.1 En la barra de la izquierda (with st.sidebar:), al menos dos filtros:
#     un desplegable o unos botones para una columna de texto, con "Todos" al principio,
#     y una barra para una columna de números.
with st.sidebar:
    st.header("Filtros")

    canales = ["Todos"] + list(leads["canal"].value_counts().index)
    canal = st.selectbox("Canal", canales)

    ocupaciones = ["Todas"] + list(leads["ocupacion"].value_counts().index)
    ocupacion = st.selectbox("Ocupación", ocupaciones)

    minutos = st.slider("Minutos en la web", 0, 40, (0, 40))


# Paso 4. Filtrar
# 4.1 Empieza con filtrados = tu tabla, y después aplica un filtro por cada widget, como en los pisos.
filtrados = leads

if canal != "Todos":
    filtrados = filtrados[filtrados["canal"] == canal]

if ocupacion != "Todas":
    filtrados = filtrados[filtrados["ocupacion"] == ocupacion]

filtrados = filtrados[(filtrados["minutos_web"] >= minutos[0]) & (filtrados["minutos_web"] <= minutos[1])]

st.write("Con estos filtros quedan", len(filtrados), "contactos.")


# Paso 5. Si no queda nada
# 5.1 Si filtrados está vacía, saca un aviso con st.warning y para el programa con st.stop().
if len(filtrados) == 0:
    st.warning("No hay ningún contacto con estos filtros. Prueba con otros.")
    st.stop()


# Paso 6. Las métricas
# 6.1 Tres métricas en columnas, con los números más importantes para tu pregunta.

st.write("Con estos filtros quedan", len(filtrados), "contactos.")
col1, col2, col3 = st.columns(3)

col1.metric("Contactos", len(filtrados))
col2.metric("Compran (%)", round(filtrados["convertido"].mean() * 100, 1))
col3.metric("Minutos en la web (mediana)", round(filtrados["minutos_web"].median(), 1))
# Paso 7. Las pestañas
# 7.1 Al menos dos pestañas: una con la tabla filtrada y otra con dos gráficos.
# 7.2 Si tus datos tienen latitud y longitud, otra pestaña con el mapa.

tab1, tab2, tab3 = st.tabs(["Contactos", "Gráficos", "¿Vale la pena llamar?"])

with tab1:
    st.dataframe(filtrados)

with tab2:
    st.subheader("Qué porcentaje compra en cada ocupación")
    st.bar_chart(filtrados.groupby("ocupacion")["convertido"].mean() * 100)

    st.subheader("Cuántos contactos llegan por cada canal")
    st.bar_chart(filtrados["canal"].value_counts())

# Paso 8. Una pregunta para el usuario
# 8.1 Una última pestaña con una pregunta, como "¿Cuánto cobrarías por tu piso?" o "¿Te habrías salvado?":
#     el usuario elige algo y la app le contesta con lo que dicen los datos.
with tab3:
    st.subheader("¿Vale la pena llamar a este contacto?")

    mi_canal = st.selectbox("¿Por qué canal ha llegado?", list(leads["canal"].value_counts().index))
    mis_minutos = st.slider("¿Cuántos minutos ha pasado en la web?", 0, 40, 5)

    # Me quedo con los contactos parecidos: del mismo canal y con 5 minutos más o menos
    parecidos = leads[(leads["canal"] == mi_canal) &
                      (leads["minutos_web"] >= mis_minutos - 5) &
                      (leads["minutos_web"] <= mis_minutos + 5)]

    # Si no hay ninguno, aviso. Si hay, digo cuántos son y qué porcentaje compró
    if len(parecidos) == 0:
        st.warning("No hay contactos parecidos para comparar.")
    else:
        porcentaje = round(parecidos["convertido"].mean() * 100)
        st.write("Hay", len(parecidos), "contactos parecidos y compró el", porcentaje, "%.")

        # Si compró el 50 % o más, mensaje en verde. Si no, en rojo
        if porcentaje >= 50:
            st.success("Prioridad alta: merece la pena llamarle pronto.")
        else:
            st.error("Prioridad baja: mejor llamar antes a otros contactos.")