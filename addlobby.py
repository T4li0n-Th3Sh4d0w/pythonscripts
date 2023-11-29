from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

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

class Lobby(Base):
    __tablename__ = 'lobbies'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    max_players = Column(Integer, nullable=False)
    Name = Column(String, nullable=False)

engine = create_engine('postgresql://dmatusik3301:oskar3301@localhost:5432/GameMatch')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def display_options(options):
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
      
def get_game_id():
  while True:
        try:
            games = session.query(Game).all()
            print("Dostępne gry:")
            for i, game in enumerate(games, start=1):
                print(f"{i}. {game.Name}")
                if i % 10 == 0:
                    input("Wciśnij Enter, aby kontynuować...")

            choice = int(input("Podaj numer gry (klucz obcy z tabeli games.id): "))
            game_id = games[choice - 1].id
            return game_id

        except (ValueError, IndexError):
            print("Nieprawidłowy numer gry. Spróbuj ponownie.")


def get_max_players():
    while True:
        try:
            max_players = int(input("Podaj maksymalną liczbę graczy (od 1 do 10): "))
            if 1 <= max_players <= 10:
                return max_players
            else:
                print("Maksymalna liczba graczy musi być od 1 do 10.")
        except ValueError:
            print("Wprowadź poprawną liczbę.")

def get_lobby_name():
    return input("Podaj nazwę lobby: ")

def add_lobby_to_database():
    game_id = get_game_id()
    max_players = get_max_players()
    name = get_lobby_name()

    new_lobby = Lobby(game_id=game_id, max_players=max_players, Name=name)
    session.add(new_lobby)
    session.commit()
    print("Lobby zostało dodane do bazy danych.")

if __name__ == "__main__":
    add_lobby_to_database()
