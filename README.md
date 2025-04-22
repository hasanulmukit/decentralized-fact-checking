# Decentralized Fact-Checking with NLP and Blockchain

This project implements a decentralized fact-checking system designed to address the biases and transparency issues inherent in centralized fact-checking platforms. Users can submit claims (e.g., news headlines) along with supporting evidence. An NLP model cross-verifies these claims against trusted sources (e.g., scientific papers, WHO reports). Validators in the community vote on the outcomes, and tokenized incentives are issued to reward accurate validations.

---

## Features

- **Decentralized Claims Submission:**  
  Users can submit claims and supporting evidence, which are recorded on a blockchain.

- **NLP-Based Verification:**  
  A fine-tuned NLP model evaluates the claim against trusted evidence sources and assigns a truth score.

- **Community Voting:**  
  Validators can vote on the NLP results, contributing to community consensus.

- **Tokenized Incentives:**  
  Rewards are distributed in the form of tokens to encourage accurate validations.

- **Dashboard Interface:**  
  A Streamlit dashboard for submitting claims, viewing current claims, voting, and monitoring token balances.

## Architecture

1. **Blockchain Network:**  
   - Developed with Solidity smart contracts.
   - Deployed on a local testnet (using Ganache) or a public Ethereum testnet.
   - Manages claim submissions, vote records, and token rewards.

2. **NLP Model:**  
   - Built on pre-trained models like DistilBERT using the Hugging Face Transformers library.
   - Fine-tuned on fact-checking datasets using free resources on Kaggle/Colab.
   - Provides a truth score for each claim.

3. **Backend Listener:**  
   - Python script using web3.py that listens for blockchain events.
   - Triggers NLP inference upon new claim submission and updates the blockchain with the result.

4. **Dashboard:**  
   - Streamlit-based user interface for claim submission, displaying claim status, and voting.
   - Integrates with the blockchain via web3.py.

---

## Technologies Used

- **Blockchain:** Solidity, Ganache, web3.py
- **NLP:** Python, Hugging Face Transformers, Google Colab/Kaggle
- **Dashboard:** Streamlit, VS Code
- **Others:** Python, JSON, REST APIs

---

## Blockchain Setup

- **Smart Contract:** The FactCheck.sol contract manages claim submissions, voting, and rewards. The contract is deployed on Ganache and interacts with our Python scripts using web3.py.
- **Token System:** A simple token reward mechanism is implemented to incentivize validators for accurate votes.
- **Event Handling:** The contract emits a ClaimSubmitted event upon new submissions, which is caught by the backend listener for triggering NLP verification.

---

## Dashboard

- The dashboard (built with Streamlit) includes:

- **Claim Submission Form:** Users submit a claim and evidence.
- **Claim Display:** A list of current claims with NLP truth scores and community votes.
- **Voting Interface:** Validators vote on claims to confirm or dispute NLP outcomes.
- **Token Balance Display:** Shows token balances for each participating address.
