import pandas as pd

def q_filter_os(conn):
  q_os = """ 
    SELECT o.os_nombre
    FROM v_os o JOIN v_prestaciones p
    ON o.os_id = p.prestacion_os
    WHERE p.prestacion_estado = 1
      AND p.prestacion_id >= 1
  """

  return pd.read_sql(q_os, conn)

def q_loc_map(os_condition, conn):
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
  return pd.read_sql(query, conn)