## Verification Overview

The current directory contains Certora's formal verification of the Angstrom protocol.

In this directory you will find several subdirectories:

1. **specs** - Contains all the specification files that were written by Certora for the Angstrom protocol. Some files merely contain definitions or functions that serve as summarizations. They are being used in the primary specs that contain rules. The different specification files are described below.

2. **helpers** - Contains helper contracts that either introduce new Solidity getter functions, or contracts that serve as tests for libraries, i.e. they implement an external function that calls internal library functions.

3. **patches** - Contains a list of git patch files that record changes to the source code, which are applied before the verification in order to resolve some Prover technical issues.
   It's worth noting that these modifications to the code are rather minor and are needed to bypass some internal analysis issues.
   Essentially, they do not change the meaning of the code, as they replace the optimized inline-assembly with its original Solidity counterpart. The equivalence between the two verions could be easily proven.
   In order to apply/revert the patches, one could simply run the munge/unmungh.sh script located in the scripts sub directory.

4. **confs** - Contains Prover configuration files for the verification of different contracts in this repository. 

5. **scripts** - Contains the scripts to apply and remove munges, and a script to run configuration files. 

</br>

## Certora Prover installation Instructions

Refer to the Certora Prover official docs for installing it:
https://docs.certora.com/en/latest/docs/user-guide/install.html

General running instrcutions could also be found in the docs:
https://docs.certora.com/en/latest/docs/user-guide/running.html

## Running Instructions

To run a verification job:

1. Open terminal and `cd` your way to the main directory in the Angstrom repository.

2. Run:

```sh
    certora/scripts/CertoraRunScript <conf_file>
```

Where <conf_file> stands for the name of the configuration file from certora/confs, for example `solvency.conf`.

</br>


## Scope of the Verification 

The contracts in scope of the verification are:
- `PoolRewards.sol`
- `GrowthOutsideUpdater.sol`
- `PoolUpdates.sol`

## Summarizations and Patches

To simplify formal verification, we apply summarizations and patches. Summaries replace any function call with a call to the summarizing CVL function, these are given in **specs/summaries**. Patches apply a change to the original code to simplify behavior, these are done when summaries are not possible. Most patches we make replace assembly code with equivalent non-assembly code, these are given in **patches**.

## Specifications

### PoolRewardsProperties.spec

- **growthInsideUnchangedInTickMove**: verifies that calls to `getGrowthInside` give the same value before and after calls to `updateAfterTickMove`. 

### Solvency.spec

We consider a solvency property that should be preserved when `updatePools` is called. For this, we have a harness function `updateRewardsAndDelta` that harnesses the relevant functionality from `_updatePool`. The rules aim to show that the sum of all liquidity providers' rewards and the Angstrom delta is unchanged upon calls to `updateRewardsAndDelta`. Given this does not hold we settle for showing that this sum can only be decreased - which favors the Angstrom contract. 
This is checked for 4 scenarios: 
- **updatePoolSolvencyEqCurrentOnly1LP**: considers 1 liquidity provider, and reward distribution to the current tick, and aims to show equality of the sum of solvency components before and after the call.
- **updatePoolSolvencyLeqCurrentOnly1LP**: considers 1 liquidity provider, and reward distribution to the current tick, and aims to show the sum of solvency components can only be decreased.
- **updatePoolSolvencyLeqCurrentOnly2LPs**: considers 2 liquidity providers, and reward distribution to the current tick, and aims to show the sum of solvency components can only be decreased.
- **updatePoolSolvencyLeqNotCurrentOnly1LP**: considers 1 liquidity provider, and reward distribution below/above the current tick (including), and aims to show the sum of solvency components can only be decreased.

### Hooks.spec

We consider different properties that should be satisfied by the hooks `beforeAddLiquidity` and `beforeRemoveLiquidity` and their relation to reward calculation. To do this we have a harness function `simulateRewardsCalculation` that harnesses the rewards calculation from `beforeRemoveLiquidity`. 
Properties of the hooks should be considered in the context in which the hooks are called, namely, modifying liquidity. For this, we have the CVL function `modifyLiquiditySummaryCVL` that manualy modifies the pool and position liquidities (without calling PoolManager's modifyLiquidity - which is too difficult for the prover). 

Adding liquidity should not change rewards, we check this in two rules:
- **addLiquidityDoesNotIncreaseRewards**: adding liquidity and calling the hook does increase the rewards.
- **addLiquidityDoesNotDecreaseRewards**: adding liquidity and calling the hook does decrease the rewards, which is less problematic.

Other integrity rules:
- **noRewardsForNewPosition**: adding liquidity to an empty position and then taking rewards does not give any rewards.
- **noRewardsAfterRemoval**: removing liquidity twice does not grant extra rewards.
- **noRewardsAfterAdditionsToTwoNewPositions**: adding liquidity to two empty positions cannot create rewards. This rule was designed to identify a bug in an older version of the protocol (Issue 5.1.1 in Spearbit's audit)