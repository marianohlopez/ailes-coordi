import streamlit as st
from main import config, conn
from ui.cards_detail_proc import cant_details
from ui.charts_detail_proc import chart_mod_prest, chart_altas_bajas, chart_prest_pa
from logic.filters import year_filter

config()

st.title("Detalle de procesos")

#--- Tarjetas - Prest. con y sin pa, total
cant_details(conn)

#--- Grafico de anillo, Prest con y sin PA
chart_prest_pa(conn)

#--- Gráfico de barras - Cant. de prest por modalidad
chart_mod_prest(conn)

#--- Filtro de Año

year = st.selectbox("Seleccione el año", ["2026", "2025", "2024"])

# Condición de año para la consulta
year_condition = year_filter(year)

# Gráfico de lineas - altas y bajas de prestaciones
chart_altas_bajas(conn, year_condition)






