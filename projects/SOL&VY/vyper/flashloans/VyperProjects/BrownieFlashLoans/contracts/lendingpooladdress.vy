# ERC20 Interface
interface ERC20:
    def balanceOf(address: address) -> uint256: view
    def allowance(owner: address, spender: address) -> uint256: view
    def transfer(recipient: address, amount: uint256) -> bool: nonpayable
    def transferFrom(sender: address, recipient: address, amount: uint256) -> bool: nonpayable
    def approve(spender: address, amount: uint256) -> bool: nonpayable

# Pool Interface
interface Pool:
    def depositTokens(amount: uint256) -> bool: nonpayable
    def withdrawTokens(amount: uint256) -> bool: nonpayable

# Contract with constructor
ERC20Token: ERC20
pool: Pool

@external
@payable
def __init__(pool_address: address, token_address: address):
    assert pool_address != empty(address), "Invalid pool address"
    assert token_address != empty(address), "Invalid token address"
    
    self.Pool = Pool(pool_address)
    self.ERC20Token = ERC20(token_address)

@external
def deposit(amount: uint256) -> bool:
    assert msg.sender != empty(address), "Invalid sender address"
    assert amount > 0, "Amount must be greater than zero"

    # Transfer tokens from sender to the contract
    assert self.ERC20Token.transferFrom(msg.sender, self, amount), "Token transfer failed"

    # Deposit tokens into the pool
    assert self.Pool.depositTokens(amount), "Deposit to pool failed"

    return True

@external
def withdraw(amount: uint256) -> bool:
    assert msg.sender != empty(address), "Invalid sender address"
    assert amount > 0, "Amount must be greater than zero"

    # Withdraw tokens from the pool
    assert self.Pool.withdrawTokens(amount), "Withdrawal from pool failed"

    # Transfer tokens from the contract to the sender
    assert self.ERC20Token.transfer(msg.sender, amount), "Token transfer failed"

    return True
