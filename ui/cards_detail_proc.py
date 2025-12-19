import streamlit as st
from data.quieries_detail_proc import q_prest_pa, q_sin_pa_30

# Cant de alumnos, cant de prestaciones y alum. con dos prest.
def cant_details(conn):

  alum_con_pa, alum_sin_pa = q_prest_pa(conn)

  sin_pa_30 = q_sin_pa_30(conn)

  card_con_pa = f"""
    <div class="card-container">
        <div class="card">
            <div class="card-title">Prestaciones con PA</div>
            <div class="card-value">{alum_con_pa}</div>
        </div>
    </div>
    """

  card_sin_pa = f"""
    <div class="card-container">
        <div class="card">
            <div class="card-title">Prestaciones sin PA</div>
            <div class="card-value">{alum_sin_pa}</div>
        </div>
    </div>
    """
  
  card_sin_30 = f"""
  <div class="card-container">
      <div class="card">
          <div class="card-title">Sin PA + de 30 días</div>
          <div class="card-value">{sin_pa_30}</div>
      </div>
  </div>
  """

  card_total = f"""
  <div class="card-container">
      <div class="card">
          <div class="card-title">Total</div>
          <div class="card-value">{alum_con_pa + alum_sin_pa}</div>
      </div>
  </div>
  """
  col1, col2, col3 = st.columns(3)

  with col1:
      st.markdown(card_con_pa, unsafe_allow_html=True)

  with col2:
      st.markdown(card_sin_pa, unsafe_allow_html=True)

  with col3:
    st.markdown(card_sin_30, unsafe_allow_html=True)
  
  st.markdown(card_total, unsafe_allow_html=True)