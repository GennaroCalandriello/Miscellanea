from vyper.interfaces import ERC20

# interface ERC20:
#     def totalSupply() -> uint256: view
#     def balanceOf(account: address) -> uint256: view
#     def transfer(recipient: address, amount: uint256) -> bool: nonpayable
#     def allowance(owner: address, spender: address) -> uint256: view
#     def approve(spender: address, amount: uint256) -> bool: nonpayable
#     def transferFrom(sender: address, recipient: address, amount: uint256) -> bool: nonpayable

name: public(String[32])
symbol: public(String[32])
decimals: public(uint8)
totalSupply: public(uint256)
# balances : public(HashMap[address,uint256])
balanceOf: public(HashMap[address,uint256])
allowance: public(HashMap[address,HashMap[address,uint256]])
minter: address

event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256

event Approval:
    owner: indexed(address)
    spender: indexed(address)
    value: uint256

@external
def __init__(_name: String[32], _symbol: String[32], _decimals: uint8, _totalSupply: uint256):
    initial_supply: uint256 = _totalSupply * 10 ** convert(_decimals, uint256)
    self.name = _name
    self.symbol = _symbol
    self.decimals = _decimals
    self.totalSupply = _totalSupply
    self.minter = msg.sender
    self.balanceOf[msg.sender] = initial_supply

@external
def transferFrom(_from: address, _to:address, _value:uint256) ->bool:
    self.balanceOf[_from] -= _value
    self.balanceOf[_to] += _value
    self.allowance[_from][msg.sender]-=_value
    log Transfer(_from, _to, _value)
    return True

@external
def approve(_spender: address, _value: uint256) -> bool:
    self.allowance[msg.sender][_spender]=_value
    log Approval(msg.sender, _spender, _value)
    return True

@external
def mint(_to: address, _value:uint256):
    assert msg.sender == self.minter
    self.balanceOf[_to] += _value
    self.totalSupply += _value
    log Transfer(empty(address), _to, _value)

@internal
def _burn(_to: address, _value: uint256):
    assert _to!=empty(address)
    self.totalSupply-=_value
    self.balanceOf[_to]-=_value
    log Transfer(_to, empty(address), _value)

@external
def burn(_value: uint256):
    self._burn(msg.sender, _value)

@external
def burnFrom(_to:address, _value:uint256):
    self.allowance[_to][msg.sender]-=_value
    self._burn(_to, _value)

@external
def transfer(_to : address, _value : uint256) -> bool:
    """
    @dev Transfer token for a specified address
    @param _to The address to transfer to.
    @param _value The amount to be transferred.
    """
    # NOTE: vyper does not allow underflows
    #       so the following subtraction would revert on insufficient balance
    self.balanceOf[msg.sender] -= _value
    self.balanceOf[_to] += _value
    log Transfer(msg.sender, _to, _value)
    return True



