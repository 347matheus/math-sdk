from src.config.config import Config
from src.config.distributions import Distribution, DistributionConditions
from src.write_data.force import *
from src.config.bet_mode import BetMode

class GameConfig(Config):
    def __init__(self):
        super().__init__()
        self.game_id = "0_0_ways"
        self.provider_number = 0
        self.working_name = "sample ways game"
        self.wincap = 5000
        self.win_type = "ways"
        self.rtp = 0.97
        self.construct_paths(self.game_id)
        
        # Game Dimensions
        self.num_reels = 5
        self.num_rows = [0]*self.num_reels #Optionally include variable number of rows per reel
        #Board and Symbol Properties
        self.paytable = {}
    
        self.include_padding = True
        self.special_symbols = {
            "wild": ["W"],
            "scatter": ["S"],
            "multiplier": []
        }

        self.freespin_triggers = {
           self.base_game_type : {3:8, 4:12, 5: 15},
           self.free_game_type: {2: 4, 3:6, 4:8, 5:10}
        }
        self.anticipation_triggers = {
            self.base_game_type : 2,
            self.free_game_type:1
        }
        #Reels
        reels = {
            "BR0": "BR0.csv",
            "FR0": "FR0.csv"
        }
        self.reels = {}
        for r,f in reels.items():
            self.reels[r] = self.read_reels_csv(str.join("/",[self.reelsPath,f]))

        self.bet_modes = [
            BetMode(
                name = "base",
                title= "standard game entry",
                description = "default game entry type",
                cost = 1.0,
                rtp = self.rtp,
                max_win = self.wincap,
                auto_close_disables = False,
                is_feature = True,
                is_enhanced_mode = False,
                is_buy_bonus = False,
                distributions = [
                    Distribution(
                        criteria="winCap", 
                        quota=0.001, 
                        # win_criteria=self.wincap, 
                        conditions = {
                            "reel_weights": {self.base_game_type : {"BR0":1}, self.free_game_type: {"FR0":1}},
                            "force_wincap": True,
                            "force_freespins": True
                        }),
                    Distribution(
                        criteria="freeGame", 
                        quota=0.1, 
                        conditions= {
                            "reel_weights": {self.base_game_type: {"BR0": 1}, self.free_game_type: {"FR0":1}},
                            "force_wincap": False,
                            "force_freespins": True
                        }),
                    Distribution(
                        criteria="0", 
                        quota=0.4, 
                        win_criteria=0.0, 
                        conditions= {
                            "reel_weights": {self.base_game_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freespins": False
                        }),
                    Distribution(
                        criteria="baseGame", 
                        quota=0.5, 
                        conditions= {
                            "reel_weights": {self.base_game_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freespins": False
                    })
                ]
            )
        ]
        