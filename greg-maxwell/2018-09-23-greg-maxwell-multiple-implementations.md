---
title: Multiple Implementations 
speakers: ['Greg Maxwell']
transcript_by: Michael Folkson
date: 2018-09-23
---

Location: Bitcointalk

https://bitcointalk.org/index.php?topic=5035144.msg46077622#msg46077622

# Risks of multiple implementations

They would create more risk. I don't think there is any reason to doubt that this is an objective fact which has been borne out by the history.

First, failures in software are not independent. For example, when BU nodes were crashing due to xthin bugs, classic were also vulnerable to effectively the same bug even though their code was different and some triggers that would crash one wouldn't crash the other. There have been many other bugs in Bitcoin that have been straight up replicated many times, for example the vulnerable to crash through memory exhaustion due to processing loading a lot of inputs from the database concurrently: every other implementation had it to, and in some it caused a lot more damage.

Even entirely independently written software tends to have  similar faults:

“By assuming independence one can obtain ultra-reliable-level estimates of reliability even though the individual versions have failure rates on the order of 10^-4. Unfortunately, the independence assumption has been rejected at the 99% confidence level in several experiments for low reliability software.

Furthermore, the independence assumption cannot ever be validated for high reliability software because of the exorbitant test times required. If one cannot assume independence then one must measure correlations. This is infeasible as well—it requires as much testing time as life-testing the system because the correlations must be in the ultra-reliable region in order for the system to be ultra-reliable. Therefore, it is not possible, within feasible amounts of testing time, to establish that design diversity achieves ultra-reliability. Consequently, design diversity can create an “illusion” of ultra-reliability without actually providing it.”

https://tatourian.blog/2016/11/19/building-ultra-reliable-software/

More critically, the primary thing the Bitcoin system does is come to consensus:  Most conceivable bugs are more or less irrelevant so long as the network behaves consistently.  Is an nlocktime check a < or a <= check? Who cares... except if nodes differ the network can be split and funds can be taken through doublespending the reorg.  Are weird "hybrid pubkeys" allowed? Who cares... except if nodes differ the network can be split and funds can be taken through doublespending the reorg.  What happens when a transaction has a non-nonsensical signature that indicates sighash single without a matching output? Who cares... except if nodes differ the network can be split and funds can be taken through doublespending the reorg. And so on.  For the vast majority of potential bugs having multiple incompatible implementations turns a non-event into a an increasingly serious vulnerability.

Even for an issue which isn't a "who cares" like allowing inflation of the supply adding a surprise disagreement between nodes does not help matters!  The  positive effect it creates is that you might notice it after the fact faster but for that benefit you don't actually need additional full implementations, just monitoring code.  In the case of CVE-2018-17144 the sanity checks on node startup would also detect the bad block. On the negative, they just cause a consensus split and result in people being exposed to funds loss in a reorg-- which is the same kind of exposure that they'd have in a single implementation + monitoring then fixing the issue when detected, other than perhaps the reorg(s) might be longer or shorter in one case or another.

In this case ABC also recently totally reworked the detection of double spends as a part of their "canonical transaction order" changes which require that double spending checks be differed and run as a separate check after processing because transactions are required to be out of their logical casual ordering.  Yet they both failed to find this bug as part of testing that change and also failed to accidentally fix it.

Through all the history of Bitcoin, altcoin forks copying the code, other reimplementations and many other consensus bugs, some serious and some largely benign,  this is the first time someone working on another serious implementation that someone actually uses has actually found one.  I might be forgetting something, but I'm certainly not forgetting many. Kudos to awemany. In all other cases they either had the same bugs without knowing it, or accidentally fixed it creating fork risk creating vulnerability without knowing it. It also isn't like there being multiple implementations is new-- for the purpose of this point every one of the 1001 altcoins created by copying the Bitcoin code count as a separate implementation too, or at least the ones which are actively maintained do.

Having more versions also dilutes resources, spreading review and testing out across other implementations. For the most part historically the Bitcoin project itself hasn't suffered much from this: the alternatives have tended to end up just barely maintained one or two developer projects (effectively orphaning users that depended on them, -- another cost to that diversity) and so it doesn't look like they caused much meaningful dilution to the main project.  But it clearly harms alternatives, since they usually end up with just one or two active developers and seldom have extensive testing.  Node diversity also hurts security by making it much more complicated to keep confidential fixes private. When an issue hits multiple things its existence has to be shared with more people earlier, increasing the risk of leaks and coincidentally timed cover changes can give away a fix which would otherwise go without notice. In a model with competing implementations some implementers might also hope to gain financially by exploiting their competitions bugs, further increasing the risk of leaks.

Network effects appear to have the effect that in the long run one one or maybe a few versions will ultimately have enough adoption to actually matter. People tend to flock to the same implementations because they support the features they need and can get the best help from others using the same stuff. Even if the benefits didn't usually fail to materialize, they'd fail to matter through disuse.

Finally, diversity can exist in forms other than creating more probability disused, probably incompatible implementations.  The Bitcoin software project is a decentralized collaboration of dozens of regular developers.  Any one of the participants there could go and make their own implementation instead (a couple have, in addition to).  The diversity of contributors there do find and fix and prevent LOTS of bugs, but do so without introducing to the network more incompatible implementations.   That is, in fact, the reason that many people contribute there at all: to get the benefit of other people hardening the work and to avoid damaging the network with potential incompatibilities.

All this also ignores the costs of implementation diversity unrelated to reliability and security, such as the redundancy often making improvements more expensive and slow to implement.

TLDR: In Bitcoin the system as a whole is vulnerable to disruption of any popular implementation has a consensus bug: the disruption can cause financial losses even for people not running the vulnerable software by splitting consensus and causing reorgs. Implementations also tend to frequently reimplement the same bugs even in the rare case where they aren't mostly just copying (or transliterating) code, which is good news for staying consistent but means that even when consistency isn't the concern the hoped-for benefit usually will not materialize. Also network effects tend to keep diversity low regardless, which again is good for consistency, but means but bad for diversity actually doing good. To the extent that diversity can help, it does so primarily through review and monitoring which are better achieved through collaboration on a smaller number of implementations.
