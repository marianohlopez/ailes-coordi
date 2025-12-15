import streamlit as st
import plotly.express as px
from data.queries_prest import q_alum_coordis

# Gráfico - Prestaciones y alumnos por coordinadora
def chart_alum_coordis(conn):
  df = q_alum_coordis(conn)

  # Pasar a formato largo para doble barra
  df_long = df.melt(
      id_vars='coordi_nombre_apellido',
      value_vars=['alumnos', 'prestaciones'],
      var_name='tipo',
      value_name='cantidad'
  )

  fig = px.bar(
      df_long,
      x='coordi_nombre_apellido',
      y='cantidad',
      color='tipo',
      barmode='group',
      text='cantidad',
      labels={
          "coordi_nombre_apellido": "Coordinador",
          "cantidad": "Cantidad",
          "tipo": "Tipo"
      }
  )

  fig.update_layout(
      title_text="",
      height=600,
      margin=dict(l=20, r=20, t=20, b=160), 
      xaxis_tickangle=45
  )

  st.plotly_chart(fig, use_container_width=True)