import streamlit as st
import plotly.express as px
from data.queries_seg_inf import q_seg_coordi, q_inf_cat

# GRÁFICO DE BARRAS - SEGUIMIENTOS POR COORDINADORA
def chart_seg_coordi(conn):

  df_seg_coordi = q_seg_coordi(conn)

  fig_seg_coordi = px.bar(
    df_seg_coordi,
    x='nombre_coordi',
    y='seguim_total',
    title='Seguimientos por coordinadora',
    text='seguim_total',
    custom_data=[
      'nombre_coordi',
      'interc_con_prof',
      'superv',
      'interc_con_flia',
      'seguim',
      'interc_con_esc',
      'seguim_total'
    ]
  )

  fig_seg_coordi.update_traces(
    hovertemplate=
    "<b>%{customdata[0]}</b><br><br>"
    "Intercambio con profesionales: %{customdata[1]}<br>"
    "Supervisión: %{customdata[2]}<br>"
    "Intercambio con familias: %{customdata[3]}<br>"
    "Seguimiento: %{customdata[4]}<br>"
    "Intercambio con escuela: %{customdata[5]}<br><br>"
    "<b>Total: %{customdata[6]}</b><extra></extra>",
    textposition='outside'
  )

  fig_seg_coordi.update_layout(
    title_x=0.4,
    height=450,
    showlegend=False,
    xaxis_title="Coordinadora",
    yaxis_title="Cant. de seguimientos"
  )

  st.plotly_chart(fig_seg_coordi, use_container_width=True)

# GRÁFICO DE BARRAS - INFORMES POR CATEGORIA
def chart_inf_cat(conn):
  df_inf_cat = q_inf_cat(conn)

  fig_inf_cat = px.bar(
    df_inf_cat,
    x='categ',
    y='cant',
    title='Informes',
    labels={'categ': 'Tipo', 'cant': 'Cantidad'},
    text='cant'
  )

  fig_inf_cat.update_layout(
    title_x=0.4,
    height=450,
    showlegend=False,
    xaxis_title="Tipos de informe",
    yaxis_title="Cantidad"
  )

  st.plotly_chart(fig_inf_cat, use_container_width=True)
