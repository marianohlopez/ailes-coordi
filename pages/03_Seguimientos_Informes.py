import streamlit as st
from main import config, conn
from ui.charts_seg_inf import chart_seg_coordi, chart_inf_cat
from ui.cards_seg_inf import cant_seg_inf


config()

st.title("Seguimientos - Informes")

#--- Tarjetas - Seguimientos e informes
cant_seg_inf(conn)

#--- Grafico de barras - Seguimientos por coordinadora
chart_seg_coordi(conn)

#--- Grafico de barras - Informes por categoria
chart_inf_cat(conn)