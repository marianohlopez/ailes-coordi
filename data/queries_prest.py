import pandas as pd

# Tarjetas - cant de alumnos y cant de prestaciones
def q_prest_alum(conn):
  q_prest_alum = f"""
    SELECT 
      COUNT(DISTINCT a.alumno_id) AS cant_alumnos,
      COUNT(DISTINCT p.prestacion_id) AS cant_prestaciones
    FROM 
      v_os o
    JOIN 
      v_prestaciones p ON p.prestacion_os = o.os_id
    JOIN 
      v_alumnos a ON p.alumno_id = a.alumno_id
    WHERE 
      p.prestacion_estado_descrip = "ACTIVA" COLLATE utf8mb4_0900_ai_ci
      AND prestacion_anio = 2025
      AND prestipo_nombre_corto != 'TERAPIAS'
      AND p.prestacion_id NOT IN (521,1950)
      AND p.alumno_apellido != "Machado (Prueba)"
  """
  df_prest_alum = pd.read_sql(q_prest_alum, conn)

  # Extraer los valores
  cant_alumnos = df_prest_alum['cant_alumnos'][0]
  cant_prestaciones = df_prest_alum['cant_prestaciones'][0]

  return cant_alumnos, cant_prestaciones

#--- Tarjeta - cant. de alumnos con dos prestaciones

def q_two_prest(conn):
  query = """ 
    SELECT 
      COUNT(*) AS alumnos_con_dos_prestaciones
    FROM (
      SELECT 
        prestacion_alumno,
        COUNT(*) AS cant_prestaciones
      FROM 
        v_prestaciones
      WHERE 
        prestacion_estado_descrip = 'ACTIVA' COLLATE utf8mb4_0900_ai_ci
        AND prestacion_anio = 2025
        AND prestipo_nombre_corto != 'TERAPIAS'
        AND prestacion_id NOT IN (521,1950)
        AND alumno_apellido != 'Machado (Prueba)'
      GROUP BY 
        prestacion_alumno
      HAVING 
        COUNT(*) = 2
    ) AS t;
 """
  df = pd.read_sql(query, conn)

  return df['alumnos_con_dos_prestaciones'][0]

# Tarjeta - cant. de coordinadoras
def q_cant_coordis(conn):
  query = """ 
    SELECT 
      COUNT(DISTINCT p.prestacion_coordi) AS cant_coordi
    FROM 
      v_prestaciones p
    JOIN v_coordinadores c 
      ON p.prestacion_coordi = c.coordi_id
    WHERE 
      p.prestacion_estado = 1
      AND p.prestacion_coordi IS NOT NULL
      AND p.prestacion_coordi NOT IN (2, 14)
 """
  df = pd.read_sql(query, conn)

  return df['cant_coordi'][0]

# Gráfico - Cant. de alumnos y prestaciones por Coordinadora

def q_alum_coordis(conn):
  query = """
    SELECT 
      CONCAT(coordi_apellido, ', ', coordi_nombre) as coordi_nombre_apellido,
      COUNT(DISTINCT alumno_id) AS alumnos,
      COUNT(DISTINCT prestacion_id) AS prestaciones
    FROM v_prestaciones
    WHERE
      prestacion_estado IN (0, 1)
      AND prestipo_nombre_corto != 'TERAPIAS'
      AND coordi_apellido IS NOT NULL
      AND prestacion_coordi NOT IN (2, 14)
    GROUP BY coordi_nombre, coordi_apellido
  """
  return pd.read_sql(query, conn)


