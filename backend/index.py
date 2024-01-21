from web3 import Web3
import multiprocessing
import smtplib
from email.mime.text import MIMEText
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment Variables
infura_project_id = os.getenv('INFURA_PROJECT_ID')
gmail_user = os.getenv('GMAIL_USER')
gmail_password = os.getenv('GMAIL_PASSWORD')
recipient_email = os.getenv('RECIPIENT_EMAIL')
token_contract_address = os.getenv('TOKEN_CONTRACT_ADDRESS')
token_contract_abi = os.getenv('TOKEN_CONTRACT_ABI')

# Initialize Web3 and Contract
ethereum_node_endpoint = f'https://mainnet.infura.io/v3/{infura_project_id}'
w3 = Web3(Web3.HTTPProvider(ethereum_node_endpoint))
contract = w3.eth.contract(address=token_contract_address, abi=token_contract_abi)

def send_email(subject, body, to_email):
    # Google SMTP
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = to_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, msg.as_string())
        server.close()
        print('Email sent!')
    except Exception as e:
        print('Failed to send email:', e)
        # fallback SMTP here

def monitor_transfers():
    transfer_filter = contract.events.Transfer.createFilter(fromBlock='latest')
    while True:
        for event in transfer_filter.get_new_entries():
            if event.args.to == '0x0000000000000000000000000000000000000000':
                send_email("Transfer Detected", str(event), recipient_email)
        time.sleep(10)

# Load balance by using Multiprocessing
if __name__ == "__main__":
    # Using multiprocessing for load balancing
    p = multiprocessing.Process(target=monitor_transfers)
    p.start()
    p.join()
