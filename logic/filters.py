import streamlit as st
from data.queries_map import q_filter_os

# Filtro selector de OS

def filtro_os(conn):

  df_os = q_filter_os(conn)

  obras_sociales = ['Todas las os'] + list(df_os['os_nombre'].unique())

  # Selector en Streamlit
  selected_os = st.selectbox("Seleccione una obra social:", obras_sociales)

  # Condición de os en la consulta
  os_condition = ""
  if selected_os != "Todas las os":
      os_condition = f"AND o.os_nombre = '{selected_os}'"
      
  return os_condition

# Filtro de Año

def year_filter(year):

  # Condición de año en la consulta
  year_condition = ""
  if year != "":
      year_condition = f"AND prestacion_anio = {year}"

  return year_condition