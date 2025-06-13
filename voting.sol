// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    struct Candidate {
        uint256 id;
        uint256 voteCount;
        string name;
    }

    mapping(uint256 => Candidate) public candidates;
    mapping(address => bool) public hasVoted;

    event VoteCasted(address indexed voter, uint256 indexed candidateId);

    function vote(uint256 candidateId) public {
        require(!hasVoted[msg.sender], "You have already voted.");
        require(candidates[candidateId].id == candidateId, "Invalid candidate.");

        candidates[candidateId].voteCount += 1;
        hasVoted[msg.sender] = true;

        emit VoteCasted(msg.sender, candidateId);
    }

    function addCandidate(uint256 candidateId, string memory name) public {
        require(candidates[candidateId].id == 0, "Candidate already exists.");
        candidates[candidateId] = Candidate(candidateId, 0, name);
    }

    function getVotes(uint256 candidateId) public view returns (uint256) {
        return candidates[candidateId].voteCount;
    }
}
