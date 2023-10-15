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
    #df3 = df2[df2['Parte Demandada'].str.contains('^(?=.*quintana roo)(?=.*gerente)')]
    #df3 = df2[df2['Parte Demandada'].str.contains(cadd,case=False)]
    print(busq_cols)
    print(texto_split)
    df3 = df2[df2["Parte Demandada"].isin(['*quintana roo'])]
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
    df = pd.read_csv(uploaded_file)
    df2 = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)
else:
    df2 =pd.DataFrame()
    st.sidebar.error('### **No se ha cargado archivo para analizar.**', icon="ℹ️")

#st.sidebar.markdown("""---""")

busq_radio = st.sidebar.radio("## **Tipo de busqueda:**", ["Exacta", "Aproximada"])
textos = st.sidebar.text_area("## **Ingresa los terminos a buscar** 🔎", height=200, placeholder="Ingrese los terminos a buscar separados por comas - Ejemplo: delegacion, infonavit, gerente, imss")
textos= textos.replace(", ",",")
texto_split = textos.split(",")
print(texto_split)

#st.sidebar.markdown("""---""")
if not df2.empty:
    busq_cols = st.sidebar.multiselect("## Buscar en los siguientes columnas", list(df2.columns.values.tolist()))


#texto_join_and = (r'^(?=.*Good)(?=.*East)')
#print(texto_join)


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






# words = '|'.join(['comisión de inconformidades','dirección', 'recaudación fiscal',
#          'delegación', 'gerente', 'director general',
#          'titular','delegado','delegada', 'gerencia', 'gerencia de recaudación fiscal','gerente de recaudación fiscal'])
# words2 = '|'.join(['quintana roo', 'qroo','q.roo'])
# words3 = '|'.join(['instituto del fondo nacional de la vivienda para los trabajadores','infonavit','vivienda'])

# df = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)
# df1 = df.loc[(df['No. Expediente'].isin(dfMD['Expediente'].unique()))]
# df2 = df[df['Parte Demandada'].str.contains(words)]
# df3 = df2[df2['Parte Demandada'].str.contains(words2)]
# df4 = df3[df3['Parte Demandada'].str.contains(words3)]
# dfTotal = df4.merge(df1, how = 'outer')
# dfTotal = dfTotal.apply(lambda x: x.str.upper() if x.dtype == "object" else x)



# id_notif = df_notificadores['usuario_Blue_Naa'].drop_duplicates()
# notif = st.sidebar.selectbox('Seleccionar notificador 👥', df_notificadores['nombre_Candidato'])
# notifsel = df_notificadores[df_notificadores['nombre_Candidato'] == notif]
# notitext = notifsel['usuario_Blue_Naa'].to_string(index=False)
# #print(df_bluemessaging['fecha_accion_fiscal'].dtype)
# fechas = pd.to_datetime(df_bluemessaging['fecha_accion_fiscal'].unique())
# fec_ini = fechas.min(skipna = True)
# fec_fin = fechas.max(skipna = True)


#fec_ini = date(2023,1,1)
#fec_fin = date.today()

# date1 = st.sidebar.date_input('Fecha inicial 📅', fec_ini)
# date2 = st.sidebar.date_input('Fecha final 📅', fec_fin)

#print(df_bluemessaging.head())
#print(notitext)
# print("Date1: ", date1)
# print("Date2: ", date2)
# print("-----------------------")




# if notif:
    
#     #df_selection = df_bluemessaging[(df_bluemessaging['user'] == notitext) & (df_bluemessaging['fecha_accion_fiscal'] >= date1)  & (df_bluemessaging['fecha_accion_fiscal'] < date2) ]  
#     df_selection = df_bluemessaging[(df_bluemessaging['user'] == notitext)]  
#     df_selection_notif = df_notificadores[df_notificadores['usuario_Blue_Naa'] == notitext]
#     num_days = len(df_selection['fecha_accion_fiscal'].unique())
#     #print(df_bluemessaging['user'].dtype)
#     #print(df_selection.head())
#     #print(df_selection_notif.head())
    
#     if df_selection.empty:
#         st.sidebar.markdown("""---""")
#         st.sidebar.caption("### :blue[No existen datos para este Notificador]")
#     else:
#         st.sidebar.markdown("""---""")
#         st.sidebar.caption(f"### **ID Notificador:** :blue[{df_selection_notif['usuario_Blue_Naa'].iloc[-1]}]")
#         st.sidebar.caption(f"### **Nombre:** :blue[{df_selection_notif['nombre_Candidato'].iloc[-1]}]")
#         st.sidebar.caption(f"### **Despacho:** :blue[{df_selection_notif['despacho'].iloc[-1]}]")
#         st.sidebar.caption(f"### **Carta Acreditación NAA:** :blue[{df_selection_notif['folio_Acred_Naa'].iloc[-1]}]")
#         st.sidebar.caption(f"### **Carta Acreditación PAE:** :blue[{df_selection_notif['folio_Acred_Pae'].iloc[-1]}]")
#         st.sidebar.caption(f"### **RFC:** :blue[{df_selection_notif['rfc'].iloc[-1]}]")
#         st.sidebar.caption(f"### **CURP:** :blue[{df_selection_notif['curp'].iloc[-1]}]")
#             # CALL FUNCTIONS TO LOAD INITIAL MAP, CHANGE CHECKBOX AND LOAD MARKS
#             #initial_query = "nrp == @nrp"
    
#         load_initial_map()
#         load_marks()
#             #load_images()
#             #change_checkbox()
#         #st_Data = st_folium(CircuitsMap, width=1000, height=600)
        
#         fig_notif_diaria = px.histogram(
#             df_selection,
#             x="nombre_estatus",
#             y="folio",
#             histfunc='count',
#             text_auto= True,
#             title="<b>Diligencias por estatus del notificador seleccionado</b>",
#             template="plotly_white",
#             labels={"nombre_estatus": "Estatus", "folio": "Numero de Folios"},
#             #color_discrete_sequence= ["#E31937"],
#         )
#         fig_notif_diaria.update_layout(
#             plot_bgcolor="rgba(0,0,0,0)",
#             #xaxis_tickprefix = '$', 
#             yaxis_tickformat = ',.0f',
#             showlegend = True,
#             bargap = 0.1)
        
#         left_column, right_column = st.columns([3,2])
#         #left_column.st_folium(CircuitsMap) width=1000, height=600
#         with left_column:
#             st_Data = st_folium(CircuitsMap, width=1000, height=600)

#         right_column.plotly_chart(fig_notif_diaria, use_container_width=True)

#         st.markdown("""---""")
#         #df_style = df_selection.style.apply()
#         #st.dataframe(df_selection.style.apply(color_coding(d_index), axis=1))
#         #st.dataframe(df_selection.style.map_index(color_coding))
#         #st.dataframe(df_selection.style.apply(color_coding, axis=1))
#         st.dataframe(df_selection)
# else:
#     st.sidebar.markdown("""---""")
#     st.sidebar.caption("### :blue[Seleccione un Notificador]")    




