import "./Summaries/ERC20cvl.spec";
import "./Summaries/extsload.spec";
import "./Summaries/Math.spec";
import "./Summaries/SignatureCheckerLib.spec";
import "./Summaries/TickMathSummary.spec";
import "./Summaries/UniV4TickFunctionsCVL.spec";
import "./Summaries/CalldataReader.spec";

using PoolManagerHarness as PoolManager;

methods {
    // function extsload(uint256) external returns (uint256) => NONDET DELETE;
    // function _.sync(PoolManagerHarness.Currency) external => DISPATCHER(true);
    function updateRewardsAndDelta(PoolUpdates.CalldataReader, PoolUpdates.SwapCall, PoolUpdates.PoolId, bool) external envfree;
    
    function updatePools(PoolUpdates.CalldataReader, PoolUpdates.PairArray) external returns (PoolUpdates.CalldataReader) envfree;
    function updatePool(PoolUpdates.CalldataReader, PoolUpdates.SwapCall, PoolUpdates.PairArray pairs) 
        external returns (PoolUpdates.CalldataReader) envfree;
    function getDeltaOfAsset(address) external returns (int256) envfree;
    function getSwapCallAsset(PoolUpdates.SwapCall) external returns address envfree;
    function simulateRewardsCalculation(address, PoolUpdates.PoolKey, IPoolManager.ModifyLiquidityParams) external returns (uint256) envfree;
    function toId(PoolUpdates.PoolKey) external returns PoolUpdates.PoolId envfree;
    function getSwapCallId(PoolUpdates.SwapCall) external returns PoolUpdates.PoolId envfree;
    function getPositionLiquidity(address, PoolUpdates.PoolId, IPoolManager.ModifyLiquidityParams) external returns (uint128) envfree;
    function getPoolLiquidity(PoolUpdates.PoolId) external returns (uint128) envfree;
    function getCurrentOnly(PoolUpdates.PoolUpdateVariantMap) external returns (bool) envfree;
    function getCurrentTick(PoolUpdates.PoolId id) external returns (int24) envfree;
    function getTickLiquidityHarness(PoolUpdates.PoolId, int24) external returns (uint128, int128) envfree;
    function getGlobalGrowth(PoolUpdates.PoolId id) external  returns (uint256) envfree;

    function readBool_harness(PoolUpdates.CalldataReader) external returns (PoolUpdates.CalldataReader, bool) envfree;
    function readU8_harness(PoolUpdates.CalldataReader) external returns (PoolUpdates.CalldataReader, uint8) envfree;
    function readU16_harness(PoolUpdates.CalldataReader) external returns (PoolUpdates.CalldataReader, uint16) envfree;
    function readU32_harness(PoolUpdates.CalldataReader) external returns (PoolUpdates.CalldataReader, uint32) envfree;
    function readI24_harness(PoolUpdates.CalldataReader) external returns (PoolUpdates.CalldataReader, int24) envfree;
    function readU40_harness(PoolUpdates.CalldataReader) external returns (PoolUpdates.CalldataReader, uint40) envfree;
    function readU64_harness(PoolUpdates.CalldataReader) external returns (PoolUpdates.CalldataReader, uint64) envfree;
    function readU128_harness(PoolUpdates.CalldataReader) external returns (PoolUpdates.CalldataReader, uint128) envfree;
    function readAddr_harness(PoolUpdates.CalldataReader) external returns (PoolUpdates.CalldataReader, address) envfree;
    function readU160_harness(PoolUpdates.CalldataReader) external returns (PoolUpdates.CalldataReader, uint160) envfree;
    function readU256_harness(PoolUpdates.CalldataReader) external returns (PoolUpdates.CalldataReader, uint256) envfree;
    function readU24End_harness(PoolUpdates.CalldataReader) external returns (PoolUpdates.CalldataReader, PoolUpdates.CalldataReader) envfree;
}



// We want to show that when updatePools is called the solvency invariant is maintained
// That is: TotalTokenBalance(alpha) = Delta(alpha) + Sum(UserBalances) + Sum(LPRewards) + Fees
// In update pools only the delta and rewards should change.
// so as a first step we verify that the sum of these are perserved.



// should be violated - see issues I02, I03 
rule updatePoolSolvencyEqCurrentOnly1LP() {
    PoolUpdates.CalldataReader reader;
    PoolUpdates.PoolKey poolKey;
    PoolUpdates.SwapCall swapCall; 
    address asset = getSwapCallAsset(swapCall);
    PoolUpdates.PoolId id = getSwapCallId(swapCall); 
    bool currentOnly = true;
    int24 currentTick = getCurrentTick(id);

    require id == toId(poolKey), "consistency between poolKey and swapCall id"; 
    uint128 poolLiquidity = getPoolLiquidity(id); 

    PoolUpdates.CalldataReader reader1;
    uint128 amountCurrent; 
    (reader1, amountCurrent) = readU128_harness(reader);
    uint128 expectedLiquidity;
    PoolUpdates.CalldataReader reader2; 
    (reader2, expectedLiquidity) = readU128_harness(reader1);

    IPoolManager.ModifyLiquidityParams params1;
    int24 tickLower1 = params1.tickLower;
    int24 tickUpper1 = params1.tickUpper;

    address LP1;
    uint128 liquidity1 = getPositionLiquidity(LP1, id, params1);
 
    require liquidity1 == poolLiquidity, "only LP1 has liquidity for the pool";
    
    uint256 preRewardLP1 = simulateRewardsCalculation(LP1,poolKey,params1); 
    int256 preDelta = getDeltaOfAsset(asset); 

    mathint preRewardsAndDelta = preRewardLP1 + preDelta; 

    updateRewardsAndDelta(reader, swapCall, id, currentOnly);

    uint256 postRewardLP1 = simulateRewardsCalculation(LP1,poolKey,params1); 
    int256 postDelta = getDeltaOfAsset(asset); 

    mathint postRewardsAndDelta = postRewardLP1 + postDelta;

    assert postDelta <= preDelta, "Angstrom delta decreases - see overview table"; 
    assert postRewardLP1 >= preRewardLP1, "rewards increase - see overview table"; //can be violated - overflow in globalGrow
    assert postRewardsAndDelta == preRewardsAndDelta, "sum of delta and rewards is unchanged"; //can be violated and decrease
}

// verifies 
rule updatePoolSolvencyLeqCurrentOnly1LP() {
    PoolUpdates.CalldataReader reader;
    PoolUpdates.PoolKey poolKey;
    PoolUpdates.SwapCall swapCall; 
    address asset = getSwapCallAsset(swapCall);
    PoolUpdates.PoolId id = getSwapCallId(swapCall); 
    bool currentOnly = true;
    int24 currentTick = getCurrentTick(id);

    require id == toId(poolKey), "consistency between poolKey and swapCall id"; 
    uint128 poolLiquidity = getPoolLiquidity(id); 

    PoolUpdates.CalldataReader reader1;
    uint128 amountCurrent; 
    (reader1, amountCurrent) = readU128_harness(reader);
    uint128 expectedLiquidity;
    PoolUpdates.CalldataReader reader2; 
    (reader2, expectedLiquidity) = readU128_harness(reader1);

    IPoolManager.ModifyLiquidityParams params1;
    int24 tickLower1 = params1.tickLower;
    int24 tickUpper1 = params1.tickUpper;

    address LP1;
    uint128 liquidity1 = getPositionLiquidity(LP1, id, params1);
 
    require liquidity1 == poolLiquidity, "only LP1 has liquidity for the pool";
    
    uint256 preRewardLP1 = simulateRewardsCalculation(LP1,poolKey,params1); 
    int256 preDelta = getDeltaOfAsset(asset); 

    mathint preRewardsAndDelta = preRewardLP1 + preDelta; 

    updateRewardsAndDelta(reader, swapCall, id, currentOnly);

    uint256 postRewardLP1 = simulateRewardsCalculation(LP1,poolKey,params1); 
    int256 postDelta = getDeltaOfAsset(asset); 

    mathint postRewardsAndDelta = postRewardLP1 + postDelta;

    assert postRewardsAndDelta <= preRewardsAndDelta, "Changes in delta and rewards can only favor Angstrom"; 
}

// Violated - potential rounding errors

// intuitive simplified explanation to why it should hold.
// the change in delta is -rewardTotal which is the sum of amounts for different ticks + donateToCurrent
// the change in simulated rewards:
// rewards are calculated from rewardGrowthOutside and globalGrowth that gets changed in the loop
// globalGrowth += X128MathLib.flatDivX128(amount, liquidity)  - this is total liquidity in some range - think about this.
// rewardGrowthOutside += X128MathLib.flatDivX128(amount, liquidity) (sometimes)
// if an LP takes out all the liquidity they get the full reward which is 
// rewards = X128MathLib.fullMulX128(growthInside - position.lastGrowthInside, positionTotalLiquidity)
// this is the positionTotalLiquidity before liquidity was removed (kind of strange)
// 
// say only one tick and this led to globalGrowthInside growing by amount1/liquidity, so total = amount1 
// and lastGrowthInside should be unchanged
// so it seems that rewards grow by amount1/Totalliquidity * liquidityLP1 (with app. **128...)
// amount1/TotalLiq * LiqLP1 + amount1/TotalLIq * LiqLP2 - amount1 = 0 

rule updatePoolSolvencyLeqCurrentOnly2LPs() {
    PoolUpdates.CalldataReader reader;
    PoolUpdates.PoolKey poolKey;
    PoolUpdates.SwapCall swapCall; 
    address asset = getSwapCallAsset(swapCall);
    PoolUpdates.PoolId id = getSwapCallId(swapCall); 
    bool currentOnly = true;
    int24 currentTick = getCurrentTick(id);

    require id == toId(poolKey), "consistency between poolKey and swapCall id"; 
    uint128 poolLiquidity = getPoolLiquidity(id); 

    IPoolManager.ModifyLiquidityParams params1;
    IPoolManager.ModifyLiquidityParams params2;

    address LP1;
    address LP2;
    require LP1 != LP2;
    uint128 liquidity1 = getPositionLiquidity(LP1, id, params1);
    uint128 liquidity2 = getPositionLiquidity(LP2, id, params2);

    require liquidity1 + liquidity2 == poolLiquidity, "only LP1,LP2 have liquidity in the pool";
    
    uint256 preRewardLP1 = simulateRewardsCalculation(LP1,poolKey,params1); 
    uint256 preRewardLP2 = simulateRewardsCalculation(LP2,poolKey,params2); 
    int256 preDelta = getDeltaOfAsset(asset); 

    mathint preRewardsAndDelta = preRewardLP1 + preRewardLP2 + preDelta; 

    uint256 preGlobalGrowth = getGlobalGrowth(id);

    PoolUpdates.CalldataReader reader1;
    uint128 amountCurrent; 
    (reader1, amountCurrent) = readU128_harness(reader);
    uint128 expectedLiquidity;
    PoolUpdates.CalldataReader reader2; 
    (reader2, expectedLiquidity) = readU128_harness(reader1);

    require expectedLiquidity == poolLiquidity, "assuming bundle builders give the correct liquidity";

    // assumptions that bundle builders can enforce to prevent < solvency, but these still don't guarantee it 
    // require !( amountCurrent != 0 && expectedLiquidity != poolLiquidity),
    //     "bundle builders prevent this situation from ocurring";
    // int24 tickLower1 = params1.tickLower;
    // int24 tickUpper1 = params1.tickUpper;
    // require tickLower1 <= currentTick && currentTick < tickUpper1, "LP1 is active"; 
    // require liquidity1 != 0, "LP1 has liquidity in the range";

    updateRewardsAndDelta(reader, swapCall, id, currentOnly);

    uint256 postRewardLP1 = simulateRewardsCalculation(LP1,poolKey,params1); 
    uint256 postRewardLP2 = simulateRewardsCalculation(LP2,poolKey,params2); 
    int256 postDelta = getDeltaOfAsset(asset); 
    uint256 postGlobalGrowth = getGlobalGrowth(id);

    mathint postRewardsAndDelta = postRewardLP1 + postRewardLP2 + postDelta;

    // these assertions would help proving the goal - they actually help finding the counterexample
    assert postGlobalGrowth - preGlobalGrowth <= flatDivX128CVL(amountCurrent,poolLiquidity);
    assert postDelta - preDelta <= -amountCurrent;
    assert postRewardLP1 - preRewardLP1 <= fullMulX128CVL(flatDivX128CVL(amountCurrent,poolLiquidity),liquidity1);
    assert postRewardLP2 - preRewardLP2 <= fullMulX128CVL(flatDivX128CVL(amountCurrent,poolLiquidity),liquidity2);
    assert postRewardLP1 - preRewardLP1 + postRewardLP2 - preRewardLP2 <= amountCurrent;

    // goal
    assert postRewardsAndDelta <= preRewardsAndDelta, "Changes in delta and rewards can only favor Angstrom";
}


// Rule with currentOnly = false, and 1 LP, verifies
rule updatePoolSolvencyLeqNotCurrentOnly1LP() {
    PoolUpdates.CalldataReader reader;
    PoolUpdates.PoolKey poolKey;
    PoolUpdates.SwapCall swapCall; 
    address asset = getSwapCallAsset(swapCall);
    PoolUpdates.PoolId id = getSwapCallId(swapCall); 
    bool currentOnly = false;
    int24 currentTick = getCurrentTick(id);

    require id == toId(poolKey), "consistency between poolKey and swapCall id"; 
    uint128 poolLiquidity = getPoolLiquidity(id); 

    IPoolManager.ModifyLiquidityParams params1;
    int24 tickLower1 = params1.tickLower;
    int24 tickUpper1 = params1.tickUpper;

    address LP1;
    uint128 liquidity1 = getPositionLiquidity(LP1, id, params1);

    // Assumtpions - maybe need more
    require liquidity1 == poolLiquidity, "only LP1";

    PoolUpdates.CalldataReader reader1;
    int24 startTick; 
    (reader1,startTick) = readI24_harness(reader);
    PoolUpdates.CalldataReader reader2;
    uint128 liquidityInLoop; 
    (reader2,liquidityInLoop) = readU128_harness(reader1);
    PoolUpdates.CalldataReader newreader; 
    PoolUpdates.CalldataReader amountsEnd; 
    (newreader,amountsEnd) = readU24End_harness(reader2);

    uint128 amount_iter1;
    PoolUpdates.CalldataReader newreader1; 
    (newreader1,amount_iter1) = readU128_harness(newreader);

    uint128 donateToCurrent;
    PoolUpdates.CalldataReader newreader2; 
    (newreader2,donateToCurrent) = readU128_harness(newreader1);


    uint128 startTickLiquidity; 
    int128 startTickNetLiquidity; 
    (startTickLiquidity,startTickNetLiquidity) = getTickLiquidityHarness(id,startTick);

    // continue to unpack the values and try to write some interesting assumptions on them

    // SIMPLIFIED CASE
    // require liquidityInLoop == poolLiquidity;
    require startTickNetLiquidity == 0;
    require tickLower1 <= currentTick && currentTick < tickUpper1;

    uint256 preRewardLP1 = simulateRewardsCalculation(LP1,poolKey,params1); 
    int256 preDelta = getDeltaOfAsset(asset); 

    mathint preRewardsAndDelta = preRewardLP1 + preDelta; 

    updateRewardsAndDelta(reader, swapCall, id, currentOnly);

    uint256 postRewardLP1 = simulateRewardsCalculation(LP1,poolKey,params1); 
    int256 postDelta = getDeltaOfAsset(asset); 

    mathint postRewardsAndDelta = postRewardLP1 + postDelta;

    assert postRewardsAndDelta <= preRewardsAndDelta, "Changes in delta and rewards can only favor Angstrom";
}
