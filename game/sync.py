from redis import Redis
from uuid import getnode as get_mac # Permet de chopper l'addresse MAC (Pour identifier de manière unique les joueurs)
import json

class Server(Redis):
    def __init__(self, *args, **kwargs):
        """
        host: str, port: int, decode_responses: bool
        """
        super().__init__(*args, **kwargs)

    def sync_game(self, game_id: str, ) -> ...:
        """
        Upload les coordonnées et status du joueur.
        Telecharge les données des autres joueurs.
        """


        val = self.get(game_id)
        if val is None:
            raise AttributeError("Ce `game_id` n'est pas défini")
        return int(val)

    def upload_player(self, key: str, value: int):
        self.set(key, int(value))
    
if __name__ == "__main__":
    x = Server(host = "localhost", port = 6379, decode_responses = True)

    online_state = x.sync_game(1)
    print(online_state)
    