# Nfts

Smart Contract example for simpleNFT deployed @ **0x5e76df22686883e0649c61d89891310814c2bd9b** on Eth Testnet - **Sepolia**

Smart Contract example for advancedNFT deployed @ **0x0226baCB371bf7228167F8F4A8dA5260F5AB9E60** on Eth Testnet - **Sepolia**

.

OpenSea link for simpleNFTs:
https://testnets.opensea.io/collection/flags-10

OpenSea link for advancedNFTs:
https://testnets.opensea.io/collection/flags-14

(metadata might be outdated though)

# Deploy

## Testnet
To deploy on a testnet, get your keys for that testnet and the project id from infura.io.

For example Sepolia testnet:
```
$export PUBLIC_KEY="your_public_key"
$export PRIVATE_KEY="your_private_key"
$export WEB3_INFURA_PROJECT_ID="your_infura_project_id"
$brownie networks add Ethereum sepolia host="https://sepolia.infura.io/v3/46213ad1bb2845c5"your_infura_project_id" chainid=11155111
$export PINATA_API_KEY="your_pinata_api_key"
$export PINATA_API_SECRET="your_pinata_secret_key"
```
Then deploy the smart contract:
```
$brownie run scripts/simpleNFT/deploy.py --network sepolia
$brownie run scripts/advancedNFT/deploy.py --network sepolia
```

# Mint NFTs

## simpleNFT
- Edit the metadata in [](./json) with the details for the NFT you want to create
- Store the json somewhere on the internet (preferably ona decentralized platform)
- Add the link to the json on [](./brownie-config.yaml)
- Edit last line of [](./scripts/simpleNFT/createNFT.py) to contain the new country
Run:
```
$brownie run scripts/simpleNFT/createNFT.py --network sepolia
```

## advancedNFT
Run the script createNFT and a random NFT from the 3 countries list will be created. Create as many as wanted.
```
$brownie run scripts/advancedNFT/createNFT.py --network sepolia
```
Once all the NFTs are created, then you have 2 options:
1. Run your own IPFS node, create the Metadata for each of the NFTs and upload it to IPFS. (Metadata will only be available when you are running the node)
2. Create the Metadata for each NFT and then upload it to Pinata.

For option 1, simply run your ipfs node and then run the createMetadata script.
```
$ipfs daemon
$brownie run scripts/advancedNFT/createMetadata.py --network sepolia
```
For option 2, run the createMetadata script and then upload to pinata the metadata of each type of NFT (by modifying the 8th line - filePath - of the uploadToPinata.py script).
```
$brownie run scripts/advancedNFT/createMetadata.py --network sepolia
Then repeat the following step for each type of NFT
$brownie run scripts/advancedNFT/uploadToPinata.py
```

# Add the metadata to the NFTs

## advancedNFT

Edit the "countryMetadataDic" dictionary that is in the setNFTuri.py script in order to have the URI that you created on the previous step.
For the option 1, the URI was printed on the console when running the createMeatadata script. (But you can also get the the URI by visiting the data that was stored on your ipfs node)
For option 2, the URI should look like this "https://ipfs.io/ipfs/YOUR_TOKEN?filename=YOUR_FILE.json", where you can get YOUR_TOKEN for each NFT on your pinata account and YOUR_FILE is the name of each .json that was uploaded.

Once the dictionary is updated with the URI of each type of NFT then run:

```
$brownie run scripts/advancedNFT/setNFTuri.py --network sepolia
```

