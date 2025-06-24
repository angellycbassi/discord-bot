"""
Utility functions for the Discord RPG Bot.
Contains shared logic and helper functions used across different modules.
"""

import re
import random
from typing import Tuple, Optional

def roll_dice(dice_str: str) -> Tuple[int, list, str]:
    """
    Parse and roll dice in XdY+Z format.
    
    Args:
        dice_str (str): Dice string in format XdY+Z (e.g., "2d6+3")
    
    Returns:
        Tuple[int, list, str]: (total result, individual rolls, formatted string)
    
    Example:
        >>> roll_dice("2d6+3")
        (11, [4, 4], "2d6+3 = [4, 4] + 3 = 11")
    """
    pattern = r"(\d+)d(\d+)([+-]\d+)?"
    match = re.match(pattern, dice_str.lower())
    
    if not match:
        raise ValueError("Invalid dice format. Use XdY+Z format (e.g., 2d6+3)")
    
    num_dice = int(match.group(1))
    sides = int(match.group(2))
    modifier = int(match.group(3) or 0)
    
    rolls = [random.randint(1, sides) for _ in range(num_dice)]
    total = sum(rolls) + modifier
    
    result_str = f"{dice_str} = {rolls}"
    if modifier:
        result_str += f" {'+' if modifier > 0 else ''}{modifier}"
    result_str += f" = {total}"
    
    return total, rolls, result_str

def load_data(file_path: str) -> dict:
    """
    Load JSON data from a file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict: Loaded data or empty dict if file doesn't exist
    """
    import json
    import os
    
    if not os.path.exists(file_path):
        return {}
        
    with open(file_path, 'r') as f:
        return json.load(f)

def save_data(data: dict, file_path: str) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data (dict): Data to save
        file_path (str): Path to the JSON file
    """
    import json
    import os
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
