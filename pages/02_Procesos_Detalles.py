import streamlit as st
from main import config, conn
from ui.cards_detail_proc import cant_details
from ui.charts_detail_proc import chart_mod_prest, chart_altas_bajas

config()

st.title("Detalle de procesos 2025")

#--- Tarjetas - Prest. con y sin pa, total
cant_details(conn)

#--- Gráfico de barras - Cant. de prest por modalidad
chart_mod_prest(conn)

# Gráfico de lineas - altas y bajas de prestaciones
chart_altas_bajas(conn)






