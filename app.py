import streamlit as st
from web3 import Web3
import json

# Connect to local blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
contract_address = "YOUR_DEPLOYED_CONTRACT_ADDRESS"

# Load contract ABI
with open("FactCheck_abi.json", "r") as f:
    contract_abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=contract_abi)
account = w3.eth.accounts[0]  # For demo; ideally, connect via wallet integration

st.title("Decentralized Fact-Checking Dashboard")

# Section: Submit a new claim
st.header("Submit a New Claim")
claim_text = st.text_input("Claim Text")
evidence = st.text_area("Evidence")
if st.button("Submit Claim"):
    tx = contract.functions.submitClaim(claim_text, evidence).buildTransaction({
        'from': account,
        'nonce': w3.eth.get_transaction_count(account),
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei')
    })
    # For demo, assume account signing is done here (use Ganache key)
    signed_tx = w3.eth.account.sign_transaction(tx, private_key="YOUR_PRIVATE_KEY")
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    st.success(f"Claim submitted! Transaction hash: {tx_hash.hex()}")

# Section: Display claims
st.header("Current Claims")
claim_count = contract.functions.claimCount().call()
for i in range(1, claim_count + 1):
    claim = contract.functions.claims(i).call()
    st.subheader(f"Claim ID: {claim[0]}")
    st.write(f"**Claim:** {claim[1]}")
    st.write(f"**Evidence:** {claim[2]}")
    st.write(f"**NLP Score:** {claim[6]} / 100")
    st.write(f"**Positive Votes:** {claim[3]}, **Negative Votes:** {claim[4]}")
    # Add vote buttons (for simplicity, one vote per refresh)
    if st.button(f"Vote Positive (ID {claim[0]})"):
        tx = contract.functions.voteOnClaim(claim[0], True).buildTransaction({
            'from': account,
            'nonce': w3.eth.get_transaction_count(account),
            'gas': 2000000,
            'gasPrice': w3.toWei('50', 'gwei')
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key="YOUR_PRIVATE_KEY")
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        st.success("Voted Positive!")
    if st.button(f"Vote Negative (ID {claim[0]})"):
        tx = contract.functions.voteOnClaim(claim[0], False).buildTransaction({
            'from': account,
            'nonce': w3.eth.get_transaction_count(account),
            'gas': 2000000,
            'gasPrice': w3.toWei('50', 'gwei')
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key="YOUR_PRIVATE_KEY")
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        st.success("Voted Negative!")
