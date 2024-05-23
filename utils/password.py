from passlib.context import CryptContext

# Создаем объект CryptContext для управления хэшированием паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Функция для хэширования пароля"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Функция для проверки пароля"""
    return pwd_context.verify(plain_password, hashed_password)
