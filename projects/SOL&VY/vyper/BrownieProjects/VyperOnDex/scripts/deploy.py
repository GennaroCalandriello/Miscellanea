import os
from brownie import accounts, network, web3, interface, UniswapTest2
from web3 import Web3


def main():
    PRIVATE_KEY = os.environ["PRIVATE_KEY"]
    my_account = accounts.add(PRIVATE_KEY)
    print("Deploying...")
    deployer = accounts[0]
    print("Deployer Address : ", deployer.address)
    my_contract = UniswapTest2.deploy(
        {"from": deployer, "gas_limit": 1000000, "gas_price": 2 * 10**10}
    )
    # print("Contract deployed to:", my_contract.address)
