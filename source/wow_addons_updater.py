import os
import json
import zipfile
import cloudscraper
from bs4 import BeautifulSoup


BASE_URL = "https://www.curseforge.com"
GAME_VERSION_RETAIL = "1738749986%3A517"
GAME_VERSION_CLASSIC = "1738749986%3A67408"
HTTP = cloudscraper.create_scraper()


class Addon:
    def __init__(self, name, version, game_version, url):
        self.name = name
        self.version = version
        self.game_version = game_version
        self.url = url

    def __str__(self):
        return f"[name={self.name}, version={self.version}, game_version={self.game_version}, url={self.url}]"

    def to_short_string(self):
        return f"_{self.name}__{self.version}__({self.game_version})"


def find_addon_latest_version(addon_name, game_version):
    print(f"Collecting '{addon_name}'")

    url = f"{BASE_URL}/wow/addons/{addon_name}/files/all?filter-game-version={game_version}"
    response = HTTP.get(url)
    response.raise_for_status()

    html_parser = BeautifulSoup(response.text, "html.parser")
    rows = html_parser.find_all("tr")

    for row in rows[1:]:
        cols = row.find_all("td")
        release_type = cols[0].text.strip()

        if release_type == "R":
            addon_version = cols[1].text.strip()
            addon_game_version = cols[4].text.strip()
            addon_url = f"{BASE_URL}{cols[1].find('a')['href']}"
            addon = Addon(addon_name, addon_version, addon_game_version, addon_url)
            return addon

    print(f"Error: '{addon_name}' not found")
    return None


def download_addon(addon: Addon):
    print(f"Downloading '{addon.to_short_string()}.zip'")

    response = HTTP.get(addon.url)
    response.raise_for_status()

    html_parser = BeautifulSoup(response.text, "html.parser")
    a_tag_buttons = html_parser.find_all("a", {"class": "button button--hollow"})

    for a_tag in a_tag_buttons:
        url = a_tag.get("href")
        if url.startswith(f"/wow/addons/{addon.name}/download/"):
            response = HTTP.get(f'{BASE_URL}{url}/file')
            response.raise_for_status()

            current_directory = os.path.dirname(os.path.realpath(__file__))
            output_zip_file_path = f"{current_directory}/{addon.to_short_string()}.zip"

            with open(output_zip_file_path, "wb") as zip_file:
                zip_file.write(response.content)
                return True

    print(f"Error: could not download '{addon.to_short_string()}.zip'")
    return False


def extract_addon(addon: Addon):
    print(f"Extracting '{addon.to_short_string()}.zip'")

    current_directory = os.path.dirname(os.path.realpath(__file__))
    output_zip_file_path = f"{current_directory}/{addon.to_short_string()}.zip"

    with zipfile.ZipFile(output_zip_file_path, "r") as zip:
        zip.extractall(current_directory)


def get_config():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = f"{current_directory}/config.json"
    with open(file_path, "r") as file_stream:
        return json.load(file_stream)


def collect_addons():
    config = get_config()
    game_version_string = config["game-version"]
    game_version = GAME_VERSION_RETAIL if (game_version_string == "retail") else GAME_VERSION_CLASSIC
    addon_names = config["addons"]

    found_addons = list()
    for addon_name in addon_names:
        addon = find_addon_latest_version(addon_name, game_version)
        if addon:
            found_addons.append(addon)

    downloaded_addons = list()
    for addon in found_addons:
        success = download_addon(addon)
        if success:
            downloaded_addons.append(addon)

    return downloaded_addons


def update_addons():
    addons = collect_addons()
    for addon in addons:
        extract_addon(addon)


if __name__ == '__main__':
    update_addons()
