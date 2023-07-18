from brownie import advancedNFT, config, network
from scripts.advancedNFT import helpfulScripts
from web3 import Web3


def deployNftSC():
    account = helpfulScripts.getAccount()
    
    nftContract = advancedNFT.deploy(
        helpfulScripts.getContractAddress("vrfCoordinator", account),
        helpfulScripts.getContractAddress("subscriptionId", account),
        helpfulScripts.getContractAddress("keyHash", account),
        {'from': account},
    )
    return nftContract

def main():
    deployNftSC()