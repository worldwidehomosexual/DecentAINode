import click
import pyperclip
# from app import application
from web3 import Web3
import os

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command()
@click.option('-l', '--length', type=int, help='Length of password to be generated')
@click.option('-o', '--option', type=click.Choice(['1', '2', '3', '4']), default = '4',
    help='''Options\n
    1 - alphabetic lowercase\n
    2 - alphabetic both cases\n
    3 - alphanumeric\n
    4 - alphanumeric + special characters'''
)
def generate(length, option):
    click.echo(length)
    click.echo(option)
    """generates a random password of length and type"""
    logo = """
    +-----------------------------+
    | Thank you for using Ranpass |
    +-----------------------------+
    """
    # generate random password
    password = "cool" # application.generate(int(length), int(option))

    # copy password to clipboard
    try:
        pyperclip.copy(password)
        click.echo('Password has been copied to clipboard\n')
    except Exception:
        click.echo('Could not copy password to clipboad\n')

    # output password and info to terminal
    click.echo(password)
    click.echo(logo)
    

@cli.command()
@click.option("-i", "--info", is_flag=True, show_default=True, default=False, help="Get wallet associated to the node.")
@click.option("-c", "--create", is_flag=True, show_default=True, default=False, help="Create a new wallet if it doesn't exist.")
@click.option("-s", "--save", prompt=True, default="", help="Save user's provided seed phrase and treat that as the wallet.")
def wallet(info, create, save):
    
    # only one of the the parameters can be true
    if (info + create + save) > 1:
        click.echo("Only one of the parameters can be true")
        return
    
    if (info):
        web3 = Web3()
        web3.eth.account.enable_unaudited_hdwallet_features()
        mnemonic = ""
        
        # ensure that mnemonic file exists
        if (not (os.path.exists('mnemonic.txt'))):
            click.echo("Mnemonic file doesn't exist. Please create a new wallet using the -c flag or save a wallet using -s")
            return
        
        with open('mnemonic.txt') as f:
            lines = f.readlines()
            if (len(lines) == 0):
                click.echo("No wallet found. Please create a new wallet using the -c flag or save a wallet using -s")
                return
            if (len(lines) > 1):
                click.echo("More than one line found in mnemonic.txt. Please delete the extra lines and try again.")
                return
            mnemonic = lines[0]
            # mnemonic must have 12 words
            if (len(mnemonic.split(" ")) != 12):
                click.echo("Invalid mnemonic. Mnemonic must have 12 words.")
                return
            
        account = web3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/60'/0'/0/0")
        click.echo(account.address)
        
    # Check if mnemonic file already exists, if it exists don't allow to replace
    with open('mnemonic.txt') as f:
        lines = f.readlines()
        if (len(lines) > 0):
            click.echo("Mnemonic file already exists. Please consider before replacing the mnemonic.")
            return
    
    if (create):
        web3 = Web3()
        web3.eth.account.enable_unaudited_hdwallet_features()
        mnemonic = web3.eth.account.generate_mnemonic()
        account = web3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/60'/0'/0/0")
        click.echo("Address: " + account.address)
        click.echo("Mnemonic: " + mnemonic)
        click.echo("Please save this mnemonic in a safe place. This will be used to recover your wallet in the future.")
        with open('mnemonic.txt', 'w') as f:
            f.write(mnemonic)
    
    if (save):
        web3 = Web3()
        web3.eth.account.enable_unaudited_hdwallet_features()
        mnemonic = save
        # mnemonic must have 12 words
        if (len(mnemonic.split(" ")) != 12):
            click.echo("Invalid mnemonic. Mnemonic must have 12 words.")
            return
        account = web3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/60'/0'/0/0")
        click.echo("Address: " + account.address)
        click.echo("Mnemonic: " + mnemonic)
        click.echo("Please save this mnemonic in a safe place. This will be used to recover your wallet in the future.")
        with open('mnemonic.txt', 'w') as f:
            f.write(mnemonic)
            

