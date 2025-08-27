import pandas as pd

def q_filter_os(conn):
  q_os = """ 
      SELECT o.os_nombre
      FROM v_os o JOIN v_prestaciones p
      ON o.os_id = p.prestacion_os
      WHERE p.prestacion_estado_descrip = "ACTIVA" COLLATE utf8mb4_0900_ai_ci
    AND p.prestacion_id >= 1
  """

  return pd.read_sql(q_os, conn)