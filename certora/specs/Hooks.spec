import "./Summaries/ERC20cvl.spec";
import "./Summaries/extsload.spec";
import "./Summaries/Math.spec";
import "./Summaries/SignatureCheckerLib.spec";
import "./Summaries/TickMathSummary.spec";
import "./Summaries/UniV4TickFunctionsCVL.spec";
import "./Summaries/CalldataReader.spec";

using PoolManagerHarness as PoolManager;

methods {
    function updatePools(PoolUpdates.CalldataReader, PoolUpdates.PairArray) external returns (PoolUpdates.CalldataReader) envfree;
    function beforeAddLiquidity(address,PoolUpdates.PoolKey,IPoolManager.ModifyLiquidityParams,bytes) external returns (bytes4);
    function beforeRemoveLiquidity(address,PoolUpdates.PoolKey,IPoolManager.ModifyLiquidityParams,bytes) external returns (bytes4);
    function simulateRewardsCalculation(address, PoolUpdates.PoolKey, IPoolManager.ModifyLiquidityParams) external returns (uint256) envfree;
    function getGrowthInside(PoolUpdates.PoolId, int24, int24, int24) external returns (uint256) envfree;
    function getRewardGrowthOutside(PoolUpdates.PoolId, int24) external returns (uint256) envfree;
    function getLastGrowthInside(address,PoolUpdates.PoolId,IPoolManager.ModifyLiquidityParams) external returns (uint256) envfree;
    function getCurrentTick(PoolUpdates.PoolId) external returns (int24) envfree;
    function toId(PoolUpdates.PoolKey) external returns PoolUpdates.PoolId envfree;
    function getGlobalGrowth(PoolUpdates.PoolId id) external  returns (uint256) envfree;
    function getPositionLiquidity(address, PoolUpdates.PoolId, IPoolManager.ModifyLiquidityParams) external returns (uint128) envfree;
    function getIsInitialized(PoolUpdates.PoolId, int24, int24) external returns (bool) envfree;
    function PoolManager.setPoolLiquidity(PoolUpdates.PoolId, uint128) external envfree;
    function getPoolLiquidity(PoolUpdates.PoolId) external returns (uint128) envfree;
    function Position.calculatePositionKey(address, int24, int24, bytes32) internal returns (bytes32);
    function PoolManager.setPositionLiquidity(PoolUpdates.PoolId, address, IPoolManager.ModifyLiquidityParams, uint128) external envfree;
    function getPositionLiquidity(address, PoolUpdates.PoolId, IPoolManager.ModifyLiquidityParams) external returns (uint128) envfree;
    // function getUniswapUserDelta(PoolUpdates.Currency, address) external returns (int256) envfree;
}

function modifyLiquiditySummaryCVL(address sender, PoolUpdates.PoolId id, IPoolManager.ModifyLiquidityParams params) {
    // should technically also set some other values but this is not essential.
    mathint poolLiquidity = getPoolLiquidity(id);
    uint128 newPoolLiquidity = require_uint128(poolLiquidity + params.liquidityDelta);
    PoolManager.setPoolLiquidity(id, newPoolLiquidity);
    mathint positionLiquidity = getPositionLiquidity(sender,id,params);
    uint128 newPositionLiquidity = require_uint128(positionLiquidity + params.liquidityDelta);
    PoolManager.setPositionLiquidity(id, sender, params, newPositionLiquidity);
}

rule addLiquidityDoesNotIncreaseRewards() {
    address sender;
    PoolUpdates.PoolKey key;
    int24 tickSpacing = key.tickSpacing;
    PoolUpdates.PoolId id = toId(key);
    IPoolManager.ModifyLiquidityParams params; 
    int256 liquidityDelta = params.liquidityDelta;
    require liquidityDelta > 0, "the hook is called on on positive liquidity changes.";
    bytes hookdata;
    env e;

    int24 tickLower = params.tickLower;
    bool isInitializedLower = getIsInitialized(id,tickLower,tickSpacing);
    int24 tickUpper = params.tickUpper; 
    int24 currentTick = getCurrentTick(id); 
    uint256 growthInsidePre = getGrowthInside(id,currentTick,params.tickLower,params.tickUpper);
    uint256 lastGrowthInsidePre = getLastGrowthInside(sender,id,params);

    // simplification 
    // require tickLower < currentTick && currentTick < tickUpper, "simplfication";

    bool isInitializedUpper = getIsInitialized(id,tickUpper,tickSpacing);
    uint128 positionLiquidityPre = getPositionLiquidity(sender, id, params);
    require positionLiquidityPre > 0 => (isInitializedLower && isInitializedUpper), "If the position has liquidity the ticks are initialized";

    uint256 rewardsPre = simulateRewardsCalculation(sender,key,params);


    // notice that the reward calculation is in the same range for which we add liquidity.
    beforeAddLiquidity(e, sender, key, params, hookdata); // hookdata is unused in the hook

    // modify liquidity is too difficult for the prover - instead we call the summary
    // PoolManager.poolModifyLiquidityHarness(e, key, params, hookdata);
    modifyLiquiditySummaryCVL(sender,id,params);
    
    uint128 positionLiquidityPost = getPositionLiquidity(sender, id, params);
    uint256 rewardsPost = simulateRewardsCalculation(sender,key,params);
    uint256 growthInsidePost = getGrowthInside(id,currentTick,params.tickLower,params.tickUpper);
    uint256 lastGrowthInsidePost = getLastGrowthInside(sender,id,params);
    assert rewardsPost <= rewardsPre, "rewards only decrease"; 
}

rule addLiquidityDoesNotDecreaseRewards() {
    address sender;
    PoolUpdates.PoolKey key;
    int24 tickSpacing = key.tickSpacing;
    PoolUpdates.PoolId id = toId(key);
    IPoolManager.ModifyLiquidityParams params; 
    int256 liquidityDelta = params.liquidityDelta;
    require liquidityDelta > 0, "the hook is called on on positive liquidity changes.";
    bytes hookdata;
    env e;

    int24 tickLower = params.tickLower;
    bool isInitializedLower = getIsInitialized(id,tickLower,tickSpacing);
    int24 tickUpper = params.tickUpper; 
    int24 currentTick = getCurrentTick(id); 
    uint256 growthInsidePre = getGrowthInside(id,currentTick,params.tickLower,params.tickUpper);
    uint256 lastGrowthInsidePre = getLastGrowthInside(sender,id,params);

    // simplification 
    require tickLower < currentTick && currentTick < tickUpper, "simplfication";

    bool isInitializedUpper = getIsInitialized(id,tickUpper,tickSpacing);
    uint128 positionLiquidityPre = getPositionLiquidity(sender, id, params);
    require positionLiquidityPre > 0 => (isInitializedLower && isInitializedUpper), "If the position has liquidity the ticks are initialized";

    uint256 rewardsPre = simulateRewardsCalculation(sender,key,params);


    // notice that the reward calculation is in the same range for which we add liquidity.
    beforeAddLiquidity(e, sender, key, params, hookdata); // hookdata is unused in the hook

    // modify liquidity is too difficult for the prover - instead we call the summary
    // PoolManager.poolModifyLiquidityHarness(e, key, params, hookdata);
    modifyLiquiditySummaryCVL(sender,id,params);
    
    uint128 positionLiquidityPost = getPositionLiquidity(sender, id, params);
    uint256 rewardsPost = simulateRewardsCalculation(sender,key,params);
    uint256 growthInsidePost = getGrowthInside(id,currentTick,params.tickLower,params.tickUpper);
    uint256 lastGrowthInsidePost = getLastGrowthInside(sender,id,params);
    assert rewardsPost >= rewardsPre, "rewards only increase"; 
}

rule noRewardsForNewPosition() {
    address sender;
    PoolUpdates.PoolKey key;
    int24 tickSpacing = key.tickSpacing;
    PoolUpdates.PoolId id = toId(key);
    IPoolManager.ModifyLiquidityParams params; 
    int256 liquidityDelta = params.liquidityDelta;
    require liquidityDelta > 0, "the hook is called on on positive liquidity changes.";
    bytes hookdata;
    env e;

    int24 tickLower = params.tickLower;
    bool isInitializedLower = getIsInitialized(id,tickLower,tickSpacing);
    int24 tickUpper = params.tickUpper; 
    bool isInitializedUpper = getIsInitialized(id,tickUpper,tickSpacing);
    uint128 positionLiquidityPre = getPositionLiquidity(sender, id, params);
    require positionLiquidityPre > 0 => (isInitializedLower && isInitializedUpper), "If the position has liquidity the ticks are initialized";

    require positionLiquidityPre == 0, "new position";

    int24 currentTick = getCurrentTick(id); 
    uint256 growthInsidePre = getGrowthInside(id,currentTick,params.tickLower,params.tickUpper);
    uint256 lastGrowthInsidePre = getLastGrowthInside(sender,id,params);

    // notice that the reward calculation is in the same range for which we add liquidity.
    beforeAddLiquidity(e, sender, key, params, hookdata); // hookdata is unused in the hook

    // modify liquidity is too difficult for the prover - instead we call the summary
    // PoolManager.poolModifyLiquidityHarness(e, key, params, hookdata);
    modifyLiquiditySummaryCVL(sender,id,params);
    
    uint128 positionLiquidityPost = getPositionLiquidity(sender, id, params);
    uint256 rewardsPost = simulateRewardsCalculation(sender,key,params);
    uint256 growthInsidePost = getGrowthInside(id,currentTick,params.tickLower,params.tickUpper);
    uint256 lastGrowthInsidePost = getLastGrowthInside(sender,id,params);
    assert rewardsPost == 0, "no rewards"; 
}

rule noRewardsAfterAdditionsToTwoNewPositions() {
    address sender;
    PoolUpdates.PoolKey key;
    int24 tickSpacing = key.tickSpacing;
    PoolUpdates.PoolId id = toId(key);
    env e;

    IPoolManager.ModifyLiquidityParams params1; 
    int256 liquidityDelta1 = params1.liquidityDelta;
    require liquidityDelta1 > 0, "the hook is called on on positive liquidity changes.";
    bytes hookdata1;

    IPoolManager.ModifyLiquidityParams params2; 
    int256 liquidityDelta2 = params2.liquidityDelta;
    require liquidityDelta2 > 0, "the hook is called on on positive liquidity changes.";
    bytes hookdata2;

    int24 tickLower1 = params1.tickLower;
    bool isInitializedLower1Pre = getIsInitialized(id,tickLower1,tickSpacing);
    int24 tickUpper1 = params1.tickUpper; 
    bool isInitializedUpper1Pre = getIsInitialized(id,tickUpper1,tickSpacing);
    int24 tickLower2 = params2.tickLower;
    bool isInitializedLower2Pre = getIsInitialized(id, tickLower2, tickSpacing);
    int24 tickUpper2 = params2.tickUpper;
    bool isInitializedUpper2Pre = getIsInitialized(id, tickUpper2, tickSpacing);

    uint128 positionLiquidity1Pre = getPositionLiquidity(sender, id, params1);
    require positionLiquidity1Pre == 0, "new position";
    uint128 positionLiquidity2Pre = getPositionLiquidity(sender, id, params2);
    require positionLiquidity2Pre == 0, "new position";

    // int24 currentTick = getCurrentTick(id); 
    // uint256 growthInsidePre = getGrowthInside(id,currentTick,params.tickLower,params.tickUpper);
    // uint256 lastGrowthInsidePre = getLastGrowthInside(sender,id,params);

    // add liquidity to both positions
    beforeAddLiquidity(e, sender, key, params1, hookdata1); 
    modifyLiquiditySummaryCVL(sender,id,params1);

    bool isInitializedLower1Mid = getIsInitialized(id, tickLower1, tickSpacing);
    bool isInitializedUpper1Mid = getIsInitialized(id, tickUpper1, tickSpacing);
    bool isInitializedLower2Mid = getIsInitialized(id, tickLower2, tickSpacing);
    bool isInitializedUpper2Mid = getIsInitialized(id, tickUpper2, tickSpacing);

    require isInitializedLower1Mid && isInitializedUpper1Mid, "after the addition the ticks are initialized";

    beforeAddLiquidity(e, sender, key, params2, hookdata2); 
    modifyLiquiditySummaryCVL(sender,id,params2);
    
    uint128 positionLiquidity1Post = getPositionLiquidity(sender, id, params1);
    uint128 positionLiquidity2Post = getPositionLiquidity(sender, id, params2);

    uint256 rewards1Post = simulateRewardsCalculation(sender,key,params1);
    uint256 rewards2Post = simulateRewardsCalculation(sender, key, params2);
    assert rewards1Post == 0, "no rewards for position 1";
    assert rewards2Post == 0, "no rewards for position 2";

    // uint256 growthInsidePost = getGrowthInside(id,currentTick,params.tickLower,params.tickUpper);
    // uint256 lastGrowthInsidePost = getLastGrowthInside(sender,id,params);
}

rule noRewardsAfterRemoval() {
    address sender;
    PoolUpdates.PoolKey key;
    IPoolManager.ModifyLiquidityParams params;
    bytes hookdata;
    env e;

    // Call the beforeRemoveLiquidity hook
    beforeRemoveLiquidity(e, sender, key, params, hookdata);

    // After removal, rewards should be zero
    uint256 rewardsPost = simulateRewardsCalculation(sender, key, params);
    assert rewardsPost == 0, "No rewards after liquidity removal";
}

// rule that would catch the bug they had
// simulate rewards calc
// call some uniswap function
// simulate rewards calc

