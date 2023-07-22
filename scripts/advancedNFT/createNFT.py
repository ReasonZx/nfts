from brownie import advancedNFT, config, network
from scripts.advancedNFT import helpfulScripts, deploy
from web3 import Web3
import time



def createNft(account, nftSC):
    nftSC = advancedNFT[len(advancedNFT) - 1]
    tx = nftSC.createNFT("None", {"from": account})
    tx.wait(1)
    print("Waiting on randomWords VRFCoordinator fullfillment...")
    event = helpfulScripts.listenForEvent(
        nftSC, "countryAssigned", timeout=120, pollInterval=5
    )
    tokenId = event.args.tokenId
    countryId = event.args.country
    country = helpfulScripts.getCountry(countryId)

    print("Country of tokenId {} is {}".format(tokenId, country))
    return tx



def main():
    account = helpfulScripts.getAccount()

    if ("fork" in network.show_active()) :
        nftSC = deploy.deployNftSC()
    else:  
        nftSC = advancedNFT[-1]

    createNft(account, nftSC)