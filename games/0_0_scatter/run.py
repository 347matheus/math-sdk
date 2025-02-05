"""Main file for generating results for sample scatter-pay game."""

from gamestate import GameState
from game_config import GameConfig
from src.write_data.write_data import create_books
from src.write_data.write_configs import generate_configs
from src.wins.win_manager import WinManager

if __name__ == "__main__":

    num_threads = 1
    rust_threaeds = 20
    batching_size = 5000
    compression = False
    profiling = False

    num_sim_args = {
        # "base": int(1e2),
        "bonus": int(1e2),
    }

    config = GameConfig()
    winManager = WinManager(config.basegame_type, config.freegame_type)
    gamestate = GameState(config)

    create_books(
        gamestate,
        config,
        num_sim_args,
        batching_size,
        num_threads,
        compression,
        profiling,
    )
    generate_configs(gamestate)
