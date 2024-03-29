# World of Warcraft Addons Updater
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/dbrizov/wow-addons-updater/blob/master/LICENSE)

A simple python script that automatically updates your World of Warcraft addons

![wow_addons_updater.gif](https://github.com/dbrizov/wow-addons-updater/blob/master/docs/wow_addons_updater.gif)

## Requirements
If you want to run the script manually, you need:
- Python 3.6+
- [bs4](https://www.crummy.com/software/BeautifulSoup)
- [cloudscraper](https://github.com/VeNoMouS/cloudscraper)

```
pip install bs4
pip install cloudscraper
```

There's also an executable file which can be found under the [releases](https://github.com/dbrizov/wow-addons-updater/releases) tab.

## How It Works
Before running the `wow_addons_updater.py` or `wow_addons_updater.exe`, you need to configure which addons you want to download.<br>
This is done in the `wow_addons_updater.ini` file which looks like this:
```
[General]
game_version = retail
download_directory = F:\Games\World of Warcraft\_retail_\Interface\AddOns

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

**[General]**
- **game_version** - `retail`, `classic` or `wotlk`
- **download_directory** - this is the path to your addons folder

**[Addons]**
- This section contains the list of addons you want to download

The names of the addons should be extracted from the **URLs** of the addons' pages.<br>
Lets say for example that you want to download **Deadly Boss Mods**.<br>
You have to navigate to the URL of the addon - [https://www.curseforge.com/wow/addons/deadly-boss-mods](https://www.curseforge.com/wow/addons/deadly-boss-mods)<br>
The name of the addon in the config file is the last part of the URL - `deadly-boss-mods`.

When you run the script it will do 3 things:
- **Collect the latest versions of the addons**
- **Download the addons** - keep in mind that it always downloads them, even if they are up to date. I might add a pre-filter in the collecting phase, so it downloads only the outdated ones.
- **Extract the addons**
