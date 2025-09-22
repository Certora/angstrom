methods {
    function PoolManagerHarness.extsload(bytes32 slot) external returns (bytes32) => NONDET DELETE;
    function PoolManagerHarness.extsload(bytes32[] slots) external returns (bytes32[] memory) => ArbBytes32(slots) DELETE;
    function PoolManagerHarness.extsload(bytes32 startSlot, uint256 nSlots) external returns (bytes32[] memory) => ArbNBytes32(startSlot, nSlots) DELETE;
    function PoolManagerHarness.exttload(bytes32[] slots) external returns (bytes32[] memory) => ArbBytes32(slots) DELETE;

    function IUniV4.getPoolLiquidity(address manager, PoolManager.PoolId id) internal returns (uint128) => getActiveLiquidity(manager, id);
    function IUniV4.getTickLiquidity(address manager, PoolManager.PoolId id, int24 tick) internal returns (uint128, int128) => getTickLiquidityExt(manager, id, tick);
    function IUniV4.getPositionLiquidity(address manager, PoolManager.PoolId id, bytes32 positionKey) internal returns (uint128) => getPositionLiquidityExt(manager, id, positionKey);
    function IUniV4.getSlot0(address manager, PoolManager.PoolId poolId) internal returns (PoolManager.Slot0) => getSlot0Direct(manager, poolId);
    function IUniV4.getPoolBitmapInfo(address manager, PoolManager.PoolId id, int16 wordPos) internal returns (uint256) => getPoolBitmapInfoExt(manager, id, wordPos);
    
    // function IUniV4.gudExtsload(address manager, uint256 slot) internal returns (uint256) => NONDET;

    // function PoolGetters.getSqrtPriceX96(PoolManager.PoolId poolId) external returns (uint160) envfree;
    // function PoolGetters.getTick(PoolManager.PoolId poolId) external returns (int24) envfree;
    // function PoolGetters.getProtocolFee(PoolManager.PoolId poolId) external returns (uint24) envfree;
    // function PoolGetters.getLpFee(PoolManager.PoolId poolId) external returns (uint24) envfree;
    // function PoolGetters.getLiquidity(PoolManager.PoolId poolId) external returns (uint128) envfree;
    // function PoolGetters.getPositionLiquidity(PoolManager.PoolId poolId, bytes32 positionId) external returns (uint128) envfree;
    // function PoolGetters.getTickLiquidity(PoolManager.PoolId poolId, int24 tick) external returns (uint128, int128) envfree;
    // function PoolGetters._getSlot0(PoolManager.PoolId poolId) internal returns (bytes32) => getSlot0Direct(poolId);
}

/// Returns an arbitrary bytes32 array with the same length as the slots input array.
function ArbBytes32(bytes32[] slots) returns bytes32[] {
    bytes32[] data;
    require data.length == slots.length;
    return data;
}

/// Returns an arbitrary bytes32 array of length nSlots.
function ArbNBytes32(bytes32 startSlot, uint256 nSlots) returns bytes32[] {
    bytes32[] data;
    require data.length == nSlots;
    return data;
}

/// Getters of the pool state using direct storage access.
function getTickLiquidityExt(address manager, PoolManager.PoolId poolId, int24 tick) returns (uint128,int128) {
    require manager == PoolManager;
    return (PoolManager._pools[poolId].ticks[tick].liquidityGross, PoolManager._pools[poolId].ticks[tick].liquidityNet);
    
    // if (manager == PoolManagerA) {
    //     return (PoolManagerA._pools[poolId].ticks[tick].liquidityGross, PoolManagerA._pools[poolId].ticks[tick].liquidityNet);
    // } else if (manager == PoolManagerB) {
    //     return (PoolManagerB._pools[poolId].ticks[tick].liquidityGross, PoolManagerB._pools[poolId].ticks[tick].liquidityNet);
    // } else {
    //     return (PoolManager._pools[poolId].ticks[tick].liquidityGross, PoolManager._pools[poolId].ticks[tick].liquidityNet);
    // }
}

function getActiveLiquidity(address manager, PoolManager.PoolId poolId) returns uint128 {
    require manager == PoolManager;
    return PoolManager._pools[poolId].liquidity;
    
    // if (manager == PoolManagerA) {
    //     return PoolManagerA._pools[poolId].liquidity;
    // } else if (manager == PoolManagerB) {
    //     return PoolManagerB._pools[poolId].liquidity;
    // } else {
    //     return PoolManager._pools[poolId].liquidity;
    // }
}

function getPositionLiquidityExt(address manager, PoolManager.PoolId poolId, bytes32 positionId) returns uint128 {
    require manager == PoolManager;
    return PoolManager._pools[poolId].positions[positionId].liquidity;
    
    // if (manager == PoolManagerA) {
    //     return PoolManagerA._pools[poolId].positions[positionId].liquidity;
    // } else if (manager == PoolManagerB) {
    //     return PoolManagerB._pools[poolId].positions[positionId].liquidity;
    // } else {
    //     return PoolManager._pools[poolId].positions[positionId].liquidity;
    // }
}

function getSlot0Direct(address manager, PoolManager.PoolId poolId) returns PoolManager.Slot0 {
    require manager == PoolManager;
    return PoolManager._pools[poolId].slot0;
    
    // if (manager == PoolManagerA) {
    //     return PoolManagerA._pools[poolId].slot0;
    // } else if (manager == PoolManagerB) {
    //     return PoolManagerB._pools[poolId].slot0;
    // } else {
    //     return PoolManager._pools[poolId].slot0;
    // }
}

function getPoolBitmapInfoExt(address manager, PoolManager.PoolId poolId, int16 wordPos) returns uint256 {
    require manager == PoolManager;
    return PoolManager._pools[poolId].tickBitmap[wordPos];
    
    // if (manager == PoolManagerA) {
    //     return PoolManagerA._pools[poolId].tickBitmap[wordPos];
    // } else if (manager == PoolManagerB) {
    //     return PoolManagerB._pools[poolId].tickBitmap[wordPos];
    // } else {
    //     return PoolManager._pools[poolId].tickBitmap[wordPos];
    // }
}
