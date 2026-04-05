import json
from web3 import Web3

# Connect to local Ganache RPC
# Setup Ganache on 127.0.0.1:7545
rpc_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(rpc_url))

# --- REPLACE THESE WITH YOUR ACTUAL VALUES ONCE DEPLOYED IN GANACHE ---
# 1. Provide the deployed contract address
CONTRACT_ADDRESS = "0x..." # Fill this after deploying via compiled tools/Remix/truffle
# 2. Provide the Ganache account address you want to use to send transactions
SENDER_ADDRESS = "0x..." 
SENDER_PRIVATE_KEY = "..." 
# ----------------------------------------------------------------------

# The ABI generated from BloodDonation.sol
CONTRACT_ABI = json.loads("""
[
	{
		"anonymous": false,
		"inputs": [
			{"indexed": false, "internalType": "string", "name": "donorId", "type": "string"},
			{"indexed": false, "internalType": "string", "name": "bloodGroup", "type": "string"},
			{"indexed": false, "internalType": "string", "name": "donationDate", "type": "string"},
			{"indexed": false, "internalType": "string", "name": "hospitalName", "type": "string"},
			{"indexed": false, "internalType": "string", "name": "verificationStatus", "type": "string"}
		],
		"name": "RecordAdded",
		"type": "event"
	},
	{
		"inputs": [
			{"internalType": "string", "name": "_donorId", "type": "string"},
			{"internalType": "string", "name": "_bloodGroup", "type": "string"},
			{"internalType": "string", "name": "_donationDate", "type": "string"},
			{"internalType": "string", "name": "_hospitalName", "type": "string"},
			{"internalType": "string", "name": "_verificationStatus", "type": "string"}
		],
		"name": "addDonationRecord",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [{"internalType": "uint250", "name": "index", "type": "uint256"}],
		"name": "getRecord",
		"outputs": [
			{"internalType": "string", "name": "donorId", "type": "string"},
			{"internalType": "string", "name": "bloodGroup", "type": "string"},
			{"internalType": "string", "name": "donationDate", "type": "string"},
			{"internalType": "string", "name": "hospitalName", "type": "string"},
			{"internalType": "string", "name": "verificationStatus", "type": "string"}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getRecordsCount",
		"outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
		"name": "records",
		"outputs": [
			{"internalType": "string", "name": "donorId", "type": "string"},
			{"internalType": "string", "name": "bloodGroup", "type": "string"},
			{"internalType": "string", "name": "donationDate", "type": "string"},
			{"internalType": "string", "name": "hospitalName", "type": "string"},
			{"internalType": "string", "name": "verificationStatus", "type": "string"}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
""")

def log_donation_to_blockchain(donor_id, blood_group, donation_date, hospital_name, verification_status):
    """
    Records a completed/verified donation onto the Ethereum blockchain via Ganache.
    Note: Ensure Ganache is running and the contract is deployed. 
    If not, this function will silently print to console to prevent crashing the Django app during dev.
    """
    if not w3.is_connected() or CONTRACT_ADDRESS == "0x...":
        print("Blockchain Warning: Web3 is not connected or Contract Address is not set. Skipping blockchain log.")
        return None

    try:
        contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)
        
        # Build the transaction
        transaction = contract.functions.addDonationRecord(
            str(donor_id),
            str(blood_group),
            str(donation_date),
            str(hospital_name),
            str(verification_status)
        ).build_transaction({
            'from': SENDER_ADDRESS,
            'nonce': w3.eth.get_transaction_count(SENDER_ADDRESS),
            'gas': 2000000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })

        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=SENDER_PRIVATE_KEY)

        # Send the signed transaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        print(f"[BLOCKCHAIN SUCCESS] Transaction hash: {w3.to_hex(tx_hash)}")
        return w3.to_hex(tx_hash)

    except Exception as e:
        print(f"[BLOCKCHAIN ERROR] {e}")
        return None

