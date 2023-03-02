
from web3 import Web3
import json
from web3.providers.rpc import HTTPProvider
import asyncio


contractAddress = '0x24506584c6e294982213aD56f774edA62462bB04'
address2 = Web3.toChecksumAddress(contractAddress)

PROVIDER = "wss://polygon-mainnet.g.alchemy.com/v2/_tn9X7pFnXwYXYi8Q33gQjRg_B3Dey_4"
web3 = Web3(Web3.WebsocketProvider(PROVIDER))

import json
abi = 1
with open("./artifacts/InferenceManager.json", "r") as f:
    abi = json.load(f)
    abi = abi["abi"]

fContract = web3.eth.contract(abi=abi,address=address2)


# define function to handle events and print to the console
def handle_event(event):
    print(Web3.toJSON(event))
    # and whatever


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main_loop():
    
    event_filter = fContract.events.RequestRecieved.createFilter(fromBlock='latest')
    #block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()

