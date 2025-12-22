import streamlit as st
import plotly.express as px
from data.queries_detail_proc import q_mod_prest, q_altas_bajas

# GRÁFICO DE BARRAS - MODALIDADES DE PA

def chart_mod_prest(conn):

  df_mod_prest = q_mod_prest(conn)

  fig_mod_prest = px.bar(
      df_mod_prest,
      x='calcpagopamod_nombre',
      y='cant',
      title='MODALIDADES DE PA',
      labels={'calcpagopamod_nombre': 'Modalidad', 'cant': 'Cantidad de prestaciones'},
      text='cant',
  )

   # Forzar texto horizontal
  fig_mod_prest.update_traces(
    textangle=0,
  )

  # Ajustar layout para que se use todo el ancho
  fig_mod_prest.update_layout(
      title_x=0.5,
      height=400,
      showlegend=False
  )

  # Mostrar en Streamlit
  st.plotly_chart(fig_mod_prest, use_container_width=False)

# Gráfico de lineas - altas y bajas de prestaciones

def chart_altas_bajas(conn):
    
    initial_balance = 0

    df = q_altas_bajas(conn)

    # acumulados
    df["bajas_acum"] = df["cant_bajas"].cumsum()
    df["altas_acum"] = initial_balance + (df["cant_altas"] - df["cant_bajas"]).cumsum()

    fig = px.line(
        df,
        x="periodo",
        y=["bajas_acum", "altas_acum"],
        title="Evolución de altas y bajas",
        labels={
            "value": "Cantidad acumulada",
            "periodo": "Periodo",
            "altas_acum": "Altas (acum)",
            "bajas_acum": "Bajas (acum)",
        },
        color_discrete_map={
            "altas_acum": "green",
            "bajas_acum": "red",
        },
        markers=True,
        custom_data=["cant_altas", "cant_bajas"]
    )

    # hovertemplate para mostrar custom_data
    fig.update_traces(
        hovertemplate=
        "Periodo: %{x}<br>" +
        "Cantidad acumulada: %{y}<br>" +
        "Altas del mes: %{customdata[0]}<br>" +
        "Bajas del mes: %{customdata[1]}"
    )

    # layout
    fig.update_layout(
        xaxis_title="Periodo",
        yaxis_title="Cantidad acumulada",
        legend_title="Serie",
        title_x=0.5,
        height=420
    )

    fig.update_xaxes(type="category")

    # mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)