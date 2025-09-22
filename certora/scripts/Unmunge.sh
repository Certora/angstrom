git apply -R ./certora/patches/IAngstromAuth.patch
git apply -R ./certora/patches/TopLevelAuth.patch
git apply -R ./certora/patches/PoolConfigStore.patch
git apply -R ./certora/patches/Pair.patch
git apply -R ./certora/patches/PoolUpdates.patch
git apply -R ./certora/patches/Positions.patch
git apply -R ./certora/patches/StoreKey.patch
git apply -R ./certora/patches/SwapCall.patch
cd contracts/lib/v4-periphery/lib/v4-core
git apply -R ../../../../../certora/patches/Position.patch
git apply -R ../../../../../certora/patches/FullMath.patch
cd ../../../../..