from brownie import (accounts, network, config, Contract, LinkToken, web3)
import time

contractList = {
    "link": LinkToken
}

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

def getAccount():
    if network.show_active() == "development" or ("fork" in network.show_active()):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def getContractAddress(_contractName, _account=None):
    if network.show_active() == "development":
        mockAggregator = MockV3Aggregator.deploy(18, 2000000000000000000000, {"from": _account})
        return mockAggregator.address
    else:
        return config["networks"][network.show_active()][_contractName]


def getContract(_contractName, _account=None):
    SCaddress = getContractAddress(_contractName, _account)
    if network.show_active() == "development":
        print("Functionality not available in development network. Use testnet or local fork.")
        exit()
    elif(_contractName not in contractList):
        print("Using LINK as default Token to fund contract")
        contract = Contract.from_abi(LinkToken.name, SCaddress, LinkToken.abi)
    else:
        contract = Contract.from_abi(contractList[_contractName]._name, SCaddress, contractList[_contractName].abi)
    
    return contract 


def fundSC (_SCadress, _account=None, _tokenName=None, _ammount = 100000000000000000):      #0.1
    if(not _account):
        _account = getAccount()

    if((not _tokenName) or (_tokenName not in contractList)):
        print("Using LINK as default Token to fund contract")
        tokenSC = getContract("link")
    else :
        tokenSC = getContract(_tokenName)

    tx = tokenSC.transfer(_SCadress, _ammount, {"from": _account})
    tx.wait(1)
    
    print("Contracted funded!")
    return tx


def getCountry(countryNumber):
    switch = {0: "DE", 1: "PT", 2: "CH"}
    return switch[countryNumber]


def listenForEvent(brownieContract, event, timeout=500, pollInterval=5):
    #Blocking function to wait for a SC event (polling it)
    web3Contract = web3.eth.contract(
        address=brownieContract.address, abi=brownieContract.abi
    )
    startTime = time.time()
    currentTime = time.time()
    eventFilter = web3Contract.events[event].createFilter(fromBlock="latest")
    while currentTime - startTime < timeout:
        for eventResponse in eventFilter.get_new_entries():
            if event in eventResponse.event:
                print("Found event!")
                return eventResponse
        time.sleep(pollInterval)
        currentTime = time.time()
    print("Timeout reached, no event found.")
    return {"event": None}