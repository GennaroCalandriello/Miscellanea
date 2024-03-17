from vyper.interfaces import ERC20

interface ISwapV3Router:
    def exactInputSingle(params: Bytes[179]) -> uint256: payable
    def exactOutputSingle(params: Bytes[179]) -> uint256: payable

ISWAP : constant(address) = 0xE592427A0AEce92De3Edee1F18E0157C05861564
DAI: constant(address) = 0xDF1742fE5b0bFc12331D8EAec6b478DfDbD31464
WETH: constant(address) = 0x2e3A2fb8473316A02b8A297B982498E661E1f6f5

ISwapRoute: ISwapV3Router

struct ExactInputSingleParams:
    tokenIn: address
    tokenOut: address
    fee: uint24
    recipient: address
    deadline: uint256
    amountIn: uint256
    amountOutMinimum: uint256
    sqrtPriceLimitX96: uint160
    
struct ExactOutputSingleParams:
    tokenIn: address
    tokenOut: address
    fee: uint24
    recipient: address
    deadline: uint256
    amountIn: uint256
    amountOutMinimum: uint256
    sqrtPriceLimitX96: uint160

@external
def __init__():
    self.ISwapRoute = ISwapV3Router(ISWAP)

@internal
def pack(params: ExactInputSingleParams) -> Bytes[179]:
    packed: Bytes[179] = concat(
        slice(convert(params.tokenIn, bytes32), 12, 20),
        slice(convert(params.tokenOut,bytes32), 12, 20),
        convert(params.fee, bytes3),
        slice(convert(params.recipient, bytes32), 12, 20),
        convert(params.deadline, bytes32),
        convert(params.amountIn, bytes32),
        convert(params.amountOutMinimum, bytes32),
        convert(params.sqrtPriceLimitX96, bytes20)
    )
    return packed




@external
def swapExactInputSingle(amountIn: uint256)-> uint256:

    # ERC20(DAI).transferFrom(msg.sender, self, amountIn)
    # ERC20(DAI).approve(ISWAP, amountIn)
    self.transferFrom(DAI, msg.sender, self, amountIn)
    self.approve(DAI, ISWAP, amountIn)

    params : ExactInputSingleParams = ExactInputSingleParams({
        tokenIn: DAI,
        tokenOut: WETH,
        fee: 3000,
        recipient: msg.sender,
        deadline: block.timestamp,
        amountIn: amountIn,
        amountOutMinimum: 0,
        sqrtPriceLimitX96: 0
    })


    amountOut: uint256 = 0

    amountOut = self.ISwapRoute.exactInputSingle(self.pack(params))
    # amountOut=ISwapV3Router(ISWAP).exactInputSingle(self.pack(params))


    return amountOut

@external
def exactOutputSingle(amountOut: uint256)-> uint256:

    ERC20(DAI).transferFrom(msg.sender, self, amountOut)
    ERC20(DAI).approve(ISWAP, amountOut)

    params : ExactInputSingleParams = ExactInputSingleParams({
        tokenIn: DAI,
        tokenOut: WETH,
        fee: 3000,
        recipient: msg.sender,
        deadline: block.timestamp,
        amountIn: amountOut,
        amountOutMinimum: 0,
        sqrtPriceLimitX96: 0
    })

    amountIn: uint256 = 0
    amountIn = ISwapV3Router(ISWAP).exactOutputSingle(self.pack(params))

    return amountIn

@internal
def transferFrom(token: address, sender: address, recipient: address, amount: uint256) -> bool:
    result: Bytes[32]= raw_call(token, concat(method_id("transferFrom(address,address,uint256)"), convert(sender, bytes32), convert(recipient, bytes32), convert(amount, bytes32)), max_outsize=32, gas=50000)
    success: bool = len(result) > 0

    assert success, "Transfer failed"
    return success

@internal
def approve(token: address, spender: address, amount: uint256) -> bool:
    result: Bytes[32] = raw_call(token, concat(method_id("approve(address,uint256)"), convert(spender, bytes32), convert(amount, bytes32)), max_outsize=32, gas=50000)
    success: bool = len(result) > 0
    assert success, "Approval failed"
    return success
