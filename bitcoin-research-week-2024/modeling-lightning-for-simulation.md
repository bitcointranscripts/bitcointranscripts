---
title: Modeling Lightning for Simulation
date: 2024-11-21
---

## How can we achieve the most realistic simulations?

- **Ad-hoc Simulations for Individuals**:
  How can we develop a framework that better suits everyone's needs?
  Each paper uses its own simulations. It would be better to have a unified solution that is broadly applicable.

- The research papers differ significantly in what they measure, leading to the use of custom simulations (e.g., pathfinding, routing, and other models).
  While different use cases might justify this variation, we still need a unified strategy.

- **Unified Simulations**:
  It should be possible to simulate these scenarios more systematically. For instance, _Warnet_ can provide a uniform simulation framework. It shares similarities with _Polar_ but focuses more on specific lightning network simulations, while tools like _Simln_ generate payment scenarios for the Lightning Network.

## Simulation Challenges

1.  **Data Availability and Usage:**

    - Some nodes share limited public data.

    - Simulation challenges include topology, capacity, policies, and node availability.

    - Node availability can be inferred when peers mark all channels as disabled via gossiping.

    - Using probabilistic methods may help estimate availability.

2.  **Balance Probing and Validation:**

    - Reliable balance data is often unavailable, complicating validation.

    - While balance probing can help determine balance distribution, _River might_ provide supplementary data.

    - Assuming one direction channel balance often improves routing but may not reflect reality.

3.  **Privacy and Model Use Cases:**

    - Models can evaluate privacy, routing, and new feature implementations.

    - Claims that Lightning can process a million payments per second are often exaggerated.

    - Accurate throughput measurement is essential to assess network changes.

4.  **Overfitting Risks and Data Handling:**

    - Avoid overfitting by using generic data or randomized datasets where specific data is unavailable.

    - Use mutations of current data to validate results.

5.  **Stress Testing:**

    - Stress testing helps evaluate network resilience under adverse conditions.

    - Researchers should adopt a holistic perspective, analyzing the network as a whole.

## Simulation Best Practices

- Cluster data by graph neighborhoods. If data is limited for certain neighborhoods, validate simulations within those and acknowledge uncertainties elsewhere.

- Use _Warnet_ to spin up Lightning nodes and _Simln_ to generate payments.

- Explore attack scenarios (e.g., AS-level attacks) using these tools to understand vulnerabilities.

  - _Warnet_'s AS mapping is useful not only for Lightning but also for Bitcoin core nodes.

## Challenges in Modeling Lightning Network Payments

1.  **Node Categorization:**

    - Accurate categorization of nodes is difficult as nodes don't self-identify their roles.

    - Collaboration with companies like _CashApp_ may help classify nodes.

2.  **Payment Flows:**

    - The Lightning Network has diverse payment flows. Achieving realistic models requires node categorization and balance distribution analysis.

## Data Sources and Feature Requests for Simln

1.  **Desired Data:**

    - From sources like _CashApp_, _River_, and personal nodes.

    - Publicly available data.

2.  **Feature Requests for Simln:**

    - JSON support for network topology.

    - Node classification based on inbound payments and balance distribution.

    - Scaling functionality for large networks.

    - Dynamic topology generation and payment configurations.

3.  **Integration Options:**

    - _Simln_ should be able work independently or with _Warnet_.

    - While _Simln_ handles payment simulations, dynamic topology generation scripts can complement it in a _Warnet_ scenario.

![Flipchart1](https://raw.githubusercontent.com/bitcointranscripts/media/refs/heads/main/bitcoin-research-week-2024/modeling-lightning-for-simulation/flipchart1.jpg)

![Flipchart2](https://raw.githubusercontent.com/bitcointranscripts/media/refs/heads/main/bitcoin-research-week-2024/modeling-lightning-for-simulation/flipchart2.jpg)

![Flipchart3](https://raw.githubusercontent.com/bitcointranscripts/media/refs/heads/main/bitcoin-research-week-2024/modeling-lightning-for-simulation/flipchart3.jpg)
