import pygame as pg

class Sprite(pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, spritesheet_size: tuple = (1,1), default_text_coordinates: tuple = (0,0), scale: float = 1) -> None:
        """
        self.sheet_size: La taille de la spritesheet en tiles (i.e le nombre de textures dedans)
        self.default_text_coordinates: Où se placer sur la spritesheet par default
        self.size: La taille d'une texture
        """
        super().__init__()

        self.spritesheet_size = spritesheet_size
        
        self.scale = scale # Scale factor
        self.sheet = image # The spritesheet

        self.size = [image.get_width(), image.get_height()]

        if (self.size[0] % self.spritesheet_size[0] != 0):
            raise ArithmeticError("spritesheet_size must divise the image size")
        if (self.size[1] % self.spritesheet_size[1] != 0):
            raise ArithmeticError("spritesheet_size must divise the image size")

        self.size[0] /= self.spritesheet_size[0]
        self.size[1] /= self.spritesheet_size[1]

        self.text_coordinates = default_text_coordinates

        self.sheet = pg.transform.scale(self.sheet, (
            self.size[0] * self.spritesheet_size[0],
            self.size[1] * self.spritesheet_size[1])
        )

        # Texture de la taille d'un sprite de la sheet
        self.cropped_texture = pg.Surface((self.size[0], self.size[1]), pg.SRCALPHA)
        self.texture = pg.Surface((self.size[0] * self.scale, self.size[1] * self.scale), pg.SRCALPHA)

        self.set_texture_coordinates(self.text_coordinates)

    def set_texture_coordinates(self, coordinates: tuple) -> None:
        
        self.text_coordinates = coordinates
        self.cropped_texture = pg.Surface((self.size[0], self.size[1]), pg.SRCALPHA)

        self.cropped_texture.fill((0,0,0,0))
        self.cropped_texture.blit(self.sheet, (-self.size[0] * self.text_coordinates[0], -self.size[1] * self.text_coordinates[1]))

        pg.transform.scale(self.cropped_texture, (self.size[0] * self.scale, self.size[1] * self.scale), self.texture)
        