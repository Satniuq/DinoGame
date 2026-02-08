#data/highscore_repository.py

from data.storage import load_json, save_json

FILENAME = "highscores.json"
MAX_ENTRIES = 10

def load_highscores():
    return load_json(FILENAME, [])

def add_score(player, score):
    scores = load_highscores()

    scores.append({
        "player": player,
        "score": int(score)
    })

    # ordena do maior para o menor
    scores.sort(key=lambda x: x["score"], reverse=True)

    # mantém só top 10
    scores = scores[:MAX_ENTRIES]

    save_json(FILENAME, scores)

def get_top_scores():
    return load_highscores()
