from itertools import combinations

from game_handler import is_run, is_set


def find_best_solution(player_tiles, table_tiles):
    max_hand_used = 0
    best_solution = None
    table_remaining_groups = None
    hand_tiles = None
    max_length = 5  # 5 is the max length of group

    # first , check player tiles can create new run or set , don't need use table tiles
    for r in range(3, min(len(player_tiles) + 1, max_length)):
        for hand_combo in combinations(player_tiles, r):
            if all(is_run(c) or is_set(c) for c in [hand_combo]):
                hand_used = len(hand_combo)
                if hand_used > max_hand_used:
                    max_hand_used = hand_used
                    best_solution = hand_combo
                    table_remaining_groups = table_tiles
                    hand_tiles = hand_combo

    # 1. Iterate over all combinations of player's hand tiles
    for r in range(1, min(len(player_tiles) + 1, max_length)):
        for hand_group in combinations(player_tiles, r):

            # 2. Iterate over all table_groups and individual tiles in each group
            for table_group in table_tiles:
                for i in range(1, min(len(table_tiles) + 1, max_length)):
                    for table_combo in combinations(table_group, i):
                        # Combine player hand group with the current table tile
                        new_group = list(hand_group) + list(table_combo)

                        # 3. Check if the new combination is a valid group
                        if len(new_group) >= 3 and (is_run(new_group) or is_set(new_group)):
                            remaining_table_group = []
                            tile_unique_ids = [tile.unique_id for tile in table_combo]
                            for tile in table_group:
                                # Remove the current table tile from the table group
                                if tile.unique_id not in tile_unique_ids:
                                    remaining_table_group.append(tile)

                            # Check if the remaining tiles in the table_group form a valid group
                            if (not remaining_table_group or
                                    is_run(remaining_table_group) or
                                    is_set(remaining_table_group)):
                                hand_used = len(hand_group)

                                # 4. Check if this uses more player hand tiles than the current best
                                if hand_used > max_hand_used:
                                    max_hand_used = hand_used
                                    best_solution = new_group
                                    table_remaining_groups = (
                                            [g for g in table_tiles if g != table_group] + [remaining_table_group])
                                    hand_tiles = hand_group

    # best_solution not None, return best_solution
    if best_solution:
        sorted_best_combo = sort_tiles_in_group(best_solution)
        sorted_remaining_groups = [sort_tiles_in_group(group) for group in table_remaining_groups]
        return hand_tiles, sorted_best_combo, sorted_remaining_groups

    return None, None, table_tiles


def generate_all_possible_groups(tiles):
    # generate all possible groups
    all_groups = []
    for r in range(3, len(tiles) + 1):
        for group in combinations(tiles, r):
            if is_run(group) or is_set(group):
                all_groups.append(group)
    return all_groups


def sort_tiles_in_group(group):
    # ordered by Tiles number
    return sorted(group, key=lambda tile: tile.number)


def remove_tiles_from_group(all_table_tiles, used_tiles):
    # remove tiles from the table tiles
    for used_tile in used_tiles:
        all_table_tiles.remove(used_tile)

    return all_table_tiles

