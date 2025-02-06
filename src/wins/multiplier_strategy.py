"""Specifies how to incorporate multipliers into base wins"""

from typing import List, Dict


class MultiplierStrategy:
    """
    Global multipliers, symbol multipliers, combined multipliers or no actions
    All functions return [final_win_amount], [applied multiplier]
    """

    def apply_mult(self, strategy: str, win_amount: float = 0.0, positions: list = []):
        """Apply multiplier method to win_amount and winning symbol positions."""
        self.strat = {
            "global": self.apply_global_mult(win_amount),
            "symbol": self.apply_added_symbol_mult(win_amount, positions),
            "combined": self.apply_combined_mult(win_amount, positions),
        }
        return self.strat[strategy]

    def apply_global_mult(self, win_amount: float) -> tuple:
        """Enhance win global multiplier"""
        return (win_amount * self.global_multiplier, self.global_multiplier)

    def apply_added_symbol_mult(self, win_amount: float, positions: List[Dict]) -> tuple:
        """Get multiplier attribute from all winning positions"""
        symbol_multiplier = 0
        for pos in positions:
            if (
                self.board[pos["reel"]][pos["row"]].check_attribute("multiplier")
                and self.board[pos["reel"]][pos["row"]].get_attribute("multiplier") > 1
            ):
                symbol_multiplier += self.board[pos["reel"]][pos["row"]].get_attribute("multiplier")
        return (win_amount * max(symbol_multiplier, 1), max(symbol_multiplier, 1))

    def apply_multiplied_symbol_mult(self, win_amount: float, positions: List[Dict]) -> tuple:
        """Get multiplier attribute from all winning positions"""
        symbol_multiplier = 0
        for pos in positions:
            if self.board[pos["reel"]][pos["row"]].check_attribute("multiplier"):
                symbol_multiplier += self.board[pos["reel"]][pos["row"]].getAttribute("multiplier")
        return (win_amount * max(symbol_multiplier, 1), max(symbol_multiplier, 1))

    def apply_combined_mult(self, win_amount: float, positions: List[Dict]):
        """Apply symbol multipliers and then global multiplier"""
        win, sym_mult = self.apply_added_symbol_mult(win_amount, positions)
        return (win, sym_mult * self.global_multiplier)
