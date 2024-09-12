from collections import deque

import pygame
import sys

import game_handler
import game_solution_solver
from game_engine import GameEngine
from game_window_settings import show_user_areas, game_main_menu, show_background, draw_button, display_message, \
    show_player_rack_tiles, show_drawn_tiles, show_table_tiles, show_remain_tiles_count, show_round_over_screen, \
    show_grid_area, show_game_info_log

# Initialize Pygame
pygame.init()
screen_width, screen_height = 1200, 800
table_tiles_area_rect = pygame.Rect(150, 150, 896, screen_height - 300)  # Table groups area
screen = pygame.display.set_mode((screen_width, screen_height))
info_box_rect = pygame.Rect(700, 0, 500, 70)  # x, y, width, height

button_blue = (54, 118, 177)
button_green = (151, 187, 128)
black = (0, 0, 0)
white = (255, 255, 255)
red = (199, 0, 0)
yellow = (255, 255, 0)
orange = (255, 100, 0)
blue = (0, 0, 220)
green = (0, 100, 0)
gray = (128, 128, 128)

# Set font for text
header_font = pygame.font.Font(None, 84)
font = pygame.font.Font(None, 74)
tiles_font = pygame.font.Font(None, 45)
font_smaller = pygame.font.Font(None, 32)
font_smallest = pygame.font.Font(None, 20)
font_game_info = pygame.font.Font(None, 22)

# Game state
game_state = 'main_menu'
game_screen_bg = ''
round_state = ''
game_engine = GameEngine()

game_info_deque = deque(maxlen=3)
player_order_list = []
tile_show_start = None
tile_width, tile_height = 32, 50
tile_gap = 3  # Gap between tiles

show_player_drawn_tiles = False
player_drawn_tiles = None
player_index = 0
player_positions = {}

msg1_show_start = None
msg2_show_start = None
show_duration = 2000
message_round_begin = "Round begin, choose a random tile to decide order"
message_first_player = "First player is "

# Game loop
running = True

while running:
    current_time = pygame.time.get_ticks()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if game_state == 'main_menu':
        game_screen_bg = pygame.image.load('images/main_screen_background.jpeg')
        game_screen_bg.set_alpha(10)
        show_background(game_screen_bg)
        game_state = game_main_menu(game_state, header_font, font, events)
        round_state = 'Round start'

    elif game_state == 'game_screen':
        # Display the game screen with background image
        game_screen_bg = pygame.image.load('images/game_screen_background.jpeg')
        show_background(game_screen_bg)

        player_positions = show_user_areas(game_engine, round_state == "play begin")

        if round_state == 'Round start':
            if draw_button('Start Round', 500, 380, 200, 50, font_smaller, events):
                msg1_show_start = current_time
                print(f"++++++++ Game Start ++++++++")
                game_info_deque.append('Game Start!')
                round_state = 'show message 1'

        if round_state == 'show message 1':
            if current_time - msg1_show_start <= show_duration:
                # display round begin message
                display_message(message_round_begin, font_smaller, white)

            else:
                player_order_list = game_handler.decide_first_player(game_engine)
                round_state = 'show order tile'
                tile_show_start = current_time

        # If player order has been decided, draw the player order tiles
        if round_state == 'show order tile':
            if current_time - tile_show_start <= show_duration:
                # display each player order tile
                show_player_rack_tiles(game_engine, player_positions, True)
            else:
                round_state = 'show message 2'
                msg2_show_start = current_time

        if round_state == 'show message 2':
            if current_time - msg2_show_start <= show_duration:
                for player in player_order_list:
                    if player.is_your_turn:
                        # display message who is the first player
                        display_message(f"{message_first_player}:{player.player_name}", font_smaller, white)
                        break
            else:
                round_state = 'send tiles'
                for player in player_order_list:
                    if player.is_your_turn:
                        game_info_deque.append(f"{player.player_name} is the first")

        # Starting send each player 14 tiles
        if round_state == 'send tiles':
            game_handler.send_begin_tiles_to_player(game_engine)
            round_state = "play begin"
            # refresh user area to highlight the first player
            show_user_areas(game_engine, True)
            pygame.display.update()
            game_info_deque.append('Round begin!')

        if round_state == "play begin":
            # show grid area
            show_grid_area(game_engine)
            # show remain tiles count in tiles pool
            show_remain_tiles_count(game_engine)
            # show table tiles
            show_table_tiles(game_engine, table_tiles_area_rect)
            # display each player's tiles
            show_player_rack_tiles(game_engine, player_positions, False)

            if draw_button("Show All Tiles", 150, 750, 130, 40, font_smallest, events):
                # show computer's tiles
                if game_engine.show_tiles_back_picture:
                    game_engine.show_tiles_back_picture = False
                else:
                    game_engine.show_tiles_back_picture = True

            which_player = game_engine.players[player_index]
            if not which_player.is_computer:
                player = which_player
                if player.is_your_turn:
                    if draw_button('Draw Tiles', 675, 750, 100, 40, font_smallest, events):
                        # draw two random tiles from pool, and show on the screen
                        player_drawn_tiles = game_handler.draw_random_two_tiles(game_engine)
                        show_player_drawn_tiles = True

                    if draw_button('Play for Me', 785, 750, 120, 40, font_smallest, events):
                        # make player to be computer
                        player.is_computer = True
                        player.is_your_turn = False
                        game_engine.players[player_index + 1].is_your_turn = True
                        player_index += 1

                    if show_player_drawn_tiles:
                        clicked_tile = show_drawn_tiles(game_engine, player_drawn_tiles, player_positions)
                        pygame.display.update()
                        if clicked_tile is not None:
                            # remove the drawn tile
                            game_handler.remove_from_pool(game_engine, clicked_tile)
                            game_handler.add_to_rack(player, clicked_tile)
                            # remove the display of the two random tiles
                            show_player_drawn_tiles = False
                            player.is_your_turn = False
                            game_engine.players[player_index + 1].is_your_turn = True
                            player_index += 1
                else:
                    player_index += 1
                    if player_index > 3:
                        player_index = 0

            else:
                # computer player
                computer = which_player
                if computer.is_your_turn:
                    # check can form a valid group
                    print(f"++++++++ is {computer.player_name} turn++++++++")
                    if computer.need_give_first_group:
                        first_valid_group = game_handler.find_first_valid_group(computer)
                        if first_valid_group:
                            game_info_deque.append(f"{computer.player_name} first valid groups: {first_valid_group}")
                            for group in first_valid_group:
                                for tile in group:
                                    game_handler.remove_from_rack(computer, tile)
                                game_handler.add_table(game_engine, group)
                            # first valid group is formed, pass to next player
                            computer.need_give_first_group = False
                        else:
                            # can't form a valid group, draw a random tile from pool and end turn
                            tile = game_handler.get_random_tile_and_remove_it_from_pool(game_engine)
                            print(f"no first valid group, {computer.player_name} draw a tile {tile}")
                            game_info_deque.append(f"{computer.player_name} no first valid group, draw a {tile}")
                            game_handler.add_to_rack(computer, tile)
                    else:
                        hand_tiles, solution_group, table_remain_groups = game_solution_solver.find_best_solution(
                            computer.player_rack, game_engine.tables)
                        # no solution_group and remain tiles is not 0
                        if not solution_group and len(game_engine.all_tiles) > 0:
                            # can't form a valid group, draw a random tile from pool and end turn
                            tile = game_handler.get_random_tile_and_remove_it_from_pool(game_engine)
                            print(f"no solution, {computer.player_name} draw a tile {tile}")
                            game_info_deque.append(f"{computer.player_name} no solution, draw a {tile}")
                            game_handler.add_to_rack(computer, tile)
                        elif not solution_group:
                            # can't form a valid group, end turn
                            print(f"no solution and no tile to draw, {computer.player_name} end turn")
                        else:
                            # can form a valid group, remove tiles from rack and end turn
                            print(f"best solution group is : {solution_group}")
                            print(f"use {computer.player_name} hand tiles : {hand_tiles}")
                            game_info_deque.append(f"{computer.player_name} use {hand_tiles} form {solution_group}")
                            for tile in hand_tiles:
                                game_handler.remove_from_rack(computer, tile)
                            game_handler.clear_tables(game_engine)
                            game_handler.add_remain_groups(game_engine, table_remain_groups)
                            game_handler.add_table(game_engine, solution_group)

                    # check winner
                    round_score_list = game_handler.check_winner(game_engine, computer)
                    # if round_score_list is not empty, means winner is produced
                    if round_score_list:
                        # game is over
                        print(f"++++++++ Round Over ++++++++")
                        game_info_deque.append('Round Over!')
                        game_state = 'round_over'
                        round_state = 'round_over'
                    else:
                        # pass to next player
                        computer.is_your_turn = False
                        # pass to the next player
                        player_index += 1
                        if player_index > 3:
                            player_index = 0
                        game_engine.players[player_index].is_your_turn = True
                else:
                    player_index += 1
                    if player_index > 3:
                        player_index = 0

                # player back control
                if game_engine.players[0].is_computer:
                    if draw_button("I'm back", 675, 750, 100, 40, font_smallest, events):
                        # make player to be computer
                        game_engine.players[0].is_computer = False

    elif round_state == 'round_over':
        show_background(game_screen_bg)
        show_user_areas(game_engine, False)
        show_remain_tiles_count(game_engine)
        show_player_rack_tiles(game_engine, player_positions, False)

        if draw_button("Show All Tiles", 150, 750, 130, 40, font_smallest, events):
            # show computer's tiles
            if game_engine.show_tiles_back_picture:
                game_engine.show_tiles_back_picture = False
            else:
                game_engine.show_tiles_back_picture = True

        show_round_over_screen(game_engine)

        if draw_button('Play Again', 500, 580, 200, 50, font_smaller, events):
            # init_game settings
            round_state = 'Round start'
            game_state = 'game_screen'
            game_engine = GameEngine()
            game_info_deque.clear()

            player_order_list = []
            tile_show_start = None

            show_player_drawn_tiles = False
            player_drawn_tiles = None
            player_index = 0

            player_positions = show_user_areas(game_engine, round_state == "play begin")

            msg1_show_start = None
            msg2_show_start = None

    show_game_info_log(game_info_deque)

    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
