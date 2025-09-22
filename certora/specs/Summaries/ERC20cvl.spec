methods {
    // ERC20 standard
    function _.name()                                           external => NONDET; // can we use PER_CALLEE_CONSTANT?
    function _.symbol()                                         external => NONDET; // can we use PER_CALLEE_CONSTANT?
    function _.decimals()                                       external => PER_CALLEE_CONSTANT;
    function _.totalSupply()                                    external => totalSupplyCVL(calledContract) expect uint256;
    function _.balanceOf(address a)                             external => balanceOfCVL(calledContract, a) expect uint256;
    function _.allowance(address a, address b)                  external => allowanceCVL(calledContract, a, b) expect uint256;
    function _.approve(address a, uint256 x)                    external with (env e) => approveCVL(calledContract, e.msg.sender, a, x) expect bool;
    function _.transfer(address a, uint256 amount)              external with (env e) => transferCVL(calledContract,e.msg.sender, a, amount) expect bool;
    function _.transfer(address token, address a, uint256 amount) external with (env e) => safeTransferCVL(token, e.msg.sender, a, amount) expect void;

    function _.safeTransferETH(address to, uint256 amount) internal with (env e) => transferETHcvl(e.msg.sender, to, amount) expect void;
    function _.safeTransferAllETH(address to) internal with (env e) => transferAllETHcvl(e.msg.sender, to) expect void;
    function _.forceSafeTransferETH(address to, uint256 amount, uint256 gasStipend) internal with (env e) => transferETHcvl(e.msg.sender, to, amount) expect void;
    function _.forceSafeTransferAllETH(address to, uint256 gasStipend) internal with (env e) => transferAllETHcvl(e.msg.sender, to) expect void;
    function _.forceSafeTransferETH(address to, uint256 amount) internal with (env e) => transferETHcvl(e.msg.sender, to, amount) expect void;
    function _.forceSafeTransferAllETH(address to) internal with (env e) => transferAllETHcvl(e.msg.sender, to) expect void;
    function _.trySafeTransferETH(address to, uint256 amount, uint256 gasStipend) internal with (env e) => transferETHwithSucc(e.msg.sender, to, amount) expect bool;
    function _.trySafeTransferAllETH(address to, uint256 gasStipend) internal with (env e) => transferAllEthWithSucc(e.msg.sender,to) expect bool;

    function _.safeTransferFrom(address token, address from, address to, uint256 amount) internal with (env e) => safeTransferFromCVL(token, e.msg.sender, from, to, amount) expect void;
    function _.trySafeTransferFrom(address token, address from, address to, uint256 amount) internal with (env e) => transferFromCVL(token, e.msg.sender, from, to, amount) expect bool;
    function _.safeTransferAllFrom(address token, address from, address to) internal with (env e) => safeTransferAllFromCVL(token, e.msg.sender, from, to) expect uint256;
    function _.safeTransfer(address token, address to, uint256 amount) internal with (env e) => transferCVL(token, e.msg.sender, to, amount) expect bool;
    function _.safeTransferAll(address token, address to) internal with (env e) => safeTransferAllCVL(token, e.msg.sender, to) expect uint256;
    function _.safeApprove(address token, address to, uint256 amount) internal  with (env e) => forceApproveCVL(token, e.msg.sender, to, amount) expect void;
    function _.safeApproveWithRetry(address token, address to, uint256 amount) internal with (env e) => forceApproveCVL(token, e.msg.sender, to, amount) expect void;
    function _.balanceOf(address token, address account) internal => balanceOfCVL(token, account) expect uint256;
    function _.totalSupply(address token) internal => totalSupplyCVL(token) expect uint256;
    
    function _.safeTransferFrom2(address token, address from, address to, uint256 amount) internal with (env e) => safeTransferFromCVL(token, from, from, to, amount) expect void;
    function _.permit2TransferFrom(address token, address from, address to, uint256 amount) internal with (env e) => forceApproveCVL(token, from, to, amount) expect void;
    function _.permit2(address token, address owner, address spender, uint256 amount, uint256 deadline, uint8 v, bytes32 r, bytes32 s) internal with (env e) => forceApproveCVL(token, owner, spender, amount) expect void;
    function _.simplePermit2(address token, address owner, address spender, uint256 amount, uint256 deadline, uint8 v, bytes32 r, bytes32 s) internal with (env e) => forceApproveCVL(token, owner, spender, amount) expect void;
    // function permit2Approve(address token, address spender, uint160 amount, uint48 expiration) internal with (env e) => 
    // function permit2Lockdown(address token, address spender) internal with (env e) =>
}

/// CVL implementation of ETH
ghost mapping (address => uint256) ethBalances;

function transferETHcvl(address from, address to, uint256 amount) {
    ethBalances[from] = assert_uint256(ethBalances[from] - amount);
    ethBalances[to] = require_uint256(ethBalances[to] + amount);
}

function transferAllETHcvl(address from, address to) {
    transferETHcvl(from,to,ethBalances[from]);
}

function transferETHwithSucc(address from, address to, uint256 amount) returns bool {
    bool nondetSuccess;
    if (!nondetSuccess) return false;

    if (ethBalances[from] < amount) return false;
    ethBalances[from] = assert_uint256(ethBalances[from] - amount);
    ethBalances[to] = require_uint256(ethBalances[to] + amount);
    return true;
}

function transferAllEthWithSucc(address from, address to) returns bool {
    return transferETHwithSucc(from, to, ethBalances[from]);
}




/// CVL simple implementations of IERC20:
/// token => totalSupply
ghost mapping(address => uint256) totalSupplyByToken;
/// token => account => balance
ghost mapping(address => mapping(address => uint256)) balanceByToken;
/// token => owner => spender => allowance
ghost mapping(address => mapping(address => mapping(address => uint256))) allowanceByToken;

// function tokenBalanceOf(address token, address account) returns uint256 {
//     return balanceByToken[token][account];
// }

function totalSupplyCVL(address token) returns uint256 {
    return totalSupplyByToken[token];
}

function balanceOfCVL(address token, address a) returns uint256 {
    return balanceByToken[token][a];
}

function allowanceCVL(address token, address a, address b) returns uint256 {
    return allowanceByToken[token][a][b];
}

function approveCVL(address token, address approver, address spender, uint256 amount) returns bool {
    // should be randomly reverting xxx
    bool nondetSuccess;
    if (!nondetSuccess) return false;

    allowanceByToken[token][approver][spender] = amount;
    return true;
}

function transferFromCVL(address token, address spender, address from, address to, uint256 amount) returns bool {
    // should be randomly reverting xxx
    bool nondetSuccess;
    if (!nondetSuccess) return false;

    if (allowanceByToken[token][from][spender] < amount) return false;
    allowanceByToken[token][from][spender] = assert_uint256(allowanceByToken[token][from][spender] - amount);
    return transferCVL(token, from, to, amount);
}

function transferCVL(address token, address from, address to, uint256 amount) returns bool {
    // should be randomly reverting xxx
    bool nondetSuccess;
    if (!nondetSuccess) return false;

    if(balanceByToken[token][from] < amount) return false;
    balanceByToken[token][from] = assert_uint256(balanceByToken[token][from] - amount);
    balanceByToken[token][to] = require_uint256(balanceByToken[token][to] + amount);  // We neglect overflows.
    return true;
}

function safeTransferCVL(address token, address from, address to, uint256 amount) {
    balanceByToken[token][from] = require_uint256(balanceByToken[token][from] - amount);
    balanceByToken[token][to] = require_uint256(balanceByToken[token][to] + amount);
}

function safeTransferAllCVL(address token, address from, address to) returns uint256 {
    uint256 amount = balanceByToken[token][from];
    safeTransferCVL(token, from, to, amount);
    return amount;
}

function safeTransferFromCVL(address token, address spender, address from, address to, uint256 amount) {
    allowanceByToken[token][from][spender] = require_uint256(allowanceByToken[token][from][spender] - amount);
    balanceByToken[token][from] = require_uint256(balanceByToken[token][from] - amount);
    balanceByToken[token][to] = require_uint256(balanceByToken[token][to] + amount);
}

function safeTransferAllFromCVL(address token, address spender, address from, address to) returns uint256 {
    uint256 amount = balanceByToken[token][from];
    safeTransferFromCVL(token, spender, from, to, amount);
    return amount;
}

function forceApproveCVL(address token, address approver, address spender, uint256 amount) {
    allowanceByToken[token][approver][spender] = amount;
}