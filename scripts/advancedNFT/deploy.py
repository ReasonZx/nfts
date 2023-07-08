from brownie import advancedNFT, config, network
from scripts.advancedNFT import helpfulScripts
from web3 import Web3


def deployNftSC():
    account = helpfulScripts.getAccount()
    
    nftContract = advancedNFT.deploy(
        helpfulScripts.getContractAddress("vrfCoordinator", account),
        helpfulScripts.getContractAddress("link", account),
        helpfulScripts.getContractAddress("fee", account),
        helpfulScripts.getContractAddress("keyHash", account),
        {'from': account},
    )
    helpfulScripts.fundSC(nftContract, account,"link", _ammount = 100000000000000000) #0.1
    return nftContract

def main():
    deployNftSC()