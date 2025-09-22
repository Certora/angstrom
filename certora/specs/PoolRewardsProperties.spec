import "./Summaries/ERC20cvl.spec";
import "./Summaries/extsload.spec";
import "./Summaries/Math.spec";
import "./Summaries/SignatureCheckerLib.spec";
import "./Summaries/TickMathSummary.spec";
import "./Summaries/UniV4TickFunctionsCVL.spec";

using PoolManagerHarness as PoolManager;

methods {
    function updateAfterTickMoveHarness(PoolUpdatesHarness.PoolId id, address uniV4, int24 prevTick, int24 newTick, int24 tickSpacing) external envfree;
    function getGrowthInsideHarness(int24 current, int24 lower, int24 upper) external returns (uint256) envfree;
    function getGlobalGrowthConst() external returns (uint256) envfree;
    function getRewardGrowthOutside(PoolUpdatesHarness.PoolId id, int24 tick) external returns (uint256) envfree;
}

function rewardInitializationAssumption(PoolUpdatesHarness.PoolId id, int24 tick, address uniV4, int24 tickSpacing) {  
    uint256 rewardGrowthOutside = getRewardGrowthOutside(id,tick);
    bool initialized = isInitializedCVL(uniV4,id,tick,tickSpacing);
    require rewardGrowthOutside != 0 => initialized;
}

// this is part of solvency being maintained in the updatePools function.
rule growthInsideUnchangedInTickMove() {
    PoolUpdatesHarness.PoolId id;
    address uniV4;
    int24 lower;
    int24 upper;
    int24 prevTick;
    int24 newTick;
    int24 tickSpacing;

    require tickSpacing !=0 , "tick Spacing is never zero";
    require upper % tickSpacing == 0, "tick boundaries are multiples of tickSpacing";
    require lower % tickSpacing == 0, "tick boundaries are multiples of tickSpacing";
    require lower < upper, "tick order";

    bool lowerInitialized = isInitializedCVL(uniV4,id,lower,tickSpacing);
    bool upperInitialized = isInitializedCVL(uniV4,id,upper,tickSpacing);
    require lowerInitialized, "tick boundaries are initialized";
    require upperInitialized, "tick boundaries are initialized";

    // This is what we would like to add, but it's not allowed in CVL
    // require (forall int24 tick. getRewardGrowthOutside(id,tick) > 0 => isInitializedCVL(uniV4,id,tick,tickSpacing));
    // so instead we have a function that generates this assumption for some tick instance and we instantiate it with all the releavnt ticks.
    int24 tickValue1 = normalizeUncheckedCVL(prevTick,tickSpacing);
    int24 tickValue2 = require_int24(tickValue1 + tickSpacing); 
    int24 tickValue3 = require_int24(tickValue1 - tickSpacing); 

    rewardInitializationAssumption(id,tickValue1,uniV4,tickSpacing);
    rewardInitializationAssumption(id,tickValue2,uniV4,tickSpacing);
    rewardInitializationAssumption(id,tickValue3,uniV4,tickSpacing);

    // test values
    // require tickSpacing == 10;
    // require prevTick > 0;
    // require newTick == 17;

    uint256 globalGrowthPre = getGlobalGrowthConst();
    uint256 growthInsidePre = getGrowthInsideHarness(prevTick,lower,upper);
    updateAfterTickMoveHarness(id,uniV4,prevTick,newTick,tickSpacing);
    uint256 growthInsidePost = getGrowthInsideHarness(newTick,lower,upper);
    uint256 globalGrowthPost = getGlobalGrowthConst();

    assert growthInsidePost == growthInsidePre , "growth inside is unchanged";
}

