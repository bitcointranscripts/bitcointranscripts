---
title: Present And Future Tech Challenges In Bitcoin
transcript_by: Bryan Bishop
tags:
  - contract-protocols
speakers:
  - Peter Todd
  - Adam Back
  - Pierre Roberge
---
1 on 1: Present and future tech challenges in bitcoin

<https://twitter.com/kanzure/status/1043484879210668032>

PR: Hi everybody. I think I have the great fortune to moderate this panel in the sense that we have really great questions thought by the organizers. Essentially we want to ask Adam and Peter what are their thoughts on the current and the future tech challenges for bitcoin. I'm just going to start with that question, starting with Peter.

PT: Oh, we better have a good answer for this one. There's a lot of excitement around ethereum smart contracts and I think all of that hype will move to bitcoin. I think we have a good handle for simple ways to send money on bitcoin, although we don't for scalably sending money and we don't have a good handle on complex integration into other systems. The recent double spending bug was a good example. How do we get better programming practices to make this tech easier to develop and write code for and get it right the first time? I don't necessarily have all the answers there but I think it's going to be a big challenge in how we are going to go forward.

AB: We had the scaling debate already. I'd sooner see a privacy and fungibility debate next. There's dandelion. Also more privacy coming from Schnorr signatures and taproots to make more transactions look uniform. The bigger question for me is whether in the future we can get confidential transactions actually involved in bitcoin directly, and the debate tha twould arise around that because it's a tradeoff- the transactions are bigger. There's some technical discussions about how that works, and then also a discussion about whether the wider community wants that. In some discussions, I've seen like on reddit there was a big discussion thread on this. They wanted more fungibility nad privacy on bitcoin but that's just one segment of the community.

PR: Let's start with confidential transactions. You were explaining to me Adam that the compromise or tradeoffs in confidential transactions tha tit's baed on discrete log and Schnorr... in the future, when, and if discrete log were to be broken, depending on design decisions we take now, it could either mean privacy could be gone and revealed for the past transactions or we could have an inflationary problem or double spending. Could you elaborate on this?

AB: It seems to be a fairly fundamental limit that you can either have perfect privacy so that if in the far future the discrete log for the key size bitcoin uses gets broken, it would either break privacy. Confidential transactions only encrypts the values, it doesn't obscure the addresses. It would revert the privacy and it would revert to the current play where the values are in cleartext anyway. If you take privacy in paramount and if discrete log is broken in the future then it would blow up the whole coin because it would allow undetectable inflation which would render the coin pointless at this point. I would favor losing privacy in the evnet of the failure because keeping the supply cap is very fundametal to bitcoin.

PT: I'd favor losing the supply cap. You can't place a price on people's freedom. If you lose bitcoin, you can put a price on that. But if you lose privacy, people's lives are affected. They could end up in jail or whatever.

PR: For all of this to happen, somehow we need to reach consensus at a high level. Just passing segwit was crazy and long. How do you guys see that unfolding the next potential upgrade to bitcoin to both accomodate either more smart contracts or privacy or fungibility. You threw a curve ball at me on this one. I'd like you to talk more about this. But also Schnorr and scaling I think could fall into this category.

AB: It would be more interesting debate to see happen about whether people want to see more fungibility. There are many forms of consensus in bitcoin other than the mining-based consensus algorithm. There's also technical consensus for the technical community to hash out details until there's a clear winner. There's also the market and community consensus about what does the market think; if a change was made and the market participants don't agree, then you end up with 2 or more coins. It's healthy to talk about privacy and fungibility. It's hard to argue against that bitcoin should follow the user interests and wishes. If users want privacy and fungibility then I think that's what we should deliver. Basically user's wishes were born out in the market and therefore the companies that provide services with UASF situation.... So, I think the breakdown with privacy might be different. There might be people with different tradeoffs for fast low-cost retail payments. Some of the people in that direction might not care about privacy; the interests might break down across different lines. That could be interesting. Some of the short-term things are more straightforward like Schnorr and taproot. That's much more obvious. Confidential transactions trades off against scalability and size. We might need to see more tech improvements to reduce the size of the transactions. Bulletproofs make the transactions smaller, but they don't solve the inflation problem.

PT: You can definitely do ethereum smart contracts on bitcoin right now, although it may require more thought and sophistication. For the privacy side of things, I think lightning has reasonably good privacy. Anything that scales has to have better privacy than the status quo of give every transaction to every person in the world. Even paypal has better privacy against certain adversaries than that. When I use paypal, I don't think North Korea gets my transaction data.

AB: Other than doing off-chain with oracles and some patents that keep the contract off-chain unless there's a dispute.... another area of research.. we have Russell O'Connor working on a smart contract language at Blockstream called Simplicity. It has formal proof semantics and lets you do proofs about the code. We might try this out on the Elements sidechain, which is an open-source project. Lower-level smart contracts with formal proofs might be a way to extend bitcoin's opcode-based smart contracts.

PR: You both were mentioning to me that there might be some market pressure orp eople thinking maybe we shouln't improve bitcoin's privacy because current fungibility levels are somewhat okay and hard to censor. The fear that if we make it more private then we could lose support or tolerance from the state. Do you think this is good or bad?

PT: I don't think that viewpoint comes from market pressure. People who actually own bitcoin, to own a digital currency and own something useful to do with it, fungibility and privacy is unquestionably good. If you're imagining a bitcoin where that's not true, you're not imagining bitcoin. You're imagining fiat. I think the pressure won't come from the market, but rather from service companies. Miners is an example where they might say they're politically exposed and they don't want to be seen for advocating for improvements in privacy or fungibility. This is not the market speaking. This is just influence key actors trying to exert their influence. It's important that bitcoin owners, the members of the market, recognize this and say "no" you're a service company and you don't speak for us. You're just someone we send money to prove a service.

AB: That was one of the positive outcomes about the fork debates in the past year. It was instructive to many people with many different viewpoints. I think it's been showed decissively that the bitcoin investors and bitcoin users at the end of the day, win. They stick with the main chain and don't go with a fork. If users want a feature then that's ultimately what happens. You often hear about exchanges having difficulties maintaining stable banking relationships. But that's how they make thier money; by providing a service.

PT: Good privacy is not unknown. zcash has a lot of problems with its low usage, but in theory it's a complete private anonymous currency. And yet it's still getting listed on exchanges, it still has wallets, and so on. So there are competitors to bitcoin which provides these features. For bitcoin this is simply competition. In the US, we're seeing zcash getting institutional support that don't fit this narrative that if you're private you can't have any banking relationships at all. It's harder, but there's ways around this.

AB: Fungibility is pretty related to privacy. If a currency isn't fungible then i twill become difficult to use. Pierre used the question, is bitcoin fungibility careful enough yet? It seems like the current bitcoin fungibility largely comes from the fact that if one miner won't process your transaction then probably another one would. I think bitcoin fungibility is not in a great shape at the moment. We should do what we can to fix this. The companies doing taint searching or taint tracing... in some cases it causes people to leave an exchange and close their account because they made a transfer to a gambling site or they received a payment from a gambling site. This trend is actually quite bad.

PT: What paypal actually does for fungibility is significantly less worse than the taint stuff we see in bitcoin. If you send money to me on paypal for something inoccuous, paypal won't freeze my account even if you're a criminal. In bitcoin, that equivalent situation can happen and taint your coins.

PR: What about code base quality? Lightning is also more code and it expands the code base and exposure to bugs. Do you see this as an upcoming challenge?

AB: The introduction of layers like lightning is good. Whatever change you make in lightning can't effect bitcoin's base layer reliability. You can also have competing versions of lightning. It's much more forgiving in that sense. It still has to be careful because people could lose money in it.

PR: When do you think we could roll out Schnorr signatures or bulletproofs? Is it 10 years, 5 years, 1 year?

AB: Peter is probably a better person to answer that. I don't actually write bitcoin software. I'm more interested in the cryptography. Schnorr from an indirect viewpoint or people workikng on it, it seems that the technology could converge fairly quickly like next year or the following year. Confidential transactions is a bit more difficult.

PT: I've been working on stuff building on bitcoin but not directly Bitcoin Core software. I'm inclined to agree with Adam, within a year seems plausible. Pieter Wuille or Greg Maxwell would be a better person to ask.




