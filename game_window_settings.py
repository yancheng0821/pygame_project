import pygame

# Set the title of the window
pygame.display.set_caption('Rummikub')


def game_main_menu(game_state, header_font, font, events):
    from game_window import screen, screen_width, white

    # Displaying the game's title
    title_text = header_font.render('Rummikub', True, white)
    screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, 50))

    # Draw start button and check for click
    if draw_button('Start Game', 450, 400, 300, 100, font, events):
        game_state = 'game_screen'
    return game_state


def draw_button(text, x, y, width, height, font, events):
    from game_window import screen, black, button_blue, button_green
    mouse = pygame.mouse.get_pos()
    button_clicked = False

    # Button appearance , draw_button function code from Google web search
    pygame.draw.rect(screen, button_blue if x + width > mouse[0] > x and y + height > mouse[1] > y else button_green,
                     (x, y, width, height))
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

    # Event handling for button click
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if x + width > mouse[0] > x and y + height > mouse[1] > y:
                button_clicked = True

    return button_clicked


def show_background(game_screen_bg):
    from game_window import screen
    screen.blit(game_screen_bg, (0, 0))


# draw user areas
avatar_width, avatar_height = 50, 50
user_images = [
    pygame.transform.scale(pygame.image.load('images/player.jpeg'), (avatar_width, avatar_height)),
    pygame.transform.scale(pygame.image.load('images/computer1.jpeg'), (avatar_width, avatar_height)),
    pygame.transform.scale(pygame.image.load('images/computer2.jpeg'), (avatar_width, avatar_height)),
    pygame.transform.scale(pygame.image.load('images/computer3.jpeg'), (avatar_width, avatar_height))
]


def show_user_areas(game_engine, hight_flag):
    from game_window import screen, screen_width, screen_height, yellow

    # Bottom middle
    player_avatar = (
        screen_width // 2 - user_images[0].get_width() // 2, screen_height - user_images[0].get_height())

    # Left middle
    computer1_avatar = (0, screen_height // 2 - user_images[1].get_height() // 2)

    # Top middle
    computer2_avatar = (screen_width // 2 - user_images[2].get_width() // 2, 0)

    # Right middle
    computer3_avatar = (
        screen_width - user_images[3].get_width(), screen_height // 2 - user_images[3].get_height() // 2)

    avatar_positions = [player_avatar, computer1_avatar, computer2_avatar, computer3_avatar]

    highlight_color = yellow
    highlight_border = 7  # highlight border

    player_positions = {}
    players = game_engine.players
    for i, player in enumerate(players):
        pos = avatar_positions[i]
        avatar_image = user_images[i]
        # Highlight the specified player's avatar
        if hight_flag and player.is_your_turn:
            # Draw a rectangle around the avatar for highlight
            pygame.draw.rect(screen, highlight_color, (
                pos[0] - highlight_border, pos[1] - highlight_border, avatar_width + 2 * highlight_border,
                avatar_height + 2 * highlight_border), highlight_border)

        # Draw the avatar
        screen.blit(avatar_image, pos)
        player_positions[player] = avatar_positions[i]

    return player_positions


def display_message(message, font_smaller, white):
    from game_window import screen, screen_width, screen_height
    message_surface = font_smaller.render(message, True, white)
    screen.blit(message_surface, (screen_width // 2 - message_surface.get_width() // 2,
                                  screen_height // 2 - message_surface.get_height() // 2))


start_time = pygame.time.get_ticks()
delay = 800


def show_player_rack_tiles(game_engine, player_positions, need_disappear):
    # Draw the round order tiles for each player
    current_time = None
    if need_disappear:
        current_time = pygame.time.get_ticks()

    player_index = 0
    for i, player in enumerate(game_engine.players):
        display_time = start_time + i * delay
        # Only display the tile if the current time is past the display time
        if current_time is not None and current_time >= display_time:
            do_display_user_tiles(player, player_positions, player_index, need_disappear,
                                  game_engine.show_tiles_back_picture)
        else:
            do_display_user_tiles(player, player_positions, player_index, need_disappear,
                                  game_engine.show_tiles_back_picture)

        player_index += 1


def do_display_user_tiles(player, player_positions, player_index, need_disappear, show_tiles_back_picture):
    from game_window import screen, tiles_font, tile_width, tile_height, tile_gap, yellow

    if need_disappear:
        if player_index == 0:
            tile_x = player_positions[player][0]
            tile_y = player_positions[player][1] - tile_height - 10
        elif player_index == 1:
            tile_x = player_positions[player][0] + tile_width + 30
            tile_y = player_positions[player][1]
        elif player_index == 2:
            tile_x = player_positions[player][0]
            tile_y = player_positions[player][1] + tile_height + 10
        else:
            tile_x = player_positions[player][0] - tile_width - 10
            tile_y = player_positions[player][1]
    else:
        if player_index == 0:
            tile_x = player_positions[player][0] - len(player.player_rack) / 2 * tile_width
            tile_y = player_positions[player][1] - tile_height - 10
        elif player_index == 1:
            tile_x = player_positions[player][0] + tile_width + 30
            tile_y = player_positions[player][1] - len(player.player_rack) / 2 * tile_height
        elif player_index == 2:
            tile_x = player_positions[player][0] - len(player.player_rack) / 2 * tile_width
            tile_y = player_positions[player][1] + tile_height + 10
        else:
            tile_x = player_positions[player][0] - tile_width - 10
            tile_y = player_positions[player][1] - len(player.player_rack) / 2 * tile_height

    tiles = []
    if need_disappear:
        tiles.append(player.round_order_tile)
    else:
        tiles.extend(player.player_rack)

    for tile in tiles:
        # if tile is highlighted, draw a border around it
        # highlight = player.is_your_turn and player.highlight_group and tile in player.highlight_group
        if player.is_your_turn and player.highlight_group and tile in player.highlight_group:
            pygame.draw.rect(screen, yellow, (tile_x - 3, tile_y - 3, tile_width + 3, tile_height + 3), 3)

        # computer's tiles show back picture
        need_show_tiles_back = False
        if not need_disappear and player.player_name != "Player":
            need_show_tiles_back = True

        tile_surface = tile.create_tile_surface(tiles_font, tile_width, tile_height, show_tiles_back_picture,
                                                need_show_tiles_back)
        tile.set_rect(tile_x, tile_y, tile_width, tile_height)
        screen.blit(tile_surface, (tile_x, tile_y))

        if not need_disappear:
            if player_index == 0:
                tile_x += tile_width + tile_gap
            elif player_index == 1:
                tile_y += tile_height + tile_gap
            elif player_index == 2:
                tile_x += tile_width + tile_gap
            else:
                tile_y += tile_height + tile_gap


def show_drawn_tiles(game_engine, tiles, player_positions):
    from game_window import tile_height, tile_width, screen, tiles_font, tile_gap

    if not tiles:
        return
    tile_x = player_positions[game_engine.players[0]][0]
    tile_y = player_positions[game_engine.players[0]][1] - tile_height * 3 - 10

    clicked_tile = None
    tile_rects = []

    for tile in tiles:
        tile_surface = tile.create_tile_surface(tiles_font, tile_width, tile_height, False, False)
        screen.blit(tile_surface, (tile_x, tile_y))

        tile_rect = pygame.Rect(tile_x, tile_y, tile_width, tile_height)
        tile_rects.append((tile_rect, tile))

        tile_x += tile_width + tile_gap

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for rect, tile in tile_rects:
                if rect.collidepoint(mouse_x, mouse_y):
                    # Tile was clicked
                    clicked_tile = tile

    return clicked_tile


def show_table_tiles(game_engine, play_area_rect):
    from game_window import screen, tile_width, tile_height, tiles_font

    group_gap = tile_width
    row_gap = 0
    tile_x = play_area_rect.x
    tile_y = play_area_rect.y
    tile_rects = []

    # Show groups in table tiles
    for group in game_engine.tables:
        for tile in group:
            # Check if adding another tile would exceed the right boundary of the play area
            if tile_x + tile_width > play_area_rect.right:
                # Move to the next line
                tile_y += tile_height + row_gap
                tile_x = play_area_rect.x

            tile_surface = tile.create_tile_surface(tiles_font, tile_width, tile_height, False, False)
            screen.blit(tile_surface, (tile_x, tile_y))

            tile_rect = pygame.Rect(tile_x, tile_y, tile_width, tile_height)
            tile_rects.append((tile_rect, tile))

            tile_x += tile_width
        if len(group) > 0:
            tile_x += group_gap

        # Check if the next group starts in a new line
        if tile_x + tile_width > play_area_rect.right:
            tile_y += tile_height + row_gap
            tile_x = play_area_rect.x  # Reset x to the start of the line


def show_remain_tiles_count(game_engine):
    from game_window import screen, font_smaller, white
    # show remain tiles count in tiles pool
    remain_tiles_count = len(game_engine.all_tiles)
    remain_tiles_count_surface = font_smaller.render(f"Remain Tiles: {remain_tiles_count}", True, white)
    screen.blit(remain_tiles_count_surface, (150, 20))


def show_round_over_screen(game_engine):
    from game_window import screen, font, white

    winner = None
    for player in game_engine.players:
        if player.is_winner:
            winner = player

    winner_text = f"Congratulations! {winner.player_name} is winner"
    winner_surface = font.render(winner_text, True, white)
    screen.blit(winner_surface, (150, 150))

    for i, player in enumerate(game_engine.players):
        score_surface = font.render(f"{player.player_name} Score: {player.round_score}", True, white)
        screen.blit(score_surface, (150, 150 + 100 + i * 60))


def show_grid_area(game_engine):
    from game_window import screen, gray, tile_width, tile_height, table_tiles_area_rect

    pygame.draw.rect(screen, gray, table_tiles_area_rect, 1)

    for x in range(table_tiles_area_rect.left, table_tiles_area_rect.right, tile_width):
        pygame.draw.line(screen, gray, (x, table_tiles_area_rect.top), (x, table_tiles_area_rect.bottom))
    for y in range(table_tiles_area_rect.top, table_tiles_area_rect.bottom, tile_height):
        pygame.draw.line(screen, gray, (table_tiles_area_rect.left, y), (table_tiles_area_rect.right, y))


def show_game_info_log(game_info_deque):
    from game_window import screen, font_game_info, white, info_box_rect
    for i, game_info in enumerate(game_info_deque):
        text = font_game_info.render(f"{game_info}", True, white)
        screen.blit(text, (info_box_rect.x, info_box_rect.y + i * 20))
