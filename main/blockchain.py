from web3 import Web3
import json
import os

# Set up connection to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load contract ABI from json file
with open(os.path.join(os.path.dirname(__file__), "voting_abi.json"), "r") as abi_file:
    contract_abi = json.load(abi_file)
# Get all accounts (used for voters)
accounts = web3.eth.accounts
# Smart contract address on Ganache
contract_address = "0x6ee9182bcD5661065A54775e6e4B964988141Ba3"  # Replace with your deployed contract address

# Contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Admin account to interact with the contract
admin_account = web3.eth.accounts[0]

def add_candidate_to_blockchain(candidate_id, candidate_name):
    """Add candidate to the blockchain from the admin panel."""
    tx = contract.functions.addCandidate(candidate_id, candidate_name).transact({'from': admin_account})
    web3.eth.wait_for_transaction_receipt(tx)

def cast_vote_on_blockchain(voter_address, candidate_id):
    """Cast a vote on the blockchain."""
    tx = contract.functions.vote(candidate_id).transact({'from': voter_address})
    web3.eth.wait_for_transaction_receipt(tx)

def get_candidate_votes(candidate_id):
    """Get total votes for a candidate from the blockchain."""
    return contract.functions.getVotes(candidate_id).call()
