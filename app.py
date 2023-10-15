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
    #df3 = df2[df2['Parte Demandada'].str.contains('^(?=.*quintana roo)(?=.*vivienda)', case = False)]
    df3 = df2[df2[busq_cols].str.contains(cadd, case = False)]
    #print(busq_cols)
    #print(texto_split)
    #df3 = df2[df2["Parte Demandada"].isin(['*quintana roo'])]
    print(df3.head())
    #st.markdown("""---""")
    if df3.empty == False:
        st.dataframe(df3, height=700)
    else:
        st.warning('No existen resultados para esta busqueda.', icon='⚠')

def buscar_texto_or(textos):
    df3 = df2[df2['Parte Demandada'].str.contains(textos, case=False)]
    #st.markdown("""---""")
    if df3.empty == False:
        st.dataframe(df3, height=700)
    else:
        st.warning('No existen resultados para esta busqueda.', icon='⚠')


# ----  MAINPAGE ----
st.header("⚖ Buscador Boletin Jurisdiccional")
#st.markdown("""---""")   

# -------------- SIDEBAR ---------------------

#Upload a file, TFJA in format .csv 
st.sidebar.subheader(" **Carga del Boletín** 📑")
uploaded_file = st.sidebar.file_uploader("## **Elige un archivo...**", type=[".csv",".xls",".xlsx"], accept_multiple_files=False)

if uploaded_file is not None:
    # To read file as bytes:
    df2 = pd.read_csv(uploaded_file)
    #df2 = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)
else:
    df2 =pd.DataFrame()
    st.sidebar.error('### **No se ha cargado archivo para analizar.**', icon="ℹ️")

#st.sidebar.markdown("""---""")

busq_radio = st.sidebar.radio("## **Tipo de busqueda:**", ["Exacta", "Aproximada"])
textos = st.sidebar.text_area("## **Ingresa los terminos a buscar:** 🔎", height=200, placeholder="Ingrese los terminos a buscar separados por comas - Ejemplo: delegacion, infonavit, gerente, imss")
textos = textos.replace("\n", "-")
textos = textos.replace(",","-")
textos= textos.replace(", ","-")
textos = textos.replace("--","-")
texto_split = textos.split("-")

#st.sidebar.markdown("""---""")
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



