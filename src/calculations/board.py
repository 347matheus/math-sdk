import random
from typing import List
from src.state.state import *
from src.calculations.statistics import get_random_outcome


class Board(GeneralGameState):
    """Handles generation of a gameboard and symbols"""

    def create_board_reelstrips(self) -> None:
        """Randomly selects stopping positions from a reelstrip."""
        if self.config.include_padding:
            top_symbols = []
            bottom_symbols = []
        self.refresh_special_syms()
        self.reelstrip_id = get_random_outcome(
            self.get_current_distribution_conditions()["reel_weights"][self.gametype]
        )
        self.reelstrip = self.config.reels[self.reelstrip_id]
        anticipation = [0] * self.config.num_reels
        board = [[]] * self.config.num_reels
        for i in range(self.config.num_reels):
            board[i] = [0] * self.config.num_rows[i]
        reel_positions = [random.randrange(0, len(self.reelstrip[reel])) for reel in range(self.config.num_reels)]
        padding_positions = [0] * self.config.num_reels
        first_scatter_reel = -1
        for reel in range(self.config.num_reels):
            reelPos = reel_positions[reel]
            if self.config.include_padding:
                top_symbols.append(
                    self.create_symbol(self.reelstrip[reel][(reelPos - 1) % len(self.reelstrip[reel])])
                )
                bottom_symbols.append(
                    self.create_symbol(
                        self.reelstrip[reel][(reelPos + len(board[reel])) % len(self.reelstrip[reel])]
                    )
                )
            for row in range(self.config.num_rows[reel]):
                symbolID = self.reelstrip[reel][(reelPos + row) % len(self.reelstrip[reel])]
                sym = self.create_symbol(symbolID)
                board[reel][row] = sym
                if sym.special:
                    for special_symbol in self.special_syms_on_board:
                        for s in self.config.special_symbols[special_symbol]:
                            if board[reel][row].name == s:
                                self.special_syms_on_board[special_symbol] += [{"reel": reel, "row": row}]
                                if (
                                    board[reel][row].get_attribute("scatter")
                                    and len(self.special_syms_on_board[special_symbol])
                                    >= self.config.anticipation_triggers[self.gametype]
                                    and first_scatter_reel == -1
                                ):
                                    first_scatter_reel = reel + 1
            padding_positions[reel] = (reel_positions[reel] + len(board[reel]) + 1) % len(self.reelstrip[reel])

        if first_scatter_reel > -1 and first_scatter_reel != self.config.num_reels:
            count = 1
            for reel in range(first_scatter_reel, self.config.num_reels):
                anticipation[reel] = count
                count += 1

        for r in range(1, self.config.num_reels):
            if anticipation[r - 1] > anticipation[r]:
                raise RuntimeError

        self.board = board
        self.get_special_symbols_on_board()
        if len(self.special_syms_on_board["scatter"]) == 0 and sum(anticipation) > 0:
            print("here")
        self.reel_positions = reel_positions
        self.padding_position = padding_positions
        self.anticipation = anticipation
        if self.config.include_padding:
            self.top_symbols = top_symbols
            self.bottom_symbols = bottom_symbols

    def force_board_from_reelstrips(self, reelstrip_id: str, force_stop_positions: List[List]) -> None:
        """Creates a gameboard from specified stopping positions."""
        if self.config.include_padding:
            top_symbols = []
            bottom_symbols = []
        self.refresh_special_syms()
        self.reelstrip_id = reelstrip_id
        self.reelstrip = self.config.reels[self.reelstrip_id]
        anticipation = [0] * self.config.num_reels
        board = [[]] * self.config.num_reels
        for i in range(self.config.num_reels):
            board[i] = [0] * self.config.num_rows[i]

        reel_positions = [None] * self.config.num_reels
        for r, s in force_stop_positions.items():
            reel_positions[r] = s - random.randint(0, self.config.num_rows[r] - 1)
        for r, _ in enumerate(reel_positions):
            if reel_positions[r] is None:
                reel_positions[r] = random.randrange(0, len(self.reelstrip[r]))

        padding_positions = [0] * self.config.num_reels
        first_scatter_reel = -1
        for reel in range(self.config.num_reels):
            reelPos = reel_positions[reel]
            if self.config.include_padding:
                top_symbols.append(
                    self.create_symbol(self.reelstrip[reel][(reelPos - 1) % len(self.reelstrip[reel])])
                )
                bottom_symbols.append(
                    self.create_symbol(
                        self.reelstrip[reel][(reelPos + len(board[reel])) % len(self.reelstrip[reel])]
                    )
                )
            for row in range(self.config.num_rows[reel]):
                symbolID = self.reelstrip[reel][(reelPos + row) % len(self.reelstrip[reel])]
                sym = self.create_symbol(symbolID)
                board[reel][row] = sym

                if sym.special:
                    for special_symbol in self.special_syms_on_board:
                        for s in self.config.special_symbols[special_symbol]:
                            if board[reel][row].name == s:
                                self.special_syms_on_board[special_symbol] += [{"reel": reel, "row": row}]
                                if (
                                    board[reel][row].get_attribute("scatter")
                                    and len(self.special_syms_on_board[special_symbol])
                                    >= self.config.anticipation_triggers[self.gametype]
                                    and first_scatter_reel == -1
                                ):
                                    first_scatter_reel = reel + 1
                padding_positions[reel] = (reel_positions[reel] + len(board[reel]) + 1) % len(self.reelstrip[reel])

        if first_scatter_reel > -1 and first_scatter_reel <= self.config.num_reels:
            count = 1
            for reel in range(first_scatter_reel, self.config.num_reels):
                anticipation[reel] = count
                count += 1

        self.board = board
        self.reel_positions = reel_positions
        self.padding_position = padding_positions
        self.anticipation = anticipation
        if self.config.include_padding:
            self.top_symbols = top_symbols
            self.bottom_symbols = bottom_symbols

    def create_symbol(self, name) -> object:
        """Create a new symbol and assign relevent attributes."""
        if name not in self.symbol_storage.symbols:
            raise ValueError(f"Symbol '{name}' is not registered.")
        symObject = self.symbol_storage.create_symbol_state(name)
        if name in self.special_symbol_functions:
            for func in self.special_symbol_functions[name]:
                func(symObject)

        return symObject

    def refresh_special_syms(self) -> None:
        """Reset recorded speical symbols on board."""
        self.special_syms_on_board = {}
        for s in self.config.special_symbols:
            self.special_syms_on_board[s] = []

    def get_special_symbols_on_board(self) -> None:
        """Scans board for any active special symbols."""
        self.refresh_special_syms()
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                if self.board[reel][row].special:
                    for specialType in list(self.special_syms_on_board.keys()):
                        if self.board[reel][row].check_attribute(specialType):
                            self.special_syms_on_board[specialType].append({"reel": reel, "row": row})

    def transpose_board_string(self, board_string: List[List[str]]) -> List[List[str]]:
        """Transpose symbol names in the format displayed to the player during the game."""
        return [list(row) for row in zip(*board_string)]

    def print_board(self, board: List[List[object]]) -> List[List[str]]:
        "Prints transposed symbol names to the terminal."
        string_board = []
        max_sum_length = max(len(sym.name) for row in board for sym in row) + 1
        board_string = [[sym.name.ljust(max_sum_length) for sym in reel] for reel in board]
        transpose_board = self.transpose_board_string(board_string)
        print("\n")
        for row in transpose_board:
            string_board.append("".join(row))
            print("".join(row))
        print("\n")
        return string_board

    def board_string(self, board: List[List[object]]):
        """Prints symbol names only from gamestate.board."""
        board_str = [] * self.config.num_reels
        for reel in range(len(board)):
            board_str.append([x.name for x in board[reel]])
        return board_str
