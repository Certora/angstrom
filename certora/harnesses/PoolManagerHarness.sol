import {PoolManager} from "../../contracts/lib/v4-periphery/lib/v4-core/src/PoolManager.sol";
import {PoolKey} from "../../contracts/lib/v4-periphery/lib/v4-core/src/types/PoolKey.sol";
import {PoolId} from "../../contracts/lib/v4-periphery/lib/v4-core/src/types/PoolId.sol";
import {IPoolManager} from "../../contracts/lib/v4-periphery/lib/v4-core/src/interfaces/IPoolManager.sol";
import {Pool} from  "../../contracts/lib/v4-periphery/lib/v4-core/src/libraries/Pool.sol";
import {SafeCast} from "../../contracts/lib/v4-periphery/lib/v4-core/src/libraries/SafeCast.sol";
import {Position} from  "../../contracts/lib/v4-periphery/lib/v4-core/src/libraries/Position.sol";

contract PoolManagerHarness is PoolManager {

    using SafeCast for *;
    using Pool for *;

    constructor(address initialOwner) PoolManager(initialOwner) {} //constructor ok?

    // Harnessing the call to modify liquidity for the pool - without calling the hook and other functionality.
    function poolModifyLiquidityHarness(
        PoolKey memory key,
        IPoolManager.ModifyLiquidityParams memory params,
        bytes calldata hookData
    ) external {
        PoolId id = key.toId();
        {
            Pool.State storage pool = _getPool(id);
            // pool.checkPoolInitialized();

            pool.modifyLiquidity(
                Pool.ModifyLiquidityParams({
                    owner: msg.sender,
                    tickLower: params.tickLower,
                    tickUpper: params.tickUpper,
                    liquidityDelta: params.liquidityDelta.toInt128(),
                    tickSpacing: key.tickSpacing,
                    salt: params.salt
                })
            );
        }
    }

    // Setters for state variables of PoolManager

    function setPoolLiquidity(PoolId id, uint128 newLiquidity) external {
        Pool.State storage pool = _getPool(id);
        pool.liquidity = newLiquidity;
    }

    function setPositionLiquidity(
        PoolId id,
        address owner,
        IPoolManager.ModifyLiquidityParams memory params,
        uint128 newLiquidity
    ) external {
        Pool.State storage pool = _getPool(id);
        bytes32 positionKey = Position.calculatePositionKey(
            owner,
            params.tickLower,
            params.tickUpper,
            params.salt
        );
        Position.State storage position = pool.positions[positionKey];
        position.liquidity = newLiquidity;
    }

    // Setter for position feeGrowthInside0LastX128
    function setPositionFeeGrowthInside0LastX128(PoolId id, bytes32 positionKey, uint256 value) external {
        Pool.State storage pool = _getPool(id);
        Position.State storage position = pool.positions[positionKey];
        position.feeGrowthInside0LastX128 = value;
    }

    // Setter for position feeGrowthInside1LastX128
    function setPositionFeeGrowthInside1LastX128(PoolId id, bytes32 positionKey, uint256 value) external {
        Pool.State storage pool = _getPool(id);
        Position.State storage position = pool.positions[positionKey];
        position.feeGrowthInside1LastX128 = value;
    }

    // Setter for tick liquidityGross
    function setTickLiquidityGross(PoolId id, int24 tick, uint128 value) external {
        Pool.State storage pool = _getPool(id);
        pool.ticks[tick].liquidityGross = value;
    }

    // Setter for tick liquidityNet
    function setTickLiquidityNet(PoolId id, int24 tick, int128 value) external {
        Pool.State storage pool = _getPool(id);
        pool.ticks[tick].liquidityNet = value;
    }


}