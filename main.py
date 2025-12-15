import streamlit as st
from data.connection import get_connection
from ui.cards import cant_alum_prest, cant_coordis
from ui.charts_prest import chart_alum_coordis

def config(): 
  st.set_page_config(
    page_title="Dashboard-Coordinacion",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
  )
  # Estilo CSS
  css = open("styles.css").read()

  st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

config()

conn = get_connection()

st.title("ALUMNOS-PRESTACIONES ACTIVAS")

#--- Tarjetas - cant. de alumnos, prestaciones y alum. con dos prest.
cant_alum_prest(conn)

#--- Tarjeta - cant. de coordinadoras
cant_coordis(conn)

# Grafico de barras
chart_alum_coordis(conn)





