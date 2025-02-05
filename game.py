import random
import json

class GachaGame:
    def __init__(self, file):
        self.players = {}
        self.characters = {
            "Common": ["Common Character 1", "Common Character 2", "Common Character 3"],
            "Uncommon": ["Uncommon Character 1", "Uncommon Character 2", "Uncommon Character 3"],
            "Rare": ["Rare Character 1", "Rare Character 2", "Rare Character 3"],
            "Epic": ["Taguchi Chinatsu", "Oh Haru", "Matsushima Shika"],
            "Legendary": ["Takashima Akiko", "Anno Shinju", "Kataoka Miyako"]
        }
        self.shop_items = {
            "Garage": {"cost": 0, "requirements": []},
            "Small Building": {"cost": 50000, "requirements": []},
            "Two story Building": {"cost": 100000, "requirements": []},
            "Large Building": {"cost": 200000, "requirements": []},
            "Repair Shop": {"cost": 50000, "requirements": ["Garage"]},
            "Massage Parlour": {"cost": 100000, "requirements": ["Small Building"]},
            "Restauraunt": {"cost": 150000, "requirements": ["Small Building"]},
            "Casino": {"cost": 500000, "requirements": ["Large Building"]},
            "Boxing Gym": {"cost": 75000, "requirements": ["Two story Building"]}
        }
        self.work_activities = [
            "You poor boi, you worked minimum wage.",
            "You helped a granny cross the road",
            "You bullied a child for lunch money",
            "You stole fifteen bucks from a cripple",
            "You mowed the lawn for gramps",
            "You robbed a bank (A piggy bank)",
            "You discored 15 bucks on the ground",
            "You got into a gang fight and won",
            "You defended a group of helpless society rejects"
        ]
        self.file = file

    def add_player(
        self, player_id, player_info: dict = {"inventory": [], "currency": 100, "command_counter": 0}
    ):
        if player_id not in self.players:
            self.players[player_id] = {
                "inventory": player_info["inventory"],
                "currency": player_info["currency"],
                "command_counter": player_info["command_counter"]
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
            self.increment_command_counter(player_id)
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
            self.increment_command_counter(player_id)
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
    
    def bank_account(self, player_id):
        if player_id in self.players:
            self.increment_command_counter(player_id)
            return self.players[player_id]["currency"]
        else:
            return "Player not found."

    def shop(self):
        return self.shop_items

    def buy_item(self, player_id, item):
        if player_id in self.players:
            if item in self.shop_items:
                cost = self.shop_items[item]["cost"]
                requirements = self.shop_items[item]["requirements"]
                if all(req in self.players[player_id]["inventory"] for req in requirements):
                    if self.players[player_id]["currency"] >= cost:
                        self.players[player_id]["currency"] -= cost
                        self.players[player_id]["inventory"].append(item)
                        self.increment_command_counter(player_id)
                        return f"You bought a {item} for {cost} currency!"
                    else:
                        return "Not enough currency to buy the item."
                else:
                    return f"You need the following items to buy {item}: {', '.join(requirements)}"
            else:
                return "Item not found in shop."
        else:
            return "Player not found."

    def increment_command_counter(self, player_id):
        if self.players[player_id]["command_counter"] >= 10:
            self.players[player_id]["command_counter"] = 0
            self.distribute_currency(player_id)

    def distribute_currency(self, player_id):
        if player_id in self.players:
            for item in self.players[player_id]["inventory"]:
                if item == "Garage":
                    self.players[player_id]["currency"] -= 0
                elif item == "Small Building":
                    self.players[player_id]["currency"] -= 1000
                elif item == "Two story Building":
                    self.players[player_id]["currency"] -= 10000
                elif item == "Large Building":
                    self.players[player_id]["currency"] -= 20000
                elif item == "Repair Shop":
                    self.players[player_id]["currency"] += 500
                elif item == "Massage Parlour":
                    self.players[player_id]["currency"] += 20000
                elif item == "Restauraunt":
                    self.players[player_id]["currency"] += 30000
                elif item == "Casino":
                    self.players[player_id]["currency"] += 50000
                elif item == "Boxing Gym":
                    self.players[player_id]["currency"] += 3000
    
    def work(self, player_id):
        if player_id in self.players:
            earned_currency = random.randint(15, 100)
            self.players[player_id]["currency"] += earned_currency
            self.increment_command_counter(player_id)
            activity = random.choice(self.work_activities)
            return f"{activity} and earned {earned_currency} MUNNY"
        else:
            return "Player not found."