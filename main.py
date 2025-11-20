from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import User
from shemas import UserCreate, UserResponse
from passlib.context import CryptContext

# --- Sécurité pour hash des mots de passe ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# --- Création automatique des tables dans SQLite ---
Base.metadata.create_all(bind=engine)

# --- Dépendance pour obtenir une session DB ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Page d'accueil ---
@app.get("/")
def home():
    return {"message": "API Action ou Vérité - Zarex fonctionne !"}


# --- Route : création d'un utilisateur ---
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # Vérifier si l'email existe déjà
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    # Hasher le mot de passe
    hashed_password = pwd_context.hash(user.password)

    # Créer le user en base
    new_user = User(
        email=user.email,
        name=user.name,
        pseudo=user.pseudo,
        age=user.age,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
