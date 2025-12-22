import pandas as pd

# Tarjetas - cant de prest. con pa y sin pa
def q_prest_pa(conn):
  q_prest_alum = f"""
    SELECT 
      COUNT(DISTINCT CASE WHEN prestacion_pa IS NOT NULL THEN prestacion_id END) AS prestaciones_con_pa,
      COUNT(DISTINCT CASE WHEN prestacion_pa IS NULL THEN prestacion_id END) AS prestaciones_sin_pa
    FROM v_prestaciones
    WHERE
      prestacion_estado IN (0, 1)
      AND prestipo_nombre_corto != 'TERAPIAS'
      AND coordi_apellido IS NOT NULL
  """
  df_prest_alum = pd.read_sql(q_prest_alum, conn)

  # Extraer los valores
  prest_con_pa = df_prest_alum['prestaciones_con_pa'][0]
  prest_sin_pa = df_prest_alum['prestaciones_sin_pa'][0]

  return prest_con_pa, prest_sin_pa

#--- Tarjeta - cant. de alumnos con dos prestaciones

def q_sin_pa_30(conn):
  query = """ 
    SELECT 
      COUNT(*) AS prestaciones_sin_pa_mas_30_dias
    FROM (
      SELECT 
        p.prestacion_id,
        DATEDIFF(
          CURDATE(),
          COALESCE(MAX(a.asignpa_pa_fec_baja), a.asignpa_fec1)
        ) AS dias_sin_pa
      FROM v_prestaciones p
      LEFT JOIN v_asignaciones_pa a 
        ON p.prestacion_id = a.asignpa_prest
      WHERE 
        p.prestipo_nombre_corto != 'TERAPIAS'
        AND p.prestacion_pa IS NULL
        AND p.prestacion_estado = 1
      GROUP BY 
        p.prestacion_id
      HAVING 
        dias_sin_pa > 30
    ) t;
 """
  df = pd.read_sql(query, conn)

  return df['prestaciones_sin_pa_mas_30_dias'][0]

# Gráfico de barras - Modalidades de PAs

def q_mod_prest(conn):
  query = """
    SELECT 
      calcpagopamod_nombre,
      COUNT(DISTINCT prestacion_id) AS cant
    FROM v_prestaciones
    WHERE
      prestacion_estado IN (0, 1)
      AND prestipo_nombre_corto != 'TERAPIAS'
      AND coordi_apellido IS NOT NULL
      AND prestacion_pa IS NOT NULL
      GROUP BY calcpagopamod_nombre;
  """
  return pd.read_sql(query, conn)

#--- Gráfico de barras con altas y bajas de prestaciones

def q_altas_bajas(conn):
   
  q_altas_bajas = """
    SELECT 
        periodo,
        SUM(cant_altas) AS cant_altas,
        SUM(cant_bajas) AS cant_bajas
    FROM (
        SELECT 
            DATE_FORMAT(prestacion_fec_pase_activo, '%%Y-%%m') AS periodo,
            COUNT(*) AS cant_altas,
            0 AS cant_bajas
        FROM v_prestaciones
        WHERE prestacion_fec_pase_activo IS NOT NULL
        AND prestacion_anio IN (2025, 2026)
        AND prestipo_nombre_corto != "TERAPIAS"
        GROUP BY DATE_FORMAT(prestacion_fec_pase_activo, '%%Y-%%m')
        
        UNION ALL
        
        SELECT 
            DATE_FORMAT(prestacion_fec_baja, '%%Y-%%m') AS periodo,
            0 AS cant_altas,
            COUNT(*) AS cant_bajas
        FROM v_prestaciones
        WHERE prestacion_fec_baja IS NOT NULL
        AND prestacion_fec_pase_activo IS NOT NULL
        AND prestacion_anio IN (2025, 2026)
        AND prestipo_nombre_corto != "TERAPIAS"
        GROUP BY DATE_FORMAT(prestacion_fec_baja, '%%Y-%%m')
    ) t
    GROUP BY periodo
    ORDER BY periodo;
  """
   
  df_altas_bajas = pd.read_sql(q_altas_bajas, conn)

  return df_altas_bajas