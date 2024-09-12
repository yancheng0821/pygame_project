import random

from itertools import combinations


def add_to_all_tiles(game_engine, tile):
    game_engine.all_tiles.append(tile)


def add_to_rack(player, tile):
    rack = player.player_rack
    rack.append(tile)
    player.player_rack = sort_tiles_in_group(rack)


def remove_from_rack(player, tile):
    player.player_rack.remove(tile)


def add_to_table(game_engine, tiles):
    game_engine.tables.append(tiles)


def add_table(game_engine, group):
    game_engine.tables.append(group)


def add_remain_groups(game_engine, groups):
    game_engine.tables.extend(groups)


def clear_tables(game_engine):
    game_engine.tables.clear()


def get_random_tile(game_engine):
    # get a tile
    random_tile = random.choice(game_engine.all_tiles)
    return random_tile


def remove_from_pool(game_engine, tile):
    game_engine.all_tiles.remove(tile)


def get_random_tile_and_remove_it_from_pool(game_engine):
    # get a tile
    random_tile = get_random_tile(game_engine)
    # remove this tile
    remove_from_pool(game_engine, random_tile)
    return random_tile


def is_run(tiles):
    if len(tiles) < 3:
        return False
    diff_colors = set()
    for tile in tiles:
        diff_colors.add(tile.colour)
    if len(diff_colors) > 1:
        return False

    numbers = []
    for tile in tiles:
        numbers.append(tile.number)
    numbers = sorted(numbers)

    if not all(numbers[i] == numbers[i - 1] + 2 for i in range(1, len(numbers))):
        return False

    odd_or_even = numbers[0] % 2
    return all(number % 2 == odd_or_even for number in numbers)


def is_set(tiles):
    if len(tiles) < 3:
        return False

    diff_numbers = set()
    for tile in tiles:
        diff_numbers.add(tile.number)
    if len(diff_numbers) > 1:
        return False

    diff_colors = set()
    for tile in tiles:
        diff_colors.add(tile.colour)

    return len(diff_colors) == len(tiles)


def sum_tiles(tiles):
    result_sum = 0
    for tile in tiles:
        result_sum += tile.number

    return result_sum


def max_sum_tile_number(group):
    # Get the highest tile number in a group
    return sum(tile.number for tile in group)


def find_first_valid_group(player):
    first_valid_group = []
    tiles = player.player_rack

    max_length = 5  # 5 is the max length of group
    for i in range(3, min(len(tiles) + 1, max_length + 1)):
        for group in combinations(tiles, i):
            if is_run(group) or is_set(group):
                first_valid_group.append(group)

    first_valid_group.sort(key=max_sum_tile_number, reverse=True)
    print(f"find all groups: {first_valid_group}")

    unique_id_set = set()
    unique_id_set_memory = set()
    index = 0
    result = []
    flag = True
    for group in first_valid_group:
        for tile in group:
            index += 1
            unique_id_set.add(tile.unique_id)
            if len(unique_id_set) != index:
                flag = False
        if flag:
            result.append(group)
            unique_id_set_memory = unique_id_set
        else:
            unique_id_set = unique_id_set_memory

        index = len(unique_id_set)
        flag = True

    sum_number = 0
    for group in result:
        sum_number += sum_tiles(group)
    if sum_number < 30:
        result.clear()

    print(f"choose the best:{player.player_name}'s first valid groups : {result}")

    return result


def decide_first_player(game_engine):
    play_order_list = []
    max_num = 0
    first_player = None
    players = game_engine.players
    for player in players:
        tile = get_random_tile(game_engine)
        player_num = tile.number
        player.round_order_tile = tile
        print(f"{player.player_name} drawn a {tile}")

        if player_num > max_num:
            max_num = player_num
            first_player = player

        play_order_list.append(player)

    for player in play_order_list:
        if player.player_name == first_player.player_name:
            player.is_your_turn = True
            print(f"++++++++first player is : {player.player_name}++++++++")
            break

    return play_order_list


def send_begin_tiles_to_player(game_engine):
    print(f"start send tiles to each player")
    for player in game_engine.players:
        for _ in range(game_engine.init_tiles_number):
            # add tile to this player rack
            add_to_rack(player, get_random_tile_and_remove_it_from_pool(game_engine))

        player.player_rack = sort_tiles_in_group(player.player_rack)


def sort_tiles_in_group(group):
    # ordered by Tiles number
    return sorted(group, key=lambda tile: tile.number)


def draw_random_two_tiles(game_engine):
    draw_tiles = []
    for _ in range(2):
        tile = get_random_tile(game_engine)
        draw_tiles.append(tile)
    return draw_tiles


def check_winner(game_engine, computer_or_player):
    winner_is_produced = False
    if len(computer_or_player.player_rack) == 0:
        computer_or_player.is_winner = True
        print(f"!!!!!!!!{computer_or_player.player_name} : Rummikub!!!")
        winner_is_produced = True

    round_score_list = []
    if winner_is_produced:
        sum_score = 0
        for player in game_engine.players:
            sum_score += sum_tiles(player.player_rack)
            score = -(sum_tiles(player.player_rack))
            player.round_score = score
            if player.player_name != computer_or_player.player_name:
                round_score_list.append(player)

        computer_or_player.round_score = sum_score
        round_score_list.append(computer_or_player)

        game_engine.rounds.append(round_score_list)

    return round_score_list
