import streamlit as st
import pandas as pd
import pydeck as pdk
from assets.coords import coords
from data.queries_map import q_loc_map

def chart_map(filter_os, conn):

  df = q_loc_map(filter_os, conn)

  # Agrupar por localidad
  df_grouped = df.groupby("localidad_nombre").agg(
      prestaciones=("prestacion_id", "count"),
      alumnos=("prestacion_alumno", pd.Series.nunique)
  ).reset_index()

  # Unir datos con coordenadas
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

  # Crear mapa con Pydeck
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

  st.pydeck_chart(pdk.Deck(
      layers=[layer],
      initial_view_state=view_state,
      map_style="light",  # fondo blanco
      tooltip={"text": "{localidad}\nPrestaciones: {prestaciones}\nAlumnos: {alumnos}"}
  ))