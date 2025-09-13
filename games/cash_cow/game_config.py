from config.config import Config
import random

class GameConfig(Config):
    def get_game_math(self):
        return {
            "layout": {
                "reels": 5,
                "rows": 5,
                "paylines": 15
            },
            "symbols": {
                "low": ["Cenoura", "Maçã", "Uvas", "Ovos", "Balde de Leite"],
                "mid": ["Fazendeira", "Fazendeiro", "Vaca Dourada"],
                "high": ["WildSymbol"]
            },
            "paytable": {
                "Cenoura": {"3": 0.2, "4": 0.4, "5": 1.0},
                "Maçã": {"3": 0.2, "4": 0.4, "5": 1.0},
                "Uvas": {"3": 0.2, "4": 0.4, "5": 1.0},
                "Ovos": {"3": 0.2, "4": 0.4, "5": 1.0},
                "Balde de Leite": {"3": 0.2, "4": 0.4, "5": 1.0},
                "Fazendeira": {"3": 0.5, "4": 2.0, "5": 4.0},
                "Fazendeiro": {"3": 0.5, "4": 2.0, "5": 4.0},
                "Vaca Dourada": {"3": 2, "4": 6, "5": 12},
                "WildSymbol": {"5": 25}
            },
            "VS_symbol": {
                "multiplier_range": [2, 100],
                "expands_to_full_reel": True,
                "combine_rule": "sum"
            },
            "bonus_features": [
                {
                    "name": "GoldenCowHunt",
                    "trigger": {"scatter": "Vaca Dourada", "count": 3},
                    "phase1": {
                        "spins": 3,
                        "collectable": ["WildSymbol"],
                        "reset_spins_on_collect": True,
                        "max_collect_wilds": 15,
                        "max_multiplier": 100
                    },
                    "phase2": {
                        "showdown_spins": 3,
                        "apply_collected_wilds": True,
                        "apply_accumulated_multiplier": True
                    }
                }
            ],
            "max_win_multiplier": 12500
        }

    def simulate_round(self):
        print("🌰 Simulando uma rodada de Cash Cow!")
        payout = 0.0
        win = False
        bonus_triggered = False

        if random.random() < 0.28:  # Ajustado: 0.27 → 0.28
            payout = random.choice([0.3, 0.5, 1, 2, 3, 5, 8])
            print(f"✅ Vitória na rodada! Pagamento: {payout}")
            win = True

        if random.random() < 0.005:
            bonus_triggered = True
            bonus_win = self.simulate_bonus_round()
            payout += bonus_win
            print(f"🎯 Bônus Golden Cow Hunt ativado! Ganho no bônus: {bonus_win}")

        return {
            "payout": payout,
            "win": win,
            "bonus_triggered": bonus_triggered
        }

    def simulate_bonus_round(self):
        print("🐄 Iniciando bônus: Golden Cow Hunt!")
        spins_left = 3
        collected_wilds = 0
        multipliers = []

        while spins_left > 0:
            print(f"🎲 Rodada bônus - Spins restantes: {spins_left}")
            if random.random() < 0.35:
                multiplier = 3
                multipliers.append(multiplier)
                collected_wilds += 1
                print(f"🌟 Vaca dourada coletada! Multiplicador {multiplier}x")
                spins_left = 3
            else:
                spins_left -= 1

            if collected_wilds >= 15:
                print("💥 Número máximo de vacas douradas alcançado!")
                break

        total_multiplier = sum(multipliers) if multipliers else 1
        base_bonus_win = 4  # Ajustado: 3 → 4
        final_bonus_payout = base_bonus_win * total_multiplier

        print(f"🏆 Ganho total do bônus: {final_bonus_payout:.2f} (Base: {base_bonus_win} x Mult: {total_multiplier})\n")
        return final_bonus_payout

