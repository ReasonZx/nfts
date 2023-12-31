// contracts/MyNFT.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
// import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";




contract advancedNFT is VRFConsumerBaseV2, ERC721URIStorage {

    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint64 subscriptionId;
    VRFCoordinatorV2Interface COORDINATOR;
    enum Country{DE, PT, CH}
    mapping(uint256 => Country) public tokenIdMappedToCountry;
    mapping(uint256 => address) public requestIdMappedToSender;
    mapping(uint256 => uint256) public requestIdToTokenId;
    mapping(uint256 => string) public requestIdToTokenURI;
    event requestedNFT(uint256 indexed requestId, address requester);
    event countryAssigned(uint256 indexed tokenId, Country country);

    constructor(address _vrfCoordinator, uint64 _subscriptionId, bytes32 _keyhash) 
    VRFConsumerBaseV2(_vrfCoordinator)
    ERC721("Flags", "FLAG") {
        tokenCounter    = 0;
        keyhash         = _keyhash;
        COORDINATOR = VRFCoordinatorV2Interface(_vrfCoordinator);
        subscriptionId = _subscriptionId;
    }
    



    function createNFT(string memory tokenURI) public returns (uint256){
        uint256 requestId = COORDINATOR.requestRandomWords(keyhash, subscriptionId, 3, 1000000, 1);
        requestIdMappedToSender[requestId] = msg.sender;
        requestIdToTokenURI[requestId] = tokenURI;
        emit requestedNFT(requestId, msg.sender);
    }

    function fulfillRandomWords(uint256 requestId, uint256[] memory randomNumber) internal override {
        uint256 newTokenId = tokenCounter;
        string memory tokenURI = requestIdToTokenURI[requestId];
        address owner = requestIdMappedToSender[requestId];

        _safeMint(owner, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        Country country = Country(randomNumber[0] % 3);
        tokenIdMappedToCountry[newTokenId] = country;
        requestIdToTokenId[requestId] = newTokenId;
        emit countryAssigned(newTokenId, country);

        
        tokenCounter++;

    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not owner nor approved.");
        _setTokenURI(tokenId, _tokenURI);
    }

}