from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import random

Base = declarative_base()

class GameType(Base):
    __tablename__ = 'game_type'
    Type = Column(String, nullable=False, primary_key=True)

class Platform(Base):
    __tablename__ = 'platforms'
    Type = Column(String, nullable=False, primary_key=True)

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    platform_id = Column(String, ForeignKey('platforms.Type'), nullable=False)
    Game_Type_ID = Column(String, ForeignKey('game_type.Type'), nullable=False)
    Name = Column(String, nullable=False)
    av_lobbies = Column(Integer, nullable=False)

engine = create_engine('postgresql://dmatusik3301:oskar3301@localhost:5432/GameMatch')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def display_options(options):
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

def get_choice(options):
    while True:
        try:
            choice = int(input("Wybierz numer: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Nieprawidłowy numer. Spróbuj ponownie.")
        except ValueError:
            print("Wprowadź numer.")

def add_game_to_database():
    # Pobierz dostępne opcje dla Game_Type_ID z bazy danych
    game_types = session.query(Game_Type.Type).all()
    display_options(game_types)
    selected_game_type = get_choice(game_types)

    # Pobierz dostępne opcje dla platform_id z bazy danych
    platforms = session.query(Platform.Type).all()
    display_options(platforms)
    selected_platform = get_choice(platforms)

    name = input("Podaj nazwę gry: ")
    av_lobbies = random.randint(0, 10)

    new_game = Game(platform_id=selected_platform, Game_Type_ID=selected_game_type, Name=name, av_lobbies=av_lobbies)
    session.add(new_game)
    session.commit()
    print("Gra została dodana do bazy danych.")

if __name__ == "__main__":
    add_game_to_database()
