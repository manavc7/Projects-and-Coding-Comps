import gamelib
import random
import math
import warnings
from sys import maxsize
import json

edge_positions = [[0, 13], [27, 13], [1, 12], [2, 11], [3, 10], [4, 9], [5, 8], [22, 8], [6, 7], [7, 6], [8, 5], [9, 4], [18, 4], [10, 3], [17, 3], [11, 2], [16, 2], [12, 1], [15, 1], [13, 0], [14, 0]]

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

        if game_state.turn_number < 5:
            self.interceptor_send(game_state)
        else:
            if self.detect_enemy_unit(game_state, unit_type=None, valid_x=None, valid_y=[14, 15]) > 10:
                self.demolisher_send(game_state)
            else:
                if game_state.turn_number % 2 == 1:
                    best_loc = self.least_damage_spawn_location(game_state, edge_positions)
                    game_state.attempt_spawn(SCOUT, best_loc)
                
                support_locations = [[3, 13], [4, 12], [5, 11], [6, 10], [7, 9], [8, 8], [9, 7], [10, 6], [10, 5], [19,6], [20,7], [21,8],[22,9],[23,10],[24,11],[25,12],[26,13]]
                deployaple_support = self.filter_blocked_locations(support_locations, game_state)
                game_state.attempt_spawn(SUPPORT, deployaple_support)

    def random_scout(self, game_state):
        while game_state.get_resource(MP)>0.99:
            pos = random.choice(edge_positions)
            if game_state.can_spawn(SCOUT, pos):
                game_state.attempt_spawn(SCOUT, pos)
         
    def demolisher_send(self, game_state):
        pos = random.choice(edge_positions)
        if game_state.can_spawn(DEMOLISHER, pos):
            game_state.attempt_spawn(DEMOLISHER, pos)

    def interceptor_send(self, game_state):
        deploy_locations = self.filter_blocked_locations(edge_positions, game_state)
        while game_state.get_resource(MP) >= game_state.type_cost(INTERCEPTOR)[MP] and len(deploy_locations) > 0:
            deploy_index = random.randint(0, len(deploy_locations) - 1)
            deploy_location = deploy_locations[deploy_index]
            game_state.attempt_spawn(INTERCEPTOR, deploy_location)

    def build_defences(self, game_state):
        wall_positions = [[2, 13], [3, 12], [4, 11], [5, 10], [6, 9], [7, 8], [8, 7], [9, 6], [10, 5], [16,5], [17,5], [18,5]]
        game_state.attempt_spawn(WALL, wall_positions)
        
        turret_locations = [[9, 7], [18, 7], [6, 10], [12, 4], [12, 7], [15, 7], [9, 10],[4,12],[4,13],[5,13],[3,13]]
        while game_state.get_resource(SP)>20:
            turret_rand = random.choice(turret_locations)
            game_state.attempt_spawn(TURRET, turret_rand)
            
        support_locations = [[11, 5], [12, 5], [13, 5], [14, 5,], [15, 5]]
        game_state.attempt_spawn(SUPPORT, support_locations)        

    def build_reactive_defense(self, game_state):
        for location in self.scored_on_locations:
            build_location = [location[0], location[1] + 1]
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
        """
        This is the action frame of the game. This function could be called 
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at in json-docs.html in the root of the Starterkit.
        """
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