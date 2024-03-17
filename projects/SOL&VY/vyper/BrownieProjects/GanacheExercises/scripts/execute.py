from brownie import accounts, config, network, Erc20Cutri
from deployer import get_account

RAFC = "0x4f010Bbf0D0645Cb638D1983787A97958FfA4445"  # RaffCoin on Sepolia Testnet
RCC = "0x18d9445e62575A73B71e33B2aC4c461c80e77E8d"  # RaffCutriCoin on Sepolia Testnet
totalSupply = 25 * 10**19  # RaffCutriCoin max supply


def main(transfer=True):
    allowance = totalSupply
    transferAmount = totalSupply
    burningAmount = 34550
    _account = get_account()
    raffcoin = Erc20Cutri[-1]

    if transfer:
        raffcoin.approve(_account, allowance, {"from": _account})
        print("-----------Approved--------------")
        raffcoin.transferFrom(
            _account,
            RCC,
            transferAmount - 100,
            {"from": _account, "gas_limit": 1000000, "gas_price": 2 * 10**10},
        )
        print("-----------Transfered--------------")
    else:
        raffcoin.burn(
            burningAmount,
            {"from": _account, "gas_limit": 1000000, "gas_price": 2 * 10**10},
        )
        print("-----------Burned--------------")


if __name__ == "__main__":
    main()
