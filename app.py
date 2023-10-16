import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from streamlit_folium import st_folium
import folium
from folium import IFrame
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import urllib.request
import base64
import os
import streamlit.components.v1 as components
from datetime import date

d_index = 1

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Buscador Boletin TFJA", page_icon="⚖", layout="wide",)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


def buscar_text_and(cadd):
    df3 = df2[df2[busq_cols].str.contains(cadd, case = False)]
    if df3.empty == False:
        st.dataframe(df3, height=700)
        st.write("**Se encontraron %s registros que coinciden en el campo - %s -.**" % (str(df3[busq_cols].count()), busq_cols))
    else:
        st.warning('No existen resultados para esta busqueda.', icon='⚠')

def buscar_texto_or(textos):
    df3 = df2[df2['Parte Demandada'].str.contains(textos, case=False)]
    if df3.empty == False:
        st.dataframe(df3, height=700)
        st.write("**Se encontraron %s registros**" % str(df3[busq_cols].count()))
    else:
        st.warning('No existen resultados para esta busqueda.', icon='⚠')


# ----  MAINPAGE ----
st.header("⚖ Buscador Boletin Jurisdiccional")

# -------------- SIDEBAR ---------------------

#Upload a file, TFJA in format .csv 
st.sidebar.subheader(" **Carga del Boletín** 📑")
uploaded_file = st.sidebar.file_uploader("## **Elige un archivo...**", type=[".csv",".xls",".xlsx"], accept_multiple_files=False)

if uploaded_file is not None:
    # To read file as bytes:
    df2 = pd.read_csv(uploaded_file)
else:
    df2 =pd.DataFrame()
    st.sidebar.error('### **No se ha cargado archivo para analizar.**', icon="ℹ️")


busq_radio = st.sidebar.radio("## **Tipo de busqueda:**", ["Exacta", "Aproximada"])
textos = st.sidebar.text_area("## **Ingresa los terminos a buscar:** 🔎", height=200, placeholder="Ingrese los terminos a buscar separados por comas - Ejemplo: delegacion, infonavit, gerente, imss")

textos = textos.replace("\n", "-")
textos = textos.replace(",","-")
textos= textos.replace(", ","-")
textos = textos.replace("--","-")
texto_split = textos.split("-")


if not df2.empty:
    busq_cols = st.sidebar.selectbox("## **Buscar en los siguiente columna:**", list(df2.columns.values.tolist()))


# ------ CODE FOR BUTTON ------
if st.sidebar.button("Buscar 🔎",type="primary"):
    if busq_radio == "Exacta":
        cad =""
        for i in texto_split:
            cad = cad + '(?=.*' + i + ')'
        #cad = "r'^" + cad + "'"
        cad  = "^" + cad
        #print("Cadena concatenada", cad)
        buscar_text_and(cad)
    else:
        texto_join = "|".join(texto_split)
        buscar_texto_or(texto_join)
        #print("texto join", texto_join)

expander = st.sidebar.expander("Instrucciones de uso...")
expander.write(" 1. Descargar el Boletin Jurisdiccional en la pagina de la TFJA https://www.tfja.gob.mx/boletin/jurisdiccional/ en formato .CSV  \n 2. Cargar/Subir el archivo descargado en la parte superior para iniciar la busqueda. \n 3. Ingresar los conceptos/teminos a buscar separados por (,) y dar click en buscar. \n 4. Busqueda Exacta: Devuelve la busqueda de filas donde aparezcan el o los teminos completos. \n 5. Busqueda Aproximada: Devuelve todas las filas donde aparcezca cualquiera de los terminos buscados.")


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 95%;
background-color: white;
color: black;
text-align: right;

}
</style>
<div class="footer">
<p>Developed by 👨‍💻<a style='display: block; text-align: right;' href="https://www.linkedin.com/in/daniel-l%C3%B3pez-villegas-0aaa353b/" target="_blank">Daniel López Villegas</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)





