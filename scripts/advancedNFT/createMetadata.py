import os
import requests
import json
from brownie import advancedNFT, network
from metadata import sampleMetadata
from scripts.advancedNFT.helpfulScripts import getCountry
from pathlib import Path


def main():
    nftSC = advancedNFT[-1]
    nNfts = nftSC.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(nNfts)
    )
    writeMetadata(nNfts, nftSC)


def writeMetadata(nNfts, nftSC):
    for nftId in range(nNfts):
        nftMetadata = sampleMetadata.metadataTemplate
        country = getCountry(nftSC.tokenIdMappedToCountry(nftId))
        metadataFileName = (
            "./metadata/"
            + str(nftId)
            + "-"
            + country
            + ".json"
        )
        if Path(metadataFileName).exists():
            print(
                "{} already found, delete it to overwrite!".format(
                    metadataFileName)
            )
        else:
            print("Creating Metadata file: " + metadataFileName)
            nftMetadata["name"] = getCountry(
                nftSC.tokenIdMappedToCountry(nftId)
            )
            nftMetadata["description"] = "The flag of {}!".format(
                nftMetadata["name"]
            )
            imageToUpload = None
            imagePath = "./img/{}.jpg".format(
                country.lower().replace('_', '-'))
            imageToUpload = uploadToIpfs(imagePath)
            
            nftMetadata["image"] = imageToUpload
            with open(metadataFileName, "w") as file:
                json.dump(nftMetadata, file)
            uploadToIpfs(metadataFileName)


def uploadToIpfs(filePath):
    with Path(filePath).open("rb") as fp:
        imageBinary = fp.read()
        ipfsUrl = (
            os.getenv("IPFS_URL")
            if os.getenv("IPFS_URL")
            else "http://localhost:5001"
        )
        response = requests.post(ipfsUrl + "/api/v0/add",
                                 files={"file": imageBinary})
        ipfsHash = response.json()["Hash"]
        fileName = filePath.split("/")[-1:][0]
        imageUri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfsHash, fileName)
        print(imageUri)
    return imageUri