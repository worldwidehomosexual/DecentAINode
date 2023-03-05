import os
from contract import fContract
from chain import handle_event, web3, Web3

# from web3 import Web3
# import json
# from web3.providers.rpc import HTTPProvider
# from web3.middleware import geth_poa_middleware

# PROVIDER = "wss://polygon-mainnet.g.alchemy.com/v2/_tn9X7pFnXwYXYi8Q33gQjRg_B3Dey_4"
# web3 = Web3(Web3.WebsocketProvider(PROVIDER))
# web3.middleware_onion.inject(geth_poa_middleware, layer=0)


def register_on_contract(cost):
    
    # Get account
    web3.eth.account.enable_unaudited_hdwallet_features()
    mnemonic = ""
    with open('mnemonic.txt') as f:
        lines = f.readlines()
        mnemonic = lines[0]
    account = web3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/60'/0'/0/0")
    
    # Send call to register on contract
    chain_id = web3.eth.chain_id
    tx = fContract.functions.registerResponder(cost, "").buildTransaction({
        "chainId": chain_id,
        'nonce': web3.eth.getTransactionCount(account.address),
        'from': account.address
    })
    print(tx)
    signed_tx = web3.eth.account.signTransaction(tx, private_key=account.key)

    sentTx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    
    # Send call to fetch all past events from contract with 0x in responder field
    event_filter = fContract.events.RequestRecieved.createFilter(fromBlock='1401055', argument_filters={'responder':"0x0000000000000000000000000000000000000000"})
    
    # Select random 10 and send to model_runner
    count = 0
    for PairCreated in event_filter.get_all_entries():
        print("Sending to model_runner")
        handle_event(PairCreated)
        count += 1
        if count == 10:
            break
