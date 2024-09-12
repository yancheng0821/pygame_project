import pygame


class Tiles:
    def __init__(self, colour, number):
        self.colour = colour
        self.number = number
        self.image_path = ""
        self.tiles_back_image_path = "images/tiles_back.jpeg"
        self.image = None
        self.rect = None
        self.unique_id = None

    def __str__(self):
        from game_window import red, blue, green, orange, black
        if self.colour == red:
            return f"Red {self.number}"
        elif self.colour == blue:
            return f"Blue {self.number}"
        elif self.colour == green:
            return f"Green {self.number}"
        elif self.colour == orange:
            return f"Orange {self.number}"
        elif self.colour == black:
            return f"Black {self.number}"

    def __repr__(self):
        return self.__str__()

    def set_rect(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def create_tile_surface(self, tiles_font, tile_width, tile_height, show_tiles_back_picture, need_show_tiles_back):
        combined_surface = None
        if show_tiles_back_picture and need_show_tiles_back:
            # Load the tile back image
            tile_image = pygame.image.load(self.tiles_back_image_path)
            tile_image = pygame.transform.scale(tile_image, (tile_width, tile_height))
            combined_surface = pygame.Surface((tile_width, tile_height))
            combined_surface.blit(tile_image, (0, 0))
        else:
            # Load the tile image
            tile_image = pygame.image.load(self.image_path)
            tile_image.set_alpha(200)
            tile_image = pygame.transform.scale(tile_image, (tile_width, tile_height))

            # Render the tile's number
            tile_number_surface = tiles_font.render(str(self.number), True, self.colour)
            number_x = (tile_width - tile_number_surface.get_width()) // 2
            number_y = (tile_height - tile_number_surface.get_height()) // 2

            # Create a new surface combining the tile image and the number
            combined_surface = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
            combined_surface.blit(tile_image, (0, 0))
            combined_surface.blit(tile_number_surface, (number_x, number_y))

        return combined_surface


class Player:
    def __init__(self, player_name, is_computer):
        self.player_name = player_name
        self.player_rack = []
        self.round_score = 0
        self.round_order_tile = None
        self.is_your_turn = False
        self.need_give_first_group = True
        self.highlight_group = []
        self.is_computer = is_computer
        self.is_winner = False

    def __str__(self):
        return f"{self.player_name} tiles: {self.player_rack}"


class GameEngine:

    def __init__(self):
        from game_window import red, blue, green, orange, black
        self.players = [Player("Player", False),
                        Player("Computer 1", True),
                        Player("Computer 2", True),
                        Player("Computer 3", True)]
        self.numbers = 15
        self.colours = [red, blue, green, orange, black]
        self.min_len = 3
        self.init_tiles_number = 14
        self.all_tiles = self.get_all_tiles()
        self.tables = []
        self.rounds = []
        self.show_tiles_back_picture = True

    def get_all_tiles(self):
        from game_window import red, blue, green, orange, black
        tiles = []
        tile_number = 0
        unique_id = 1
        for colour in self.colours:
            for _ in range(2):
                for _ in range(1, self.numbers + 1):
                    tile_number += 1
                    tile = Tiles(colour, tile_number)
                    tile.unique_id = unique_id
                    if colour == black:
                        tile.image_path = "images/blackTiles.jpeg"
                    if colour == blue:
                        tile.image_path = "images/blueTiles.jpeg"
                    if colour == red:
                        tile.image_path = "images/redTiles.jpeg"
                    if colour == orange:
                        tile.image_path = "images/orangeTiles.jpeg"
                    if colour == green:
                        tile.image_path = "images/greenTiles.jpeg"
                    tiles.append(tile)
                    unique_id += 1
                    if tile_number == 15:
                        tile_number = 0

        return tiles

    # test code function
    def set_player_rock(self):
        from game_handler import get_random_tile

        for player in self.players:
            for _ in range(self.init_tiles_number):
                tile = get_random_tile(self)
                player.player_rack.append(tile)
