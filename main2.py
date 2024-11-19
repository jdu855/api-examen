from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import jwt
from pydantic import BaseModel 

# Crear la aplicación FastAPI
app = FastAPI()

# Esquema de seguridad OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class  UserLogin(BaseModel):
    username:str
    password: str

# Simulación de usuarios en memoria
users = {
    "miguel": {"username": "miguel", "password": "123456", "email": "lopez@gmail.com"}
}

# Función para generar el token JWT
def encode_token(payload: dict) -> str:
    token = jwt.encode(payload, key="secret", algorithm="HS256")
    return token

# Función para decodificar el token JWT
def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        # Decodificamos el token usando la clave "secret" y el algoritmo "HS256"
        data = jwt.decode(token, key="secret", algorithms=["HS256"])
        return data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

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


@app.post("/login_json")
def login(form_data:UserLogin):
    # Buscar el usuario en la base de datos simulada
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=404, detail="icorrect user or password")
    
    # Generar el token
    token = encode_token({"username": user["username"], "email": user["email"]})

    # Devolver el token generado
    return {"access_token": token, "token_type": "bearer"}

# Ruta de perfil de usuario (requiere autenticación)
@app.get('/users/profile')
def profile(my_user: Annotated[dict, Depends(decode_token)]):
    return my_user



@app.get('/users', dependencies=[Depends(decode_token)])
def user_list():
    return users