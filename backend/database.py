import pymysql
from config import Config

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=Config.DB_PORT,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    """Execute a database query"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            
            if commit:
                connection.commit()
                return cursor.lastrowid
            
            if fetch_one:
                return cursor.fetchone()
            
            if fetch_all:
                return cursor.fetchall()
            
            return None
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()