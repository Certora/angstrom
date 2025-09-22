git apply ./certora/patches/IAngstromAuth.patch
git apply ./certora/patches/TopLevelAuth.patch
git apply ./certora/patches/PoolConfigStore.patch
git apply ./certora/patches/Pair.patch
git apply ./certora/patches/PoolUpdates.patch
git apply ./certora/patches/Positions.patch
git apply ./certora/patches/StoreKey.patch
git apply ./certora/patches/SwapCall.patch
cd contracts/lib/v4-periphery/lib/v4-core
git apply ../../../../../certora/patches/Position.patch
git apply ../../../../../certora/patches/FullMath.patch
cd ../../../../..