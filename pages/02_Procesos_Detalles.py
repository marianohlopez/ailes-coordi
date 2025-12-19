import streamlit as st
from main import config, conn
from ui.cards_detail_proc import cant_details

config()

st.title("Detalle de procesos 2025")

cant_details(conn)





