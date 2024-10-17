---
title: Bitcoin Lightning Privacy - FUD and Facts
transcript_by: Stephan Livera
speakers:
  - Anthony Ronning
date: 2021-05-21
media: https://stephanlivera.com/download-episode/3343/276.mp3
---
podcast: https://stephanlivera.com/episode/276/

Stephan Livera:

Anthony welcome to the show.

Anthony Ronning:

Hi Stephan. Glad to be here. Thanks for inviting me on.

Stephan Livera:

Yeah. So I saw your article and I thought, well, we’ve got to do a discussion about this one. I think it will be very valuable for people who are trying to think more clearly about the privacy implications of Lightning. But tell us a little bit about yourself. Who are you and what’s your interest in Bitcoin and Lightning privacy?

Anthony Ronning:

Yeah.Thanks. My name is Anthony Ronning. You know, I first started back in the Bitcoin scene back in 2017 and really just a spectator at the beginning. But then started getting more into development and even as early as 2018, started like playing around with the Lightning network a little bit and then. We even had some meetups in the local Dallas area for it. So just eventually just kept doing like hackathons and little things here and there for Lightning and eventually ended up doing Bitcoin and Lightning full-time for a few years now. So it’s been like a wild ride and Lightning is like progressing like super rapidly. So it’s one of those things, especially with the article, I just wanted to dive in and make sure that there’s a lot of privacy concerns and maybe some hand waving and I just kinda wanted to — even for my own self, just to kind of get a clear picture of where we are with Lightning privacy. And if I were to start a new node from scratch, how would I try to achieve the best privacy that I could?

Stephan Livera:

Yeah. That makes a lot of sense. And so just to keep it accessible for people who are listening, maybe they’re new, they have maybe a very basic level understanding of Bitcoin. Maybe they’ve just used a hardware wallet. They’ve never tried any spending or things like that. What does it look like? Could you just give us a basic idea? What are the basic mechanics of using Lightning and how does it help us achieve the scalability that we all want?

Anthony Ronning:

Yeah, exactly. And it’s really a good question. I think there’s like very two distinct types of UX’s when it comes to Lightning, there’s that mobile wallet user, where we got some really nice Lightning service providers, LSPs that really come in and try to abstract as much as they can away from the user. So literally, they look at their wallet, their mobile wallet, like maybe it’s Muun, Phoenix or Breez. And it’s really just like a balance that they have and they scan invoices and stuff and it tries to abstract everything. But on the other hand, you got users that like run their own node. Maybe it sits on like a raspberry Pi or a server somewhere — RaspiBlitz or Umbrel are really good. Raspberry Pi based nodes that have come out recently and are really pretty good as far as like trying to make the user like have their own node and their own wallets and stuff.

Anthony Ronning:

But essentially with the Lightning network, no matter what, like what method you’re using, at least behind the scenes, what you basically have is if you think about your Bitcoin wallet and you think about UTXOs — unconfirmed transaction outputs just to put it simply it’s you have your Bitcoin wallet balance and, but that balance consists you know inputs — unconfirmed inputs. So like, I’d like to think of them like dollar bills. Like you have your wallet in your pocket, you have a $5 bill, you have a $10 bill, right? But in total, yeah. $15. Right? So with Lightning network, you essentially lock up one of those UTXOs with another peer on the network. Maybe it’s like a merchant that you use a lot. Maybe it’s like BitRefill or like, Starbucks is always the iconic case where instead of going to make an on chain transaction every time you want to buy something from Starbucks and having to like wait for confirmations or the whole shebang and paying those on chain fees, just for a coffee, what you essentially do is lock up that UTXO and you, and that peer, instead of broadcasting a transaction, every time you want to spend with Lightning you kind of hold onto the state, you and that peer.

Anthony Ronning:

And then whenever you’re ready to close out the channel, maybe you don’t, channels can go on forever. You essentially just make payments back and forth. And then when you’re ready, you broadcast that final state to the chain and you can freely use your Bitcoin again to make on chain purchases and stuff. So like, just to put it simply a Lightning wallet, you’ll lock up a UTXO. So and then from there you can make you know, basically unlimited spans as long as you have a balance without having a broadcast on chain. And it even goes further than that. It’s not just the peer you’re connected to, so it’s not to Starbucks, but then from there you can make spends to the people Starbucks is connected to and so on and so forth kind of goes down the line.

Stephan Livera:

Yeah. So let me just summarize some of that just for, so let’s say you’re a totally new user. You don’t quite understand what’s going on here in Lightning. Okay. So think of it this way, this idea of the UTXO or the unspent transaction output. What we’re doing is let’s say Anthony and I opened a channel together. What I’m doing in that case is I’m opening a channel to him. And what we’re doing is we’re creating — we’re putting a coin in the, sort of in the middle of a us, if you will, it’s a multisignature. So we both have to sign to spend that, but there’s a special trick with Lightning where each party can, pre-sign a transaction and give it to the other side, and then we can unilaterally close that. And so if you’re just thinking if you’re a listener and you’re thinking, Oh, I’ve got my Trezor or my ledger or my coldcard, what’s going on with all this?

Stephan Livera:

Well, what you need is a special wallet for this, and it deals with Lightning for you. So if you just want an easy way to get started, if you’re a newbie, Muun, or Phoenix or Breez, or some of the good non-custodial Bitcoin and Lightning wallets. Now, if you’re a low income level, or if you let’s say in the El Salvador case, you might have to use a custodial wallet, like wallet of Satoshi or blue wallet on the default set up. Right. That’s just a few examples just for a new user. Now there are different kinds of users, right? So as you were saying, if you just want to be able to spend and receive on the mobile wallet, right. Muun, Phoenix, Breez, wallet of Satoshi, blue wallet, these are all examples. You’ve got the more hardcore Lightning user. Let’s say the guy who wants to have his remote control home node, right?

Stephan Livera:

He’s got his Umbrel or his Nodl or his myNode or a BTCpay. And they are out and about, and they want to use their wallet on their phone, and they might have Zeus or zap wallet or spark connecting back to c-lightning. So that’s kind of the more hardcore Lightning user. And then we’ve got the routing node operator. So that’s kind of a more special one where now you are actually trying to set up channels, because as we were saying, we can set up that channel between us, but then it can also route, not just between you and me, but to the other people that say you are connected to. So can you tell us a little bit about some of those other types of users? So routing node operators and merchants, for example, what’s their use on Lightning network? What are they doing with all this stuff?

Anthony Ronning:

Yeah exactly. I’ll start with merchants for merchants. It’s really good because they can accept payments instantly. And then they don’t have to worry about like confirmation and stuff with merchants and node operators. They kind of have this interesting incentive. So in that case where I’m routing a payment, maybe through Starbucks to get to you. Starbucks in this case, if they’re the node in the middle, they actually can collect a fee off of that. And right now, like fees are like super low sometimes it’s just like a single Satoshi for a fee. So Lightning node operators but you know, in that one Satoshi fee, I mean, if you’ve got thousands and thousands of payments going through the Lightning network on, any given day those fees add up.

Anthony Ronning:

So if you’re talking to few thousands of Toshi is even a day, I mean, that’s a few bucks here and there it completely adds up. And then some of the people in the Lightning network will actually make thousands of dollars a month routing payments some of the more long-term Lightning node operators. So you know, it’s not always this expectation that you’re going into it making a lot of money as a node operator, but there is this incentive of being able to lock up liquidity to the necessary places that kind of want it. And then in turn your 24/7 node routing payments for other people, and you’re collecting a little fee off of that. So that’s kind of like from a rowdy note as perspective, and even a merchant as well, merchant will have their 24/7 node. That pretty much function the same way.

Stephan Livera:

Yep. And so for listeners who are new, if you are, let’s say you want to set up and take Lightning payment in-person or in like a shop in that kind of context, you might look at say an app like Breez, right. They can set up, they’ve got a very easy merchant set up, or on the other hand, if you want to someone you can go to set up for you to take Lightning, you can go to OpenNode or if you’re more sovereign, you can go to BTCpay server and set up your own thing now. Okay. So I think we’ve set some of the background for listeners. Let’s talk a little bit now about the actual privacy implications, right? Because, Oh, sorry. One other point. I think it’s important for people to understand Lightning. I see it as mostly a scalability thing.

Stephan Livera:

But it can potentially have some privacy benefits versus us spending just naively on chain. Because if I spend on chain, I might actually reveal my entire balance to you. Whereas if I spend on Lightning, that’s actually, it sort of depends, you know what exactly I’m doxing there to you, but it’s arguably better than a naive on chain transaction. Although I would say it’s kind of like, if you want to have the least privacy leakages in Bitcoin today, you’re probably looking at using Samourai wallet and staying on chain and doing everything correctly with the coinjoin and so on. But I think it’s important to talk about where are the potential places we’re falling down in the Lightning network. So maybe you want to talk a little bit about some of the privacy leakages from a high level for your Lightning users.

Anthony Ronning:

Yeah, exactly. And you’re exactly right about you know, there on chain history that lives forever. Right. but your temporary payments or the payments that you’re making those won’t, but there’s still like some leakages, as you said, like you know, if you’re a routing node operator and you’re opening up a bunch of channels, you’re locking up a bunch of UTXOs together you know, those UTXOs can be kind of revealing, like you said, like they link back to your original balances. They like back to the sources of the payments. So like, if you’re coming from Coinbase and you’re going straight into a Lightning nodes, like Coinbase can see that other people may make inferences as well. But but then there’s also like even just setting up your Lightning node you know, if you were to use your Lightning node needs to be on 24/7, basically, if you want to be like a good merchant or a good routing node, so you basically have to set that up and there’s two ways to basically go about it.

Anthony Ronning:

You can be an IP based node. So your IP address. So if you’re running at home and you have your node from using your IP address, I mean, that basically doxes at least an approximate location of where you’re at. You can look that IP address, that IP address up online and kind of see approximate location of you. So like typically people would suggest using Tor as the mode of using — setting up your Lightning network. And from there if you it’s a little bit less reliable using Tor it’s not like you’re not going to get like, as much like speed or reliability as if you did IP-based, but at least like, nobody can see like where you live. You know, if you have your node, your IP node on like AWS, everyone can see that’s on AWS.

Anthony Ronning:

AWS knows if they’re monitoring Lightning network, they know where that server is. So in general, it’s just like a more private way to use Lightning, just setting that up. But then, yeah, from a high level, like just setting up your node to receive payments, you have to pretty much in some way, dox yourself to receive a payment. and we can definitely get more into what I mean by that, you have to reveal certain information to the sender. But from at least like a positive note, I would say like in general, like senders have like way better privacy than they do on chain. Like you said, if I spend an on chain transaction with Starbucks or something they can look up that transaction online online, and they can see the wallet that it came from, the address that came from.

Anthony Ronning:

And there, if you have other UTXOs on there and you have other history on there they can even see like, Oh, wow, like this guy has a history of sending to these addresses that are linked to bad things or things that we don’t approve of whatever that may be, or even mixing, is still something that’s pretty taboo, especially with exchanges. So senators have way better privacy on the Lightning network as a result. But but it’s still not like a perfect solution in some ways, but it’s still, like you said, better than just being on chain and everything being revealed.

Stephan Livera:

Yeah. And I think it is also important. So when we’re talking about this stuff, we hear people talk about this concept of threat modeling and thinking about exactly who is that user trying to be private from and what are they trying to hide from who, or right. Or just rather, I shouldn’t say hide, but not reveal, let’s say. So as an example, it’s just spending on chain. People might be revealing their entire — they might be revealing their salary or what’s their spending on and who it’s going to, whereas at least in the Lightning network, if you have a Lightning balance on your mobile phone and you’re spending out, it’s sort of, you’re doxing that not out to the entire world, you might be doxing that to certain individuals or certain parties. An example might be, let’s say you are a new user and you’re just using say, Muun wallet.

Stephan Livera:

Well, Muun wallet knows who, the company Muun would know who you are paying, but the outside world doesn’t necessarily have a clear picture. Maybe someone who’s trying to actively see value on the in terms of interposing on the route, maybe they have a little bit of information about you, but it’s, I guess at the end of the day, there’s different, I guess, levels of adversarial person who’s trying to spy on you. Right. So it’s like, you might say, okay, against like some government agency, there’s no way you’re hiding against them, but if you’re hiding against, let’s say random onlookers or a private investigator, maybe you can be private against those kinds of people.

Anthony Ronning:

Yeah, exactly. And what you brought up with the Muun case, it is a great point because Muun kind of sits in the middle of their users’ transactions. Right. So if a Muun user is paying another Muun user, like Muun can see that. Right. but then again, like, is that much of a concern to you? Well, you it goes back to you know, if you’re using Muun just to play around with and using small funds, no one, I think no one really cares that much about you, but if you’re like, a high risk individual. It’s funny, even Edward Snowden last week came on and was even saying from a privacy perspective, Lightning and shenanigans. and I wouldn’t say shenanigans. But it’s definitely like if you are, high-risk like Edward Snowden, like there’s a lot of things to be concerned about using Lightning then I wouldn’t necessarily consider it you know, safe enough for him to kind of openly use. Maybe he should read my article and kind of figure out all the things he could do to be more private. But yeah, it definitely goes back to like a threat model too, because there’s things that an active attacker could figure out that are pretty revealing. So like for instance, they can figure out there’s this concept known as like private channels where you can basically have — so this scenario where I described where I open up a channel with Starbucks or anyone else if I’m a routing node operator, I want that to be public. So that way I can collect fees and other people route through me to get to Starbucks and I can collect fee payments that way as well.

Anthony Ronning:

But then there’s this concept known as private channels whic is really more unannounced channels. So you don’t announce it to hold, not your network, just you and the other peer knows by default. But you know, active attackers could figure it out actually by using probing attacks which we can get into, but yeah, like active attackers can actually get a lot of information out, but then it goes back to, okay. You know, maybe an active attacker, just a single person, a private investigator, or maybe a smaller chain analytics company they can try to active attack as much as they want as fast as they can. There is still timing limits, I think in one of the papers like for instance, balance probing, there’s a balance probing attack and that takes like 20 seconds per channel.

Anthony Ronning:

So if you’re just like one node and you’re trying to scan tens of thousands of channels, that could take a while, it could take a few days or more. But you know, if you have a lot of nodes, if you have a lot of resources, if you’re NSA level and you have a lot of Bitcoin funds or whatever then you definitely can have like that if you can definitely try to do these active attacks and get a lot of information more quickly.

Stephan Livera:

Yeah. So I guess maybe…

Anthony Ronning:

So. Yeah. Like it’s definitely a fund based. Yeah,

Stephan Livera:

Yeah. So maybe we’d summarize that then is okay, fine. If you’re a super spy, don’t be using Lightning and expecting that it’s going to be private, you need to be using other tools, but if you are using Lightning more for the sake of easy user experience and maybe some additional privacy compared to naive on chain spending, that’s probably a fair statement I would say. So let’s get into balance probing. Now you’re telling us a little bit about that. What is a channel balance and how does someone balance probe? Why is that a problem? And what’s the benefit of it too, right?

Anthony Ronning:

Yeah, exactly. It can kind of go both ways. So in this scenario where I opened up a channel with Starbucks and I put up my UTXOs say it’s for one Bitcoin, all that balance is on my side. So Starbucks didn’t put up anything on their side, right? So Starbucks can’t send me anything through this Lightning channel, but I can send up to one Bitcoin to Starbucks or through Starbucks if I wanted to. But that also means not only Starbucks can send me anything, but even other peers can send me anything through that channel either, which is, it’s an interesting, because by default, you don’t know other nodes on the network, don’t know the balances of each channel. You kind of know these public channels and that you can possibly route up to a Bitcoin or whatever the channel amount is, but you don’t know what funds sit on what side and it would be a privacy concern and kind of like a network gossip concern as well, flooding the network with this information you know, it wouldn’t scale anyways.

Anthony Ronning:

But besides that it is a privacy concern because if balances were revealed and you can kind of see the flow of funds across the network, and you can see when funds are collected by individuals, stuff like that. So it turns out with balance probing you can actually figure out balances. An attacker could actively start sending a bunch of fake payments through channels with the intention that it will never resolve, it’s using like a fake payment hash so fake data. And as soon as if that transaction were to get through to that node it would reveal certain information. So for instance if you’re trying to figure out the balance between me and Starbucks, and you’re sending a bunch of payments through Starbucks and trying to get to me, if half a Bitcoin transaction wasn’t going through, then you would know that, okay, there’s not half a Bitcoin transaction balance on Starbucks side.

Anthony Ronning:

But so you would lower the amount until it finally goes through. And let’s say like a thousand satoshi or 2000 satoshi is, were able to get through. Then that most of the balance is on my side. So like basically 0.9 Bitcoin is on my Lightning node at any given time. And if that were to change, if all of a sudden you were to probe me the next day, and you figured out that, Oh, wow, like now Anthony only has like 0.1 Bitcoin on the side. You know, I made a pretty large payment to somebody, maybe it was Starbucks, maybe it was another person. So I think with these balance probing attacks, you can hone in on an individual and an individual node and really try to figure out balances there. But theoretically like an active attacker with a lot of resources you know, maybe NSA level could balance probe the entire network and try to get a good estimate of where flow of funds are moving.

Anthony Ronning:

Maybe they won’t get exact estimates of like individual payments. You know, that would be pretty difficult, but at least being able to see the flow of funds across the network. And if you get into situations where it’s, you can maybe figure out it’s originating from a certain node doing some really large payments. So I think like with Lightning network, you can kind of blend in good enough, even with balance probing, if you’re just like a small general user. And as the network grows, it’s going to get increasingly harder to do these balance attacks. And it’s going to be less accurate as time goes on. And as more people are actually using Lightning network, especially for larger payments, the smaller payments kind of flow blend in a lot easier. Yeah,

Stephan Livera:

That’s a good point, actually. So it, actually, the privacy might increase over time as the network grows. And now there’s one other point to think about with probing, which is some Lightning wallets actually use a form of this to give a better user experience to their users. So Jack Mallers, on one of the recent episodes, talked about that also where with some of his users on strike and potentially on zap also, where he wants to be able to probe to figure out how much fee they’re going to pay and fine, it might also be a reliability thing where maybe there’s some use of probing to give a better user experience. And with all of these things for listeners, there’s a trade-off here, right? Because you could try to make it more private, but then it might be less reliable. And maybe the payments won’t go through as quickly, or maybe the experience won’t be as good because you won’t know roughly how much fee you’re going to pay. It might be 2 sats. It might be 10 sats, might be a 100 sats. We don’t know. And probing helps the wallet developers give a better user experience and business Lightning businesses give a better user experience to their customers. Right?

Anthony Ronning:

Yeah. Everything you said was exactly right. And even as, especially for custodial wallets, like Strike, they need to know the fee and show that to the user before they send the payment, they can’t just send the payment and come back to the user and say, Oh, Hey, by the way, yeah, we sent your payment, but Hey, look, it’s going to cost a dollar. You know, or it ended up costing us a dollar. So you got to pay it. So you need to know ahead of time what that fee is going to be. And then present that to the user and say, okay, we’ll send this to, you know hundred satoshi you know, payment, but you know, it’ll cost this much to do it. And then it at least gives the user a better experience that way. So, yeah, you’re exactly right. and in fact even like balance probing, like you could use it for good to try to even actively balance probe the entire network to see where liquidity is being needed and drained up. And you can actually start allocating funds as a Lightning node operator to that direction. So there’s definitely pros and cons to balance probing and the fact that you can do it, but from a privacy perspective, it’s a con.

Stephan Livera:

Yeah, of course. And now we were touching on this as well, but around Lightning transaction history. Right. So as we were saying, in order for somebody to see what you’re doing on Lightning, I mean, some of it is, yeah, just looking at what’s the channel graph, right? So when the Lightning node spins up, it’s trying to say, Hey what’s the state of the network? What are, where are all the nodes out there? Show me what are all the public channels, but then also to actually see those transactions, it might be necessary for a surveillance person to try to interpose themselves inside that route. And so that they can then try to understand, “Oh, this is the flow of funds it’s coming. And I can see are based on the structure of the network. It looks like this payment might’ve come from this group of node. Maybe I can narrow it down to some of these five nodes”… or something like that. Or maybe that’s a little bit of a concern for people. But again, it requires active surveillance, right. To do that, as opposed to just a chain surveillance from who can just download the blockchain and just look at literally what’s on the blockchain to see the flow of the Bitcoins.

Anthony Ronning:

Yeah, exactly. Besides just balance probing in general, there’s there’s other tasks like, like you said, if a node, if one of these attackers is actually sitting in the middle of a payment there’s timing attacks that they could do. So if you know, this would be more on the destination side, but if it took on average 500 millisecond or sorry, a hundred milliseconds for each hop they can make estimates of, okay, we routed this payment and it took five seconds to come back or not five seconds, maybe 500 milliseconds to come back as a successful payment. So we know that on average it’ll probably be five hops away and then they can kind of do surveillance too like, okay, what node would be five hops away? That it’s kind of sending to, or if it’s like, if it’s instantly a hundred milliseconds and then know, Oh, okay, well that was the next destination was actually, sorry, the next hop was actually the destination.

Anthony Ronning:

So they can kind of come up with metrics like that. and especially if they are, they can even constantly probe the network to figure out the times between each nodes and even narrow down the timing of attacks as well. But then, but then, yeah, you could even think of it in a way where an instance where an attacker actually has many nodes on the network and they can actually correlate together in order to see where payments are going. So if for instance, there’s — I’m trying to pay BitRefill and I’m going through six different nodes, but three of those nodes, or two of those nodes are an active listener, the same person. But they have some random alias online. It doesn’t look like it’s from the same person. They can actually correlate that payment together and see, okay, cool.

Anthony Ronning:

We, they could at least see four different hops, right? If they’re two on each side, they can see a hop on each side where it came in, where it went out and then on their other node, their second node, they can see where it came in, where it came out, and then they can see that it’s the same payment hash and the same amount as well. And they can say, okay, cool. They can try to get more accurate representation of where it may have came from and where it went to. It’s also interesting with Lightning network, there’s a lot of like different graph algorithms to like, figure out if the best and shortest path that you can make. So if you were to combine some of these attacks with the actual graphing algorithms that are being used for Lightning nodes, you can actually even just try to figure out okay, cool. Based on the path that it took, we know that, like you said, this payment came from this direction and it’s probably going in this direction. So as a one of the suggestions I mentioned, which isn’t really reasonable for a user to do today, a more highly advanced user could, is actually create random, spontaneous payments that just go through a bunch of random, different nodes that it really shouldn’t normally go to in order to try to…

Stephan Livera:

Right. To sort of spoof the data.

Anthony Ronning:

Exactly.

Stephan Livera:

Yeah. Gotcha. And I think that’s also another point where listeners, you might be interested in my prior episode or going back now with Rusty, where we spoke about MPP and so the concept you mentioned there was payments correlation. And so I might not be to explain this perfectly, but in Lightning there’s this pre-image. And so the sender of the payment, once once that payment is to finally release it, they’re releasing the pre-image. And so it’s asking the same question, right? So what is going to change once we get taproot? Hopefully it looks like we’re going to get it the Lightning network can change to this thing called point time locking, and that might fix some, or help some of the routing aspects there where it would actually help have well payment decorrelation. Right. Or stop the payment correlation, rather is probably more precise way to put it right. Yeah,

Anthony Ronning:

Exactly. The payment as it’s going through each hop. Instead of it being the same hash, every time it will look different, every hop. So you can’t exactly correlate the same payments together. If you are like colluding with other routers, or you literally are multiple routers at the same time routing the same payment, like it fixes that to a degree. I think you could still do reasonable estimates based like, okay, cool. Like if you are two nodes on the network and a payment went through both those nodes you could see that. Okay, cool. Like in this, in this very same five second period, this one payment with an amount of 2,510 Satoshis went through my node. And then a second later went through my other node. So you can’t correlate it as much as you can today with it being the same payment hash. But you can still kind of try to do reasonable estimates based on the amounts of stuff. It would be more of a, yeah, it would take a little bit more effort, but maybe still possible.

Stephan Livera:

Yeah. And it’s, I guess, with many of these things, there are some counter measures, but it all comes down to trade-offs and there’s not really a clear, “this is the best way to do it.” And so I think in many cases, the network will sort of just stay, and any easy wins. Of course, I’m sure Lightning protocol developers and Lightning wallet developers will take the easy wins, but there are fundamentally just going to be some trade-offs here around how much effort they put into trying to make it private versus reliability, or just trying to make everything scale better.

Anthony Ronning:

Yeah, exactly. And in the case of timing attacks, that one is really difficult because we literally want the Lightning network to be as fast as possible. Right. We want speedy, fast payments, but if we were to try to solve some timing attacks, one of the methods of doing that would be to add random delays through each hop maybe it’s between a hundred milliseconds to a whole second. But as you start trying to do things like balance, probing, things like that it starts to exponentially increase the time it takes to do a probing and then do the actual payment itself. So that would be a huge, a UX degradation if we were to try to mitigate timing attacks. So just, for the sake of privacy.

Stephan Livera:

Yep. And so now let’s talk a little bit about the channel graph because every time we are opening and closing a channel, so I guess, let me back up a sec and think from the perspective of a new user, they might be thinking, Oh, see if I just stay on Lightning, then I’m just private because I never had to touch the chain. But the reality obviously is no, you still had to open and close channels and in practice as well. It’s not just about the setup, the initial setup, right. Because it’s one thing to just initially set up channels. It’s also about how do you have that flow going through, because you might have to do loop in loop out, or you might need to you know, you might need to do some channel management. And in those moments, there will be an on chain impact. And in those moments, people can correlate things together. They can surveil you in that way. So can you tell us a little bit about the implications there of channel open and channel close? What’s that mean for us as users?

Anthony Ronning:

Yeah, exactly. The Lightning network, thankfully, is really interesting in this one way where as an outside party, you don’t really know which node opened the channel between the two parties. So if I open a channel with you to the outsiders, like, I mean, of course that I’m the initiator of the channel and I put up my UTXO lock up with you, but to outsiders, it just looks like, “okay, Hey, this brand new channel appeared, it’s using this UTXO and it’s between these two nodes and we really don’t know who made that” which is thankfully a really good property of the Lightning network. But then, like you said, it kind of goes down like, let’s say for instance I opened up a channel with you. No one else knows except you and me.

Anthony Ronning:

And then I use the change of that. So like, let’s say I have one Bitcoin in the UTXO and I only wanted to open half a Bitcoin channel with you. I use the change, the other 0.5 and I opened it up with Starbucks. And then all of a sudden you can see that this one node he had originally this one input, this one UTXO originally, and it split into two. And now there’s two channels, both coming from the same node. You can then infer. Okay. Stephan, you probably weren’t the open channel initiator to begin with. And Starbucks probably wasn’t either because the know that opens a channel and has change back, they get the change back, of course. Right. So then they can, you can basically correlate and see that, okay, this, the same person opened up multiple channels.

Anthony Ronning:

So you know, what one of the things people say is, okay, I’ll be fine. I’ll just open up a bunch of private channels. And but even from there, that’s, the private channels can be revealed. and even with the on chain heuristics and opening a channel and opening and closing, like a lot of this can still be revealed anyway. So it’s really my one suggestion is like either open up a channel, like if you’re trying to be the most private as possible, which some may not be this necessary, but if you really want to have at least a 50% doubt of who opened the channel to begin with either open up the channel with the full amount of the UTXO or mix the change afterwards, cause it could it could be me or you that mixed change afterwards. We both have the same reasonable doubt of who it could have been and then use that change, that mixed change to open up a new channel if you want.

Stephan Livera:

Yeah. Right. And so some of that might be theoretical but difficult to do today because many of the Lightning wards, well, as far as I know, none of the Lightning wallets have like coinjoin functionality built into them. So as an example, you might have to run your stuff through Samourai wallet whirlpool, for example, and then spend that into your Lightning wallet or Lightning node, right. Your LND or C-Lightning or whichever Lightning implementation. And then from there open the channel. But then in that example, if I wanted to open another one with the change, well, I can’t do that. Cause I’m going to have to now, spend that back out, run it back through a Whirlpool back into the Lightning node. Like until it’s all kind of meshed together, that’s just not going to be a reality for most users. However though I know, Lisa Neigut from the Blockstream team recently did do a dual-funded channel and that’s an interesting one as well, because that could also kind of — I don’t know exactly, but maybe that could be structured like a PayJoin and maybe it would all sort of start to break that heuristic there as well. What do you think?

Anthony Ronning:

Yeah, no dual funded channels is great. Even the fact that it exists now shows that not only did we have a 50% that it was either me or you that opened the channel, but now we have a 50% or less than whatever. I’m not sure the exact implementation of how it looks, but you’re exactly right. It is a PayJoin too. So it could have been both parties that put their inputs together into that channel. So it could have been just me. It could have been just you. And even so it adds this dynamic of you know, possibilities that it could be either one or both. So you can’t exactly core, it does look kind of like a PayJoin. The one con that I do have so there is an instance where an active attacker could try to initiate a dual funded request with another person that is accepting the funding requests in order to fish out what their possible UTXO is. Right. Because there’s still cross signing that has to happen. And both parties have to reveal what UTXOs they’re going to use for the channel. So I could back out midway and see what UTXO, you were going to use. And then I just leave. So if I see that UTXO used again in some open or part of some channel opening, I can at least say, okay, that was Lisa’s UTXO that she had and then they can say, okay, because that was Lisa’s UTXO we know the other UTXOs. So if there was just too may have been the other person. So but again, this is where an active attacker is needed. And I’m sure like, if there’s like, you could probably see this abuse happening, maybe I’m not sure of the exact details, but just the fact that it exists right now, at least you know, if a chain analytics company started up in five years, they can’t like go back and actively try to snoop out, dual-funded channels that are happening right now.

Anthony Ronning:

So it’s just the fact that exists, adds more doubt into channel openings, which is pretty cool.

Stephan Livera:

Right. Yeah. And so there was a paper, which I’m sure you’ve probably looked at this, but it was called Cross Layer De-anonymization. Right. And so that was essentially this concept that we’re talking about of looking at what’s happening on chain versus what’s happening on the Lightning world. And as it, like your example with the change output, this is that was some of the work that they were looking at in that paper. And so that paper looks like it’s the kind of approach that some of the chain surveillance companies might adopt that. And they might also, because it’s obviously there are NDAs and — they can’t, they don’t reveal this, but it’s kind of colloquially known that there’s information sharing between the exchanges and the chain surveillance companies. So, as an example, if the exchange company knows that I, Stephan Livera bought this number of Bitcoins from this exchange, and then later they say, Oh, he spent it out to this address.

Stephan Livera:

And then from this address, we can see that Stephan opened this channel here and then the change output there, you can sort of see where they could start to sort of build that picture on, say me as an example unless I took active steps to obfuscate that. Right. So as an example, if I used a coinjoin before doing that, or if I had done that only with coins that I had purchased in-person, and not from like a KYC exchange, right. I guess there are different steps in ways that a person could try to obfuscate this a little bit. And obviously if you’re not Edward Snowden, James Bond, super spy, you just want some level of privacy, then maybe that’s something that you could get there. But any thoughts on that?

Anthony Ronning:

Yeah exactly. One of the things that I wanted to bring up about that paper, which was new to me, which was interesting, even just opening private channels. And like, let’s say a node opened up a private channel like me and you open up a private channel. And then we we have let’s say nobody really knows it exists. I mean, there’s private channel probing attacks, but let’s say nobody knew it existed, but then part of that balance goes to me when we close. And part of the balance goes to you when we close, but then we use that change to open up public channels. They can both see that, okay, this, this one output was actually used in two different public channel openings, afterwards. And they can actually deduce that. Okay. We know with a pretty high degree that even if they were private channels, even after the fact, so like, this is not an after the fact they could see that with a reasonable doubt that input was used in the private channel afterwards.

Anthony Ronning:

So that’s, that’s an interesting aspect out of that paper, but yeah, you’re exactly right, like you wouldn’t necessarily want, — I would say like always like mix your change or sorry, mix your UTXOs, after you get them from exchange before going to the Lightning network, just to kind of yeah. Build enough doubt that you’re using the Lightning network. I mean, today it’s fine. I think, I mean, we have exchanges using Lightning, but you know, at a certain time coinjoin usage wasn’t so blacklisted with exchanges at one point. Right. So who knows if exchanges started to catch on or regulators start to catch on and actually disapprove the use of Lightning because they see it as a sort of mixing technology. We don’t — I think for now we’re okay, but you never know in the future, so yeah.

Anthony Ronning:

Either mixing your change or trying to I can talk about this more, but trying to source UTXOs from alternative sources, like you said, non KYC sources, or even what’s interesting services, like BitRefill Thor where they’ll, they’ll actually open a channel with you. So you’re not using your UTXO at all. You’re just using one of Bitrefill’s UTXOs, or you can lease channels out with something like Lightning loop and you can have someone else open the channel with you that way as well. But yeah, my suggestion would be either like to use mixed coins for channel openings or to try to even source UTXOs from other places.

Stephan Livera:

Yeah.That’s a really interesting idea. So we might as well go into that. So this idea of using someone else’s coins to set up your Lightning node or to get started into the Lightning world, or so I guess probably the main two pathways for the person who wants some kind of privacy in the Lightning network, but not super spy level. Right. They might buy some coins, non KYC run it through a coin join, open the channel, open the private channel to who they want to spend to and then make sure they’re mixing the change. That’s probably the flow, right. So that kind of person, and then the flow for the person who wants to — let’s say use someone else’s UTXO. So what does that look like if they wanted to spin up a Lightning node or maybe have a mobile wallet, what would that look like?

Anthony Ronning:

Yeah. So w with some of these services that are kind of like, are external services, so not natively built into Lightning network. I know with dual funded you know, you kind of partial get that, but so for instance, like BitRefill Thor you can go to their website and you can just probably, I don’t know the URL, just Google BitRefill Thor and you can actually even pay in Lightning to open up to have them open up a channel with another node. So for instance, like one of the things that I want to do is like, have these like disposable throwaway, Lightning nodes where or I send funds into BitRefill in order to open up a channel with whatever node of my choosing. So you basically just put in your public key and then they will do the connection requests.

Anthony Ronning:

Then there’s also like Lightning Pool, which I really like Lightning Pool. I use it as a leaser. Basically the idea is that — let’s say you want someone to open up a channel with you, which helps solve the inbound liquidity problem, you will pay an on chain transaction basically to have them to have some random node that’s selling online. You don’t know who it is beforehand. But you have them open a channel with your node. And then Lightning Labs is actually coming out with a product soon called sidecar channels which you can even pay to have it go to — have that channel opening happen with another node. That’s not related to yours at all. It could be any node that you do it. So each of these methods of like trying to source a different UTXOs, or trying to get other people to open up a channel with you it’s all gonna kind of be like external services. So like Bitrefill Thor, Lightning pool, they all have their own websites. LNBig is another one. And then I think yalls.org is another one. So those four that I know of that actually have this service where you can go on their websites and pay and have them open a channel with you.

Stephan Livera:

Yeah, that’s awesome. And then the other thing to think about here is it’s one thing to get these set up initially, but then it’s also about the flow actually happening, because let’s say you’re a merchant or you are regularly spending and now you need to refill so this is where some of the swapping in and out, right? So listeners, you can check out my earlier episode with Alex Bosworth, where we spoke about some of these ideas. But Anthony, maybe you want to touch on some of that idea around actually maintaining this Lightning economy. And how would you refill, let’s say, so as an example, let’s say you are spending, and now you need to refill your Lightning wallet. How do you do that?

Anthony Ronning:

Yeah, exactly. And the, and there’s two ways to go about it. Sometimes like one method is okay. You’re spending a lot and now you’ve just emptied out one of your channels. And then now what do you do? Do you, close that channel and just start have nothing or do you actually go through the effort of refilling it? and this is where like, it even helps on the privacy perspective as well. But just in general, like you can you know, maybe maybe you spin up another node to do this, but maybe use a service like Lightning loop and Lightning loop. They have two services, loop in and loop out. So you can actually pay if you wanted to loop in you can pay Lightning labs, some fee.

Anthony Ronning:

It’s not like an insane amount. But you know, you’ll pay an on chain fee and basically Lightning labs will send, send the payments to whatever invoice you’d give it basically. And there’s other services like that too. Lightning labs their loop in and loop out is probably the most well-known. So you pay them an on chain fee, an on chain transaction, and then boom, they send you the same amount or minus the fees into your Lightning node to refill your — in this case, outbound liquidity. But then you can also go the opposite way as well. You could loop out. So this actually helps, I think on.

Stephan Livera:

for a merchant, right?

Anthony Ronning:

Yeah exactly. So let’s say you are receiving a lot of Bitcoin through your Lightning channels, and then now you can’t actually receive any more, right? Like you’ve maxed out your inbound liquidity. So you have multiple options there. You can, like I said, try to get other people to open channel with you to help solve the liquidity problem. So they put their funds up, open up with you and they basically allocated liquidity to you. Or you can use loop out and spend down your channel. So you push — your funds out and you’ll actually receive an on chain transaction from that from the loop server, from the Lightning labs team you’ll receive a brand new UTXO. and what that basically does is you just spent down — you still have the same amount of Bitcoin, right? You get that on chain, transaction worth whatever amount minus the fees, but then now you can receive payments again from other people in the network. and it’s actually a good way to to source a brand new UTXO as well,

Stephan Livera:

Right? Yeah. So just walking that through because for new people, that might be a bit difficult. So let’s say, so thinking back to that analogy with the channels, remember, it’s like an abacus and there’s beads on that Abacus. And imagine if you’re a merchant and now you’ve already been selling lots and lots of products that people have been paying you. So now in your channels, all the beads are sitting on your side, or if you’re thinking pipes, the water is on your side. Now what you need to do is kind of flush it back out or push it back the other way. So what you’re going to do is push the Lightning balance back to the other side of the channel, make a Lightning payment, right. And then receive it back on chain. Right? So it’s kind of like taking money out of your left pocket and putting it in your right pocket, but we’re just manipulating, what’s going on in terms of Lightning, versus on chain Bitcoin balance.

Stephan Livera:

So in this example, loop owls, you are making a Lightning payment out to Lightning labs, in Lightning, but then you’re receiving it back on Bitcoin on chain, right? Just spelling that out for the listener. So you understand what’s going on. There and then the other benefit, as you were saying is that actually could be a little bit interesting from a privacy perspective because it helps obfuscate a little bit what actually happened on chain because now outside observer doesn’t know what’s happened there, right. They don’t necessarily know that you’ve taken it out and pulled it back on chain, because you could have taken that back on chain into your coinjoin wallet, which you then run through a coinjoin and now, boom, you’ve received this money and the outside spy, it doesn’t necessarily know what’s going on of what your behavior is. Right?

Anthony Ronning:

Yeah. And I actually kind of prefer that method to doing a coinjoin on that, because I mean, with coin join usage. We are, unfortunately in this situation where it’s blacklisted basically in a lot of exchanges. So just seeing the fact that you were part of that coinjoin, it looks negative. Right. But for now, at least I’m getting the UTXOs. So from Lightning labs, it has like no connection to your identity at all. You didn’t get it from a KYC service, you didn’t get it. It wasn’t part of a coinjoin. You just get this brand new UTXO. So by looping out. So like, if I were starting up a new like today in order to try to get the most amount of privacy, I would like basically open up what I would do.

Anthony Ronning:

I would mix one UTXO, open the channel with that. And then if I wanted to open more channels from that, cause maybe I wanted to be, I still wanted to be a Lightning node operator. I just don’t want all my UTXO hosts to be doxed. I would just keep looping out, keep pushing funds open. I would open channels, push the funds all the way to the loop server, get a brand new UTXO from the loop and then use that to open new channels. And that way you still have the new, you’re not using the change from a previous channel. So you’re not doxing both channels that the fact that you were the channel opener and then you’re also yeah. So you still have that 50%. We don’t know which node Oh, used the Lightning labs funds to open up the channel between two nodes. So it’s yeah.

Stephan Livera:

Gotcha. Yeah. That’s a really interesting idea. And I guess who knows so even with coinjoin, it’s not all exchanges that are blacklisting them by the way, just for the listeners, some exchanges don’t like it and others are more anti chain surveillance. Just so listeners know and also probably a good point also to talk about when we are receiving Bitcoin, we have to dox certain parts of we have to show, Hey, I want to take the payment to this node. So could you talk a little bit about that part of Lightning privacy and what people can do about that aspect of it as in receiver privacy basically.

Anthony Ronning:

Yeah, exactly. I’m glad you brought that up. So as we get into these situations where like, let’s say you didn’t do anything that I suggested and you opened a bunch UTXOs maybe that are mixed, maybe they’re from Coinbase, maybe they’re from maybe even in this one scenario, which would kind of suck for a receiver, is that someone from that was part of a dark net market or something used, opened up a Lightning channel with you. Right. So you don’t have you, weren’t the one that did it. But still it’s a 50%. Okay. We don’t know which channel used it. So it is an interesting trust scenario. So let’s say you have some UTXOs and some channels that may to some regulars of bad may, maybe it’s fine, or maybe their KYCed. When you are trying to receive a paymernt, through the Lightning network, you basically, in most scenarios, you would give an invoice to the sender and you typically you’ll specify the amount and other things, but some of the things you do, you do reveal your public key, your nodes public key, and the sender can look that up — look up your public key through maybe their own Lightning node or through a service like 1ml.com and see all the channels that you have and all the UTXOs that make up the channels.

Anthony Ronning:

They can see if you’re using an IP address, they can see your IP address. So, you know it could like if — I know there’s sanctioned countries and IP addresses that are from sanctioned countries, that wouldn’t look good. So like, if you were from these countries don’t use the IP address option to receive funds. But yeah, in general, you give out all that information, IP address channels UTXOs making up your channels, all of that. When you, when you give an invoice to another person and then they can run chain analytics on those UTXOs and maybe blacklist you if they don’t like some of your UTXOs, even if you aren’t even the person that opened the channel, right? Like, so whether or not regulators or exchanges that are highly compliant will get into the situation it’s unknown to me, but I think it’s definitely a possibility.

Anthony Ronning:

And even if it’s not an exchange or regular service, if you’re, if I’m giving it to you and you see that I have 200 channels and all of that makes up like five Bitcoin or more on my node and total you’re like, “Damn! He’s a rich dude. Let me go to his house!” Because with Lightning network, you actually, your Lightning node is a hot wallet. You have to have your funds on a device, whether it’s your mobile phone or it’s a raspberry Pi at home or something, the funds are hot. So you can show up when I’m at home, or you can show up with a $5 wrench and try to say, “Okay, I know you have a Lightning node here somewhere. Give it to me!” So you’re doxing addresses sorry, amounts, UTXOs, your IP address, if you’re using IP all of that information.

Anthony Ronning:

And if you’re using private channels, so some people say, well if I have any risky UTXO shows or anything, I’ll just open the private channels. If you want to receive down those private channels, you have to reveal those as well. And when you reveal private channels, you reveal the UTXO making up those private channels. So you’re not even safe with private channels there. So it’s a whole lot of information that you do reveal and that other party senders people that you give the invoice to, if you just post it online on Twitter which some people do say, Hey, pay me. I can anyone can then look up that note and see all the information. Yeah. So definitely like for receivers, it’s terrible privacy for senders. It’s a whole lot better.

Stephan Livera:

And with that, so as part of the channel graph or the route, when nodes use that to try and calculate a route and so on, they, there’s also that short channel ID. Right. And as you point out in your article that literally shows the Bitcoin, the block number, the transaction height and the output. So it’s literally doxing the exact, this is the exact output that belongs to me or to you. And here I am world come and get me. And if you have any way in which that is being doxed out publicly, now some large companies, are probably find they’ve got an office they’ve got security or whatever. Like that’s not a big deal for them, but for the sovereign Lightning user, the sovereign individual out there, this might be more of a concern for them. Right?

Anthony Ronning:

Because even with those private channels yeah. Amount is doxxed as well. and things like that. So, yeah, you’re exactly right. Like there was a proposal to kind of like make the channel IDs random, which I think would have been a whole lot better, but currently channels do basically show the UTXO and the amount and then you can run on chain analytics specifically on the private channel, the private channel IDs that you reveal. So that’s why, like, one of the things that it’s a shame is that we do call them private channels. And when in reality, we should just call them unannounced channels because there’s not really an expectation of privacy. They’re not hidden from the world if you were to send out invoices and you can even do like private channel probing that to try to figure out a private channel between two nodes by guessing the short channel ID, which you could look up on chain to kind of get a list of possible UTXO that would make up private channels.

Stephan Livera:

Yeah. All right. So let’s talk a little bit about where this is all going in the future, because there are improvements coming. And I think it’s fair that we point some of those out too. So probably a big one, obviously Taproot, which we’ve mentioned earlier, the soft fork coming to Bitcoin and it, okay. Fingers crossed, maybe this is famous last words, but it looks like it’s coming. It looks like we’re going to get the signaling for this next period, which means we might get it towards the end of this year. And if we get that, then the Lightning protocol developers and wallet developers and app developers will upgrade the Lightning network. And that might mask some of the channel opens and closes in a collaborative close case. Right.

Anthony Ronning:

Yeah, exactly.

Stephan Livera:

And as we mentioned, so taproot will enable the point time locking routing also. So that’s another one where we’re going to get a privacy win there, probably the dual funded channels aspect of it. So if that becomes more common, that can be like a steganographic heuristic breaker. So for listeners who are interested check out, I think it’s episode 149 [https://stephanlivera.com/episode/149/] with waxwing Adam Gibson, he’s very well known for talking about that. And he can talk about the steganographic nature of that. And some of the possibilities around maybe batch channel opening, or batch some doing some of these ideas that might give a little bit more privacy. So do you have anything to add there in terms of where we’re going? What sort of steps are coming in the future that might help or mitigate some of these privacy leakages?

Anthony Ronning:

A lot of people know it as rendezvous routing. I think we may get something a little bit different that’s kind of similar called route blinding. Basically, the theory of it is that when you are a receiver and you don’t want to maybe dox who you are I think with one rendezvous routing, you would actually encrypt some of the information, some of the routing information in the invoice to give the sender, and then the sender has to get it to a certain note. It could be, it could be whatever choosing the receiver and then from there, the rest of the payment will fulfill. So the sender doesn’t know who the actual receiver will be. They just need to get a payment to the certain node. And then the rest of the payment will go through.

Anthony Ronning:

So rendezvous routing will definitely like help receiver privacy. We may end up getting something similar called route blinding, which will try to accomplish the same thing there. So those two are like probably from a privacy perspective, kind of the bigger ones that will help along with taproot and shielding you know, helping shield what could Lightning channel open or close. And then there’s also like other aspects, like, yeah, being able one of the things I think we can accomplish today and maybe it will improve with eltoo is like either the concept of channel batch openings, like you said, or even channel factories where you can collaborate with a bunch of peers and open up channels that way. So the way even with like batch channel opens, you see what I like about it?

Anthony Ronning:

I don’t know, like you said where there’s not a Samourai wallet for Lightning yet. Right. but it would be cool if there is this collaborative batch channel opening where all the inputs, instead of it, belonging to one node that is opening the channel and dual funded payments, instead of it belonging to just possibly two nodes that opened up the channel, you can even extend it to be five, six, whatever, whoever decides to join in the batch channel opening they all put their inputs together and they’ll get outputs to the other nodes and there’ll be channel openings that way. So I think some of those would definitely prove kind of more so on the on chain layer of it, but rendezvouz routing or route finding will definitely help on the receiver privacy part, which I’m excited about.

Stephan Livera:

That’s cool. And you touched on eltoo there as well. So for listeners check out episode 200 [https://stephanlivera.com/episode/200/] with Christian Decker, where we talk about the required soft fork for that, which is anyprevout and I’m hopeful that after this taproot one, then maybe we get anyprevout and then we get eltoo and then we can have some of that stuff. But so as I understand, eltoo definitely helps in terms of backups, scalability and you know, it might sort of start putting us on that pathway. Do you see any other privacy implications of that or is it mostly around scalability there?

Anthony Ronning:

I think L2 is mostly around scalability. And another aspect just I believe channel closers — cooperative channel closers look a lot healthier too, and there’s not this punishment mechanism to them. So I think — but with L2, we’ll also get channel factories. Which I haven’t looked too deeply at it, but I do believe we can kind of get a similar situation where we do get what looks like a cooperative batch channel opening. So I’m excited for channel factories as well from L2, from anyprevout. So hopefully we can get all those things within the next few years.

Stephan Livera:

All right. So let’s try and finish this with some practical or actionable tips for end users out there. So if someone is just an everyday user and they just want to be able to spend a little bit more privately, do you have any tips for them and maybe sort of say, okay, at the beginner level, here’s what you would say, and maybe at the more intermediate or advanced level, here’s what you would say for them?

Anthony Ronning:

Definitely. I would say for just general senders you know, if you’re not trying to be a James Bond or Edward Snowden, if you know a lot about mixing or you have mixed before and coinjoin before try to try to do that before opening up your channels. If you’re just general sender and you want to achieve some privacy just open up one channel, may you know, for the most part, just open up a channel with like a really good node on Lightning network and Lightning Labs just released a product called Terminal, which helps show you some good channels you could possibly connect to. Lightning network has definitely improved to a point where like, it can facilitate like really large payments now pretty quickly.

Anthony Ronning:

So just connect to one node and you send your payments that way. And for the most part, you’re not going to have any trouble. And even if you want to, like still receive, I always like point to Muun wallet as like a really good while at that has implemented some pretty good privacy techniques to help users. And then it also abstracts a lot of the channel management and worries there. So if you still want to have some privacy as like a receiver they do a pretty good job of like rotating public keys and channel IDs whenever they create a new invoice which is definitely like a big improvement from always doxing the same public key, every time you make an invoice, so for just general receivers yeah. And even general senders to Muun Wallet it’s a pretty good one.

Stephan Livera:

Yeah. That’s a cool one. So, I mean, yeah, you could maybe do a coin join and fund it with a coinjoined UTXO, and then I guess for a beginner who just wants an easy Muun wallet sort of set up, maybe that’s going to be helpful. And I know also Phoenix wallet has Tor built in as well. So that’s maybe another useful feature for some users out there. Again not Edward Snowden, James Bond level, but just, if you just want an easy spending yeah. Any tips for the Lightning node operators out there who want to try to set up a routing node, but they want to have a little bit more privacy than just open everything out there. What are some the practical tips for them?

Anthony Ronning:

Yeah, definitely. Like I said earlier, use Tor you know, maybe don’t set an alias that reveals who you are. Like, don’t say, I wouldn’t make a node and say I’m Anthony and dox myself to the whole Lightning network. And then, yeah, I would say like my suggestion and like what I would do it, like if I want to be like an operator and on a brand new note, I would open up a channel with one mixed UTXO, like one large one and, or maybe like put in a few UTXOs — mixed UTXOs if that wasn’t enough and then I would just keep looping out and get new UTXOs and just using those UTXOs to find more channels that way I’m funding channels with UTXOs not tied to my identity, and things like that.

Anthony Ronning:

So, and then from there, like, you’re pretty safe if you ever close channels. I would suggest like throw them into a Samourai wallet or another coin join implementation if you can. I know it starts getting costly, doing that over and over again. But yeah, those would be kind of my core suggestions. And then definitely like go through the article and jump to the end and I kind of lay it all out. And if you don’t want to be like completely private, you can like omit some things, but at least read the article to see if you omitted certain things, what are the connotations to that? So you at least know you’re more educated user in regards to privacy, and that’s kind of the purpose that I wanted to get out of the Lightning the article I wrote.

Stephan Livera:

And I think maybe one final note I might make as well, it’s just around, I don’t want to scare people away from using Lightning because I think ultimately let’s remember it is a huge scalability win, right? If we are bullish, we’re all bullish on Bitcoin here. And we think the number is going up into all the numbers are going to go up, right? Like number of users, price and fees are going to go up. And so, as we speak today, it might be a couple dollars to get an on chain transaction. But, if this thing is going where we all think it is, it’s going way, way higher. It might be $50 for a transaction on chain. We don’t know. And so over time, it’s going to be useful to have Lightning because there are a lot of people already using it as well.

Stephan Livera:

And I think if you just look, naively at what’s going on Bitcoin on chain, you might think, Oh, every block, only 2000 or 3000 transactions in a Bitcoin block, but that’s really more like settlements. Right? And if we look at some of the data we’re seeing now companies like BitRefill or Bitfinex, or even Zebedee with their online Lightning gaming, we’re seeing a lot of transactions happening over the Lightning network, literally thousands and thousands of transactions that are instant. So it is a huge win. And I guess my purpose and what I was thinking with this episode is the idea is we’re trying to clarify for people what’s FUD and what’s facts, right? What’s the truth of the matter around Lightning? And I want to say, I still think it’s very much useful. I’m very much a promoter of Lightning. But let’s also be aware about the privacy implications. So I guess that’s kind of a final note for me, but, do you have any final thoughts there for the listeners?

Anthony Ronning:

Yeah, exactly. That I’m a huge Lightning advocate. I love building on Lightning. I love using Lightning. I use Lightning all the time. and yeah, I’m not trying to scare anyone away. Definitely. and then, like you said, the sooner you can open Lightning channels, the better, it’s just like when we’re talking about privacy, like I have a pretty high bar in my head, like to try, there’s no such thing as perfect privacy. I don’t think you’re going to ever get perfect privacy ever in life — in general. So for me it was like, okay, let’s, let’s figure out best ways. You can try to get the most amount of privacy on your Lightning network in reasonable ways today. Like what can we do today? Not in the future, like right now.

Anthony Ronning:

So yeah, so like if you don’t want to employ all the methods because it’ll cost more in fees and it’s problematic, like that’s fine. you’re probably not doing things that for the most part would look bad or doxing yourself too much or anything like that. So definitely not trying to scare anyone away. Just if you have the time and you want to try to be a private person, or maybe you are a high risk individual, and you do want to try to get the best privacy. You can definitely read the article and give it a look. And one great aspect of Lightning is that transactions aren’t permanent like on chain transactions. So it’s like a lot of it’s revealed through active attackers. So there’s huge gains for privacy in that regards where a lot of the attacks. Temporary. so it’s pretty good.

Stephan Livera:

Excellent. So listeners, I’ll put, obviously as always, I’ll put the links in the show notes, but Anthony, where can listeners find you online?

Anthony Ronning:

Yeah, you can mostly find me on Twitter for the most part. @cycryptr or just look up Anthony Ronning and you’ll probably find me or you can go to my blog https://abytesjourney.com/Lightning-privacy.

Stephan Livera:

Excellent. Thanks Anthony for joining me.

Anthony Ronning:

Yeah, thanks a lot. See you.
