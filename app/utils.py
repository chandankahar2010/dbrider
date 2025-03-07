from passlib.context import CryptContext
from jwt import encode

SECRET_KEY = "8812e70f4856b21acbdef0d34f44ff0465eb4fc989fe5b723e28b5e34648e528"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict):
    return encode(data, SECRET_KEY, algorithm=ALGORITHM)