from sqlalchemy import create_engine, Column, String, Integer, Enum 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.exc import IntegrityError 
from passlib.hash import bcrypt

Base = declarative_base()
class User (Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  login = Column(String, unique = True, nullable = False) 
  password = Column (String, nullable=False)
  level = Column (String, nullable=False)

engine = create_engine('postgresql://dmatusik3301:oskar3301@localhost:5432/GameMatch')

Base.metadata.create_all(engine)
Session sessionmaker(bind = engine)
session= Session()

def get_user_input():
  login = input ("Podaj login użytkownika: ")
  password = input ("Podaj hasło: ")
  level = input ("Podaj poziom użytkownika (beginner/advanced/master): ") 
  return login, password, level

def hash_password (password):
  return bcrypt.hash (password)
  
def add_user_to_database (login, hashed_password, level):
  new_user = User (login=login, password=hashed_password, level=level) 
  session.add(new_user)
  try:
    session.commit()
    print ("Użytkownik został dodany do bazy danych")
  except IntegrityError as e:
    session.rollback()
    print (f"Błąd: {e}")
    print ("Nie udało się dodać użytkowika")
  
if __name__ == "__main__":
    user_login, user_password, user_level = get_user_input() 
    hashed_password=hash_password (user_password)
    add_user_to_database (user_login, hashed_password, user_level)
