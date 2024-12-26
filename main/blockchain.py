from web3 import Web3
import json
import os
from .models import Candidate
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
    # Check if the candidate already exists on the blockchain
    try:
        # Check if candidate already exists on blockchain
        existing_candidate = contract.functions.candidates(candidate_id).call()
        if existing_candidate[0] != 0:
            print(f"Candidate {candidate_name} already exists on the blockchain.")
            return None

        # If candidate doesn't exist, add to blockchain
        tx = contract.functions.addCandidate(candidate_id, candidate_name).transact({'from': admin_account})
        receipt = web3.eth.wait_for_transaction_receipt(tx)

        if receipt['status'] == 1:
            print(f"Candidate {candidate_name} added successfully.")
        else:
            print(f"Transaction failed.")

        return receipt
    except Exception as e:
        print(f"Error adding candidate: {e}")
        return None

def cast_vote_on_blockchain(voter_address, candidate_id):
    """Cast a vote on the blockchain."""
    tx = contract.functions.vote(candidate_id).transact({'from': voter_address})
    web3.eth.wait_for_transaction_receipt(tx)

def get_candidate_votes(candidate_id):
    """Get total votes for a candidate from the blockchain."""
    try:
        votes = contract.functions.getVotes(candidate_id).call()
        return votes
    except Exception as e:
        print(f"Error fetching votes for candidate {candidate_id}: {str(e)}")
        return 0  # Return 0 votes in case of an error
def sync_candidates_to_blockchain(candidate_id, candidate_name):
    """Sync candidates from the database to the blockchain."""
    # Add the logic to add the candidate to the blockchain
    try:
        # Check if candidate already exists on blockchain
        existing_candidate = contract.functions.candidates(candidate_id).call()
        if existing_candidate[0] != 0:
            print(f"Candidate {candidate_name} already exists on the blockchain.")
            return None

        # If candidate doesn't exist, add to blockchain
        tx = contract.functions.addCandidate(candidate_id, candidate_name).transact({'from': admin_account})
        receipt = web3.eth.wait_for_transaction_receipt(tx)

        if receipt['status'] == 1:
            print(f"Candidate {candidate_name} added successfully.")
        else:
            print(f"Transaction failed.")

        return receipt
    except Exception as e:
        print(f"Error adding candidate: {e}")
        return None