from brownie import accounts, config, network, Erc20Cutri
import os


def get_account(ganache=False):
    if ganache:
        PRIVATE_key = os.environ["PRIVATE_KEY_GANACHE"]
        accounts.add(PRIVATE_key)
    else:
        Private_key = os.environ["PRIVATE_KEY"]
        accounts.add(Private_key)

    return accounts[0]


def main():
    totalSupply = 25 * 10**8
    _account = get_account()
    print("Deployer Address : ", _account.address)
    DAI_deploy = Erc20Cutri.deploy(
        "RaffCutriCoin",
        "RCC",
        18,
        totalSupply,
        {"from": _account, "gas_limit": 1000000, "gas_price": 2 * 10**10},
    )
    print("---------Token deployed at : ", DAI_deploy.address, "-----------")


if __name__ == "__main__":
    main()

# _name: String[32], _symbol: String[32], _decimals: uint8, _totalSupply: uint256
