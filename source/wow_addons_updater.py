import os
import zipfile
import cloudscraper
import logging
from configparser import ConfigParser
from requests import ReadTimeout
from requests import HTTPError
from requests import ConnectionError
from bs4 import BeautifulSoup


BASE_URL = "https://www.curseforge.com"
GAME_VERSION_RETAIL = "1738749986%3A517"  # URL argument for retail addons
GAME_VERSION_CLASSIC = "1738749986%3A67408"  # URL argument for classic addons
HTTP = cloudscraper.create_scraper()  # HTTP requester
HTTP_REQUEST_TIMEOUT = 15  # 15 seconds
FILE_NAME = "wow_addons_updater.py"  # For some reason the build tool doesn't recognize '__file__' so I have to hardcode the name of the script file
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(FILE_NAME))


logging.basicConfig(filename=f"{CURRENT_DIRECTORY}/wow_addons_updater.log", filemode="w", level=logging.DEBUG)


def log(message: str):
    print(message)
    logging.info(message)


def log_error(message: str):
    print(message)
    logging.error(message)


def get_config():
    file_path = f"{CURRENT_DIRECTORY}/wow_addons_updater.ini"
    config = ConfigParser(allow_no_value=True)
    config.read(file_path)
    return config


def get_download_directory():
    config = get_config()
    download_directory = CURRENT_DIRECTORY
    if "download_directory" in config["General"]:
        download_directory = config["General"]["download_directory"].replace("\\", "/")

    return download_directory


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
    log(f"Collecting '{addon_name}'")

    try:
        url = f"{BASE_URL}/wow/addons/{addon_name}/files/all?filter-game-version={game_version}"
        response = HTTP.get(url, timeout=HTTP_REQUEST_TIMEOUT)
        response.raise_for_status()

        html_parser = BeautifulSoup(response.text, "html.parser")
        rows = html_parser.find_all("tr")

        for row in rows[1:]:
            cols = row.find_all("td")
            release_type = cols[0].text.strip()

            if release_type == "R":  # R stands for Release
                addon_version = cols[1].text.strip()
                addon_game_version = cols[4].text.strip()
                addon_url = f"{BASE_URL}{cols[1].find('a')['href']}"
                addon = Addon(addon_name, addon_version, addon_game_version, addon_url)
                return addon
    except ReadTimeout:
        log_error(f"Error: HTTP request timed out after {HTTP_REQUEST_TIMEOUT} seconds")
    except HTTPError:
        log_error(f"Error: HTTP status code {response.status_code}")
    except ConnectionError:
        log_error("Error: Can't connect to server")

    return None


def download_addon(addon: Addon):
    log(f"Downloading '{addon.to_short_string()}.zip'")

    try:
        response = HTTP.get(addon.url, timeout=HTTP_REQUEST_TIMEOUT)
        response.raise_for_status()

        html_parser = BeautifulSoup(response.text, "html.parser")
        a_tag_buttons = html_parser.find_all("a", {"class": "button button--hollow"})

        for a_tag in a_tag_buttons:
            url = a_tag.get("href")
            if url.startswith(f"/wow/addons/{addon.name}/download/"):
                response = HTTP.get(f"{BASE_URL}{url}/file", timeout=HTTP_REQUEST_TIMEOUT)
                response.raise_for_status()

                download_directory = get_download_directory()
                output_zip_file_path = f"{download_directory}/{addon.to_short_string()}.zip"

                with open(output_zip_file_path, "wb") as zip_file:
                    zip_file.write(response.content)
                    return True
    except ReadTimeout:
        log_error(f"Error: HTTP request timed out after {HTTP_REQUEST_TIMEOUT} seconds")
    except HTTPError:
        log_error(f"Error: HTTP status code {response.status_code}")
    except ConnectionError:
        log_error("Error: Can't connect to server")

    return False


def extract_addon(addon: Addon):
    log(f"Extracting '{addon.to_short_string()}.zip'")

    download_directory = get_download_directory()
    output_zip_file_path = f"{download_directory}/{addon.to_short_string()}.zip"

    with zipfile.ZipFile(output_zip_file_path, "r") as zip:
        zip.extractall(download_directory)


def collect_addons():
    config = get_config()
    game_version_string = config["General"]["game_version"]
    game_version = GAME_VERSION_RETAIL if (game_version_string == "retail") else GAME_VERSION_CLASSIC
    addon_names = config["Addons"]

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
    log(f"Download directory: '{get_download_directory()}'")
    addons = collect_addons()
    for addon in addons:
        extract_addon(addon)


if __name__ == "__main__":
    update_addons()
