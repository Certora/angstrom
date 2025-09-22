import "../../contracts/src/modules/PoolUpdates.sol";
//import {IUniV4} from "../../contracts/src/interfaces/IUniV4.sol";
import {Pool} from "../../contracts/lib/v4-periphery/lib/v4-core/src/libraries/Pool.sol";
import {SafeCast} from "../../contracts/lib/v4-periphery/lib/v4-core/src/libraries/SafeCast.sol";
import {PoolManager} from "../../contracts/lib/v4-periphery/lib/v4-core/src/PoolManager.sol";
import {PoolRewards,PoolRewardsLib} from "../../contracts/src/types/PoolRewards.sol";
// import {GrowthOutsideUpdaterHarness} from "./GrowthOutsideUpdaterHarness.sol";
import {Asset} from "../../contracts/src/types/Asset.sol";
// import {TransientPrimitivesLib,tint256} from "contracts/lib/transient-goodies/src/TransientPrimitives.sol";
import {CalldataReader,CalldataReaderLib} from "../../contracts/src/types/CalldataReader.sol";
import {SwapCall} from "../../contracts/src/types/SwapCall.sol";
import {CurrencyDelta} from "../../contracts/lib/v4-periphery/lib/v4-core/src/libraries/CurrencyDelta.sol";

contract PoolUpdatesHarness 
    is 
    PoolUpdates
    {
    
    using IUniV4 for IPoolManager;
    using SafeCast for *;
    // using TransientPrimitivesLib for *;

    constructor(IPoolManager uniV4, address controller)
        UniConsumer(uniV4)
        TopLevelAuth(controller)
    {}

    function _domainNameAndVersion()
        internal
        pure
        override
        returns (string memory, string memory)
    {
        return ("PoolUpdates", "v0");
    }

    function extsload(uint256 slot) external view returns (uint256 value) {
        assembly ("memory-safe") {
            value := sload(slot)
        }
    }

    function updatePools(CalldataReader reader, PairArray pairs) external returns (CalldataReader) {
        return _updatePools(reader, pairs);
    }

    SwapCall _swapCall; 

    function updatePool(CalldataReader reader, SwapCall calldata swapCall, PairArray pairs) external returns (CalldataReader) {
        _swapCall = swapCall;
        return _updatePool(reader,_swapCall,pairs);    
    }

    // IMPORTANT - REVIEW
    function updateRewardsAndDelta(CalldataReader reader, SwapCall calldata swapCall, PoolId id, bool currentOnly) external {
        _swapCall = swapCall;
        
        int24 currentTick = UNI_V4.getSlot0(id).tick();
        uint256 rewardTotal;
        (, rewardTotal) = _decodeAndReward(
            currentOnly, reader, poolRewards[id], id, swapCall.tickSpacing, currentTick
        );
        bundleDeltas.sub(swapCall.asset0, rewardTotal);  //EFFECT - HERE THE DELTAS CHANGE

    }

    function getDeltaOfAsset(address asset) external returns (int256) {
        return bundleDeltas.deltas[asset].get();
    }

    // simulating the process of rewards calculation from beforeRemoveLiquidity
    function simulateRewardsCalculation(
        address sender,
        PoolKey calldata key,
        IPoolManager.ModifyLiquidityParams calldata params
    ) external view returns (uint256) {
        unchecked {
            PoolId id = _toId(key);
            (Position storage position, bytes32 positionKey) =
                positions.get(id, sender, params.tickLower, params.tickUpper, params.salt);
            int24 currentTick = UNI_V4.getSlot0(id).tick();
            uint256 growthInside =
                poolRewards[id].getGrowthInside(currentTick, params.tickLower, params.tickUpper);

            uint128 positionTotalLiquidity = UNI_V4.getPositionLiquidity(id, positionKey);
            uint256 rewards = X128MathLib.fullMulX128(
                growthInside - position.lastGrowthInside, positionTotalLiquidity
            );
        return rewards;
        }
    }

    function getCurrentTick(PoolId id) external view returns (int24) {
        return UNI_V4.getSlot0(id).tick();
    }

    function getGrowthInside(PoolId id, int24 currentTick, int24 tickLower, int24 tickUpper) external view returns (uint256) {
        return poolRewards[id].getGrowthInside(currentTick, tickLower, tickUpper);
    }

    function getRewardGrowthOutside(PoolId id, int24 tick) external view returns (uint256) {
        return poolRewards[id].rewardGrowthOutside[uint24(tick)];
    }
    
    function getGlobalGrowth(PoolId id) external view returns (uint256) {
        return poolRewards[id].globalGrowth;
    }

    function getGlobalGrowthConst() external view returns (uint256) {
        return _poolRewards.globalGrowth;
    }

    function getLastGrowthInside(address sender, PoolId id, IPoolManager.ModifyLiquidityParams calldata params) external view returns (uint256) { 
        (Position storage position, bytes32 _positionKey) =
            positions.get(id, sender, params.tickLower, params.tickUpper, params.salt);
        return position.lastGrowthInside;
    }

    function toId(PoolKey calldata key) external pure returns (PoolId) {
        return _toId(key); 
    }

    function getSwapCallAsset(SwapCall calldata swapCall) external pure returns (address) {
        return swapCall.asset0;
    }

    function getSwapCallId(SwapCall calldata swapCall) external pure returns (PoolId) {
        return swapCall.getId();
    }

    function getPositionLiquidity(address sender, PoolId id, IPoolManager.ModifyLiquidityParams calldata params) external returns (uint128) { 
        (Position storage position, bytes32 positionKey) =
            positions.get(id, sender, params.tickLower, params.tickUpper, params.salt);
        return UNI_V4.getPositionLiquidity(id, positionKey);
    }

    // Returns the total liquidity of a pool given its PoolId
    function getPoolLiquidity(PoolId id) external view returns (uint128) {
        return UNI_V4.getPoolLiquidity(id);
    }

    function getTickLiquidityHarness(PoolId id, int24 tick) external view returns (uint128 liquidityGross, int128 liquidityNet) {
        return UNI_V4.getTickLiquidity(id, tick);
    }

    function getCurrentOnly(PoolUpdateVariantMap self) external view returns (bool) {
        return self.currentOnly();
    }

    function getIsInitialized(PoolId id, int24 tick, int24 tickSpacing) external view returns (bool) {
        return UNI_V4.isInitialized(id, tick, tickSpacing);
    }

    // Harnesses for functions from PoolRewards.sol:

    // the next functions use this constant _poolRewards -- this would be problematic if there are multiple pool rewards that should be considered. 
    PoolRewards _poolRewards; 

    function getGrowthInsideHarness(int24 current, int24 lower, int24 upper)
        external
        returns (uint256 growthInside)
    {
        return PoolRewardsLib.getGrowthInside(_poolRewards, current, lower, upper); // fix
    }
 
    function updateAfterTickMoveHarness(
        PoolId id,
        IPoolManager uniV4,
        int24 prevTick,
        int24 newTick,
        int24 tickSpacing
    ) external {
        PoolRewardsLib.updateAfterTickMove(_poolRewards,id,uniV4,prevTick,newTick,tickSpacing);
    }

    // WHY DOESNT IT COMPILE
    // function getUniswapUserDelta(Currency currency, address target) external view returns (int256) {
    //     return CurrencyDelta.getDelta(currency, target);
    // }
    
    function readBool_harness(CalldataReader self) external pure returns (CalldataReader, bool value) {
        return CalldataReaderLib.readBool(self);
    }

    function readU8_harness(CalldataReader self) external pure returns (CalldataReader, uint8 value) {
        return CalldataReaderLib.readU8(self);
    }

    function readU16_harness(CalldataReader self) external pure returns (CalldataReader, uint16 value) {
        return CalldataReaderLib.readU16(self);
    }

    function readU32_harness(CalldataReader self) external pure returns (CalldataReader, uint32 value) {
        return CalldataReaderLib.readU32(self);
    }

    function readI24_harness(CalldataReader self) external pure returns (CalldataReader, int24 value) {
        return CalldataReaderLib.readI24(self);
    }

    function readU40_harness(CalldataReader self) external pure returns (CalldataReader, uint40 value) {
        return CalldataReaderLib.readU40(self);
    }

    function readU64_harness(CalldataReader self) external pure returns (CalldataReader, uint64 value) {
        return CalldataReaderLib.readU64(self);
    }

    function readU128_harness(CalldataReader self) external pure returns (CalldataReader, uint128 value) {
        return CalldataReaderLib.readU128(self);
    }

    function readAddr_harness(CalldataReader self) external pure returns (CalldataReader, address value) {
        return CalldataReaderLib.readAddr(self);
    }

    function readU160_harness(CalldataReader self) external pure returns (CalldataReader, uint160 value) {
        return CalldataReaderLib.readU160(self);
    }

    function readU256_harness(CalldataReader self) external pure returns (CalldataReader, uint256 value) {
        return CalldataReaderLib.readU256(self);
    }

    function readU24End_harness(CalldataReader self) external pure returns (CalldataReader, CalldataReader) {
        return CalldataReaderLib.readU24End(self);
    }
}