import pygame as pg
import numpy as np
import colorsys

class Sprite(pg.sprite.Sprite):

    def hue_shift(self, hue_offset: float):
        """ Fonction assez lente: A faire qu'une fois ! """
        self.hue_offset = hue_offset

        arr = pg.surfarray.array3d(self.sheet).astype(np.float32) / 255.0
        alpha = pg.surfarray.array_alpha(self.sheet)

        for x in range(arr.shape[0]):
            for y in range(arr.shape[1]):
                r, g, b = arr[x, y]
                h, s, v = colorsys.rgb_to_hsv(r, g, b)
                h = (h + self.hue_offset) % 1.0
                arr[x, y] = colorsys.hsv_to_rgb(h, s, v)

        arr = (arr * 255).astype(np.uint8)

        self.sheet = pg.surfarray.make_surface(arr)
        self.sheet = self.sheet.convert_alpha()
        pg.surfarray.pixels_alpha(self.sheet)[:] = alpha
        self.set_texture_coordinates(self.text_coordinates)



    def __init__(self, image: pg.Surface, spritesheet_size: tuple = (1,1), default_text_coordinates: tuple = (0,0), scale: float = 1, hue_offset: float = 0) -> None:
        """
        self.sheet_size: La taille de la spritesheet en tiles (i.e le nombre de textures dedans)
        self.default_text_coordinates: Où se placer sur la spritesheet par default
        self.size: La taille d'une texture
        """
        super().__init__()

        self.spritesheet_size = spritesheet_size
        
        self.scale = scale # Scale factor
        self.sheet = image # The spritesheet
        self.hue_offset = hue_offset

        self.size = [image.get_width(), image.get_height()]

        if (self.size[0] % self.spritesheet_size[0] != 0):
            raise ArithmeticError("spritesheet_size must divise the image size")
        if (self.size[1] % self.spritesheet_size[1] != 0):
            raise ArithmeticError("spritesheet_size must divise the image size")

        self.size[0] //= self.spritesheet_size[0]
        self.size[1] //= self.spritesheet_size[1]

        self.text_coordinates = default_text_coordinates

        # Texture de la taille d'un sprite de la sheet
        self.image = pg.Surface((self.size[0] * self.scale, self.size[1] * self.scale), pg.SRCALPHA)
        self.rect = self.image.get_rect()

        self.texture = pg.Surface((self.size[0], self.size[1]), pg.SRCALPHA)

        self.hue_shift(self.hue_offset)
        self.set_texture_coordinates(self.text_coordinates)

    def set_texture_coordinates(self, coordinates: tuple) -> None:

        self.text_coordinates = coordinates
        self.texture = pg.Surface((self.size[0], self.size[1]), pg.SRCALPHA)

        self.texture.fill((0,0,0,0))
        self.texture.blit(self.sheet, (-self.size[0] * self.text_coordinates[0], -self.size[1] * self.text_coordinates[1]))

        pg.transform.scale(self.texture, (self.size[0] * self.scale, self.size[1] * self.scale), self.image)
        