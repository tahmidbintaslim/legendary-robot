import redis
import json
from web3 import Web3
import multiprocessing
import smtplib
from email.mime.text import MIMEText
import os
import time
from dotenv import load_dotenv
import logging


# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Load environment variables
load_dotenv()

# Environment Variables
infura_project_id = os.getenv('INFURA_PROJECT_ID')
gmail_user = os.getenv('GMAIL_USER')
gmail_password = os.getenv('GMAIL_PASSWORD')
recipient_email = os.getenv('RECIPIENT_EMAIL')
token_contract_address = os.getenv('TOKEN_CONTRACT_ADDRESS')
token_contract_abi = os.getenv('TOKEN_CONTRACT_ABI')

# Initialize Web3
ethereum_node_endpoint = f'https://mainnet.infura.io/v3/{infura_project_id}'
try:
    w3 = Web3(Web3.HTTPProvider(ethereum_node_endpoint))
    if not w3.is_connected():
        logging.error("Failed to connect to Ethereum node.")
        exit(1)
except Exception as e:
    logging.error(f"Error connecting to Ethereum node: {e}")
    exit(1)

except Exception as e:
    logging.error(f"Error connecting to Ethereum node: {e}")
    exit(1)

# Convert address to checksum format
try:
    checksum_address = Web3.to_checksum_address(token_contract_address)
except Exception as e:
    logging.error(f"Invalid contract address: {e}")
    exit(1)

# Initialize Contract with checksum address
try:
    contract = w3.eth.contract(address=checksum_address, abi=token_contract_abi)
except Exception as e:
    logging.error(f"Error initializing contract: {e}")
    exit(1)
    
def serialize_event(event):
    # Convert HexBytes to string and other conversions as needed
    event_dict = {
        'args': {k: str(v) for k, v in event['args'].items()},
        'event': event['event'],
        'logIndex': event['logIndex'],
        'transactionIndex': event['transactionIndex'],
        'transactionHash': event['transactionHash'].hex(),
        'address': event['address'],
        'blockHash': event['blockHash'].hex(),
        'blockNumber': event['blockNumber']
    }
    return json.dumps(event_dict)

def send_email(subject, body, to_email):
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
        logging.info('Email sent!')
    except Exception as e:
        logging.error(f'Failed to send email: {e}')
        # Fallback SMTP can be implemented here

def monitor_transfers():
    logging.info("Starting transfer monitoring...")
    try:
        transfer_filter = contract.events.Transfer.create_filter(fromBlock='latest')
        while True:
            new_entries = transfer_filter.get_new_entries()
            if new_entries:  # Check if there are new entries
                logging.info(f"New entries detected: {len(new_entries)}")
            for event in new_entries:
                logging.info(f"Detected event: {event}")
                # Write event to Redis
                event_json = serialize_event(event)  # Serialize event to JSON
                redis_client.lpush('events', event_json)
                redis_client.ltrim('events', 0, 99)  # Keep only the latest 100 events
                if event.args.to == '0x0000000000000000000000000000000000000000':
                    send_email("Transfer Detected", str(event), recipient_email)
            time.sleep(10)
    except Exception as e:
        logging.error(f'Error in transfer monitoring: {e}')

if __name__ == "__main__":
    logging.info("Starting backend service...")
    p = multiprocessing.Process(target=monitor_transfers)
    p.start()
    p.join()
