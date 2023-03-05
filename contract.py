
from web3 import Web3
import json
from web3.providers.rpc import HTTPProvider
from web3.middleware import geth_poa_middleware
import asyncio


contractAddress = '0x7C14dd39c29a22E69b99E41f7A3E607bfb63d244'
address2 = Web3.toChecksumAddress(contractAddress)

PROVIDER = "wss://polygon-mainnet.g.alchemy.com/v2/_tn9X7pFnXwYXYi8Q33gQjRg_B3Dey_4"
web3 = Web3(Web3.WebsocketProvider(PROVIDER))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

import json
abi = 1
with open("./artifacts/InferenceManager.json", "r") as f:
    abi = json.load(f)
    abi = abi["abi"]

fContract = web3.eth.contract(abi=abi,address=address2)
