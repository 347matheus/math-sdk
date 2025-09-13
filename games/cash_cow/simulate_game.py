from game_config import GameConfig

def simulate_game_rounds(num_rounds=100000):
    config = GameConfig()
    total_payout = 0.0
    total_bet = num_rounds

    for _ in range(num_rounds):
        result = config.simulate_round()
        total_payout += result["payout"]

    rtp = (total_payout / total_bet) * 100
    print(f"\nSimulated {num_rounds} rounds. Estimated RTP: {rtp:.2f}%")

if __name__ == "__main__":
    simulate_game_rounds()
