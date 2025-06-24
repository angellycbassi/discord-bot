# Discord RPG Bot

A modular Discord bot built with discord.py for managing tabletop RPG games with features for character management, combat, and inventory systems.

## Features

- Character Management:
  - Create, view, edit, and delete character sheets
  - Flexible attribute system
  - Persistent storage using JSON (ready for SQLite migration)

- Combat System:
  - Initiative tracking
  - Turn management
  - Attack and defense rolls
  - Custom dice rolling (XdY+Z format)

- Inventory Management:
  - Add and remove items
  - Track quantities
  - Item categorization
  - Inventory listing with filters

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Discord bot token:
```
DISCORD_TOKEN=your_token_here
```

## Usage

1. Start the bot:
```bash
python bot.py
```

2. Available Commands:

### Slash Commands

Character Management:
- `/create_character name race class`
- `/view_character name`
- `/edit_character name attribute value`
- `/delete_character name`

Combat:
- `/start_combat [description]`
- `/join_combat character_name [initiative_mod]`
- `/attack target dice [modifier]`
- `/defend dice [modifier]`
- `/end_combat`

Inventory:
- `/add_item character_name item_name item_type [quantity] [description]`
- `/remove_item character_name item_name [quantity]`
- `/list_inventory character_name [item_type]`

### Text Commands

Character Management:
```
!character create <name> <race> <class>
!character view <name>
!character edit <name> <attribute> <value>
!character delete <name>
```

Combat:
```
!combat start [description]
!combat join <character> [initiative_mod]
!combat attack <target> <dice> [modifier]
!combat defend <dice> [modifier]
!combat end
```

Inventory:
```
!inventory add <character> <item> <type> [quantity] [description]
!inventory remove <character> <item> [quantity]
!inventory list <character> [type]
```

## Project Structure

```
discord_rpg_bot/
├── bot.py              # Main bot file
├── config.py           # Configuration and settings
├── utils.py           # Shared utility functions
├── requirements.txt    # Project dependencies
├── data/              # Data storage directory
└── cogs/              # Command modules
    ├── character.py    # Character management
    ├── combat.py      # Combat system
    └── inventory.py    # Inventory management
```

## Development

To add new features or modify existing ones:

1. Each module in `cogs/` is independent and follows a consistent structure
2. Use docstrings and type hints for better code documentation
3. Follow the existing error handling patterns
4. Update the README with any new commands or features

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
