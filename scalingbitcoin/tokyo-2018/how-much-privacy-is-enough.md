---
title: How Much Privacy is Enough? Threats, Scaling, and Trade-offs in Blockchain Privacy Protocols
transcript_by: Bryan Bishop
tags:
  - privacy-problems
speakers:
  - Ian Miers
date: 2018-10-06
media: https://www.youtube.com/watch?v=YgtF7psIKWg&t=3700
---
unrelated, <https://arxiv.org/pdf/1706.00916.pdf>

## Introductions

Hi everybody. This is a talk on how much privacy is enough, evaluating trade-offs in privacy and scalability. This is going to be unusual for this conference because I will not be presenting new technical content. I am going to be talking about evaluating the tradeoffs between these scalability and privacy. As context, my name is Ian Miers. I am a postdoc at Cornell Tech. I've been working on privacy tech since 2011.

## Privacy tech

Back in the day, bitcoin was understood to be completely anonymous. These days, we know this is not the case.  There are in fact even companies in the ubsiness of doing analytics on the bitcoin blockchain as surveillance and so on. We've seen a large number of proposals to improve privacy ranging from simple things like don't reuse addresses, to complex cryptographic protocols, like coinjoin, mixcoin, coinswap, coinjoinxt, joinmarket, tumblebit, bolt, etc. How do you evaluate these? If you are going to do this for real world usage, you have to evaluate this. Engineers know how to run performance metrics and do back-of-the-envelope calculatiosn which is usually not controversial unless you involve twitter. But how you measure how much privacy you get is tricky, and yo uneed to figure out that answer before you figure out a scheme to use.

## Evaluating privacy

Evaluation of privacy is tricky because we can't resort to empirical results. It would be like trying to evaluate privacy on the internet in 1992 when the only website was CERN, before cookies, targeted ads, surveillance, etc. So we can't really make an empirical estimate of how much privacy these techniques provide. So you need to do something else, right? You can't really measure with empirical attacks. You need ot use thought experiments, and to do this we must understand realistic threats. As a researcher, if this data existed, I couldn't use it- I have costs concerns, I have ethical limitations, I have to go through IRBs... so instead I just have to use thought experiments and think about 5 years, 10 years, 20 years. What are the realistic threats? How do things play out in other related domains?

## Some real-world privacy threats

The common threat that people worry about was the government and law enforcement looking at what's on the blockchain. That's one threat, but by no means the only threat or the most realistic threat. We have seen that Google has been collecting payment data from Visa and Mastercard and using that for targeted ads for you. This is probably not a good thing because if Google is doing it then so are a bunch of people that you have never heard of and they are probably less reputable. Also, we know that companies want to build rich profiles about wha ttheir customers do. There was a famous case of Walmart about building up a profile based on your customer loyalty card and they could figure out if you were pregnant and they could sometimes figure that out before you know. The apocryphal story was that some teenager was pregnant and they sent her some material about pregnancy, and her dad got irate because how dare they send this content to her but it turned out she hadn't told her father.

Also, we have venmo. For those who don't know, venmo is a system for doing payments between friends for paying for a bar tab or a restaurant. It had a by-default a public feed of every transaction you've done, with your name, your recipient's name, the amount, and a memo field. So it's pretty close you get from the blockchain but instead of doing all the work to deanonymize people, they just give you that data. This was pretty stupid, but people made guides like "how to stalk your ex". This is completely creepy.

Another one more relevant to the cryptocurrency community tha twe're seeing an issue with is fungibility. We know that freshly mined coins sell for a premium, and exchanges sometimes block customers based on transaction history like where they send the money after withdrawals. Exchanges are pretty powerful; they know more than just the transaction graph, they know your trades.

## What are the defenses?

So that's why you should care about privacy and cryptocurrency. So what are the defenses? Plausible deniability is not a plausible defense. Frequently people recommend plausible deniability to me and "hey you can't prove it's me". But that's not sufficient. These algorithms don't care if it's plausibly deniable, and most people in law enforcement don't care either.

## Bitcoin privacy is not intuitive

Typically people think about third-party passive observers as the main threat. But you need to consider other attackers, like active attackers that can send payments to you, receive payments from you, interact with third-parties. You need to think about obvious attacks like merchants trying to track their customers; users who try to identify who their receivers are, and exchanges trying to track you.

## Privacy approaches

There's vanilla bitcoin where you explicitly identify origin of payments. Then there's decoy-based transaction systems where you pick 5 different origins and you hide what's going on. And then there's stronger approaches like zerocoin and zerocash where you don't even identify an origin. In bitcoin, if you pay a merchant, you have to explicitly identify where the money you're paying them came from. This is why you basically have no privacy, those transaction inputs. In decoy systems like coinjoin and monero, you hide the origin of your coins by using some decoys that aren't the real source but nobody looking at the transaction can't tell. In systems such as zerocash, you don't have any identifying information whatsoever.

## Are decoy systems private

The privacy limitations of bitcoin have been well-studied. The privacy limitations of zerocash have been studied in academic literature and in practice. But what about the decoy-based systems? This seems like one of the main things at the cryptocurrency community is considering for scalable privacy. Do these things work?

Taint tree: you can identify the possible source of funds and find the transaction graph and go look at it. You end up with a tree of possible tainted payments that go back in history where you don't know quite what happened. It's a fuzzy family tree where you have some notion of what's going on. If you pay a merchant, you can see where the payment goes, but you might not know where it goes because it might also use decoy payments. These two things give you a lot of power, and it causes a lot of problems, because you might see it repeated over multiple interactions.

One thing you could do is if you're a merchant or a set of colluding merchants is that you can track customers. Say you're going to Target every day and buying something in cash, and instead you start using cryptocurrency. Ideally, if I make three separate purchases, there should be no linkages between me. If you had real privacy, that's what we want. Looking at this naievly, it seems private. But if I buy something and I give someone $20, it probably doesn't cost $20 and I get back a change amount. I get back $5 in change. I do this in each payment. Eventually I am going to have to spend the change. The moment that one of my decoy transactions is the change that I received from that merchant. You were selecting decoys at random from all possible transactions throughout history; you can do roughly uniform sampling. The odds are that if you include a tainted coin then it's more likely that it's a tained coin from the same customer rather than other coins. So this gives information to the merchant.

Consider multiple payments made to one merchant and you don't want them to understand that you're the same person. So you have a taint tree of possible ancestors. But what happens if there's a common origin to those coins? There's going to be one source of the funds. If you look back, you can find the intersection and figure out who the person was. This works not just for one merchant, but a bunch of merchants can work together and collude about who you are and find your money. This is also a problem.

## Identifying anonymous merchants

Suppose I have a website where I take anonymous donations. I don't want to reveal my identity, my life is at risk, but I want donations for my activities, and my local government is trying to identify me. In a privacy-preserving system, it should be safe for me to take that money and deposit the money in the exchange and they would have no way to identify me. I should be safe. But this is not the case: if the government wants to identify me, they have a line on the website, it might be accessible over tor, they can just send-- say, three, tracking payments ... they could be small.. and then I take them, deposit them, and then anyone who gets the records from the exchanges (prehaps through hacking or buying them or whatever) can test whether these anonymous payments were me.... they can do this by looking at the taint tree. For any random person, it's going ot be the case that some of the deposits might involve one of those payments and it might be happenstance you might have picked one of those as your decoys and then you make a deposit. But on the other hand, you're not going to do that multiple times for 3, 5, 10 or 100 payments. So, if the government goes through and looks at all your deposits and see you have all 100 of the trace payments they sent in your taint tree, then they have with overwhelming probability some evidence that you're really that pseudonym. So this is very problematic. It violates most people's intuitions for what privacy is for cryptocurrency, and I think people using this would be vulnerable.

Repeated interactions with a malicious sender/spender are in fact dangerous.

## Dust attack: confirming where money is spent

Send some dust to my friends. I watch the taint tree and the transaction graph. If this happens a bunch of times, you can have some strong evidence that your friend is making purchases at a certain merchant. You can use this to identify where your friend is spending their money.

## Limitations of decoy approaches

Customers can be tracked. Use of change transactions and outputs breaks the privacy. Common origins can be found in taint trees. Anonymous merchants can be identified. Third parties can see where your money goes. Hiding behind 7 proxies doesn't save you here. The common perception is that bitcoin is not private, but anything more than that is considered private, but that's not the reality. There's some tradeoffs between these systems about how private they are, and you have to understand what those tradeoffs mean and what they mean to your particular scenario. I'm a little biased, I would not use any of these approaches if I really wanted privacy for myself. But again, that's the tradeoff you should be making for yourself. You need to understand the tradeoff.

## If you do use decoy schemes

These decoy schemes might be viable if there's a very large anonymity set with like 5 million origins instead of 5 origins. Also, the decoy sets have to substantially overlap across all recent transactions otherwies you get a repeated common origin problem or whatever. And finally, you have to sample the decoys very carefully. There's been a sequence of one or two papers that showed the distribution by which monero sampled their decoys didn't line up with the distribution by which real people spend their coins. There was a gap. This is now somewhat fixed. With overwhelming probability in an old version of monero, the last transaction was the real transaction. This is a hard problem to solve and I don't know how to do it. If you take this approach, you need to do rigorous analysis about how much privacy you are providing, and you need to carefully understand where things fail, and you need to acknowledge the limitations.

## Scalability

Use a zero-knowledge proof of inclusion of a coin in the utxo set like zerocash does, or use layer two scalability and do off-chain privacy stuff. That might work.
