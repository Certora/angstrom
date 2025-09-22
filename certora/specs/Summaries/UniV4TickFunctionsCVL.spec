methods {
    function TickLib.normalizeUnchecked(int24 tick, int24 tickSpacing) internal returns (int24)
        => normalizeUncheckedCVL(tick, tickSpacing);
    function IUniV4.getNextTickGt(address self, PoolUpdatesHarness.PoolId id, int24 tick, int24 tickSpacing) internal returns (bool, int24) 
        => getNextTickGtCVL(self, id, tick, tickSpacing);
    function IUniV4.getNextTickLt(address self, PoolUpdatesHarness.PoolId id, int24 tick, int24 tickSpacing) internal returns (bool, int24) 
        => getNextTickLtCVL(self, id, tick, tickSpacing);
    function IUniV4.getNextTickLe(address self, PoolUpdatesHarness.PoolId id, int24 tick, int24 tickSpacing) internal returns (bool, int24) 
        => getNextTickLeCVL(self, id, tick, tickSpacing);
    function IUniV4.isInitialized(address self, PoolUpdatesHarness.PoolId id, int24 tick, int24 tickSpacing) internal returns (bool)
        => isInitializedCVL(self,id,tick,tickSpacing);
}

// ghost mapping that holds the values for isInitialized - and does not change unless something havocs

ghost mapping (address => mapping(PoolUpdatesHarness.PoolId => mapping (int24 => mapping (int24 => bool)))) isInitializedGhost;
//write hook that when liquidity is added for a tick then this becomes true.
// CURRENTLY UNSOUND.

function isInitializedCVL(address self, PoolUpdatesHarness.PoolId id, int24 tick, int24 tickSpacing) returns bool {
    return isInitializedGhost[self][id][tick][tickSpacing];
}

// is the treatment of the underflow proper? are we reverting in the same occasions?
function normalizeUncheckedCVL(int24 tick, int24 tickSpacing) returns int24 {
    mathint remainder = tick % tickSpacing;
    mathint quotient = tick / tickSpacing;
    mathint quotient_fixed;

    if (remainder < 0) {
        require quotient_fixed == quotient - 1, "round down for negatives";
    }
    else {
        require quotient_fixed == quotient, "otherwise keep as is";
    }

    int24 res = require_int24((quotient_fixed * tickSpacing)); //maybe not accurate?
    return res;
}

// more imprecise abstractions
function normalizeUncheckedImprecise(int24 tick, int24 tickSpacing) returns int24 {
    int24 res;
    int24 quotient;
    require res <= tick, "always normalizesd down"; 
    require res > tick - tickSpacing, "can't normalize more than tickSpacing"; 
    require res == quotient * tickSpacing, "result is a multiple of tickSpacing"; 
    return res;
}

function normalizeUncheckedImprecise2(int24 tick, int24 tickSpacing) returns int24 {
    int24 res;
    require res <= tick, "always normalizesd down"; 
    require res > tick - tickSpacing, "can't normalize more than tickSpacing"; 
    return res;
}

function getNextTickGtCVL(address self, PoolUpdatesHarness.PoolId id, int24 tick, int24 tickSpacing) returns (bool,int24) {
    int24 nextTick;
    require nextTick > tick, "nextTick increases";
    require nextTick <= tick + tickSpacing, "nextTick increases at most tickSpacing";
    require nextTick % tickSpacing == 0, "nextTick is a multiple of tickSpacing";
    bool initialized = isInitializedCVL(self,id,nextTick,tickSpacing);
    return (initialized, nextTick);
}

function getNextTickLtCVL(address self, PoolUpdatesHarness.PoolId id, int24 tick, int24 tickSpacing) returns (bool,int24) {
    int24 nextTick;
    require nextTick < tick, "nextTick decreases";
    require nextTick >= tick - tickSpacing, "nextTick decreases at most tickSpacing";
    require nextTick % tickSpacing == 0, "nextTick is a multiple of tickSpacing";
    bool initialized = isInitializedCVL(self,id,nextTick,tickSpacing);
    return (initialized, nextTick);
}

function getNextTickLeCVL(address self, PoolUpdatesHarness.PoolId id, int24 tick, int24 tickSpacing) returns (bool,int24) {
    int24 nextTick;
    require nextTick <= tick, "nextTick decreases or equal";
    require nextTick > tick - tickSpacing, "nextTick decreases at most tickSpacing";
    require nextTick % tickSpacing == 0, "nextTick is a multiple of tickSpacing";
    bool initialized = isInitializedCVL(self,id,nextTick,tickSpacing);
    return (initialized, nextTick);
}
