# Blood Donation Setup & Integration Guide

This guide explains how to configure and run the upgraded Rakthdhaan Blood Donation Management System with Blockchain and Machine Learning integrations.

## 1. Environment Setup

### Install New Dependencies
We have integrated Blockchain via `web3` and Machine Learning via `scikit-learn`.
Open your terminal and run:
```bash
pip install web3 scikit-learn pandas
```

*Note: Make sure to update your `requirements.txt` to include these libraries.*

---

## 2. Blockchain Setup (Ganache)

We use Ganache to simulate a local Ethereum blockchain so you don't have to pay for transactions during development or for your final project demo.

1. **Download and Install Ganache:**
   - Go to [Truffle Suite](https://trufflesuite.com/ganache/) and download the desktop app.
2. **Start Ganache:**
   - Open Ganache and click "Quickstart".
   - This will start a local RPC server on `http://127.0.0.1:7545`.
3. **Deploy the Smart Contract:**
   - Open [Remix IDE](https://remix.ethereum.org/) in your browser.
   - Create a new file, paste the contents of `blockchain/BloodDonation.sol`.
   - Go to the "Solidity Compiler" tab and compile.
   - Go to the "Deploy & Run Transactions" tab. Change Environment to "Ganache Provider" and set URL to `http://127.0.0.1:7545`.
   - Deploy `BloodDonation`.
4. **Update `blockchain_utils.py`:**
   - Copy the deployed contract address from Remix.
   - Open `base/blockchain_utils.py` and replace `CONTRACT_ADDRESS = "0x..."` with your deployed address.
   - Copy one of the Account Address strings and its Private Key (by clicking the key icon in Ganache) and paste them into `SENDER_ADDRESS` and `SENDER_PRIVATE_KEY` respectively in `blockchain_utils.py`.

*Demo Note:* When a hospital accepts a blood donation request in their dashboard, a transaction is securely recorded. Check your Ganache "Transactions" tab to verify the blockchain block was successfully created!

---

## 3. Machine Learning Recommendation System

The ML system uses the **K-Nearest Neighbors (KNN)** algorithm utilizing the Scikit-learn module to recommend top matching donors.

### How it works:
- It processes the existing Django database models (`Donor` and `DonationRequest`).
- It extracts the donor's `location` (encoded to numerical values) and computes `days_since_last_donation`.
- It finds donors matching the exact requested blood group, and then ranks them by mathematical proximity to the requested location and prefers those who haven't donated recently.

### Testing it:
- Log in as a Hospital (or create one).
- Visit the Hospital Dashboard.
- Under the **AI Donor Recommendation** section, select a Blood Group and enter a Location.
- Click "Find Donors". It will seamlessly fetch the ML-processed result via Django JSON endpoints (`/recommend-donors/`) and render the results live on the page.

---

## 4. Running the Application
Once the dependencies are installed and Blockchain credentials are provided, run standard Django commands:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Navigate to your application and the upgraded system is fully functional!
