import streamlit as st
import pandas as pd
import pydeck as pdk
from data.connection import get_connection
from dotenv import load_dotenv
from assets.coords import coords
from logic.filters import filtro_os

load_dotenv()   

st.set_page_config(
    page_title="Dashboard Coordinación",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS para las tarjetas
css = open("styles.css").read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

#st.title("Mapa de prestaciones - Año 2025")

# -------------------------------
# 1. Conexión a MySQL
# -------------------------------
conn = get_connection()

# Obtener OS para el filtro y mostrar selector de OS
os_condition = filtro_os(conn)

query = f"""
  SELECT 
      p.prestacion_id, 
      p.prestacion_alumno, 
      l.localidad_nombre
  FROM v_prestaciones p
  LEFT JOIN v_escuelas e
      ON p.prestacion_escuela = e.escuela_id
  LEFT JOIN v_localidades l
      ON e.escuela_localidad = l.localidad_id
  JOIN v_os o 
		ON p.prestacion_os = o.os_id  
  WHERE 
      prestacion_estado = 1
      AND prestipo_nombre_corto != "TERAPIAS"
      AND l.localidad_nombre IS NOT NULL
      {os_condition}
"""

df = pd.read_sql(query, conn)

# -------------------------------
# 2. Agrupar por localidad
# -------------------------------
df_grouped = df.groupby("localidad_nombre").agg(
    prestaciones=("prestacion_id", "count"),
    alumnos=("prestacion_alumno", pd.Series.nunique)
).reset_index()

# -------------------------------
# 4. Unir datos con coordenadas
# -------------------------------
rows = []
for _, row in df_grouped.iterrows():
    loc = row["localidad_nombre"]
    if loc in coords:
        lat, lon = coords[loc]
        rows.append({
            "localidad": loc,
            "lat": lat,
            "lon": lon,
            "prestaciones": row["prestaciones"],
            "alumnos": row["alumnos"]
        })

df_map = pd.DataFrame(rows)

# -------------------------------
# 5. Crear mapa con Pydeck
# -------------------------------
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_map,
    get_position=["lon", "lat"],
    get_color="[200, 30, 0, 160]",
    get_radius="prestaciones * 100", 
    pickable=True
)

view_state = pdk.ViewState(
    latitude=-34.6, longitude=-58.45, zoom=9
)

st.subheader("📍 Mapa de ubicaciones")

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="light",  # fondo blanco
    tooltip={"text": "{localidad}\nPrestaciones: {prestaciones}\nAlumnos: {alumnos}"}
))
