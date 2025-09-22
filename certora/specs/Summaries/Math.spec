methods {
    // X128MathLib
    function X128MathLib.flatDivX128(uint128 numerator, uint256 denominator) internal returns (uint256) => flatDivX128CVL(numerator, denominator);
    function X128MathLib.fullMulX128(uint256 x, uint256 y) internal returns (uint256) => fullMulX128CVL(x,y);
    // MixedSignLib
    function MixedSignLib.add(int256 x, uint256 y) internal returns (int256) => addCVL(x,y);
    function MixedSignLib.sub(int256 x, uint256 y) internal returns (int256) => subCVL(x,y);
    function MixedSignLib.add(uint128 x, int128 y) internal returns (uint128) => addCVL2(x,y);
    function MixedSignLib.sub(uint128 x, int128 y) internal returns (uint128) => subCVL2(x,y);
    // UnsafeMath
    // function UnsafeMath.divRoundingUp(uint256 x, uint256 y) internal returns (uint256) => divUpCVL(x,y);
    // function UnsafeMath.simpleMulDiv(uint256 x, uint256 y, uint256 z) internal returns (uint256) => mulDivDownCVL(x,y,z);
    // FullMath
    // function FullMath.mulDiv(uint256 a, uint256 b, uint256 denominator) internal returns (uint256) => mulDivDownCVL(a,b,denominator);
    // function FullMath.mulDivRoundingUp(uint256 a, uint256 b, uint256 denominator) internal returns (uint256) => mulDivUpCVL(a,b,denominator);
    // FixedPointMathLib
    function FixedPointMathLib.mulDiv(uint256 x, uint256 y, uint256 d) internal returns (uint256) => mulDivDownCVL(x,y,d);
    function FixedPointMathLib.fullMulDiv(uint256 x, uint256 y, uint256 d) internal returns (uint256) => mulDivDownCVL(x,y,d);
    function FixedPointMathLib.mulDivUp(uint256 x, uint256 y, uint256 d) internal returns (uint256) => mulDivUpCVL(x,y,d);
}

/*
    NOTE: If bitvectors are used, the signed integer arithmetic in CVL breaks. 
*/


function flatDivX128CVL(uint128 numerator, uint256 denominator) returns uint256 {
    if (denominator == 0) return 0;
    return assert_uint256((numerator * (2^128)) / denominator);
}

function fullMulX128CVL(uint256 x, uint256 y) returns uint256 {
    return require_uint256((x*y)/(2^128));
}

function addCVL(int256 x, uint256 y) returns int256 {
    return require_int256(x+y);
}

function subCVL(int256 x, uint256 y) returns int256 {
    return require_int256(x-y);
}

function addCVL2(uint128 x, int128 y) returns uint128 {
    return require_uint128(x+y);
}

function subCVL2(uint128 x, int128 y) returns uint128 {
    return require_uint128(x-y);
}



// Standard CVL math summaries
function divUpCVL(uint256 x, uint256 y) returns uint256 {
    assert y !=0, "divUp error: cannot divide by zero";
    return require_uint256((x + y - 1) / y);
}

function mulDivDownCVL(uint256 x, uint256 y, uint256 z) returns uint256 {
    assert z !=0, "mulDivDown error: cannot divide by zero";
    return require_uint256(x * y / z);
}

function mulDivUpCVL(uint256 x, uint256 y, uint256 z) returns uint256 {
    assert z !=0, "mulDivDown error: cannot divide by zero";
    return require_uint256((x * y + z - 1) / z);
}

function mulDivDownCVL_no_div(uint256 x, uint256 y, uint256 z) returns uint256 {
    uint256 res;
    assert z != 0, "mulDivDown error: cannot divide by zero";
    mathint xy = x * y;
    mathint fz = res * z;

    require xy >= fz;
    require fz + z > xy;
    return res; 
}