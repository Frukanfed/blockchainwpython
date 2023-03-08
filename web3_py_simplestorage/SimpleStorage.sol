//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 myInt;

    function store(uint256 _int) public {
        myInt = _int;
    }

    struct People {
        uint256 myInt;
        string name;
    }
    People public person = People({myInt: 31, name: "frumk"});

    // view and pure dont need transactions
    // view = only for view  pure = only for math equations
    function retrieve() public view returns (uint256) {
        return myInt;
    }

    People[] public people;
    mapping(string => uint256) public nameToNumber;

    //memory = only stored during execution  storage = stored even after
    function addPerson(string memory _name, uint256 _myInt) public {
        people.push(People({name: _name, myInt: _myInt}));
        nameToNumber[_name] = _myInt;
    }
}
