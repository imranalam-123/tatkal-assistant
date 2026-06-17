from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.models.user import User
from backend.schemas.user import UserCreate

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_user(
    db: Session,
    user: UserCreate
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise Exception(
            "Email already registered"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(
            user.password
        )
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    print("=" * 50)
    print("EMAIL RECEIVED:", email)
    print("PASSWORD RECEIVED:", password)

    user = db.query(User).filter(
        User.email == email
    ).first()

    print("USER FOUND:", user)

    if not user:
        print("USER NOT FOUND")
        return None

    print("DB EMAIL:", user.email)
    print("HASHED PASSWORD:", user.password)

    try:
        match = verify_password(
            password,
            user.password
        )

        print("PASSWORD MATCH:", match)

        if not match:
            print("PASSWORD INCORRECT")
            return None

    except Exception as e:
        print(
            "PASSWORD VERIFY ERROR:",
            str(e)
        )
        return None

    print("LOGIN SUCCESS")
    return user