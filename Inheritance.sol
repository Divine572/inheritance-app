// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;


contract Inheritance {

    address public owner;
    mapping(address => uint256) public inheritances;
    mapping(address => bool) public isBeneficiary;

    event InheritanceReceived(address indexed from, uint256 amount);
    event BeneficiaryAdded(address indexed beneficiary);
    event BeneficiaryRemoved(address indexed beneficiary);
    event InheritanceDistributed(address indexed beneficiary, uint256 amount);


    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    function addBeneficiary(address beneficiary) public onlyOwner {
        isBeneficiary[beneficiary] = true;
        emit BeneficiaryAdded(beneficiary);
    }

    function removeBeneficiary(address beneficiary) public onlyOwner {
        isBeneficiary[beneficiary] = false;
        emit BeneficiaryRemoved(beneficiary);
    }

    function receiveInheritance() public payable {
        require(msg.value > 0, "Amount must be greater than zero");

        inheritances[msg.sender] += msg.value;
        emit InheritanceReceived(msg.sender, msg.value);
    }

    function distributeInheritance(address beneficiary, uint256 amount) public onlyOwner {
        require(isBeneficiary[beneficiary], "Not a valid beneficiary.");
        require(amount > 0, "Amount must be greater than zero.");
        require(amount <= inheritances[owner], "Insufficient balance.");

        inheritances[owner] -= amount;
        inheritances[beneficiary] += amount;

        emit InheritanceDistributed(beneficiary, amount);
    }



}