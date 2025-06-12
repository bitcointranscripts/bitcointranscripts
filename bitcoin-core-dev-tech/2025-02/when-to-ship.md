---
title: When does Bitcoin Core ship things?
tags:
  - bitcoin-core
date: 2025-02-26
---

## Core Principles

- Shipping requires merging first
- Sufficient review is essential
- Projects can span multiple releases
- Review time varies significantly (e.g., TxDownload: 5 months vs. leveldb changes: quick)

## Review Process

- Quality and source of ACKs matter
- Performance testing and reviews are important
- Need for more nuanced Concept ACKs/NACKs
- "Letting code bake" in master rarely uncovers major issues
- More RC testers could enable later-stage merges if we wanted

## Release Cycle Decisions

- Release scheduling influences merge timing
- Feature freeze cutoffs are typically maintainer decisions
- Time-based release cycle is somewhat flexible

## External Factors

- Project faces external pressure to ship features
- Some external pressure is considered healthy
- Project must balance external requests with maintenance burden

## Challenges

- Long review wait times
- Difficulty in getting explicit NACKs
- Balancing timely shipping with quality assurance
