import gamelib
import random
import math
import warnings
from sys import maxsize
import json

edge_positions =  [[1, 12], [2, 11], [3, 10], [4, 9], [5, 8], [22, 8], [6, 7], [7, 6], [8, 5], [9, 4], [18, 4], [10, 3], [17, 3], [11, 2], [16, 2], [12, 1], [15, 1], [13, 0], [14, 0]]
no_structure = [[0, 13], [1, 13], [1, 12], [2, 12], [2, 11], [3, 11], [3, 10], [4, 10], [4, 9], [5, 9], [5, 8], [6, 8], [6, 7], [7, 7], [7, 6], [8, 6], [8, 5], [9, 5], [9, 4], [10, 4], [10, 3], [11, 3], [11, 2], [12, 2], [12, 1], [13, 1], [13, 0]]

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        WALL = config["unitInformation"][0]["shorthand"]
        SUPPORT = config["unitInformation"][1]["shorthand"]
        TURRET = config["unitInformation"][2]["shorthand"]
        SCOUT = config["unitInformation"][3]["shorthand"]
        DEMOLISHER = config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = config["unitInformation"][5]["shorthand"]
        MP = 1
        SP = 0

        self.scored_on_locations = []

    def on_turn(self, turn_state):
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of The Mighty Chak custom algo strategy'.format(game_state.turn_number))
        game_state.suppress_warnings(True)

        self.the_mighty(game_state)

        game_state.submit_turn()

    def the_mighty(self, game_state):
        self.build_defences(game_state)
        self.build_reactive_defense(game_state)
        self.upgrade_defenses(game_state)

        if game_state.turn_number < 5:
            self.interceptor_send(game_state)
        else:
            if self.detect_enemy_unit(game_state, unit_type=None, valid_x=None, valid_y=[14, 15]) > 10:
                self.demolisher_send(game_state)
            else:
                if game_state.turn_number % 2 == 1:
                    best_loc = self.least_damage_spawn_location(game_state, edge_positions)
                    game_state.attempt_spawn(SCOUT, best_loc)

               

    def random_scout(self, game_state):
        for _ in range(10):  # Limit the number of attempts to avoid infinite loop
            if game_state.get_resource(MP) <= 0.99:
                break
            pos = random.choice(edge_positions)
            if game_state.can_spawn(SCOUT, pos):
                game_state.attempt_spawn(SCOUT, pos)

    def demolisher_send(self, game_state):
        pos = random.choice(edge_positions)
        while True:
            if game_state.can_spawn(DEMOLISHER, pos):
                game_state.attempt_spawn(DEMOLISHER, pos)
            else:
                break

    def interceptor_send(self, game_state):
        deploy_locations = self.filter_blocked_locations(edge_positions, game_state)
        for _ in range(10):  # Limit the number of attempts to avoid infinite loop
            if game_state.get_resource(MP) < game_state.type_cost(INTERCEPTOR)[MP] or len(deploy_locations) == 0:
                break
            deploy_index = random.randint(0, len(deploy_locations) - 1)
            deploy_location = deploy_locations[deploy_index]
            game_state.attempt_spawn(INTERCEPTOR, deploy_location)
            deploy_locations = self.filter_blocked_locations(edge_positions, game_state)  # Update deployable locations

    def build_defences(self, game_state):
        wall_positions = [[0, 13], [1, 13], [3, 13], [4, 13], [5, 13], [7, 13], [8, 13], [10, 13], [11, 13], [12, 13], [14, 13], [15, 13], [17, 13], [18, 13], [19, 13], [21, 13], [22, 13], [23, 13], [26, 13],[27,13],[26,12],[25,11],[24,11]]
        game_state.attempt_spawn(WALL, wall_positions)

        turret_locations = [[2,13], [6, 13], [9, 13], [13, 13], [16, 13], [20, 13], [24,13], [27,13]]
        game_state.attempt_spawn(TURRET, turret_locations)

    def upgrade_defenses(self, game_state):
        turret_locations = [[2,13], [6, 13], [9, 13], [13, 13], [16, 13], [20, 13], [24,13]]        
        wall_positions = [[0, 13], [1, 13], [3, 13], [4, 13], [5, 13], [7, 13], [8, 13], [10, 13], [11, 13], [12, 13], [14, 13], [15, 13], [17, 13], [18, 13], [19, 13], [21, 13], [22, 13], [23, 13], [26, 13],[27,13],[26,12],[25,11],[25,12],[24,11]]
        if game_state.turn_number % 2 == 1:
            game_state.attempt_upgrade(wall_positions)
        else:
            game_state.attempt_upgrade(turret_locations)

    def build_reactive_defense(self, game_state):
        for location in self.scored_on_locations:
            build_location = [location[0], location[1] + 1]
            for i in no_structure:
                if i != build_location: 
                    game_state.attempt_spawn(TURRET, build_location)


    def least_damage_spawn_location(self, game_state, location_options):
        damages = []
        for location in location_options:
            path = game_state.find_path_to_edge(location)
            damage = 0
            for path_location in path:
                damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(TURRET, game_state.config).damage_i
            damages.append(damage)

        return location_options[damages.index(min(damages))]

    def detect_enemy_unit(self, game_state, unit_type=None, valid_x=None, valid_y=None):
        total_units = 0
        for location in game_state.game_map:
            if game_state.contains_stationary_unit(location):
                for unit in game_state.game_map[location]:
                    if unit.player_index == 1 and (unit_type is None or unit.unit_type == unit_type) and (valid_x is None or location[0] in valid_x) and (valid_y is None or location[1] in valid_y):
                        total_units += 1
        return total_units

    def on_action_frame(self, turn_string):
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        for breach in breaches: 
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            if not unit_owner_self:
                gamelib.debug_write("Got scored on at: {}".format(location))
                self.scored_on_locations.append(location)
                gamelib.debug_write("All locations: {}".format(self.scored_on_locations))

    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()