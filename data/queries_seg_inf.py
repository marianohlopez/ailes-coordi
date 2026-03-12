import pandas as pd

# Gráfico de barras - Seguimientos por coordinadora
def q_seg_coordi(conn):
  q_seg_coordi = f"""
    SELECT 
      CONCAT(c.coordi_apellido, ', ', c.coordi_nombre) AS nombre_coordi,
      COUNT(DISTINCT CASE WHEN s.segcat_nombre = 'Intercambio con profesionales' THEN s.segalum_id END) AS interc_con_prof,
      COUNT(DISTINCT CASE WHEN s.segcat_nombre = 'Supervisión' THEN s.segalum_id END) AS superv,
      COUNT(DISTINCT CASE WHEN s.segcat_nombre = 'Intercambio con familias' THEN s.segalum_id END) AS interc_con_flia,
      COUNT(DISTINCT CASE WHEN s.segcat_nombre = 'Seguimiento' THEN s.segalum_id END) AS seguim,
      COUNT(DISTINCT CASE WHEN s.segcat_nombre = 'Intercambio con escuela' THEN s.segalum_id END) AS interc_con_esc,
      COUNT(DISTINCT s.segalum_id) AS seguim_total
    FROM
      v_prestaciones p
    JOIN v_seguimientos s
      ON p.prestacion_id = s.segalum_prestacion
    JOIN v_coordinadores c
      ON s.usuario_carga_id = c.user_id
    WHERE
      p.prestacion_estado IN (0, 1)
      AND p.prestipo_nombre_corto != 'TERAPIAS'
      AND s.segalum_rol_carga = 'COORDI'
      AND YEAR(s.segalum_fec_carga) = 2026 
      AND p.prestacion_anio = 2026
    GROUP BY 
      nombre_coordi
    ORDER BY
      seguim_total
  """
  return pd.read_sql(q_seg_coordi, conn)

# Grafico de barras - seguimientos por equipo técnico

def q_seg_tecnic(conn):
  q_seg_tecnic = f""" 
    SELECT 
      usuario_carga_nombre AS nombre_carga,
      COUNT(DISTINCT CASE WHEN s.segcat_nombre = 'Entrevista de admisión' THEN s.segalum_id END) AS entr_admision,
      COUNT(DISTINCT CASE WHEN s.segcat_nombre = 'Intercambio con profesionales' THEN s.segalum_id END) AS interc_con_prof,
      COUNT(DISTINCT CASE WHEN s.segcat_nombre = 'Supervisión' THEN s.segalum_id END) AS superv,
      COUNT(DISTINCT CASE WHEN s.segcat_nombre = 'Intercambio con familias' THEN s.segalum_id END) AS interc_con_flia,
      COUNT(DISTINCT CASE WHEN s.segcat_nombre = 'Seguimiento' THEN s.segalum_id END) AS seguim,
      COUNT(DISTINCT CASE WHEN s.segcat_nombre = 'Intercambio con escuela' THEN s.segalum_id END) AS interc_con_esc,
      COUNT(DISTINCT s.segalum_id) AS seguim_total
    FROM
      v_prestaciones p
    JOIN v_seguimientos s
      ON p.prestacion_id = s.segalum_prestacion
    JOIN v_users u
      ON s.usuario_carga_id = u.user_id
    WHERE
      p.prestacion_estado IN (0, 1)
      AND s.segalum_rol_carga = 'EQUIPO_TECNICO'
      AND YEAR(s.segalum_fec_carga) = 2026 
      AND p.prestacion_anio = 2026
    GROUP BY 
      nombre_carga
    ORDER BY
      seguim_total
  """
  return pd.read_sql(q_seg_tecnic, conn)

# Gráfico de barras - Informes por categoria
def q_inf_cat(conn):
  q_inf_cat = f"""
    SELECT 
      informecat_nombre AS categ,
	    COUNT(DISTINCT alumnoinforme_id) AS cant
    FROM v_prestaciones p
    LEFT JOIN v_informes i 
      ON p.alumno_id = i.alumno_id 
		  AND i.alumnoinforme_anio = '2026'
    WHERE
      p.prestipo_nombre_corto != 'TERAPIAS'
      AND p.prestacion_estado IN (0, 1)
      AND p.prestacion_anio = 2026
      AND p.prestacion_coordi IS NOT NULL
      AND i.informecat_nombre IS NOT NULL
    GROUP BY i.informecat_nombre
    ORDER BY
      cant
  """
  return pd.read_sql(q_inf_cat, conn)