from game_executables import *
from src.calculations.statistics import get_random_outcome

class GameStateOverride(GameExecutables):
    """
    This class is is used to override or extend universal state.py functions.
    e.g: A specific game may have custom book properties to reset 
    """

    def reset_book(self):
        #Reset global values used across multiple projects
        super().reset_book()
        #Reset parameters relevant to local game only

    def assign_special_sym_function(self):
        self.special_symbol_functions = {
            'W': []
        }

    def assign_mult_property(self, symbol):
        multiplier_value = get_random_outcome(self.get_current_distribution_conditions()["multiplierValues"][self.gametype])
        symbol.assign_attribute({"multiplier":multiplier_value})
    
    def check_game_repeat(self):
        if self.repeat == False:
            win_criteria = self.get_current_betmode_distributions().get_win_criteria()
            if win_criteria is not None and self.final_win != win_criteria:
                self.repeat = True 
            
