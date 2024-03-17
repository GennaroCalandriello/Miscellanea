import os
from brownie import accounts
from brownie import interface
from brownie import UniswapTest2

ganache=False

# DAI = "0xDF1742FE5B0BFC12331D8EAEC6B478DFDBD31464" # Goerli
# WETH = "0x2E3A2FB8473316A02B8A297B982498E661E1F6F5" # Goerli
# USDT = "0xC2C527C0CACF457746Bd31B2a698Fe89de2b6d49" # Goerli

DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F"  # Mainnet
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"  # Mainnet
spender_address = "0xE592427A0AEce92De3Edee1F18E0157C05861564"  # Mainnet

if not ganache:
    PRIVATE_KEY = os.environ["PRIVATE_KEY"]
else:
    PRIVATE_KEY = os.environ["PRIVATE_KEY_GANACHE"]

my_account = accounts.add(PRIVATE_KEY)
print("Msg.sender Account : ", accounts[0])
trans_DAI = 1

def main():
    test = UniswapTest2[-1]
    print("Smart Contract Address : ", test)
    tr_account = accounts[0]
    if trans_DAI:
        print("Approving DAI to test account")
        interface.ERC20(DAI).approve(tr_account, 5 * 10**18, {"from": tr_account})
        print("Transfering DAI to test account")
        interface.ERC20(DAI).transferFrom(
            tr_account, test, 5 * 10**18, {"from": tr_account}
        )
    print("Trying to swap DAI to WETH")

    test.exactInputSingle(
        1 * 10**18,
        {
            "from": tr_account,
            "allow_revert": True,
            "value": 0,
            "gas_limit": 3000000,
            "gas_price": 5 * 10**10,
        },
    )

    print("Finito")
    # ss = transf.swapExactOutputSingle(478 * 10**18, {"from": tr_account, "value": 7})


if __name__ == "__main__":
    main()
