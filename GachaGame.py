import random
import json

class GachaGame:
    def __init__(self, file):
        self.players = {}
        self.characters = {
            "Common": [
                "Common Character 1",
                "Common Character 2",
                "Common Character 3",
            ],
            "Uncommon": [
                "Uncommon Character 1",
                "Uncommon Character 2",
                "Uncommon Character 3",
            ],
            "Rare": ["Rare Character 1", "Rare Character 2", "Rare Character 3"],
            "Epic": ["Epic Character 1", "Epic Character 2", "Epic Character 3"],
            "Legendary": [
                "Legendary Character 1",
                "Legendary Character 2",
                "Legendary Character 3",
            ],
        }
        self.file = file

    def add_player(
        self, player_id, player_info: dict = {"inventory": [], "currency": 100}
    ):
        if player_id not in self.players:
            self.players[player_id] = {
                "inventory": player_info["inventory"],
                "currency": player_info["currency"],
            }
            return "Player added!"
        else:
            return "Player already exists."

    def remove_player(self, player_id):
        if player_id in self.players:
            self.players[player_id]["inventory"] = []
            del self.players[player_id]
            return "Player removed"
        else:
            return "Player does not exist."

    def reset_player(self, player_id):
        if player_id in self.players:
            self.remove_player(player_id)
            self.add_player(player_id)
            return "Player reset"
        else:
            return "Player does not exist."

    def roll_gacha(self, player_id):
        if player_id in self.players:
            if self.players[player_id]["currency"] >= 1:
                self.players[player_id]["currency"] -= 1
                rarity = random.choices(
                    ["Common", "Uncommon", "Rare", "Epic", "Legendary"],
                    weights=[50, 30, 15, 4, 1],
                    k=1,
                )[0]
                character = random.choice(self.characters[rarity])
                self.players[player_id]["inventory"].append(character)
                return f"You rolled a {character}!"
            else:
                return "Not enough currency to roll."
        else:
            return "Player not found."

    def inventory(self, player_id):
        if player_id in self.players:
            return self.players[player_id]["inventory"]
        else:
            return "Player not found."

    def save(self):
        with open(self.file, "w") as dataFile:
            json.dump(self.players, dataFile)
            dataFile.close()

    def load(self):
        with open(self.file, "r") as dataFile:
            data = json.load(dataFile)
            for id in data:
                self.add_player(id, data[id])
            dataFile.close()