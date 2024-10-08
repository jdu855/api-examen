from fastapi import FastAPI, HTTPException
import mysql.connector
from core.connection import connection
from models.user import User
app = FastAPI()
@app.get('/')
def root():
    return {"message": "hello world"}

@app.get("/users")
async def get_users():
    cursor = connection.cursor(dictionary=true)
    query = "SELECT * FROM users"

    try: 
        cursor.execute(query)
        users = cursor.fetchall()
        return users
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al conectar con mysql : {err}")
    finally:
        cursor.close()

@app.post('/user')
async def create_user(user: User):
    cursor = connection.cursor()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    values = (user.username, user.password)

    try:
        cursor.execute(query, values)
        connection.commit()
        return {"message": "Usuario creado correctamente"}
    except (mysql.connector.Error, ValueError) as err:
        raise HTTPException(status_code=500, detail=f"Error al guardar el usuario: {err}")
    finally:
        cursor.close()
      
