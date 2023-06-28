from brownie import simpleNFT, config, network
from scripts import helpfulScripts
from web3 import Web3


def deployNftSC():
    account = helpfulScripts.getAccount()
    
    nftContract = simpleNFT.deploy(
        {'from': account},
    )
    return nftContract

def main():
    deployNftSC()