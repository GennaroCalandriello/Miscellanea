from brownie import accounts, network, web3, interface
import os
from web3 import Web3


PRIVATE_KEY = os.environ["PRIVATE_KEY"]

my_account = accounts.add(PRIVATE_KEY)
print("address: ", my_account.address)
account = accounts[0]


def get_balance(account):
    DAI_GOERLI = os.environ["DAI_GOERLI"]
    WETH_GOERLI = os.environ["WETH_GOERLI"]

    token_contract_dai = interface.ERC20(DAI_GOERLI)
    token_contract_weth = interface.ERC20(WETH_GOERLI)

    daiBalance = token_contract_dai.balanceOf(account)
    wethBalance = token_contract_weth.balanceOf(account)

    print("DAI balance: ", Web3.fromWei(token_contract_dai.balanceOf(account), "ether"))
    print(
        "WETH balance: ", Web3.fromWei(token_contract_weth.balanceOf(account), "ether")
    )

    balance_wei = web3.eth.getBalance(account.address)
    balance_eth = Web3.fromWei(balance_wei, "ether")
    print("Account address:", account.address)
    print("Account balance:", balance_eth, "ETH")


def main():
    get_balance(account)


if __name__ == "__main__":
    main()
