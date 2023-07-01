# Nfts

Smart Contract example deployed @ **0x5e76df22686883e0649c61d89891310814c2bd9b** on Eth Testnet - **Sepolia**

OpenSea link for NFTs:
https://testnets.opensea.io/collection/flags-10

(metadata might be outdated though)

# Deploy

## Testnet
To deploy on a testnet, get your keys for that testnet and the project id from infura.io.

For example Sepolia testnet:
```
$export PUBLIC_KEY="your_public_key"
$export PRIVATE_KEY="your_private_key"
$export WEB3_INFURA_PROJECT_ID="your_infura_project_id"
```
```
$brownie run scripts/deploy.py --network sepolia
```

# Mint NFTs
- Edit the metadata in [](./json) with the details for the NFT you want to create
- Store the json somewhere on the internet (preferably ona decentralized platform)
- Add the link to the json on [](./brownie-config.yaml)
- Edit last line of [](./scripts/createNFT.py) to contain the new country

## Testnet
Run:
```
$brownie run scripts/createNFT.py --network sepolia
```
