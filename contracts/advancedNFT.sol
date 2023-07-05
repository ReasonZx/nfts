// contracts/MyNFT.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";



contract advancedNFT is ERC721URIStorage, VRFConsumerBase {

    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Country{DE, PT, CH}
    mapping(uint256 => Country) tokenIdMappedToCountry;
    mapping(bytes32 => address) requestIdMappedToSender;
    event requestedNFT(bytes32 indexed requestId, address requester);
    event countryAssigned(uint256 indexed tokenId, Country country);

    constructor(address _vrfCoordinator, address _linkToken, uint256 _fee, bytes32 _keyhash) public 
    VRFConsumerBase(_vrfCoordinator, _linkToken)
    ERC721("Flags", "FLAG") {
        tokenCounter    = 0;
        keyhash         = _keyhash;
        fee             = _fee;
    }


    function createNFT(string memory tokenURI) public returns (bytes32){
        bytes32 requestId = requestRandomness(keyhash,fee);
        requestIdMappedToSender[requestId] = msg.sender;
        emit requestedNFT(requestId, msg.sender);
    }

    function fulfillRandomness(bytes requestId, uint256 randomNumber) internal override {
        uint256 newTokenId = tokenCounter;
        Country country = Country(randomNumber % 3);
        tokenIdMappedToCountry[newTokenId] = country;
        emit countryAssigned(newTokenId, country);

        address owner = requestIdMappedToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter++;

    }

    function setTokenURI(uint256 tokenId, string _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not owner nor approved.");
        _setTokenURI(tokenId, _tokenURI);
    }

}