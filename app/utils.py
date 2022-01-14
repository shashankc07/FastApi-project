from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashed_pass(password: str):
    return pwd_context.hash(password)


def verify(plain_pass, hash_pass):
    return pwd_context.verify(plain_pass, hash_pass)
