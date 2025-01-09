---
title: Long-Term Mining Incentives
date: 2024-11-19
---

## Brainstorming (Sticky Notes):

- Large holders free-riding security
- No more mempool APIs only
- All fees are out of band
- Mining wars between nation-states
- Constant reorgs
- Forks (not consensus change)
- Race to the bottom between miners sending each other long to validate blocks
- No more hashrate
- SPV mining
- Fail to converge
- “Gap games” + coin hopping
- Chain halts: miners know they will get reorged out, give up mining
- Collapse of the galactic economy
- Use all the world’s energy
- Quantum computers may make hashrate not linear with power

_Not gonna consider bugs such as timewarp or extreme validation times._

## Discussion Points

### Tail Emission

- The emission can’t be linear as it’s logarithmic eventually.
- What you want is a fixed inflation as a percentage of the supply.
- Alternative solution: demurrage (the value of coin decreases over time).

### Demand for Block Space

- **Possibility**: There may be no demand for block space anymore.
- Observation: There seems to be a baseline demand for storing garbage.

### Decreasing Purchasing Power

- Scenario: Purchasing power decreases significantly but smoothly.
  - _In 100 years, 1 BTC might only buy a bottle of water._
- **Consensus in the group**: It’s OK if people don’t want to use Bitcoin anymore.
  - Purchasing power of BTC decreases, or block space demand diminishes
  - If it’s a shock and not gradual it would be a pretty bad outcome for holders.

## Exploring Use Cases:

### Proof of IDLE

- _Check the paper._

### ETF Scaling

- **Question**: What if people don’t have demand for block space anymore?
- **Discussion**: Is it a bad outcome?

### Bitcoin for Settlement Between Countries

- Hypothesis: Countries that don’t trust each other might use Bitcoin for settlement.
- Counterpoint: They might as well use the BIS.
  - BIS is trusted, but there is alwayss the threat of war which keeps them honest.
  - **Question**: Is Bitcoin really useful for this use case?

## Preventing Bad Outcomes:

- **Avoid MEV / APIs**:
  - APIs are not inherently bad but may indicate systemic issues.
  - Ethereum has transitioned to being "all APIs" with no mempool anymore.
- **Keep Open Source / Verifiability**.
- **Big Consensus Changes**:
  - Can we transition to PoS?
    - Some believe PoS isn’t interesting; if trusting a third party is necessary, a transparently trusted system might suffice.
- **Incentives Against Custodians**:
  - _“Just ban Bitcoin :)”_

## Defining the "Long-Term":

- Two generations, ~100 years.
