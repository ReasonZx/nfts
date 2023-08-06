import requests
from brownie import config
from pathlib import Path

PINATA_BASE_URL = 'https://api.pinata.cloud/'
endpoint = 'pinning/pinFileToIPFS'
# Change this to upload a different file
filepath = './metadata/3-CH.json'
filename = filepath.split('/')[-1:][0]
headers = {'pinata_api_key': config["pinata"]["key"],
           'pinata_secret_api_key': config["pinata"]["secret"]}


def main():
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())

if __name__ == "__main__":
    main()