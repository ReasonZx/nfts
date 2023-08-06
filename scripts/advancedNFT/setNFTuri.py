#!/usr/bin/python3
from brownie import advancedNFT, accounts, network, config
from metadata import sampleMetadata
from scripts.advancedNFT.helpfulScripts import getCountry, OPENSEA_FORMAT



countryMetadataDic = {
    "DE": "https://ipfs.io/ipfs/QmbAWDjLhkyj7AEwp5wGRZnSPm6UT72FpnNj3Ymt9NZndG?filename=2-DE.json",
    "PT": "https://ipfs.io/ipfs/QmYzQTJxR9nvdCscm8QpgUxc9Lzbna5LhXA6YrsGh5a8Zn?filename=0-PT.json",
    "CH": "https://ipfs.io/ipfs/QmPtmo2N87f9F5f1RfKJct6yXmHzYfW19AkqN54QtF4jRy?filename=3-CH.json",
}

def main():
    print("Working on " + network.show_active())
    advancedNftSC = advancedNFT[len(advancedNFT) - 1]
    nAdvancedNFTs = advancedNftSC.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(nAdvancedNFTs)
    )
    for tokenId in range(nAdvancedNFTs):
        country = getCountry(advancedNftSC.tokenIdMappedToCountry(tokenId))
        if not advancedNftSC.tokenURI(tokenId).startswith("https://"):
            print("Setting tokenURI of {}".format(tokenId))
            setTokenURI(tokenId, advancedNftSC,
                         countryMetadataDic[country])
        else:
            print("Skipping {}, we already set that tokenURI!".format(tokenId))


def setTokenURI(tokenId, advancedNftSC, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    advancedNftSC.setTokenURI(tokenId, tokenURI, {"from": dev})
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(advancedNftSC.address, tokenId)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')