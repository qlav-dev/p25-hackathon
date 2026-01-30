from redis import Redis
from uuid import getnode as get_mac # Permet de chopper l'addresse MAC (Pour identifier de manière unique les joueurs)
import json
from game.level import Level

"""
Architecture du stockage serveur:

{
    game_id: (Identificateur crée par l'utilisateur)
    {
        level_id: (Map id)
        mac_address + Username : {
            position: {x: FLOAT, y: FLOAT}
            speed: {x: FLOAT, y: FLOAT}
            held_object: UNIQUE IDENTIFIER
        } 
        ...
        projectiles : [
            {type: int,
            position: {x: FLOAT, y: FLOAT}
            speed: {x: FLOAT, y: FLOAT}
            }
            ...
        ]
    }
}
"""

class Server(Redis):
    def __init__(self, *args, **kwargs):
        """
        host: str, port: int, decode_responses: bool
        """
        super().__init__(*args, **kwargs)
        self.mac_address = get_mac()

    def add_player_data(self, game_state: dict, game_id: str, game: Level):
        game_state[game_id][f"{self.mac_address}-{game.player.user_name}"] = {
            "position": {
                "x": game.player.position.x,
                "y": game.player.position.y,
            },
            "speed": {
                "x": game.player.speed.x,
                "y": game.player.speed.y,
            }
        }

    def create_game(self, game_id: int, game: Level):
        game_id = str(game_id)

        # With us as only player
        initial_game_state = {
            game_id : {
                "level_id" : game.map.map_id,
            }
        }
        self.add_player_data(initial_game_state, game_id, game)
        self.set(game_id, json.dumps(initial_game_state))

    def sync_game(self, game_id: int, game: Level) -> ...:
        """
        Upload les coordonnées et status du joueur.
        Telecharge les données des autres joueurs.
        """

        val = json.loads(self.get(game_id))
        if val is None:
            raise AttributeError("Ce `game_id` n'est pas défini")

        self.add_player_data(val, str(game_id), game) # Add yourself

        print(val)
        #return int(val)

    def upload_player(self, key: str, value: int):
        self.set(key, int(value))
