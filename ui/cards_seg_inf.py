import streamlit as st
from data.queries_seg_inf import q_inf_cat, q_seg_coordi

# Cant de Seguimientos e informes
def cant_seg_inf(conn):

  df_inf_total = q_inf_cat(conn)
  df_seg_total = q_seg_coordi(conn)

  inf_total = df_inf_total['cant'].sum()
  seg_total = df_seg_total['seguim_total'].sum()

  card_seg = f"""
    <div class="card-container">
        <div class="card">
            <div class="card-title">Seguimientos</div>
            <div class="card-value">{seg_total}</div>
        </div>
    </div>
    """

  card_inf = f"""
    <div class="card-container">
        <div class="card">
            <div class="card-title">Informes</div>
            <div class="card-value">{inf_total}</div>
        </div>
    </div>
    """
  
  col1, col2 = st.columns(2)

  with col1:
      st.markdown(card_seg, unsafe_allow_html=True)

  with col2:
      st.markdown(card_inf, unsafe_allow_html=True)