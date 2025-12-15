import streamlit as st
from logic.filters import filtro_os
from ui.charts_map import chart_map
from main import config, conn

config()

st.title("Mapa de prestaciones - Año 2025")

# Obtener OS para el filtro y mostrar selector de OS
os_condition = filtro_os(conn)

st.subheader("📍 Mapa de ubicaciones")

# Mapa de prestaciones
chart_map(os_condition, conn)

