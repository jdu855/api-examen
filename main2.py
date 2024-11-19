from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import jwt

# Crear la aplicación FastAPI
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# Simulación de usuarios en memoria
users = {
    "miguel": {"username": "miguel", "password": "123456", "email": "lopez@gmail.com"}
}

# Función para generar el token JWT
def encode_token(payload: dict) -> str:
    token = jwt.encode(payload, key="secret", algorithm="HS256")
    return token

def  decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = jwt.decode(token, key:"secret", algorithm=["HS256"])
    return data



# Ruta de login
@app.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Buscar el usuario en la base de datos simulada
    user = users.get(form_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generar el token
    token = encode_token({"username": user["username"], "email": user["email"]})

    # Devolver el token generado
    return {"access_token": token, "token_type": "bearer"}

@app.get('/users/profile')
def profile(my_user:Annotated[dict, Depends(decode_token)]):
    return my_user