from web3 import Web3
import json
import time

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
contract_address = "YOUR_DEPLOYED_CONTRACT_ADDRESS"

# Load the contract ABI (exported from Remix)
with open("FactCheck_abi.json", "r") as f:
    contract_abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Your account details
account = w3.eth.accounts[0]

def handle_event(event):
    claim_id = event['args']['id']
    claim_text = event['args']['claimText']
    evidence = event['args']['evidence']
    print(f"New claim detected (ID: {claim_id}): {claim_text}")

    # Run NLP inference (import your function)
    from your_nlp_module import get_fact_check_score
    score = get_fact_check_score(claim_text, evidence)
    print(f"NLP score: {score:.2f}")

    # Update the blockchain with the NLP score
    tx = contract.functions.setNlpScore(claim_id, int(score)).buildTransaction({
        'from': account,
        'nonce': w3.eth.get_transaction_count(account),
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei')
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key="YOUR_PRIVATE_KEY")
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Updated claim {claim_id} with NLP score {score:.2f}")

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)

# Create event filter for ClaimSubmitted events
event_filter = contract.events.ClaimSubmitted.createFilter(fromBlock='latest')

# Start listening
log_loop(event_filter, 2)
