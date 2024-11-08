---
title: Lightning Network Services for the Masses
transcript_by: Stephan Livera
speakers:
  - Roy Sheinfeld
date: 2019-07-31
media: https://stephanlivera.com/download-episode/1348/94.mp3
---
podcast: https://stephanlivera.com/episode/94/

Stephan Livera: Roy, welcome to the show.

Roy Sheinfeld: Hey Stephan, great to be here.

Stephan Livera: So Roy, I’ve seen you’ve been writing some interesting posts on Medium, and obviously you’re the CEO and founder of Breez Technology, so can you just give us a little bit of a background on yourself, on you and also a little bit of your story on Bitcoin.

Roy Sheinfeld: Sure, sure, I’d be happy to. So I am a software engineer by training, I’ve been working in different position in the Israeli high tech industry for the past 15 years. My previous company that I founded was an enterprise B2B company around document collaboration called Harmon.ie. And in 2017, I left Harmon.ie in order to found Breez, and the trigger was the Lightning Network essentially. I read the paper, the white paper about Lightning Network, I saw the great progress that lnd and c-lightning are making with Lightning Network, and I realized there’s an opportunity to bring something new to the market, so alongside with two partners, we decided to found Breez, and start a new adventure in the Bitcoin ecosystem.

Roy Sheinfeld: Actually the three of us, the three founders, we’ve been investing in Bitcoin since 2013, so we’re not new to Bitcoin, but we decided to do, to roll up our sleeves and actually do something to help Bitcoin.

Stephan Livera: Back in those days, and I’ve mentioned this earlier on the podcast as well, is in the 2013 and ’14 days, there was this massive focus on this idea of merchant adoption, and I think people were sort of putting the cart before the horse and not realizing that this thing is going to proceed through stages, but definitely there are some, let’s call it user interface or user experience component that Lightning Network can really help solve for Bitcoin.

Stephan Livera: I think a couple of examples might just be things like overpayment, underpayment, the timing of the payments, and I think you were really touching on some of these in some of your Medium posts, do you want to just talk a little bit about what some of those problems are with just trying to use Bitcoin standard, you know normal Bitcoin transactions, as the payment network itself.

Roy Sheinfeld: Sure, sure, so I think there are three main problems, three main issues, in the blockchain that the Lightning Network helps mitigate. The first issue is the time it takes to confirm a transaction, so best case, it takes at least 10 minutes to confirm a Bitcoin transaction, and worst case, it can also take hours, so you don’t want to get into a coffee shop, order a coffee, pay with Bitcoin, and wait 10 minutes till the transaction is approved, right?

Roy Sheinfeld: So Lightning Network, in using the Lightning Network a transaction can occur within seconds, which is actually the user experience that users want, that user expect. So from my standpoint, Lightning Network really can help Bitcoin be on par with fiat in terms of user experience, and the time of transaction is crucial. So that’s one point, the other point is scalability.

Roy Sheinfeld: So we want to onboard all the people on the world and for Bitcoin to replace fiat economy. If we’re actually serious about that, if we actually want to do that, Bitcoin needs to scale, so you can’t have like between seven to 10 transaction per seconds, you need to be at least three or four order or magnitude and better, and Lightning Network helps Bitcoin scale, so it’s very scalable, actually there’s no limit to the number of transaction that can occur per second. It’s also just a function of the side of the Lightning Network.

Roy Sheinfeld: So scalability is key, and the third issue is the fees. So on-chain transaction is costly, it takes a lot of energy, it takes a lot of work to maintain the blockchain, rightfully so, that’s why it’s the most secure cryptocurrency that exist right now. So it can’t really handle microtransaction. If you want to buy something that cost a buck, then the fee is a buck, that doesn’t make sense. So the fees must be much lower in order to handle microtransactions, and we want Bitcoin to penetrate real world economy, and there’s a lot of microtransactions in the real world economy, and in the real world commerce, so that’s why I love Lightning Network. You can do a lot of transaction within seconds with very low fees.

Stephan Livera: Excellent, and I’m all for that. I think one thing that’s been a little difficult, and part of this is just because we’re early, is that it’s difficult to keep up with all of the different pieces of Lightning Network technology and software concepts that are evolving very rapidly before our eyes, and you had a really good post recently called, Lightning at the End of the Tunnel, and it was a really good, in some sense, summary of some of the key points to consider. So it might be good to speak to some of those and how, maybe we can talk a little bit anybody what is the user experience problem or challenge to be faced, and then what’s Breez doing to help mitigate that.

Stephan Livera: So a quick example we could start with is the zero configuration, this is the Autopilot idea, do you want to touch on that for us?

Roy Sheinfeld: Yeah, sure, sure, so the idea behind zero configuration is the fact that Lightning Network client just need to work. We want users to install a software, to install an app on their mobile phone, and everything to seamlessly work. We want a seamless onboarding experience.

Roy Sheinfeld: So zero configuration means the user doesn’t need to know all the concepts behind Lightning Network in order to use Lightning Network, he doesn’t need to know about channels, he doesn’t need to know about nodes, doesn’t need to know about inbound capacity or outbound capacity. You know all of these are implementation details that needs to be hidden from the end user.

Roy Sheinfeld: From an end user standpoint, the software just need to work exactly like you install Venmo or you install Zelle or you install PayPal and it just works, Bitcoin and using Lightning Network just need to work seamlessly for the end user.

Roy Sheinfeld: So the idea behind zero configuration is how do we get to a point, to a place, where the user just install the software, and the user is seamlessly connected to the network, and he can immediately transact on top of the Lightning Network.

Roy Sheinfeld: So there are two solutions, I think, that I am proposing, I’m presenting in my article, one is called Autopilot, by the way Breez doesn’t use Autopilot, we’re going on a different path which I’ll explain in a second. Autopilot means that once the user transferred a certain amount of Bitcoin to his wallet, then the channels are automatically opened based on a specific algorithm. It can be the reliability of the nodes, it can be based on the uptime of the nodes, it can be based on the connectivity level of the nodes, but the idea behind Autopilot that the user doesn’t have to choose specific nodes to connect to, the Autopilot chooses for him the nodes that he’s going to establish channels with. That’s the idea behind Autopilot.

Roy Sheinfeld: The problem with Autopilot is the fact that the user needs to fund the channels, meaning once these channels are established, the user can’t receive transactions. He needs to spend money in order to be able to receive money, that’s the challenge with Autopilot, so even if the algorithm works great and the channels are opened seamlessly and the user doesn’t need anything about the nodes that he’s connected to, the problem is that it still needs to spend money in order to receive money.

Stephan Livera: Yep, so let me just clarify that. I think most of my listeners tend to be intermediate or advanced, but just to keep it accessible, I think what you’re getting at there, Roy, is that let’s say you use a wallet that has Autopilot and say it’s got Neutrino, and you fund that by sending Bitcoin to the wallet, it automatically opens the channels. The problem then is in this abacus analogy, all the beads are sitting on your side, so you have no capacity to receive an incoming transaction on the Lightning Network at that point, because you need somebody else to open a channel to you for that, or we need something like dual funded channels, which is again a future concept, and so then do you want to just talk a little bit about how Breez tries to overcome that problem.

Roy Sheinfeld: Sure, sure, so there’s a second solution to the auto configuration, to zero configuration, is what I called, by the way I really liked the fact that you used the abacus analogy, which was also presented in one of my article, so an LSP is another concept that I try to push. LSP, exactly like an ISP, it’s a service that connects you to the Lightning Network.

Roy Sheinfeld: So what Breez is doing when a user installs Breez, a channel is automatically opened from the Breez hub, or in the new terminology, the Breez LSP, the channel is automatically opened to the end user node, and then the user doesn’t fund the channel, coming back to the abacus analogy, all the beads are on the LSP side, so the user can immediately receive transactions after he installs the app.

Roy Sheinfeld: So everything happens seamlessly, the LSP as a service, it’s a well connected hub, it’s a hub that manage all the connectivity to the network, so it’s connected to other hubs as well, and it manage the liquidity, and it’s very well balanced the hub, so it’s a quality of service, it provides a high quality of service to end user, unlike Autopilot, the user knows the LSP that he’s connected to, so there’s accountability here and there’s inbound liquidity. An LSP also provides inbound liquidity.

Roy Sheinfeld: So that’s the way, we’ve implemented that in Breez. When a user installs Breez, a channel is automatically opened from the Breez hub to the end user node. So once the channel is confirmed the user can immediately transact on the Lightning Network, and it can receive funds seamlessly.

Stephan Livera: And so, here’s the thing, doesn’t that cost Breez a lot of money to do that for every new user?

Roy Sheinfeld: So the question is, what do you mean it costs Breez? We lock funds, it’s still our money, so-

Stephan Livera: True.

Roy Sheinfeld: We don’t spend the money, it’s not like we spend it. The way that Lightning Network works in general you need to put some funds upfront in order to provide liquidity to the network, so we’ve decided that we want to bootstrap the Lightning Network, so in order to do that, we lock some of our funds inside the Lightning Network. So the roadmap in regards to Breez is we don’t want to undertake the entire effort ourselves, so we actually want to become an LSP platform, not just an LSP provider. So we want to use third-party LSPs, we want to present to the user other LSPs that he will able to connect to.

Roy Sheinfeld: So yes, we think that in order to bootstrap the Lightning Economy, more providers, more companies, more individual, by the way it can be also individual, it can be a user running a full node at his home, everyone can become an LSP, and once even the big players, like let’s say exchanges, will get into the picture, then we’ll have enough liquidity in order to bootstrap the Lightning Network.

Stephan Livera: Fascinating, and so then the idea might be that a user might install Breez Wallet and have different potential LSPs who they can go with to receive an incoming channel from?

Roy Sheinfeld: Exactly, and even not a single LSP, unlike an ISP, the user will be able to choose multiple LSPs. So technically, it will represent multiple channels in the underlining implementation, but the idea is not to lock the user to a specific vendor, but to allow the user based on the basic principle of decentralization, we want to enable the user to do whatever he wants, to connect to his LSP of choice, and to be able even to connect to multiple LSPs.

Stephan Livera: Yeah, that’s an interesting idea, and I can definitely see some value to that because if you were reliant on one single LSP, then you could theoretically be held hostage in some certain ways that, for example, they might censor your payments or they might, for example, set a very high fee rate, so that you must pay a massive fee to route any kind of payment through their hub or through that channel that you have with them, but then obviously in a competitive market with multiple LSPs that competitive pressure will hopefully drive down the fee.

Roy Sheinfeld: Exactly, exactly, drive down the fee and improve the quality of service. So there are a couple of, fee is one parameter, there are other criteria like the quality of service, the reliability, the percentage of failed transactions, there’s a lot of stuff that are included in being a good citizen in terms of a hub or an LSP.

Roy Sheinfeld: So we want the user to have an handle on the choice, and to be able to choose the LSP that he wants to go with, and like you said, it will be a competitive market where LSPs will compete on end users, which is the right way to go.

Stephan Livera: And another thing I was thinking of, so to your point earlier, how you were saying it’s not necessarily a cost, but in some sense you are locking up UTXOs with a particular user who has downloaded Breez Wallet, for example, so in that way, from a business entrepreneurial point of view could that be considered like working capital, and if you have a lot of users who you open the channel to them, now yes it’s true, you’re not spending the money to them, but you are in some sense tying up that UTXO in the channel to that user, and so could it be considered sort of like working capital in that you’re tying up capital to the given user?

Roy Sheinfeld: Yes, I think so, I’m not an accountant, but yes, I think it goes under the definition of working capital, yeah.

Stephan Livera: Right, and then I wonder, is there much of an entrepreneurial decision there around which users you open that channel with? A quick example I can just think of off the top of my head, there might be many users who just download the wallet, install it, use it one time, and then just never use it again, and so at that time Breez Technology, or whoever else is being the LSP has now opened up and used an UTXO that way, but I guess after some period of inactivity would you then try to revoke that or close the channel?

Roy Sheinfeld: That’s exactly what we’re doing, so currently we have a very simple mechanism that where we close inactive channels after a period of 30 days, that’s a business decision, but there can be many business decisions. So the LSP, it’s exactly like the user has a freedom of choice for the LSP that serves him, the LSP also has a freedom of choice to serve the user that they want to serve, so there can be a lot of business decisions going into a how and a why and for how long to keep the channel open, because the LSP can close the channel whenever they want, and there’s not a problem with that, the question is if they want to maximize the potential of the customer how and why should they do that.

Stephan Livera: Yeah, that’s a really interesting thing to me because I wonder, so obviously right now it’s early days, right, but I wonder if over time what would the fees sort of settle to in a more “arms-length marke”t, right?

Stephan Livera: So rather than like, “You’re my friend, I’ll just open a channel to you, just because you’re a Bitcoiner, and there’s not that many Bitcoiners”, that kind of thing, but what happens in the future, would the fee rate settle to something like one percent or maybe a bit less than that, and so it would still work out cheaper than say credit card processing, and I wonder, do you have any thoughts on that?

Roy Sheinfeld: So yeah, so I think, and that’s another thing that I’m trying to push is to make people understand and to educate people about the fact that Bitcoin needs to go peer-to-peer, the entire way. So Bitcoin can’t stay at the store of value level, it needs to become a medium of exchange in order for, we don’t want to, Bitcoin censorship for instance, right, we don’t want people or government or institutions or third-party to block Bitcoin from the moment of conversion between store of value and medium of exchange, right?

Roy Sheinfeld: So in order for Bitcoin to succeed, it needs to be a medium of exchange. Now the question is why? You know, what’s the benefit? So I think once we’ll have a true peer-to-peer economy, then we’ll have a lot more competition by definition, because it’s peer-to-peer, and that’s the reason the fees, we want companies to succeed, we want people to make, to be able to create successful ventures, to be able to sustain the Lightning Economy and the Bitcoin Economy, so I think LSPs needs to make money, but they need to make a lot less money than the current fiat and third-party intermediates.

Roy Sheinfeld: So I think eventually the fees will be much, much lower than the current fiat rates. I think it will be, I think even less than half a percent, but I don’t think it will be free, I don’t think it’s sustainable in a free model.

Stephan Livera: Yeah, I think that’s a very insightful comment, and I think we should recognize that and be open to that, and recognize the reality that somebody has to lock up capital in some sense, even if it’s not necessarily spending, that they are still locking up UTXOs, and that still has a cost in terms of on-chain fees required to open those channels, and the other-

Roy Sheinfeld: There’s a lot of cost… yeah, sorry go ahead.

Stephan Livera: Go on.

Roy Sheinfeld: I’m saying it’s not the only cost, there’s a lot of cost going into managing an LSP with a good SLA. If we want Bitcoin to have like a 99.999, the next nine reliability.

Stephan Livera: Five-nines.

Roy Sheinfeld: Yeah, five-nine and six-nines, and even seven-nines, we want to get to the next nine and if we want to get to the next nine, someone needs to take care of that, and there’s a lot of cost going into running a successful hub or a successful LSP, it means rebalancing, it means high reliability in terms of cloudapp time, it’s a lot of work, so it’s not just locking the working capital, which also cost money, you know, currently with services like BlockFi or other cryptoloan services, you can get five percent interest on your Bitcoins.

Roy Sheinfeld: So locking up in the Lightning Network has a cost, add to that the work that goes into managing an LSP and managing a hub, it’s not sustainable as a free model, someone needs to pay for that, by the way, doesn’t mean the end user will pay for that, because we want to serve businesses as well, so there’s certainly a scenario where it will be free for end users, but it will cost money for merchants.

Stephan Livera: Yeah, that’s an interesting model as well, and I think, I mean people can talk about incidence as well and OK, the customers still pay it, but that fee is built into the cost, just as today when you buy a coffee or whatever, really the credit card processing fee is just worked into the cost of buying that coffee, right?

Roy Sheinfeld: Exactly, exactly, I think what we need to-

Stephan Livera: Go on.

Roy Sheinfeld: I’m just saying I think what we need to make sure is that the system, the network is decentralized, it doesn’t depend on large players, it needs to be open, it needs to be decentralized, it needs to be peer-to-peer and that will drive the cost, that will drive lower costs.

Stephan Livera: Yeah, and now another area I’m keen to discuss with you, Roy, is just around managing the off-chain balance versus the on-chain balance. Now just for the listeners who are not familiar with that idea, let’s say, I mean there are different ways and approaches to this, some wallets take this idea of having Bitcoins that are held just as standard UTXOs and then showing you a separate Lightning balance, but what’s your thinking around how Breez Wallet presents it and how to sort of manage that.

Roy Sheinfeld: Yeah, so again, my passion, my dream is to have a Lightning service that provides an on par user experience exactly like fiat. So multiple balances doesn’t work, right? The user needs to open his app, and by the way, I don’t really like the term, wallet, because by the end of the day it’s a payment service, not just a wallet. You don’t think about Venmo or about Zelle as wallets, right, you just use them as payment apps.

Stephan Livera: Right.

Roy Sheinfeld: So the user needs to open the payment application and see a balance, and he wants to spend all the balance that he sees in his balance, right, it needs to be that simple. So the problem with Bitcoin/Lightning is the fact that you need to manage on-chain balance and an off-chain balance, and even the off-chain balance can be divided into multiple channels and currently, there’s no AMP support, so you can’t really spend funds that exist in multiple channel in a single transaction.

Roy Sheinfeld: The first challenge is how to consolidate the on-chain balance with the off-chain balance, and in Breez, we went into very unique architecture, we only maintain an off-chain balance. So it’s a Lightning only solution, we don’t expose a Bitcoin on-chain wallet, we don’t do that. That’s our way to show the user a single balance.

Roy Sheinfeld: So the user sees when he opens Breez, he only sees the off-chain balance, and in order to implement that and in order to be able to show a single balance, we actually use a technology called Submarine Swap, so the user will be able to top up his wallet by using an on-chain transaction, but Submarine Swap helps the user because it converts the on-chain transaction to a off-chain transaction.

Roy Sheinfeld: So whenever a user top up his wallet, it actually doesn’t go into a local Bitcoin wallet, what happens, we present an on-chain address, but the on-chain address is a Submarine Swap script, so Breez is obligated to execute an off-chain transaction to the funds that are received in the on-chain address.

Stephan Livera: Very clever. So then a couple of other points, so what if the user, so for example the user sets up a Breez Wallet, and they get a one million sat incoming channel, and then let’s say they want to send, they do something like, “I want to send 10 million sats on-chain to my Breez Wallet”-

Roy Sheinfeld: We have a lot of users like that.

Stephan Livera: Haha right.

Roy Sheinfeld: So the Submarine Swap defines a timelock and in this specific timelock, the off-chain transaction can occur in a specific timelock. If Breez identify that the user has put up more Bitcoins than the limit, than the channel capacity, actually it’s the current channel capacity, right?

Roy Sheinfeld: Then the user will have to wait till this timelock is expired, currently it’s 48 hours, and after the 48 hours, the user is presented with a Get Refund action in Breez and he then able to take the funds and transfer them to another Bitcoin address, an on-chain address.

Stephan Livera: Right, like another Bitcoin wallet say?

Roy Sheinfeld: Yeah, yeah.

Stephan Livera: But yeah, I think it’s an interesting approach, because the way you have it set up now, it’s much more instantaneous in terms of setup time, because I suppose it can be difficult for a newbie to think about, okay, first I’ve got to install c-lightning, and then Spark Wallet, or I need to install lnd and then Zap, or some other phone wallet, and it’s not necessarily fast to get setup, whereas with Breez, it’s a little bit more like install it one time, and off you go.

Roy Sheinfeld: That’s the entire idea, I think there’s a lot of advantages to the way that we do that, one is the onboarding experience, unlike Bitcoin wallet by the way, we have a seedless onboarding experience, because it’s Lightning only, and you don’t have to maintain an on-chain wallet, the installation and the entire onboarding experience is very, very slick, and there’s no seed, and it’s zero configuration, there’s no need to fund the channel, you don’t need to think about channels, everything just happens seamlessly.

Roy Sheinfeld: We don’t target users that want to run their own full node. You want to run your own full node, all the power to you. We aim, we target mainstream users, we want to onboard the masses to Bitcoin and to the Lightning Economy, and that’s why we want to create a service that is installable by everyone. So it just need to works, that’s our motto, it just need to work.

Roy Sheinfeld: So that’s the way we designed Breez, and that’s the way not everything is available right now, there are challenges still, but that’s the spirit.

Stephan Livera: And with the seedless setup, what does that imply then for the user and the keys? Is it that the keys are still held by the user? Are they not held by the user? How does that work here?

Roy Sheinfeld: Yeah, so of course, the keys are held by the user, but the fact that you don’t maintain an on-chain wallet, the seed doesn’t give a lot of advantage. If the user will write down the seed, then what? You will able to restore only the on-chain funds because we don’t have any on-chain funds, so it doesn’t make a lot of sense to expose the seed.

Roy Sheinfeld: But the keys are held by the user, we currently have an automatic backup to Google Drive, we’re going to support iCloud soon, but the entire idea behind Breez is how to make a great user experience in a non-custodial fashion. So we don’t want to break the Bitcoin values, the Bitcoin principles of minimized trust and this situation. So the keys are held by the user.

Roy Sheinfeld: With Lightning Network when you run your own node, and the mobile device runs a light node based on Neutrino, then it’s much more complicated than just managing an on-chain wallet, so we provide another interface, which is the Google Drive backup, and we’ll add more vendors down the road where the user will have control over the node.

Stephan Livera: Yeah, right, it’s fascinating as well that you guys have taken a more, the engineering approach to actually code up Submarine Swaps and have that implemented, because I presume then that will also help you later down the line when say you want to setup for merchants or setup for individuals and then they need to do, to refill their balance, or let’s say, another example might be if you’re a merchant or again in that abacus analogy, all the beads are now on your side, and you need to now push them back out to the other side, and I understand with Lightning Labs, they have this thing, I think it’s called Loop Out, I presume it’s a Submarine Swap, right?

Roy Sheinfeld: Yes, yes.

Stephan Livera: Would that be a similar kind of idea for Breez if you were to have merchants?

Roy Sheinfeld: Definitely, definitely. So we also have like a Loop Out service already in Breez. You can remove funds and make a lightning transaction to our hub, and our hub will make an on-chain transaction, so in order, again, to deal with liquidity, with inbound liquidity.

Roy Sheinfeld: So actually I don’t see much different between use cases, between peer-to-peer use cases and point of sale merchant use case. Users want to receive money as well. Users have to deal with inbound liquidity as well. Merchant, likewise.

Roy Sheinfeld: I think what specifically is interesting for a merchant is the ability to do that is to take the incoming Bitcoins, and at least at the first stage of penetrating the real world economy, they will want to convert their Bitcoins to fiat in realtime or near realtime. So I think that’s the only service which will be kind of unique for merchants, but we actually are working on a merchant solution based on a single source code, so we’re taking our client and we’re giving it a skin of a point of sale, and it will be presented differently to the end user.

Roy Sheinfeld: It will be like, I don’t know if you’re familiar with a Square interface. So it’s going to be like a Square app but in a non-custodial fashion, and all the capabilities of the end user will exist in the point of sale.

Roy Sheinfeld: One of the things that we’re implementing in the context of a point of sale is NFC support, so we really dislike QR, we want to improve payment experience as well so for peer-to-peer transactions we’ve implemented something called Connect To Pay in which you can share a link with your friend and all the payment is done via this link instead of QR code, and for merchants, we want to support NFC. So users will be able to pay merchants simply by tapping their phone.

Stephan Livera: Right, so that link, how does that work? Would that require the user to have fast internet?

Roy Sheinfeld: So the link, you mean the peer-to-peer link?

Stephan Livera: Yes, yes.

Roy Sheinfeld: Normal internet, it needs to be connected to the internet because like both when you do a payment in the Lightning Network, both of the nodes need to be online at the same time. So the user needs to have a decent internet connection for the payment to go through, but it’s not necessarily high bandwidth internet.

Stephan Livera: Let’s talk a little bit about routing as well. So currently the Lightning Network is source routing, so one of the, I guess, criticisms of some of the, Lightning bears, let’s say, is they say, “Oh, but hang on if you’ve got a low powered mobile device, how’s that mobile device going to be able to compute, maintain the topology of the Lightning Network in its small memory, and compute a route?” What’s the thinking that you have on that?

Roy Sheinfeld: I’ll say something that is off-topic for a second. If you want to criticize an emerging technology, you’re not doing the right thing. The good thing about Bitcoin and the great thing about Bitcoin and Lightning Network is the fact that these are technologies that are designed for real world usage, and they’re taking small steps in order to build a very solid, very robust infrastructure.

Roy Sheinfeld: So currently, Lightning Network is implementing source routing coupled with onion routing, because that’s enough for now. For the capacity of the Lightning Network right now, that’s enough. I can tell you that we in Breez have a great payment experience. Every payment is done in just a few seconds, and all this is done with very simple, very naive source routing.

Roy Sheinfeld: Also in the source routing, there’s a lot of optimizations that are being done. We use an lnd, lnd just came out with 0.7 release that includes a lot of optimization in regards to routing. So first I suggest this criticizer to take a look at the ongoing work that is being done.

Roy Sheinfeld: For the future, everyone recognize that it won’t sustain a large network. So in order to sustain a large network, we need a different routing algorithm. There are, I think, I cover in one of my articles, I have a specific article about routing, I cover two proposed algorithms. One of the algorithm is called trampoline routing, which basically means you outsource the routing to a trampoline node. A trampoline node is a node that has the entire visibility on the network, unlike a mobile device that runs a light node, and can’t have the entire topology of the network, it can hold the entire topology of the network. A trampoline node is a well connected node that runs in a server and gets consistent updates on the topology of the network and has the entire visibility of the network.

Roy Sheinfeld: So basically, you outsource the routing calculation to a trampoline node, the question is how to preserve privacy, because one of the thing that is easily attainable when using source sorting is the fact that you can do an online routing and then you maintain your privacy. So the question with trampoline, the challenge with trampoline is how you outsource the route, but still maintain privacy, and there’s different, I won’t get into too much of a technical details, but there are proposal to handle the privacy.

Roy Sheinfeld: For example to do two-layered onion routing from the source node to the trampoline node, and from the trampoline node to the destination, that’s one proposal.

Stephan Livera: Excellent, yeah, I think some of the stuff is interesting, sometimes I’m not able to fully follow, but sometimes I see on the Lightning Dev mailing list, they’ll come up with different ideas and rendezvous routing, and so on. There’s different ideas being thrown around, it’s interesting to see how quickly it’s evolving.

Roy Sheinfeld: And even people from outside, I saw proposals for ant routing, which is based on the pheromones that the ant provide when going to seek out food, and there’s another proposal based on that, and this is coming from outside the developers, which is great. Everyone is contributing to Lightning.

Stephan Livera: Great, so let’s also talk about Neutrino, which is another concept or compact block filters, which is software that’s being pushed by Lightning Labs, and that’s one idea that they have implemented within the Lightning mobile app, which is a Neutrino client. Do you have any thoughts there and is Breez making use of any of that, or not really?

Roy Sheinfeld: Yeah, yeah, definitely, so Breez, again, is a non-custodial wallet. The way to implement currently a non-custodial wallet is, there is basically two path you can go. One is using Electrum and the other is using Neutrino, we’re using lnd, that’s why we’re using Neutrino, and we were the first client to run Neutrino both on Android and on IOS, so we contribute to the Neutrino stack as well, and it’s been great, and I think Neutrino is a very good, very solid technology and it works quite well.

Roy Sheinfeld: For me the challenge with Neutrino is actually not technical challenge, it’s more of a philosophical challenge, is when you run Neutrino, when you run light nodes, how do we ensure that enough people run full nodes. So I don’t, there’s a challenge, like a game theory challenge. We need enough, we need a lot full node, everyone needs to run… the intention, the goal is for everyone to run full nodes.

Roy Sheinfeld: So if we’re making it easy for people to run light nodes, what will be the motivation to run a full node? So, that’s my challenge with Neutrino. So the way that we’ve mitigated that in Breez is we’re actually exposing the URL of the full node Neutrino is communicated with. So the user can actually configure a different full node. So we expose the trust, and we minimize the trust by allowing user to define, to configure a different full node. The question is with BIP 157, when the BIP 157 already merge into the master of Bitcoin, and once all the Bitcoin core nodes will run BIP 157, there will be a question if whether we need to keep this configuration or to remove this configuration because everything can happen seamlessly without configuration, and then I’m coming back to the philosophical question of how to ensure that enough people run full nodes.

Roy Sheinfeld: We actually have a dream in Breez to help mobile devices run full nodes as well. Currently it’s very challenging because of the mobile operating system, because of bandwidth and because of storage limitations, but I think our goal is to run, it’s a bit of a dreamy goal, but this is our goal is to run full nodes on mobile devices as well.

Stephan Livera: Right, and just to clarify that point you were making about how if BIP 157 were to be turned on by default, is that what you were getting at there rather than right now where the Breez wallet, all of the people out there with their smartphones, it’s polling back against the Breez Technology node, and I presume then if I understand you correctly that you would, considering there that the idea that each Breez Wallet might just poll out to a random node, is that what you’re saying?

Roy Sheinfeld: Yes, yes, exactly. So currently we have a configuration that in the configuration by default it communicates, the Breez Wallet communicates with Breez full node. By the way, it’s just a regular BTCD node, it’s not our hub or anything like that. So users can already define the different node and configure a different node in order not to trust Breez. That’s one of our design goals as well is to remove all trust in Breez. So it’s already available. The question if you connect randomly to a node, and that’s the challenge with BIP 157, is how do you expose one, how do you expose the trust, because I believe that everything that has trust needs to be exposed to the end user, if it just connects randomly, how do you expose this, that there’s a trust element there? And secondly if it’s that easy, how do we ensure that enough users run their own full nodes.

Stephan Livera: Yeah, those are definitely big considerations I think. We definitely do want to encourage people to run their own full node, and so the way I sort of encourage people is maybe if they do take some of these wallets that are not running off their own full node, that they try to transition towards a full node wallet, but at same time recognizing there are some people who just are not in a position to do that, but I mean some trade offs I heard are-

Roy Sheinfeld: As a technical person I also want to make technical advances, and because I believe mobile is the holy grail, I wish we were able to run full nodes in mobile devices. There are projects that does that already, but they need to be connected at all times unlike mobile devices. We have a target in Breez also to tackle this challenge as well.

Stephan Livera: And another one I was keen to ask you around is in Lightning Network, part of the security model is what is called justice transactions. So if somebody tries to cheat you with a bridge transaction, ideally your software, so in this example your lnd might pick that up and then broadcast a justice transaction to stop them stealing from you basically, how does Breez approach this and is there any idea of using watchtowers or just use of Breez technology’s servers or how does that work?

Roy Sheinfeld: So we have a background channel watcher job, that runs periodically on the mobile device, even if the app doesn’t work, is not in the program, that check the status of the channels, and whenever this background watcher identifies that the status of your channel had changed, it triggers, it prompts you to open Breez in order to broadcast this justice transaction if necessary.

Roy Sheinfeld: So we actually have like watchtower you can say, which is implemented in the client. It’s not a watchtower because it’s not a third-party node monitoring these channels, but it’s your client, your client is actually running periodically a watcher that tries to understand if the channel status has changed. Now that’s without trust, because the user can configure it runs in the same Neutrino full node architecture. It’s actually Neutrino that is responsible to understand if the status of the channels had changed.

Roy Sheinfeld: So if the users, currently if they by default uses the Breez node, they trust Breez to provide the right full node information to your Neutrino light client, but if you configure it to your own full node, then you don’t trust Breez, and you actually monitoring your channels periodically based on your own full node information. So that’s already, this is something that we already integrated into our product.

Stephan Livera: That’s very clever. So let me understand that then, so you might set up a Breez Wallet and you might have an incoming channel from Breez, however you might not actually be using Breez’s node, you might actually pair it back or connect it back against your own node, and it’s kind of like you’re getting the channel from one thing, from Breez, but you’re actually your blocks and your data from your own full node.

Roy Sheinfeld: Exactly, exactly, that’s already available in the product. Now where I want to use and leverage the watchtower technology is where currently our timelock, our HTLC, is defined to a week, 1080 blocks. So if you don’t open your mobile device, your mobile device has been shut down for a week, for more than a week, therein there is a challenge that you won’t be able to broadcast the justice transactions if someone is trying to cheat you. Now that’s a challenge where I want to leverage the watchtower technology is I wish there was a watchtower service where you can provide the different means of communication to the end user meaning for example the user can provide an email address or even a phone number for pushing SMSes, so I think the benefits of a watchtowers can be around this area as of communicating to the node, but even if the node just has been shut down for a while. So how do you broadcast this message to the end user?`

Stephan Livera: That’s clever, so yeah, that’s a good idea as well. Obviously then there’s also the privacy aspect, but the user would opt in to that I presume so that they would know, and obviously they would want to know if they’re losing money, or they’re about to lose money. It’s interesting as well the timelocking component there, so from my earlier conversation with Conner about, where we spoke about watchtowers in lnd, and he spoke about currently lnd scales that CSV, the relative timelock, Check Sequence Verify based on the amount placed into that channel.

Stephan Livera: And I recall as well with Eclair when the Eclair mobile Android wallet, Lightning wallet came out and they wanted to have incoming receive capacity they expanded that CSV time window, and I think it’s a similar concept here because the idea here is your mobile might be offline for a few days, maybe you went on a hike and you’re out of reception and at this time, somebody could try to cheat you theoretically.

Roy Sheinfeld: For us, it’s the tension between, we don’t want to lock the user funds if he wants to close the channels on one hand, on the other hand, we do want to provide a good experience in terms of security, so there’s a scenario that you’re into a hike or going to location, and your phone is shut down for a couple of days. So for us, it was the, is to find the right number that will mitigate the different advantages. I think also it makes sense to have something more dynamic, but in the Breez architecture, actually all the channels are funded in a predefined amount, so it doesn’t really help us. It helps us right now, maybe there will be a way to change that in the future, there will be a way to change that in the future using splicing and stuff like that.

Stephan Livera: Yeah, I mean that’s the thing as well, there’s so many of these amazing kind of ideas coming down the line, and then it’s a question of how do those also get incorporated into the wild with things like AMP and splicing and dual funded channels.

Roy Sheinfeld: So for us, the way that we handle these innovations is by looking at the user experience that we want to provide and then using the right technology and the right innovations that helps provide the value, so we have like a top-down approach rather than a bottom-up approach. It’s not like that we’re using everything that is popping up, we have a very clear vision of the user experience that we want to provide to our end users, and then we leverage the right technology in order to provide that.

Stephan Livera: Yeah, fascinating stuff, I think it’s really interesting to see the way it evolves out and how there’s different wallets, and people are taking different philosophies and approaches, so I suppose we’re pretty much coming to the end of the time, but maybe Roy if you just want to tell the listeners, if they want to get Breez Wallet or if they want to get in contact with you, how do they find Breez Wallet, and how do they find you?

Roy Sheinfeld: Yes, so I encourage you, everyone, to download and use our product. You can find the download in our website, https://breez.technology. I also would love to get feedback, so we have a very active Telegram group, also you can find a link in our website. So I’m on Twitter, I’m on Medium, I’m on Telegram, hit me.

Stephan Livera: All right, well look, thanks very much Roy, I appreciate you taking the time, and I had a really interesting discussion with you.

Roy Sheinfeld: Thank you so much for having me, Stephan, and have a great day.
