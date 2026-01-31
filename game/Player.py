
from pygame import Vector2
from game.holdables import Holdables
from math import exp

from game.physicsEntity import PhysicsEntity

from copy import copy


class Player(PhysicsEntity):

    def __init__(self, username: str,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Inventory
        self.inventory : List[Holdables] = []
        self.holding: int = 0 # Which inventory item is the player holding

        # Animation stuff

        self.avg_felt_g_y = 1 # G ressentis par le joueur: Permet de determiner le sprite à utiliser. 
        # Le g est determiné a partir du différentiel de vitesses: g = (\Delta v) / (\Delta t) * m / g

        self.smooth_tau = .2 # Temps caracteristique du smooth d'animation

        # Online
        self.username = username
        self.mac_address = None
    
    def update(self, dt: float, level) -> None:

        old_speed = copy(self.speed)
        self.update_position(dt, level)

        # Computes the player's g force 
        acc = (self.speed - old_speed) / dt
        felt_g_y = acc.y / level.g

        if self.grounded:
            felt_g_y += 1
        else:
            felt_g_y = max(0, felt_g_y)

        alpha = 1 - exp(-dt / self.smooth_tau)

        self.avg_felt_g_y += alpha * (felt_g_y - self.avg_felt_g_y)

        # Animation
        if self.avg_felt_g_y > .90:
            self.sprite.set_texture_coordinates((0,0))
        elif self.avg_felt_g_y > .4:
            self.sprite.set_texture_coordinates((3,0))
        elif self.avg_felt_g_y > .2:
            self.sprite.set_texture_coordinates((4,0))
        elif self.avg_felt_g_y > -.8:
            self.sprite.set_texture_coordinates((1,0))
        else:
            self.sprite.set_texture_coordinates((2,0))

        # Acceleration reset
        self.acc = Vector2(0, level.g) # After the update_position : If the gun is fired, resets the acc AFTER the position was updated
    

if __name__=="__main__":
    player = Player(None, Vector2(5,5), 10, 10, Vector2(0,0), 4)

