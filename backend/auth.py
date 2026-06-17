from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("backend/.env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)

print("SECRET_KEY =", SECRET_KEY)
print("ALGORITHM =", ALGORITHM)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("TOKEN PAYLOAD =", payload)

        return payload

    except JWTError as e:
        print("JWT ERROR =", str(e))
        return None

    except Exception as e:
        print("GENERAL ERROR =", str(e))
        return None