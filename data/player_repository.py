# data/player_repository.py

from data.storage import load_json, save_json

FILENAME = "players.json"

def load_players():
    return load_json(FILENAME, [])

def add_player(name):
    players = load_players()
    if name not in players:
        players.append(name)
        save_json(FILENAME, players)

def remove_player(name):
    players = load_players()
    players = [p for p in players if p != name]
    save_json(FILENAME, players)
