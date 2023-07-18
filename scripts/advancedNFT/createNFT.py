from brownie import advancedNFT, config, network
from scripts.advancedNFT import helpfulScripts, deploy
from web3 import Web3



def createNft(account, nftSC, country):
    tx = nftSC.createNFT("jsonNftURI", {"from": account})
    tx.wait(1)
    return tx
    
def main():
    account = helpfulScripts.getAccount()

    if ("fork" in network.show_active()) :
        nftSC = deploy.deployNftSC()
    else:  
        nftSC = advancedNFT[-1]

    createNft(account, nftSC, "pt")