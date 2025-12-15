import streamlit as st
from data.queries_prest import q_prest_alum, q_two_prest, q_cant_coordis

# Cant de alumnos, cant de prestaciones y alum. con dos prest.
def cant_alum_prest(conn):

  cant_alumnos, cant_prestaciones = q_prest_alum(conn)

  cant_two_prest = q_two_prest(conn)

  card_alum = f"""
    <div class="card-container">
        <div class="card">
            <div class="card-title">Cantidad de Alumnos</div>
            <div class="card-value">{cant_alumnos}</div>
        </div>
    </div>
    """

  card_prest = f"""
    <div class="card-container">
        <div class="card">
            <div class="card-title">Cantidad de Prestaciones</div>
            <div class="card-value">{cant_prestaciones}</div>
        </div>
    </div>
    """
  
  card_two_prest = f"""
  <div class="card-container">
      <div class="card">
          <div class="card-title">Alumnos con Dos Prestaciones</div>
          <div class="card-value">{cant_two_prest}</div>
      </div>
  </div>
  """
  col1, col2, col3 = st.columns(3)

  with col1:
      st.markdown(card_alum, unsafe_allow_html=True)

  with col2:
      st.markdown(card_prest, unsafe_allow_html=True)

  with col3:
    st.markdown(card_two_prest, unsafe_allow_html=True)

# Cant. de coordinadoras

def cant_coordis(conn):

  cant_coordis = q_cant_coordis(conn)

  card_coordis = f"""
    <div class="card-container">
        <div class="card">
            <div class="card-title">Cantidad de Coordinadoras</div>
            <div class="card-value">{cant_coordis}</div>
        </div>
    </div>
    """
  
  st.markdown(card_coordis, unsafe_allow_html=True)





