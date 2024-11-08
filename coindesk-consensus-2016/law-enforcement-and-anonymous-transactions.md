---
title: Law Enforcement And Anonymous Transactions
transcript_by: Bryan Bishop
speakers:
  - Brian Klein
  - Baker Marquart
  - Prakash Santhana
  - James Smith
---
Preliminary notes:



Contact me- <https://twitter.com/kanzure>

Law enforcement and anonymous transactions

Jason Weinstein, Blockchain Alliance, moderator

Brian Klein, Baker Marquart

Prakash Santhana, Deloitte

James Smith, Elliptic

Zooko Wilcox, doing essential zooko things (zerocash)

Ladies and gentlemen. Please take your seats. The session is about to begin.

Please welcome Jason Weinstein, Brian Klein, Prakash Santhana, James Smith, and Zooko Wilcox.

JW: Any proof-of-work finalists should go to the 7th floor elevators and leave right now. Another housekeeping issue, you are welcome to go to sli.do and use #consensus to vote or submit a question. We are going to do our best to go through as many questions as possible. We will also be around after the talk. We are going to do some brief intros. I am Jason Weinstein. I was a federal prosecutor for 15 years. During the last third of that time, I was part of cybercrime and organized crime, and now after getting companies into trouble I am now getting them out of trouble. I am also a part of Blockchain Alliance, which is 20 companies and 15 law enforcement agencies. This is to protect public safety, getting law enforcement comfortable with the tech and reducing their anxiety, and also promoting growth and the legal and regulatory environment.

JS: I am JS. I became a derivative trader before founding Elliptic. We identify suspicious activity in the bitcoin blockchain. We provide anti-money laundering (AML) to help them understand where they have a high real risk. We also work with law enforcement to help suss out illicit activity and build a case.

PS: I lead payments, fraud and risk at Deloitte. I was previously at Mastercard. I have been in the fraud business for 23 years. Preventing fraud, that is. Happy to be here and talk about this topic.

BK: I am a partner at ... I am a former federal prosecturo. Regulatory defense, civil litigation, criminal defense, I am also on the board of advisors of BlockSeer which is an analytics company.

Zooko: My background is cryptography and computer science. I am founder of zcash, which is a technology for encrypting the data into the blockchain so you can control who gets to see the data. This is a privacy-preserving currency.

JW: ... Criminals will keep using tech, if it's fast, convenient, if it makes their lives easier. They will also keep using it if it provides anonymity or a degree of protection from the eyes and ears of law enforcement. Every time there is innovation and criminals adopt it, law enforcement has to catch up. Law enforcement has to learn to understand it and how crimes are facilitated it. Law enforcement have to figure out new tech how criminals use it to commit old crimes. It's as true as phones, fax machines, phones, burner phones, skype, VoIP, paypal, there's so many examples of criminals seizing opportunities and law enforcement catching up on that. Every time there's an innovation, the law enforcement people think the world is going to end, we'll shut the whole thing down and give the criminals down, this one we're never going to figure out how to solve, sometimes it takes month sometimes it takes years, at least until new innovation screws them over. We have seen this cycle of innovation and adaptation. About the greatest example is the internet itself. Criminals figured out how to use the internet before pretty much everyone except Al Gore. Law enforcement had to be on the learning curve to figure out how the internet works. The greatest challenge is anonymity and attribution, which prosecutors call putting fingers at the keyboard. This is the hardest part of investigating online crime, and this has been true ever since Cookie Monster invented bitcoin. I heard that somewhere, is it true? They use tor, proxies and other anonymity techniques. There's new anonymizing tech, then they have to figure that out too. The takeaway then is that bitcoin and more generally just represent the lattest chapter of innovation and adaptation. In law enforcement, it's not new to blockchain, it's endemic to any crime committed using tech in any way, and law enforcement has had to grapple with this for years. It's a new twist on a new story. The twist in this case is favorable to law enforcement. When they catch up, they will ....

JW: Prakash, you hear that bitcoin is anonymous. If they have heard of it, they will say it is anonymous. If it's not true, then why is it not true?

PS: If you look at anonymity in the cryptocurrency framework, the first part is, you look at an entity, you are aware of a collection of all the addresses that belong to to them. Being able to link a collection of public addresses to an entity. If you have, are you able to see a transaction that belongs to this entity that potentially happened at a KYC or AML compliant exchange? Because then you can track the entity. Let's talk about the first part. Being able to arrive at the collection of addresses that arrived to an entity. James will talk about this some more. You could use graph theoretic and clustering techniques to arrive at a probabilistic solution set that basically says here's a list of addresses that basically belong to an entity, there are ways to do this. You need data. You can't track it with anonymous data. You need to have the capacity to look at a collection of addresses, follow transaction amounts exactly, that's the first part. The second part is more difficult, you need to be able to track an address that does a transaction at a KYC AML compliant exchange. Fraudsters can choose to not do that. If they decide to not do that, you might have a collection of addresses but you can't link the entity. There's evolving, there's an evolution in this whole space, like the Zcash... sorry I called it zoocash, it doesn't matter, it's z anyway. Zcash, where it's distributed anonymized payments. It's a distributed mixing protocol if you will. It's not a centralized mixer where you send your addresses and mix it up, so you don't know where the money is going. It's a distributed protocol. It will get even more difficult to use tech or analytics to be able to track who is holding the transaction. From what I have read about zcash, it anonymizes the sender and the receiver and the payment data, there's nothing to analyze. I am sure zooko will get into it. It becomes increasingly difficult to use analytics to track who's the entity behind it. I always go back to what law enforcement does best-- when something is difficult, they revert to low tech methods. As an example, I used to manage fraud at Mastercard. We had a program where merchants would do illegal activity like child pornography and other things, they would have a legitimate webpage where they would sell flowers, so you would use crawlers to crawl their website and see at what they are doing, but often they are able to hide behind multiple pages and block web crawlers. So after that, we do something realy simple, do a test transaction and see if the transaction goes through the same account. So you investigate the transaction, you find it's not a legit business. There are other ways like device fingerprinting, like monitoring and grabbing information, I am sure law enforcement has other capabilities they can use like Tor attacks despite the advances they will be ways to arrive this. I am not sure about this new evolution but clearly, ....

JW: Before we get to Zooko and zcash, I want to ask James to talk about how Elliptic and other companies trace breadcrumbs that people leave behind in the blockchain, to help identify fraud.

JS: We do a lot of work ... we look at transaction graphs, we understand when there are common ownership in lots of clusters of addresses. This is bitcoin-specific. In the current environment, it's important to do this stuff. Where there's an entity, but the other important part of it, is really understanding the services, the legitimate and illegitimate services, to understand how they operate, so some of them are our clients, and they have anti-money laundering services, and how those guys want to work with the regulators, but also very much understanding the ... so we spend a lot of time gathering data from the.. understanding how every market works, how every mixer works. We start to see patterns of similarity between multiple entities whether it's multiple mixing services or market services and we're able to pull out features of each one that suggests here's a transaction that might be suspicious.

JW: How much of a challenge do mixing services and tumblers present? When you are using your own analytics tool?

JS: It varies. Some of them are good. Some of them are really not good. Some of our exchanges might treat anything from a mixing service as potentially suspicious. Some of them are okay with suspicious mixing services. It depends on the mixer-- is it associated with dark marketplaces? Then you need to elevate whether you think they are risky. When mixing services become popular enough to matter to law enforcement, then we can get into that with law enforcement, but it's possible to figure this out from some mixing services. I think this comes back to your point earlier that it's a cat and mouse game. They innovate and then they adapt.

JW: So you said bitcoin involves opt-in privacy?

Zooko: The mixing services that James was mentioning was where users can opt-in to combine their transactions in order to obscure the relationships about source and destintaion. I was telling you about this because opt-in privacy cannot achieve the privacy that we want as a public quality objective. I worked in the computer security field for many years. Almost all users always use the default settings. Only a few people who are especially skilled will use something else. It's also true for bitcoiners, they use default settings. An example of a policy objective, which cannot be achieved by opt-in, is fungibility which is that all coins are created equal. You don't care which $100 bill they give you, any $100 bill should work. With opt-in privacy techniques, there's multiple classes of $100 bills, like those that recently came from a mixer. This, seems to me, will inevitably lead to sand in the ears of commerce.

BK: Oh you should put that on your website.

JW: Brian, if you put this in the press, you have represented, .... based on your participation in those cases like Silk Road and Carl Mark Force, what is your sense of where law enforcement is in the learning curve?

BK: Depends on the prosecutor, there's no specific knowledge or skill. You might have prosecutors in SF or NY and they have sophisticated agents, but sometimes you go into a market and it's the first bitcoin case, and they have read some stuff but they might have limited knowledge. There's more knowledge now and more awareness, I think there's understanding that some people use bitcoin for completely legitimate reasons. When talking with law enforcement, I have to explain often why something is totally legitimate and in good faith. Just because they happen to use bitcoin or something they don't understand doesn't mean it's criminal. I think there's... well, I get paid to educate law enforcement when I advocate for a client.

JW: We talked about challenges ,but what about advantages?

PS: The biggest problem in 2007-2008 crisis was that people were holding toxic assets. Blockchain infrastructure provides a way to get a perfect audit trail and record for all activities related to a transaction and asset. There's significant value in this. This is why the financial community is here today and interested in this. It's a good audit trail.

JS: It's the worst way to launder money. If we can't figure it out today, we can figure it out tomorrow.

PS: As we get into more smart contracts, we can see the contracts and see what you had in the past, where is it today and who is holding the asset?

JW: When I talk with law enforcement about this, like in child exploitation cases, if the person is savy they will use proxies or something and multiple hops, which you have to trace. It might take multiple years to do this. By the time you get to the right person, the ISP doesn't have the data anymore. I try to focus them on the fact that the blockchain data is there. Once you make the authentication, you don't have to worry about the data not being there. You don't need a subpoena, you can just go to the companies in the other countries, as long as you have an internet connection. Brian, you and I have heard on multiple occassions from law enforcement that the data is only useful if the data can be connected to a real person. When they do serve a subpoena, do you- is it your sense that law enforcement is trying to make an example of non-compliant exchange companies?

BK: I happen to represent .. CoinMX, that's someone in this jurisdiction they allege was running an unlicensed money transmission service. They send out press releases. There was also the Ripple Labs settlement. They really try to send a message. I don't always think it's the right message, like in the Ripple case, I think this is something that I really do think that it's something that law enforcement wants to do. They want to let people know that they will prosecute you if you are breaking the law, that they have these tools and it's out there.

JW: How is the game going to change? This goes to Zooko, talk to us about what zcash is. How does it differ from other digital currencies? How do you think this will impact law enforcement?

Zooko: First of all, zcash is not the only game in town. There's a great demand both from all kinds of members of the public and also, to my surprise I found out about a year ago, a great demand from the financial industry like banks and exchanges and payment processors, all kinds of players in finance trying to use blockchain to disrupt businesses and so on. What I have also found out in the last year is that they are some of the most specific in demanding a specific kind of privacy, which is control over disclosure of data. A blockchain to me is kind of just a funny variant of a database. Zcash is one of several technologies which is attempting to satisfy this demand for a database with control over disclosure over who gets to see the data. Zcash does this by encrypting all data in the database, then providing decryption keys to the authorized parties. Therefore it's not the opt-in type of privacy where everything is transparency by default and protected in special cases, it's the other way around where it's protected by default. It's not like, as a lot of people start with the assumption that it's the polar opposite of bitcoin, with bitcoin you can always see the blockchain, and then you can correlate what's in the blockchain with other info. Zcash is not the opposite, it's selective transparency where authorized parties can be granted the ability to see subsets of the data. And so, it's going to, assuming the tech like Zcash or Zcash itself becomes widely used both as an open currency but also a fundamental tool in blockchain deployments in finance, your question was how would this change for law enforcement? Well, I am not a law enforcement expert, but I am an expert on cryptography. Everything you said so far on the panel... most of it remains true, but not everything. For example, we heard that a critical step in investigation is knowing your customer, anti-money laundering, that would be the same if the exchange was supporting Zcash and their compliance behavior would be the same, they would disclose the correct information to law enforcement when presented with the correct subpoenas. We heard Prakash say, clustering versus exchange, I forget the, it's the exact thing with zcash as with bitcoin; the thing that changes, for law enforcement, you said it's really important for enforcement but for auditing. This is a panel about law enforcement, but it's not the most important thing in the world, and we're not building products for law enforcement.

BK: You're not building zcash for law enforcement. That's not what we're buiding for.

Zooko: It's compatible with law enforcement. There's compliance with financial service provider requirements. I agree there's a lot more value beyond being compatible with law enforcement which we want with our open permission currencies. I was interested in auditing and long-term lookback. Because that's also something that we do get into, it's not obvious to people that all of this data is in the blockchain in zcash. It might turn out there's a richer set of data that gets put into the blockchain in zcash because with an open transparent database you can't put stuff in there that you don't want everyone to see. But with an encrypted database, you could put information in there that is only supposed to be disclosed to yourself, or your future self or specific authorized party. So this is good for auditing.

PS: I see a lot of use cases around permissioned.

Zooko: Yeah.

PS: Say it's a network of financial institutions, they don't want their competitors to see their financia transactions. On the permissionless chain, you have the negative side of, unsanctioned or something money laundering wants to move cash it becomes increasingly difficult for laundering.

JS: .... someone who knows about the travel rule, which requires that in the transactions you send out, you attach CPII information to the payment, you could do that with zcash because you don't have to worry about other people seeing it. By way of regulation applying to businesses in this space, they will take the... and they .. if there is a bitcoin exchange decides to also use zcash, they will have the same regulatory requirements and understanding who they do business with. You can still go with-- you just don't get those prelinked entities that bitcoin gets you.

JW: It shouldn't tbe the anxiety that... it just means you go one hop at a time.

BK: This is going to blow law enforcement's mind, zcash will blow their mind like bitcoin did. There are many legitimate reasons to have zcash and other products like that. That's the bigger part of the story. You're building a product for, not just for law enforcement to do their job better even though it's compatible...

Zooko: It might be better for law enforcement in the long run, but probably also worse in some ways.

JW: Every innovation is done for the rest of the world, not for law enforcement. There's also-- zcash is a new tech, but law enforcement has the same issues.

BK: Law enforcement would want to ban cash, we wouldn't have cash, since it's the most untraceable. Hopefully we can have a level of privacy in our life. Just because you don't want the neighbors to see, doesn't mean you're doing something wrong.

JW: I am going to Brian's house after this. What do you think is the greatest challenge for law enforcement going forward?

BK: It's getting people to a consistent level of knowledge. When I was a federal prosecutor, they were just learning about cell phones. They know how cell phones work now, because they have cell phones. As law enforcement starts to use bitcoin, they will start to understand this. I think frankly this conference itself, we have NY here, all the biggest agencies interested in these agencies, this is a big step up from two or three years ago. Just getting this, just getting this education and comfort level.

PS: If you look at what law enforcement folks have done today, it's theft and money laundering and doing the framework to do money laundering. No matter what system you have, you're going to have theft of assets, whether blockchain or whatever - it doesn't stop it. It's not going to stop it. So I believe, with all these services, it's going to be a lot more theft happening and as a result, law enforcement might have a hard time tracking the movement of money from one account to another. That's where the big problem is-- theft of assets. If it's a permissioned environment, maybe there will be some solutions.

BK: My concern is that startups that get one knock on the door, it cripples their ability to innovative. A lot of times what I see, law enforcement is like killing a mouse with a missile and that's my worry about bitcoin and law enforcement. There needs to be a scope of balance.

JS: Companies in this space need to understand they are subject to regulation. The more successful your business is, it's even more likely that regulators will pay attention to your business.

PS: Every industry is developing a permissioned chain, but eventually they will interact with each other in the same chain. Once criminals figure out a way to take out an account in one permissioned chain, they can move their assets to other chains. This will be a big prblem.

JS: Gateways. Exchanges are helpful here.

JW: I agree with you, Brian, that educatin is huge. It didn't occur to me to buy them bitcoin.

