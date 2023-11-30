from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Lobby(Base):
    __tablename__ = 'lobbies'

    id = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)

class Followed(Base):
    __tablename__ = 'followed'

    id = Column(Integer, primary_key=True)
    lobby_id = Column(Integer, ForeignKey('lobbies.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

engine = create_engine('postgresql://dmatusik3301:oskar3301@localhost:5432/GameMatch')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def get_user_id():
    while True:
        users = session.query(User).all()
        print("Dostępni użytkownicy:")
        for i, user in enumerate(users, start=1):
            print(f"{i}. {user.login}")
            if i % 10 == 0:
                input("Wciśnij Enter, aby kontynuować...")

        choice = input("Podaj numer użytkownika (klucz obcy z tabeli users.id): ")

        # Sprawdź, czy wprowadzona wartość to liczba całkowita
        if choice.isdigit():
            choice = int(choice)
            # Sprawdź, czy wybór mieści się w dostępnych opcjach
            if 1 <= choice <= len(users):
                user_id = users[choice - 1].id
                return user_id
            else:
                print("Nieprawidłowy numer użytkownika. Spróbuj ponownie.")
        # Sprawdź, czy wprowadzono Enter (pusta wartość)
        elif not choice.strip():
            print("Wprowadzono Enter. Wybór zakończony.")
            return None
        else:
            print("Nieprawidłowa wartość. Spróbuj ponownie.")

def get_lobby_id():
    while True:
        try:
            lobbies = session.query(Lobby).all()
            print("Dostępne lobbie:")
            for i, lobby in enumerate(lobbies, start=1):
                print(f"{i}. {lobby.Name}")
                if i % 10 == 0:
                    input("Wciśnij Enter, aby kontynuować...")

            choice = input("Podaj numer lobby (klucz obcy z tabeli lobbies.id): ")

            # Sprawdź, czy wprowadzona wartość to liczba całkowita
            if choice.isdigit():
                choice = int(choice)
                # Sprawdź, czy wybór mieści się w dostępnych opcjach
                if 1 <= choice <= len(lobbies):
                    lobby_id = lobbies[choice - 1].id
                    return lobby_id
                else:
                    print("Nieprawidłowy numer lobby. Spróbuj ponownie.")
            # Sprawdź, czy wprowadzono Enter (pusta wartość)
            elif not choice.strip():
                print("Wprowadzono Enter. Wybór zakończony.")
                return None
            else:
                print("Nieprawidłowa wartość. Spróbuj ponownie.")
        except (ValueError, IndexError):
            print("Błąd podczas przetwarzania wyboru lobby. Spróbuj ponownie.")

def add_followed_event():
    user_id = get_user_id()
    if user_id is None:
        return

    lobby_id = get_lobby_id()
    if lobby_id is None:
        return

    new_followed_event = Followed(lobby_id=lobby_id, user_id=user_id)
    session.add(new_followed_event)
    session.commit()
    print("Wydarzenie śledzenia zostało dodane do tabeli followed.")

if __name__ == "__main__":
    add_followed_event()

