from brownie import simpleNFT, config, network
from scripts.simpleNFT import helpfulScripts, deploy
from web3 import Web3



def createNft(account, nftSC, country):
    tx = nftSC.createNFT(config["jsonNftURI"][country], {"from": account})
    tx.wait(1)
    return tx
    
def main():
    account = helpfulScripts.getAccount()

    if ("fork" in network.show_active()) :
        nftSC = deploy.deployNftSC()
    else:  
        nftSC = simpleNFT[-1]

    createNft(account, nftSC, "ch")