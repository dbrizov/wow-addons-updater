# World of Warcraft Addons Updater
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/dbrizov/wow-addons-updater/blob/master/LICENSE)

A simple python script that automatically updates your World of Warcraft addons

![wow_addons_updater.gif](https://github.com/dbrizov/wow-addons-updater/blob/master/docs/wow_addons_updater.gif)

## Requirements
- Python 3.6+
- [bs4](https://www.crummy.com/software/BeautifulSoup)
- [cloudscraper](https://github.com/VeNoMouS/cloudscraper)

```
pip install bs4
pip install cloudscraper
```

## How It Works
Place the `wow_addons_updater.py` and `wow_addons_updater.ini` files inside the **AddOns** folder.

Before running the script, you need to configure which addons you want to download.<br>
The `wow_addons_updater.ini` looks like this:
```
[General]
game_version = retail

[Addons]
bagnon
deadly-boss-mods
details
easy-frames
handynotes
handynotes-visions-of-nzoth
omni-cc
pawn
personal-loot-helper
raiderio
tomtom
weakauras-2
```

- In the **General** section you must specify the `game_version`. If you are playing WoW Classic, you must replace `retail` with `classic`
- The **Addons** section contains the list of addons you want to download

The names of the addons should be extracted from the **URLs** of the addons' pages.<br>
Lets say for example that you want to download **Deadly Boss Mods**.<br>
You have to navigate to the URL of the addon - [https://www.curseforge.com/wow/addons/deadly-boss-mods](https://www.curseforge.com/wow/addons/deadly-boss-mods)<br>
The name of the addon in the config file is the last part of the URL - `deadly-boss-mods`.

When you run the script it will do 3 things:
- **Collect the latest versions of the addons**
- **Download the addons** - keep in mind that it always downloads them, even if they are up to date. I might add a pre-filter in the collecting phase, so it downloads only the outdated ones.
- **Extract the addons**
