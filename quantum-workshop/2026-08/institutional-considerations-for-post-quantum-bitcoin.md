---
title: Institutional Considerations for Post-Quantum Bitcoin
transcript_by: Localhost Research
date: 2026-08-28
weight: 3
tags:
  - quantum
  - cryptography
  - custody
speakers:
  - Yehuda Lindell
additional_resources:
  - title: Slides
    url: https://btctranscripts.com/bitcoin-transcript/quantum-workshop/2026-08/institutional-considerations-for-post-quantum-bitcoin-slides.pdf
---

_For slides, please see the 'Extra Info' tab_

*(Background: started in pure theoretical cryptography, then moved into industry and applied work. This talk covers concerns at Coinbase and institutionally in general.)*

### What Customers Are Saying

- **Customers can't distinguish signal from noise.** (They want to see you in a Gartner report precisely because they can't evaluate the noise themselves.)
- Reframing the timeline question: it's not *"when will quantum computers arrive?"* but *"with what confidence can we bound the risk in a given time range?"* If you can't rule it out with ~100% confidence, there's some percentage risk the entire ecosystem collapses.
- **Conclusion: if it can happen, we need to move now.**
- Real-world impact already visible: investors and institutional customers are concerned enough that it's **dampening involvement and investment** — pulling out or not investing at all.
- **The biggest risk is inaction.** What customers need to see is a plan, people working on solutions, and actual solutions. Ethereum has a roadmap; Bitcoin is much harder — which is why the current activity (BIPs being published) matters so much for customer confidence.

### The Institutional Challenge: Scale and Constraints

- Many blockchains to support; many different signature schemes.
- **Institutions cannot move quickly** — system changes must be disclosed to regulators and some customers.
- Asset migration, operational, and security challenges all require extreme care. The stakes are enormous: custodians hold people's savings and livelihoods.
- Three ownership models to think about: **self-custody / custody / non-custodial (e.g., shared custody).**

### MPC and Threshold Signing in a PQ World

- MPC/threshold signing is used heavily in custodial settings to prevent single points of failure: keys split across multiple machines and **three environments** — cloud, employee devices, and an offline machine in a private datacenter.
- **MPC is crucial to the non-custodial model** — but not every signature scheme has an efficient MPC protocol.
- **For lattices:** with focused community effort, Lindell believes efficient MPC protocols can be built.
- **For hash-based signatures: a different story.**
  - Plain multisig doesn't support key rotation/refresh (proactive security) — you'd have to move funds on-chain, revealing your quorum.
  - *(Audience: what about Shamir?)* — That only covers key generation, not signing.

**Case study: MPC for SLH-DSA**
- Generic approach: translate signing into a Boolean circuit. Not every hash operation needs to be private, but the count is still enormous.
- Even at 32 bytes per AND gate, you're looking at **~66 GB of communication per signing operation**.
- **Not feasible** except in very limited contexts. Something better for hash-based schemes *might* exist — but it's a maybe, with low confidence.
- Potential alternative directions: **MPC-in-the-head / ZK-based** approaches, or other signature families.

> **Bottom line:** the "safest" signature scheme doesn't necessarily get you to the most secure place. Securing Bitcoin doesn't just mean securing the protocol — it means securing the keys. So: did we actually land in the optimal place?

### Stateless vs. Stateful — an Operational View

- **Stateless** is what institutions expect: signature is a function of key and message only. Back up the key once; sign forever, in parallel, multiple times — you don't care.
- **Stateful:** a mistake means big trouble. Security assumes you can verify that state storage *succeeded* and was never rolled back or deleted.
- Institutionally: multiple server instances operate independently. With state that must be replicated, **this architecture has to completely change**. The theory exists, but it's hard to implement.
- Transactions requiring multiple signatures from a single key would become sequential (or need special handling).
- *"I can say from experience: we have lost sync on state."* That cannot be allowed to happen here. The scary case isn't *knowing* you lost state — it's **not knowing**.
- Mitigation: **hybrid schemes until Q-Day**.

### There Is No Single Good Choice

- Once you look beyond the protocol to the ecosystem, everything gets fuzzy. As Ross Anderson said: *"more security is less security."*
- Open questions posed to the room:
  - Do we have time to wait for advanced MPC?
  - Should Bitcoin support **many signing schemes**? (E.g., 1-of-N addresses with different key types, all keys hashed until used — so a vulnerability in an unused type doesn't affect security.)
  - If no solution is good for everyone, what's the impact of a solution that's good for X but bad for Y?
  - If we start with stateful hash-based, do we preserve the option to move to something more advanced?
  - Should we look for **MPC-friendly hash-based schemes**, or MPC protocols for SHRINCS-like schemes? A question for this room *and* the broader cryptographic community.

### Q&A

**Q: Hybrid schemes seem popular — what are the downsides?**
- **Additional complexity is usually the enemy.** More options means the weakest link will be broken.

**Comment (audience): on Bitcoin's security model**
- We should think about the security assumptions that secure Bitcoin *as a whole*. Introducing weaker schemes becomes an existential risk. Pragmatically some optionality may be needed, but **we should not add a scheme to Bitcoin unless we're confident it will remain secure**.

**Q: If a PQ algorithm ships in ~3 years, will Coinbase require both signature schemes per address to hedge against the novel scheme?**
- *"Whatever happens, we will support it."* Bottom line: Coinbase has to support every asset. Even if Bitcoin picks something requiring 1B hash operations per signature — they'll support it. It's not pretty, but workable: e.g., **invert the architecture so MPC servers encrypt their output under a PQ encryption key and feed it to an offline device for signing.**
