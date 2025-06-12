import os
import json


class ExclusionCoinsRecord:
    def __init__(self, exclusion_coins_path: str = "GeneralUtils/exclusion_coins.json"):
        self.exclusion_coins_path = exclusion_coins_path
        if not os.path.exists(self.exclusion_coins_path):
            self.stable_coins = []
            self.problematic_coins = []
        else:
            with open(self.exclusion_coins_path, 'r') as file:
                exclusion_data = json.load(file)
            self.stable_coins = exclusion_data.get("stable_coins", [])
            self.problematic_coins = exclusion_data.get("problematic_coins", [])
            
    def add_stable_coin(self, coin_symbol: str):
        """Add a stable coin to the exclusion list."""
        
        if coin_symbol != "USDT" and coin_symbol.endswith("USDT"):
            coin_symbol = coin_symbol[:-4]
        
        if coin_symbol and coin_symbol not in self.stable_coins:
            self.stable_coins.append(coin_symbol)
            self._save_exclusion_coins()
    
    def add_problematic_coin(self, coin_symbol: str):
        """Add a problematic coin to the exclusion list."""
        
        if coin_symbol != "USDT" and coin_symbol.endswith("USDT"):
            coin_symbol = coin_symbol[:-4]
        
        if coin_symbol and coin_symbol not in self.problematic_coins:
            self.problematic_coins.append(coin_symbol)
            self._save_exclusion_coins()
    
    # -------------------- assisted functions --------------------
    def _save_exclusion_coins(self):
        """Save the updated exclusion coins to the JSON file."""
        exclusion_data = {
            "stable_coins": self.stable_coins,
            "problematic_coins": self.problematic_coins
        }
        with open(self.exclusion_coins_path, 'w') as file:
            json.dump(exclusion_data, file, indent=4)
            
    
    def filter_coins(self, coins: list) -> list:
        """Filter out stable and problematic coins from the provided list."""
        return [
            coin for coin in coins 
            if coin not in self.stable_coins and coin not in self.problematic_coins
        ]
    
# Example usage:
if __name__ == "__main__":
    
    exclusion_coins = ExclusionCoinsRecord()
    exclusion_coins.add_stable_coin("USDC")
    exclusion_coins.add_problematic_coin("XYZ")
    
    print("Stable Coins:", exclusion_coins.stable_coins)
    print("Problematic Coins:", exclusion_coins.problematic_coins)