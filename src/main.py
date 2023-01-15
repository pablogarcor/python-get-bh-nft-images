from web3 import Web3
from dotenv import load_dotenv
import os
import json
import aiohttp
import random
import asyncio

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


async def get_bh(session, url):
    async with session.get(url) as resp:
        bh_metadata = await resp.json()
        return {'tokenId': bh_metadata['tokenId'], 'image': bh_metadata['image']}


async def write_image_url_to_file():
    async with aiohttp.ClientSession() as session:

        tasks = []
        # 10k iterations to get 10k based heads
        for number in range(1, 10000 + 1):
            url = f'https://drops.api.topdogstudios.io/basedAf/token/{number}'
            tasks.append(asyncio.ensure_future(get_bh(session, url)))

        all_bh = await asyncio.gather(*tasks)
        with open('bh_list.txt', 'w') as bh_file:
            for bh in all_bh:
                json.dump(bh, bh_file)
                bh_file.write("\n")


# asyncio.run(write_image_url_to_file())

async def get_bh_image(session, url, token_id):
    ipfs_provider_list = ['gateway.pinata.cloud', 'cloudflare-ipfs.com', 'cf-ipfs.com', 'ipfs.joaoleitao.org',
                          'ipfs-gateway.cloud', 'ipfs.sloppyta.co', 'via0.com', 'ipfs.eth.aragon.network',
                          'ipfs.litnet.work', 'ipfs.runfission.com', '4everland.io', 'nftstorage.link',
                          'w3s.link', 'hub.textile.io', 'ipfs.jpu.jp', 'ipfs.io']
    random_provider = random.choice(ipfs_provider_list)
    url.replace('ipfs.io', random_provider)
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                bh_image = await resp.read()
                with open(f'img/bh_{token_id}.png', 'wb') as bh_image_file:
                    bh_image_file.write(bh_image)
                    print(f'imagen del token nº {token_id}--> DESCARGADA\n')
            else:
                print(f'imagen del token nº {token_id}--> ERROR\nProvider--> {random_provider}')
                await get_bh_image(session, url, token_id)

    except Exception:
        print(f'imagen del token nº {token_id}--> ERROR\nProvider--> {random_provider}')
        await get_bh_image(session, url, token_id)


async def save_images():
    file_list = os.listdir('img')
    downloaded_token_id_list = []
    for file_name in file_list:
        name_withour_bh_list = file_name.split('bh_')
        token_id_list = name_withour_bh_list[1].split('.png')
        downloaded_token_id_list.append(int(token_id_list[0]))
    async with aiohttp.ClientSession() as session:
        tasks = []
        with open('bh_list.txt', 'r') as bh_file:
            lines = bh_file.readlines()
            for line in lines:
                json_line = json.loads(line)
                image_url = json_line['image']
                token_id = json_line['tokenId']
                if token_id not in downloaded_token_id_list:
                    tasks.append(asyncio.ensure_future(get_bh_image(session, image_url, token_id)))

            await asyncio.gather(*tasks)


asyncio.run(save_images())

#if __name__ == '__main__':
#    file_list = os.listdir('img')
#    downloaded_token_id_list = []
#    counter = 0
#    for file_name in file_list:
#        name_withour_bh_list = file_name.split('bh_')
#        token_id_list = name_withour_bh_list[1].split('.png')
#        downloaded_token_id_list.append(int(token_id_list[0]))
#        counter += 1
#
#    print(downloaded_token_id_list)
#    is_on_list = 9972 not in downloaded_token_id_list
#    print(counter)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
