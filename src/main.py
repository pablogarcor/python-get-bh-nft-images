from web3 import Web3
from dotenv import load_dotenv
import os
import json


load_dotenv()  # take environment variables from .env.


# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
def get_w3_instance():
    provider = os.environ['HTTPS_PROVIDER_URL']
    w3 = Web3(Web3.HTTPProvider(provider))
    return w3


def get_bh_contract_instance(w3_instance):
    contract_address = os.environ['BH_CONTRACT_ADDRESS']
    contract_abi_string = os.getenv('BH_CONTRACT_ABI')
    contract_abi = json.loads(contract_abi_string)
    bh_contract = w3_instance.eth.contract(address=contract_address, abi=contract_abi)
    return bh_contract


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    w3 = get_w3_instance()
    contract=get_bh_contract_instance(w3)
    block=contract.functions.tokenURI(1).call()
    print(f'Hi, {block}')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
