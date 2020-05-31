# World of Warcraft Addons Updater
A simple python script that automatically updates your World of Warcraft addons

![wow_addons_updater.gif](https://github.com/dbrizov/wow-addons-updater/blob/master/docs/wow_addons_updater.gif)

## Requirements
If you want to run the script manually, you will need:
- Python 3.6+
- [bs4](https://www.crummy.com/software/BeautifulSoup)
- [cloudscraper](https://github.com/VeNoMouS/cloudscraper)

```
pip install bs4
pip install cloudscraper
```

Otherwise, you can just run the `wow_addons_updater.exe`

## How It Works
Place the `config.json` and `wow_addons_updater.py` files inside the **AddOns** folder.<br>
If you are using the .exe, you need to place the `wow_addons_updater.exe` instead of `wow_addons_updater.py`.

Before running the script or .exe, you need to configure which addons you want to download.<br>
The `config.json` looks like this:
```
{
    "game-version": "retail",
    "addons": [
        "bagnon",
        "deadly-boss-mods",
        "details",
        "easy-frames",
        "handynotes",
        "handynotes-visions-of-nzoth",
        "omni-cc",
        "pawn",
        "personal-loot-helper",
        "raiderio",
        "tomtom",
        "weakauras-2"
    ]
}
```

- **game-version** - if you are playing WoW Classic, you should replace it with `classic`
- **addons** - this is the list of addons you want to download

The names of the addons should be extracted from the **URLs** of the addons' pages.<br>
Lets say for example that you want to download **Deadly Boss Mods**.<br>
You have to navigate to the URL of the addon - [https://www.curseforge.com/wow/addons/deadly-boss-mods](https://www.curseforge.com/wow/addons/deadly-boss-mods)<br>
The name of the addon in the config file is the last part of the URL - `deadly-boss-mods`.

When you run the script it will do 3 things:
- **Collect the latest versions of the addons**
- **Download the addons** - keep in mind that it always downloads the addons, even if they are up to date. I might add a pre-filter in the collection phase, so it downloads only the outdated ones.
- **Extract the addons**
