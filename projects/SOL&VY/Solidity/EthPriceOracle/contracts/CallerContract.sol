pragma solidity 0.5.0;

  import "./EthPriceOracleInterface.sol";
  import "openzeppelin-solidity/contracts/ownership/Ownable.sol";

  contract CallerContract is Ownable {

      uint256 private ethPrice;
      EthPriceOracleInterface private oracleInstance;
      address private oracleAddress;
      
      mapping(uint256=>bool) myRequests;

      event newOracleAddressEvent(address oracleAddress);
      event ReceivedNewRequestIdEvent(uint256 id);
      event PriceUpdatedEvent(uint256 ethPrice, uint256 id);

      function setOracleInstanceAddress (address _oracleInstanceAddress) public onlyOwner {
        oracleAddress = _oracleInstanceAddress;
        oracleInstance = EthPriceOracleInterface(oracleAddress);
        emit newOracleAddressEvent(oracleAddress);
      }

      function updateEthPrice() public {
        uint256 id = oracleInstance.getLatestEthPrice();
        myRequests[id] = true;
        emit ReceivedNewRequestIdEvent(id);
      }

      function callback(uint256 _ethPrice, uint256 _id) public {
        
        require(myRequests[_id] ,"This request is not in my pending list.");
        ethPrice = _ethPrice;
        delete myRequests[_id];
        emit PriceUpdatedEvent(_ethPrice, _id);
      }
        modifier onlyOracle() {
        require(msg.sender == oracleAddress, "Damn! You are not authorized to call this function." );
        _;
        }

    }

 


/*
Here's how the callback function works:

First, you would want to make sure that the function can only be called for a valid id.
For that, you'll use a require statement.

Simply put, a require statement throws an error and stops the 
execution of the function if a condition is false.

Let's look at an example from the Solidity official documentation:

require(msg.sender == chairperson, "Only chairperson can give right to vote.");
The first parameter evaluates to true or false. If it's false, the function
execution will stop and the smart contract will throw an error- "Only chairperson 
can give right to vote."

Once you know that the id is valid, you can go ahead and remove it from the myRequests mapping.

Note: To remove an element from a mapping, you can use something like the following: delete myMapping[key];

Lastly, your function should fire an event to let the front-end know the price was successfully updated.
*/