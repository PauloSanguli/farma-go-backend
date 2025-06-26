import jwt
from datetime import datetime, timedelta

SECRET_KEY = "meusegredo123"
ALGORITHM = "HS256"

payload = {
    "sub": "usuario123",
    "exp": datetime.utcnow() + timedelta(minutes=5)
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print(token)
