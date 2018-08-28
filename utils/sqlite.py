import logging
import sqlite3


DDL = """
CREATE TABLE IF NOT EXISTS ewons (
  appid           text,      -- nombre de la aplicacion
  datetime        text,      -- fecha en la que se inserta o actualiza el session
  session         text,      -- token de sesion
  timeout         integer,   -- fecha en la que expira el token de session
  PRIMARY KEY(appid, datetime)
)
"""


def create_connection(db_location):
    try:
        conn = sqlite3.connect(db_location)
        return conn
    except sqlite3.Error as err:
        logging.error(err)
    return None


# timeout esta en minutos
def insert(conn, appid, session, timestamp, timeout=60):
    c = conn.cursor()
    statement = f"""
    INSERT INTO ewons 
    VALUES (
        '{appid}',
        '{timestamp}',
        '{session}',
        {timeout}
    )"""
    c.execute(statement)
    conn.commit()


def update(conn, appid, session, timestamp):
    c = conn.cursor()
    statement = f"""
     UPDATE ewons
     SET datetime = '{timestamp}',
         session = '{session}'
     WHERE app_id = '{appid}'
     """
    c.execute(statement)
    conn.commit()


def select_last_record(conn, appid):
    c = conn.cursor()
    statement = f"""
    SELECT session, timeout
    FROM ewons
    WHERE appid='{appid}'
    ORDER BY datetime desc
    LIMIT 1
    """
    return c.execute(statement).fetchone()
