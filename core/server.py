from fastapi import FastAPI
import sqlite3
import json
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from core.Raid import start_raid as run_raid_logic
from core.save import load_game, save_game

app = FastAPI()

P = Path(__file__).parent
data_F = P.parent/"data"
if not data_F.exists():
    data_F.mkdir(parents=True, exist_ok=True)
db_path = data_F / "database.db"
save_path = data_F / "save.json"
if not save_path.exists():
    initial_save = {
    "player": {
        "location": 1,
        "inventory": [],
        "money": 0,
        "owned_armor": []
    }
    }
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(initial_save, f, indent=4, ensure_ascii=False)

con = sqlite3.connect(db_path, check_same_thread=False)
c = con.cursor()
c.execute("PRAGMA foreign_keys = ON")

inventory, money, owned_armor, current_location = load_game(save_path)

debug_mode = True

app.mount("/ui", StaticFiles(directory=P.parent / "static"), name="static")

@app.get("/player")

def get_player_data():

    with open(save_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        print(data)

    return data

@app.post("/start_raid")

def start_raid(minutes: int):

    inventory, money, owned_armor, current_location = load_game(save_path)

    inventory = run_raid_logic(inventory, minutes, current_location, debug_mode, c, save_path, money, owned_armor, )
    save_game(save_path, inventory, money, owned_armor, current_location)


    return {"status": "success", "message": f"You was in raid for {minutes} minutes"}