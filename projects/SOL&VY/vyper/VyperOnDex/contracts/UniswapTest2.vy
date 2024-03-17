from vyper.interfaces import ERC20

struct ExactInputSingleParams:
    tokenIn: address
    tokenOut: address
    fee: uint24
    recipient: address
    deadline: uint256
    amountIn: uint256
    amountOutMinimum: uint256
    sqrtPriceLimitX96: uint160

event Log:
    message: String[100]
    val: uint256

interface ISwapRouter:
    def exactInputSingle(params: ExactInputSingleParams) -> uint256: nonpayable

swap_router_address: constant(address) = 0xE592427A0AEce92De3Edee1F18E0157C05861564
DAI: constant(address) = 0xDF1742fE5b0bFc12331D8EAec6b478DfDbD31464
WETH: constant(address) = 0x2e3A2fb8473316A02b8A297B982498E661E1f6f5
poolFee: constant(uint24) = 3000

swap_router: ISwapRouter

@external
def __init__():
    self.swap_router=ISwapRouter(swap_router_address)

@external
def exactInputSingle(amountIn: uint256):

    ERC20(DAI).transferFrom(msg.sender, self, amountIn)
    ERC20(DAI).approve(swap_router_address, amountIn)  

    params: ExactInputSingleParams = ExactInputSingleParams({
        tokenIn: DAI,
        tokenOut: WETH,
        fee: poolFee,
        recipient: msg.sender,
        deadline: block.timestamp+1000,
        amountIn: amountIn,
        amountOutMinimum: 0,
        sqrtPriceLimitX96: 0
    })

    result : uint256 = self.swap_router.exactInputSingle(params)
    # log Log("result", result)
    
