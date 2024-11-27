---
title: CJDNS
transcript_by: markon1-a via review.btctranscripts.com
media: https://www.youtube.com/watch?v=3P5sQwiwscI
date: '2021-03-16'
tags:
  - research
  - anonymity-networks
speakers:
  - Caleb DeLisle
  - Adam Ficsor
  - Lucas Ontivero
summary: This WRC episode shows Caleb DeLisle, the creator of the CJDNS project, discussing the benefits of decentralized mesh networking and its potential impact on the centralized internet controlled by companies. DeLisle explains the adversary tolerance of CJDNS and its use of public keys for communication verification. He also addresses concerns about the environmental impact of crypto mining and argues that it facilitates the transition to renewable energy sources. DeLisle emphasizes the attacks on decentralized finance and crypto by centralized entities and the importance of unity in the crypto community. He highlights the creation of PacketCrypt, a bandwidth-hard proof of work that incentivizes building out large amounts of bandwidth. DeLisle asserts the need to prioritize privacy, robustness, and resilience in the face of attacks and the value of positive engagement with policymakers. He also discusses the differences between CJDNS and other networking solutions, highlighting CJDNS's focus on infrastructure and resilient internet access. In addition, DeLisle mentions the potential for individuals to provide internet access to their neighbors and the financing possibilities for the Packet Network Steward. Finally, he touches on the use of Rust programming language for code review and the productivity improvements it brings in terms of security.
aliases:
  - /wasabi/research-club/cjdns/
---
## Introduction. / BIP155. / Diverse, robust, resilient p2p networking.

Lucas Ontivero: 00:00:00

Welcome to a new Wasabi Research Experience meeting.
This time we have a special guest.
His name is Caleb.
He is the creator of CJDNS project.
Basically it's a network that can replace the internet, basically, of course, that is very ambitious.
He will tell us better.
Part of this project is now already supported by the BIP155 in Bitcoin and other libraries too.
So this is an effort that part of the Bitcoin community is doing in order to have a more diverse and robust network productivity, let's say, or more resilient peer-to-peer network.
And well, CJDNS is part of that too.
Caleb, welcome, and we are happy to have you here.

## What is CJDNS. / Routing with adversarial nodes.

Caleb DeLisle: 00:01:25

Thank you very much, happy to be here.
Yeah, so CJDNS, what is CJDNS?
Really, it is a decentralized mesh networking protocol which is designed to function under in the context of some of the nodes misbehaving, that is some of the nodes being adversarial.
And that's actually very rare in routing protocols, networking protocols, because typically if one of the nodes just starts announcing garbage to the other nodes, then they will just turn the whole network into a big routing black hole.
Notable exceptions are BGP, and that's obviously how the internet is routed, but BGP is very hard to set up.
And so one of the other aspects of CJDNS is it's source routed.
That means that when you send a packet into the network...

## What is wrong with networking now? / Centralisation. / Attacks against centralisation. / War on crypto. / Decentralised finance needs decentralised networks. / Mesh network where everyone can own a piece of the internet.

Lucas Ontivero: 00:02:19

Sorry for interrupting you.
I would like to go back and ask this question for you.
What is wrong with what we have now?
What do we need?

Caleb DeLisle: 00:02:30

It's all centralized.
And it's centralized in the hands of companies that don't necessarily like us.
I mean, all you need to do is go read the newspaper, read the New York Times or read any one of these newspapers or TV stations.
And frankly, these are TV stations that haven't turned an honest profit in 20 years and they are being controlled by the centralized power structures and they are are telling the story now that we are the enemy.
We are the enemy of the people.
We are, because we're doing Bitcoin mining or any kind of crypto mining, that we need to be shut down.
We need to be stopped.
And this saber rattling that we're seeing about how it's the biggest environmental disaster in history.
And to be clear here, this is not the biggest environmental disaster in history for a couple of reasons.
One is because it's actually not that big.
To give you a reference, Russia flares off three times as much energy in gas, just from oil wells that have gas coming out.
They just flare it off into the air as the amount of energy being used by Bitcoin.
So it's actually not that big.
It's much smaller than other things that have much better lobbies.
But the other thing about crypto mining is that while it does use a lot of energy, it's also very effective at facilitating the transition to renewables because it uses the cheapest energy available and actually the cheapest available energy is what comes from renewables because there's nothing cheaper than a solar panel.
Once you put it up, it doesn't cost you anything to just let that solar panel sit there and run.

So I'm very strongly of the belief that the decentralized finance and the crypto and the mining is actually not cause of this massive environmental degradation, the reason why we're seeing this coming up in the media is because these companies these people are lodging an attack against the decentralization community and this is nothing new we go back to the 90s you have the same people you know you have Bill Gates saying that Linux is cancer.
And now, Bill Gates is buying up GitHub.
And there's all of these people who are making moves, and there is really a war on crypto going on.
It's very important right now that we're able to get our decentralized systems onto their own network.
Because if we're going to rely on a network that's run by the people who are attacking us, eventually they're going to shut us down.
So that's really why CJDNS and the PKT project is so important for me, because the point here is that we're going to be building a mesh-based network infrastructure where everybody can own a piece of the internet.
I don't want to just monologue here, I mean you have a question?

Lucas Ontivero: 00:05:46

No, no, no, no.

## Architecture of CJDNS. / IP address is fingerprint of public key. / Source routing instead of hierarchical routing. / Cloud ISPs running route servers i.e. semi-centralised.

Lucas Ontivero: 00:05:49

Now, if you can tell us what's the vision, right?
And how the technology is built in order to bypass all these restrictions and I would like personally know more about the, well I understand the technology but probably not everybody understands how it works but about it and how you work with your IPs as public keys and all the routings instead of what's the address, how to route to that address and how everything plays together.

Caleb DeLisle: 00:06:36

Absolutely.
So, CJDNS is, as I said, it is adversary tolerant.
So, you can have a bad router in that network and the network's not going to explode. There's a couple of ways that we do that.

One of them is we derive the IP address from the public key.
So we're using IP6 addresses and the address is basically the fingerprint of the public key.
So when we do that, if somebody says this is my IP address, you know that it's their IP address because you can just communicate with them and you are able to compare it to their public encryption key.

But that also poses another challenge which is that it prevents hierarchical routing which is typical of systems routing systems.
So in place of hierarchical routing we use a system of source routing and source routing means that when you send the packet into the network, it already has the entire path that needs to take all the way source to destination.
And the way that you get that route is going to be similar to the way you do a DNS lookup.
You're sending a request to a route server and that route server is giving you the path that you should use to get from point A to point B.

And where we're going with this is that there's going to be multiple cloud ISPs, what we're calling them, and these cloud ISPs operate route servers and you just choose which one you want to do business with and that one will handle the business of getting your traffic onto the network and then to where you want it to be.

Why do we have this semi-centralized model of cloud ISPs as opposed to just doing a fully decentralized, let's route on a DHT, let's do everything like that.
The reason why we're doing it the way we do it is because when your primary access to the internet is based on a network, you need to be able to call somebody when something doesn't work.
If you're paying real money to be able to get on the network, then you need to be able to make a phone call or whatever, and you need somebody to be able to handle that situation.
And we need that entity to be there, to be that network operator to be able to fix that.
But we need that not to be a monopoly that controls everybody's access to everything.
So we have these cloud ISPs, which are a little bit like just a VPN company.
And what they do is they manage all of the buying and selling of bandwidth leases from the people who are operating the actual infrastructure.

And then they find routes through the mesh in order to get you access to what you need.
Does that make sense?

## Limitations to Distributed Hash Table based routing model. / Solving the problem of: "my internet doesn't work? Who do I call?"

Lucas Ontivero: 00:09:40

Yes, but I think that is something new, isn't it?
And how was that handled before and how is that handled now?

Caleb DeLisle: 00:09:54

Yes, so original CJDNS did use a DHT and basically we beat the software up as much as we could and we realized that there are fundamental limitations to a DHT based routing model that are unsolvable without switching to something that is different.
So basically we can solve a lot of problems but the problem we can't solve is my internet doesn't work, who do I call, how do I fix this?
And because we can't really solve that who do you call problem.
That's why a fully decentralized routing infrastructure just isn't going to work in the long-term.
So in place of that, we create an ecosystem of different entities who can do routing for you and then you just get to choose which one you want to work with.

## What problem does CJDNS solve for a normal user? / A cloud VPN pays whoever is providing you with access to the internet. / TokenStrike / A token to issue bandwidth. / Lightning to trade tokens. / PacketCrypt bandwidth-hard proof-of-work

Lucas Ontivero: 00:10:54

I see.
So going down a level in complexity, I mean from a normal user, right?
Because now we are thinking all the time in normal users and translate this concept to, to my mom.
What does it mean for my mom?
What problem does this technology solve?

Caleb DeLisle: 00:11:22

Right.
So for an ordinary person, you're going to install the app onto your phone on your computer, whatever.
And then you're just going be able to access the internet via your neighbor's WiFi.
That's what we're talking about here.
You're just getting on onto your regular internet via your neighbor's WiFi and you buy a VPN and the VPN company is paying your neighbor to provide you with that access to the internet.
That's what a cloud ISP is.
It's a VPN which goes and pays the person who's providing you with the access to get to that VPN.
Does that make sense?

Lucas Ontivero: 00:12:03

It makes sense.
And how successful is this right now?
I mean, is it happening?

Caleb DeLisle: 00:12:11

So we're in really early stages at this moment.
We have the packet coin, which we're working on building all of this infrastructure on top of.
What we need is we need a very, very low cost way to transact in tokens.
Because when we're issuing bandwidth, the bandwidth is going to need to be tokenized so that people can buy and sell and trade the right to use bandwidth on a particular link.
And so we need to make a token and it's not going to work to just use Ethereum because the gas fees are just unacceptable.
So we're working on a project which we call TokenStrike.
And TokenStrike is basically you just make your own little blockchain and you sign all the blocks.
You're the issuer of the token.
You sign all the blocks.
And all that we need to do is have a means by which if the issuer does something nefarious, for example, claw back a token after they sold it to somebody, then we need to be able to identify that nefarious activity and have nodes in the network which can report to everybody that that issuer did something bad and then all of the software will be configured to not deal with that issuer until they fix their stuff.
So that's what we're working on in order to be able to tokenize and issue bandwidth.
So basically, we're talking about free tokens.
You can just make a token, you just download it to Git repository, and you compile it, and you have a token.
We're going to need that in order for these devices to sell their bandwidth as a token.
And then we're going to need to use Lightning network, which we're working on now in order to transact those tokens using HTLC contracts.
Now, CJDNS and VPN and VPN app are all in alpha testing or beta testing.
You can try out the app on Android now.
And what we're using now is we have the PKT project is based on a proof of work algorithm, which is bandwidth hard, and that bandwidth hardness is creating an artificial demand for bandwidth.
Unlike a lot of these tokens, I mean, I don't need to explain to you guys necessarily what is the difference between a token faucet and a proof of work but I'm finding a lot of people that don't understand that a proof of work is proof of fair issuance whereas all of these other kind of tokens these different issuance processes you can't prove that it was done fairly.
This is something else that I created, it's called PacketCrypt, and it is the only bandwidth hard proof of work.
So it's really just a problem that is easier to solve if you solve it together with other miners and the packet blockchain is based on the PacketCrypt bandwidth hard proof of work.
This is going to incentivize people to build out large amounts of bandwidth, which we foresee helping kickstart the decentralized bandwidth marketplace, which will finally be used for getting people off of the legacy and centralized internet.

Lucas Ontivero: 00:15:51

I don't know if I am the only one who had to make questions, but anyway, let me go with that.
So what you're saying is that basically my neighbor or I can become an internet service provider?

Caleb DeLisle: 00:16:12

Exactly.
But you're not going to need to do billing, you're not going to need to do customer service, you're not even going to need to do routing, you're just going to set up that device and it's going to start earning you packet, which I mean you can convert that to whatever currency you would prefer to have.

Lucas Ontivero: 00:16:32

So I am now an internet service provider that provides the connection to all my neighbors and they pay for bandwidth, They buy bandwidth to a company.

Caleb DeLisle: 00:16:50

Exactly, they're going to pay a company in a simple, obvious way, regular old, maybe it's $29 a month, whatever that deal is, they're going to pay that to that company in that normal, obvious way.
And then that company is going to have bandwidth traders who are going to buy those leases of bandwidth from you.
Grandma doesn't need to understand about trading bandwidth and buying the dip and these kinds of really complex things.
That's the job of financial traders.

## Why do we need PacketCrypt (PKT Network)?

Lucas Ontivero: 00:17:27

What is the proof of work that is hard in bandwidth.
Why do we need that?
Or who need that?

Caleb DeLisle: 00:17:40

The point of PacketCrypt is to create an artificial demand for bandwidth because demand drives supply.
When we create a demand for bandwidth, that's going to cause people to do to roll out more fiber.
So think about all of the Bitcoin mining equipment that's just sitting there collecting dust because it's no longer profitable, right?
You've got all this stuff from five years ago, ten years ago, and it just doesn't make any money anymore.
With PacketCrypt, if you install a fiber optic cable into your area in order to mine PacketCrypt, that fiber brings value forever, basically.
So we're leveraging the externality of PacketCrypt mining in order to get more internet to more people.

## Is the PacketCrypt bandwidth market working? / Tokenising bandwidth. / Why another coin? / Founders' fee. / Incentivise bandwidth rollout.

Lucas Ontivero: 00:18:28

Okay, perfect.
So basically, we are Bitcoiners, right?
And we are those Bitcoiners that many of us probably don't like other cryptocurrencies.
So that's why I'm asking these things.
You are saying basically that, well, the first design had some problems.
And now with this new cloud, I'm sorry, I don't remember the name, but yes, this new-

Caleb DeLisle: 00:19:06

Cloud ISP.

Lucas Ontivero: 00:19:08

Yeah.
Now, Of course you need a new token, I mean you need a way to tokenize the bandwidth in order to create a market of bandwidth.
Why is that not possible with, I mean, you need a market, right?

Caleb DeLisle: 00:19:28

Right.

Lucas Ontivero: 00:19:28

Is that market, before making my question, is that market already running?
Is it working?

Caleb DeLisle: 00:19:39

It's not really off the ground right yet, but that's because we need the token strike project in order to be able to tokenize the bandwidth.
But let me address, because you said another thing about Bitcoin maximalism, and I get it.
I've been there, I mean I've been in the Bitcoin community since 2011.
I know there's a lot of projects that are pretty shady and that's a reality here.
So why should we accept another coin as being legitimate?
So I'm going give you a general answer, which is that there is a war on crypto right now, and they are coming after the work coins first, and then once they knock down, once they're able to get control and stop they're going come after the privacy points of the going have to be hitting the narrow they're gonna be coming after the work points you know they're going be coming after the Wasabi wallet all of the ways that people can achieve liberation from these centralized powers, they're going to be coming after us.
And if we don't work together, then they are going to pick us off one at a time.
And you can see in their newspapers, they're already rattling the sword.
So we need to stick together here because there is a war against us.
And it's a war against decentralization and a war against open source and a war against individual liberty.
So that's the general answer of why we can't just bury our head in the sand and say my coin is the best, everything else is a scam.
And that's just not going to work because we will be pried apart and we will be killed one at a time.
And the specific answer, why is Packet a thing?
Why don't we just use Bitcoin, et cetera?
Well, Packet is a thing for two reasons.
And the two reasons are related to the two differences that it has from Bitcoin.
The two fundamental changes that were made.
One of them is that we have the bandwidth hard proof of work which makes it so that the mining of Packet incentivizes the rollout of network infrastructure.
The second one is that Packet has a network steward, which is basically a founder's fee, but the founder, the so-called founder, can be changed via a proof of stake based vote.
And that founder's fee is used in order to fund all of these projects in the ecosystem to develop all the technology.
Bitcoin is a great project, but it does not fund the wallets.
I mean, I'm sure you guys understand developing Wasabi is not easy because there is no funding for that.
The funding is for people who can build better SHA-256 chips.

Lucas Ontivero: 00:22:37

Yeah, okay.
Rafa?

## PKT algorithm. / Use of Lightning network.

Rafa: 00:22:40

Yeah, I was just wondering, did I understand correctly that you're using the same algorithm that Bitcoin uses so you can make use of these old like ASIC devices?

Caleb DeLisle: 00:22:54

No, the algorithm is very different but the point is that when you build out infrastructure to mine PacketCrypt that infrastructure includes fiber optic because you need that bandwidth in order to mine.
So that fiber optic that you've just run in order to mine PacketCrypt, when that mining installation becomes no longer profitable, that fiber is still there and that's still bandwidth that can reach out to people and get them on the Internet.

Rafa: 00:23:24

Got it.
You mentioned that you're using the Lightning network, can you elaborate a little bit more, like what part are you doing with that?

Caleb DeLisle: 00:23:35

We're just going to do our own Lightning Network.
You know, I mean, it's a Bitcoin fork with very few actual changes.
So the point of this, and the fact is I did not start this project in 2014, 15, 16 because I was waiting for the transaction scalability that the Lightning Network would afford.
And so then in 2019, 2018, 19, the Lightning network started to reach maturity, and so that was why I woke up the CJDNS project.
CJDNS was asleep for a good four or five years, just because the other half of the necessary technology just wasn't there yet.

Lucas Ontivero: 00:24:24

Well, something that I have never, never shared before with anyone is that I am 100% sure that they are going to come for Wasabi Wallet at least.
I'm very sure.
So, yes, I agree with you.
I think if your project finally is as useful as I think it is, of course I will need to buy those tokens with Bitcoins.
Because it's basically the currency, right?

## How can CJDNS help Bitcoin privacy? / Priority is robustness.

Lucas Ontivero: 00:25:05

Well one more question and this is my probably my last question.
Well everybody most of us probably understand that well even the IP address is the fingerprint of the public key.
We can always compute an encryption key to communicate with the other end, right?
But after that, I mean, I understand it's an end-to-end encrypted network.
What other considerations about privacy and security, but specifically about privacy, can we learn from your project?
How do you think it can help Bitcoin to make the peer-to-peer Bitcoin network a more resilient network?

Caleb DeLisle: 00:26:02

Well I mean I think that it's not so much about privacy per se, it's about robustness.
Right now, we're just praying that they don't turn us off.
I mean, as you said, that they're going to come for Wasabi wallet.
And I believe that they're not.
You know I have a strong belief that we're going to win.
We at first they ignored us and then from say 2014 to 2017 they laughed at us.
You know you remember Bitcoin is dead Bitcoin is dead Bitcoin is dead all the newspapers.
They just kept saying it.
And now we're into the stage that they're fighting us.
And we just need to take that fight and be serious about it because they are fighting us and they're telling us they're not fighting us.
But we're not going to believe them about that.
We can't just have them say, there's no war on crypto.
Just don't believe that.
It is a propaganda war.
They're going to try to fight us on the propaganda front.

I want to just hammer home how ridiculous this is.
Yesterday on Twitter everybody who used the word Memphis in a tweet was banned just and they said it was a bug, we made a mistake.
Well guess what was happening in Memphis yesterday?
Yesterday in Memphis, Tennessee, there was a protest against an oil pipeline.
Oil pipelines, I cannot hammer home enough how irresponsible it is building an oil pipeline right now because we're just at the precipice when renewable energy is going to become so cheap that oil is just going to be uncompetitive because you don't need anybody greasing oil jacks to run a solar array.
You don't need people shoveling coal to run a solar array.
Solar is going to beat the crap out of all of this stuff once it reaches the appropriate scale.
And they're still building these oil pipelines, which are just going pollute everywhere.
And you know these companies are going to walk away from these oil pipelines and just say yeah it's not our problem anymore, you clean it up and they're still building these things even now in 2021 so you know and you have these centralized platforms that are creating these bugs in order to cause people to not be able to talk about and coordinate a protest against an oil pipeline.

Lucas Ontivero: 00:28:30

Yeah.
Nopara?

## Privacy is natural.

Adam Ficsor: 00:28:33

Yeah, I wanted to say something, but you guys were touching the topic and then moving away from that and then come back all the time.
I wasn't sure, but yeah, it should be the right time that I think, if there is one thing that I learned from Wasabi and I think this would be this because and this is a very general point on privacy projects because at the beginning you know when I was telling people that this is what I'm going to do I'm going to build Bitcoin privacy wallet and everyone is saying that no you can't do that because governments hate privacy and only criminals work on privacy and things like that.
And, it's not true at all.
People in government get how important privacy is.
It's just not their first thought and no one is there to remind them that there are consequences.
But, when when you reason with people, they get it.
I mean sometimes you just ask them how much money they have and, you instantly make the point because that question makes them uncomfortable and oh you get privacy.
But the point is that these privacy projects are always started from these anarchist libertarian roots.
I think there is a very counterproductive thing here, is that, this hacker mindset is that you have to be super paranoid about everything, that's one, and added to that is that the libertarian and anarchist thought that, well, if you are working on privacy, then you're going to be thrown down.
And, that's not happening.
People get what you're doing.
What's happening is when someone creates something and advertises specifically for goods, those are, on the line of, well, what should we do with them?
And those are the things that get shut down.
But it's not that often that privacy companies get shut down.
And in fact, the problem is that no one dares to even start to work on privacy because everyone is saying that it's so dangerous.
It's not dangerous.
Everyone gets privacy.
Privacy is a human right and working on it is not dangerous, it's natural.
Sorry for my rant, but I think we should be more positive.

Lucas Ontivero: 00:31:44

But Adam, a year ago probably, we were mentioned in an internal intelligent agency that is fighting against who knows what, right?
And we are in those reports and in those investigations again and again.
I think I don't agree with you at all.

## The privacy war is not with policy makers.

Caleb DeLisle: 00:32:18

I mean, I want to jump in here because I mean, I think this is a really important topic.
We are clearly in a war, but the war is not with policy makers.
Policy makers, we need to work with them and we need to explain to them the importance of decentralizing power because this power is being centralized in the hands of a couple of these people and companies, these aristocrats, and they are holding this power over society and they're also holding power over policy makers.
You've got the European Union, they passed the GDPR, clearly they care about privacy.
Privacy is considered a fundamental human right and it is not difficult to have this conversation with policy makers it's just that a lot of people are either not doing it because they think the policy makers are the enemy which is wrong or they're just thinking that well take the case of okay CIA does a does a report on Wasabi well I mean CIA had a report on or they had some scraping from CJDNS in their internal Wiki.
That doesn't mean that they are against us.
That means that they want to know that we're here.
And we need to have a public facing answer to these people.
We need to have literature to be able to explain to policy makers, government, whatever, what we're about, who we're fighting for, we're fighting for the individual liberty of people and for democracy, and what is the other side doing?
Because the other side doesn't have any problem putting their lobbyists into government and then they're using their lobbyists to try to make government fight against us.
So we need to cut it off where it's actually happening here.

## EU parliament against encryption.

Lucas Ontivero: 00:34:15

Well, yes, I agree with that, but listen, I don't remember if this was previous week or a week before that but the the European Parliament voted for making for the messaging providers and the email providers have to be able to decrypt basically.

Caleb DeLisle: 00:34:50

Yeah, it's absolutely tragic what happened last week and this is a loss.
This is what happens when we're not lobbying, we're not talking to policy makers, the other guys go and start talking to policy makers and they are going to use their relationships with the policy makers to promote policy, which helps them to continue and establish their monopolies over control of the individual people.
So, we win some, we lose some.
The policy makers are not our enemy.
They are being pulled by our real enemy

Lucas Ontivero: 00:35:38

Anyway, they are the one that vote for these things, for just for those that don't understand what what this means is for example it's not possible to have end-to-end encryption anymore because if I provide this the chat service and I need to be able to decrypt your messages that means that end-to-end encryption is not possible anymore I mean the communication can be encrypted but no end-to-end let's say I don't know how to explain that.
Sorry, Caleb, because someone wants to speak and I don't remember.
Lokuf?

## CJDNS compared to Tor.


Please go ahead.

Lokuf: 00:36:23

Yeah.
Hi.
So I was just wondering because this sounds a little bit like the Tor project, and you have a similar concept on providing bandwidth and even though Tor itself doesn't really do any accounting on the bandwidth, but you actually have a privacy layer on top of it.
I was wondering if there is a similar risk model related to your project as being a host of the service as running a Tor exit node.
What do you think?

Caleb DeLisle: 00:36:58

It's a bit similar.
It's a bit similar as far as your risk profile when you're running a VPN.
But unlike Tor, we're not trying to have anonymity of the person versus the exit.
So we're not trying to be strong in anonymity.
Our point is to have a strong network that is robust and resilient to people shutting it down, centralized power.
Tor is going in a slightly different direction where they're they're really trying to make it so that nobody knows who anybody is and that's a very hard problem to solve and it's a very specific problem.
Tor and CJDNS and Packet will always tend to coexist because they exist on different planes and for different purposes.

Lokuf: 00:37:50

If it's okay, another question.

Lucas Ontivero: 00:37:54

Yes, please.

## Layer 2 VPN services. / IP doesn't scale down, Ethernet doesn't scale up. / CJDNS is a transport.

Lokuf: 00:37:56

Yeah, I was just wondering, it's a little bit difficult to get a Layer 2 VPN set up.
At least I don't know any service providers who would actually do that.
Do you support Layer 2?

Caleb DeLisle: 00:38:12

No, we are Layer 2.
We are a Layer 2 because we're not actually doing Ethernet.
Ethernet in my opinion is not really that useful.
It's because IP doesn't scale down and Ethernet doesn't scale up, we ended up with these two layers.
CJDNS scales both directions.
So on top of CJDNS, we just put an IP packet because it's compatible with ordinary software.
I mean, you could do Ethernet over CJDNS just like why?
That's kind of the point.

Lokuf: 00:38:54

Reasons?

Caleb DeLisle: 00:38:57

Yeah, I mean, you could do it.
It's just like doing Ethernet over like packet over SONET or SDH.
It's really the similar concept, you just have to write a little bit of code to connect it together.
CJDNS is a transport it'll transport anything you want.

Lokuf: 00:39:14

Good to know thanks.

## History of CJDNS. / Routing is easier to solve than DNS.

Lucas Ontivero: 00:39:18

Is CJDNS short for CoinJoin DNS?

Caleb DeLisle: 00:39:30

No.
Because my initials are CJD and there's a long story about that.
Originally it was supposed to be a DNS system but we pivoted it into being a routing system because routing is actually easier to solve than DNS.
DNS is a deep political problem that is not my favorite problem to try to solve.

## CJDNS vs Monero, Loki, Oxen, Mixnet. / PKT is about infrastructure not anonymity.

Lucas Ontivero: 00:39:54

Do you know about the Loki project, the project that comes from the Monero community?
It is not similar, but it's a networking solution similar to Tor and they have a coin too, I mean a token.
I don't know if it is for bandwidth.
I mean it has to be for bandwidth because what else right?
Do you know something about that in order to make a comparison?

Caleb DeLisle: 00:40:27

Yeah I know I spoke with the developers of Loki, it's a Monero fork as I recall, I mean here's the thing, they're working on anonymity and they want to do an anonymity network.
The fundamental thing is that we want to do is we want to do infrastructure.
We want to get people access to other people without having to go through networks that can be turned off.
That's like the key fundamental aspect of packet.
Whereas anonymity is just like we can solve anonymity later once we control infrastructure and people that the Bill Gates's of the world are not going to turn this off on us.

Lucas Ontivero: 00:41:18

Yes, good answer.
Okay, thank you.

Male 1: 00:41:21

I want to ask the same question.
So the main differences between CJDNS and Nymtech, I don't know if you know it, but it's similar.

Caleb DeLisle: 00:41:35

Is that Nym Mixnet?

Male 1: 00:41:37

Yes.

Caleb DeLisle: 00:41:39

I've just vaguely heard about it, but I mean, if the point is anonymity, then it's really the same answer.
It's really like we are going to be light on anonymity because anonymity costs you.
It's effort.
You have to do software development.
You have to waste resources because you're doing onion routing.
That's more resources, more latency.
That is a worse quality of service for people.
Our primary objective is to find a way to get people their primary internet access that works a hundred percent, that they can go stream the videos they want to stream, whatever they want to do, and then we can layer the anonymity on top of that.
That's a primary Internet access that's not going to get shut down because it's decentralized.

Lucas Ontivero: 00:42:31

By the way, we have a meeting especially for Mixnet.
So it is already available in YouTube if someone wants to know more about the Mixnet.
Just a question, imagine I want to be internet service provider, right?

## How do I buy internet infrastructure? / Last-mile fibre.


How can I buy?
I mean, because someone has to provide the service to me.
What is the level, I mean, I'm sure it's different from country to country, but how can I buy that?
It is possible, it is easy.
Does the telecommunication companies have a problem with that?
Can you tell us a bit?

Caleb DeLisle: 00:43:23

Absolutely.
So when you're buying internet in a data center, it is actually very easy to do.
There are lots of providers, there are lots of companies, it's very competitive.
In the data centers, we don't have a problem of people like potentially turning things off.
That's not really where the problem lies.
It's also cheap.
It's competitive, it's cheap, there's lots of options.
The problem is between the data center and your house because that's where you've got one or two companies, they have not upgraded their networks in 20 years.
They only move when there's somebody threatening them.
And basically the way that they move is to try to crush that threat so that they don't have to move anymore.
You remember back in the 90s, we had lots of dial up.
There was a big explosion of different internet service providers and then all of a sudden the cable and telephone companies they created DSL and cable and then they they just squeezed all of those little companies out of existence and then most of us have been living with DSL and cable ever since.
So if there's no competition in the market, then these companies will do absolutely nothing.
So how would you get a fast internet connection?
So you can contract, let's say you're in an area where there's no fiber you can contract to get fiber run to your house and there are companies that will do this for you it's very expensive but if you're going make money off of the people in your town, then this is potentially worthwhile for you.
And the way you do it, you find one of these companies, you contract with them.
The company that owns the telephone poles is usually legally required to allow somebody to put their cables on them as long as they follow certain rules.
That's why you have the phone, the cable, and the electricity running on the same telephone poles.
If the electric company owns the poles, they are required to let the phone company use them.
If the phone company owns the poles, they are required to let the electric company use them.
So, based on this legal requirement, you're able to use a company that will run fiber right to your house.
You're going pay for it, but it will get you internet to the nearest data center.
And then from there, you're able to lease those lines and then you're able to get fast internet, which you can then sell to your neighbors.

Lucas Ontivero: 00:46:07

Excellent, thank you.
Guys, does someone has a question for Caleb?
Okay, then what next?

## CJDNS as censorship resistant internet infrastructure.


Adam Ficsor: 00:46:23

Maybe I just like to repeat what you, what maybe my takeaway from what CJDNS is, is that I imagine this is something that goes lower than the anonymity network like Tor and the new project today for I2P, but it is going to a lower layer a little bit and it is only trying to tackle censorship resistance.
Is this what it provides?
And then we would have censorship resistant internet and on top of that it would be actually well probably anonymity networks would work better on top of that too.
Is that a fair summary or am I misunderstanding?

Caleb DeLisle: 00:47:20

Yeah, totally.
It's about censorship resistance and censorship takes many forms.
You don't think about your being censored because they haven't upgraded the quality of your internet in 20 years, but that is actually a form of censorship.
You don't have fast internet.
That is a way that you are being prevented from communicating.

Adam Ficsor: 00:47:47

All right.
Thank you.





## Can CJDNS work on any transport layer.

Lucas Ontivero: 00:47:47

So, wait.
This can be, let's say, Layer 1 and also Layer 2.
I mean, it can work also as, how to say, I forget the word, but basically it can work on top of the existing infrastructure too.
Am I right?

Caleb DeLisle: 00:48:17

Yeah.
It works.
It works either on anything that connects two computers together, including the existing internet is working for transporting data for CJDNS.

Lucas Ontivero: 00:48:31

Excellent, thank you.

## PKT Network Stewards fund projects that benefit the network.

Caleb DeLisle: 00:48:33

I wanted to make one final plug here is that because the Packet ecosystem has this institution of the network steward, we are always looking for projects and people who are developing technology in the space who need that funding, because the Packet network steward funds whatever will help benefit the objective of the project.
So it's something that Wasabi wallet can potentially participate in, or any of the side projects of Wasabi wallet can potentially participate by proposing a project to the Packet network steward and that can be funded.
It'll be funded in Packet but you know you can liquidate that to whatever you want and that's a way that we're able to bootstrap a lot of the technology that we need for this network to work.
And that again is one of the reasons why we couldn't have just done this on top of Bitcoin, because we need that aspect of the financing to build out all of this infrastructure that we need.

## How many clients are running the software? / pkt.chat

Lucas Ontivero: 00:49:50

Yes, sorry, one more question in order to have an idea of the magnitude of the growing of this project.
Do you have any idea how many, let's say, clients are running this software?

Caleb DeLisle: 00:50:07

It's a good question.
I mean, I can tell you a couple numbers.
I mean, there's about 200 people in our chat, which is paket.pkt.chat.
So, you can go there and hang out with cool people there's about 200 people in the chat there there's about 300 people on telegram I don't know exactly how many wallets there are, how many nodes and so on.
These are just kind of nebulous numbers.
That's basically what I know.

## Hyperboria / Yggdrasil

Lucas Ontivero: 00:50:43

And then what is the Hyperboria project or website or community?
What is that?

Caleb DeLisle: 00:50:50

Well, Hyperboria was a, I mean I say was, technically it still exists, but really it was about research on the CJDNS project and that in building the researching the technology of CJDNS that was going on between 2012 and 2014, 15 or so.
For the most part, Hyperboria is not really active anymore.
A lot of the people who wanted to do websites that were kind of in their own little network have moved over to the Yggdrasil project and so research continues with Yggdrasil which by the way are great friends of the Packet project.
But the Hyperboria as it were is not really a thing anymore and we're moving CJDNS from the research phase to the industrialization phase through the Packet project.

## Why use the Rust programming language? / Productivity in Rust.

Lucas Ontivero: 00:51:50

Thank you.
I have one more question.
I always have more questions.
You know, here sometimes, even where we discuss what is the best programming language.
It's probably a useless discussion.
But now, if I understand this correctly, you are, let's say, writing more new versions in Rust.
Is that correct?

Caleb DeLisle: 00:52:20

Yeah.
I mean, why?
Because I previously used C and I find it just unconscionable at this point to continue developing C or C++ because there are bugs and those bugs are going to harm people and it's just like memory corruption it's never done and like the person the very people who say oh I'll never have memory corruption bugs I'm too good I'm a good programmer that's only for idiots those are the ones who create the real problems.
Those are the ones who create the real problems.
Those are the ones who create problems that in the end, lots of people get harmed by that.
So I mean, I get it.
You know, you've got a legacy project.
It's in C, C++.
You just live with that.
That's how it is.
You do your best.
You use C comp, you use whatever you can.
No exec stack, that kind of stuff.
Which by the way, my one patch to Bitcoin was to turn on no exec stack in Bitcoin so that you know certain really simple 1990s era stack smashing attacks wouldn't work, but, at this point we want to be doing things securely.
The way that you're going to, you got to do things.
We can't just keep sticking with 20, 30, 40 years old languages.
That's my opinion anyway.

Lucas Ontivero: 00:53:47

Yes, we have some similar discussions, I remember here.
One more question about that.
How do you see the productivity of the people programming in Rust in comparison with previous experience programming in C or C++.
Because personally, I'm not a Rust programmer.
I tried to learn it many, many years ago and I was fighting against the compiler everything that I did was wrong basically so I said okay I will try this a couple of years after okay.

Caleb DeLisle: 00:54:30

Right.
Well, Rust is just very recently become on to my radar as something that's there.
I mean, five years ago, it just wasn't there yet.
You know, it was still in research phase.
So, now Rust, in my opinion, it's there.
So, you can just use it.
And as far as productivity, I mean, you pay a little bit of productivity in terms of when you're writing the code, it's a little bit less productive than if you're a C++ person, you can just bang out the C++.
But where I get major productivity improvements is when I'm reviewing the code because if I've got somebody who's making a contribution to CJDNS and they're like I've got a big huge piece of code here I have to read that line by line to see well is that is that a memory corruption issue is that a memory corruption issue is that a memory corruption issue and I know I'm not going to be perfect.
Is someone going to slip by?
I can't say honestly that nothing's going to slip by.
We're only human here.
And when somebody makes a contribution in Rust, I can just look at that I can go through it much more quickly, does have any unsafe, I can, I'm just not having to be as paranoid when I'm doing code review.
And I'm sure you understand the same thing, you get if you especially if you accept anonymous pull requests into the Wasabi wallet.
You got to look at that code.
You're like well Is that somebody trying to do underhanded crap to try to fool me, and that's just like that's the worst thing ever.

Lucas Ontivero: 00:56:06

Yep, we have no the problem with the memory because we're programming them in a managed language. 
We have a garbage collector.
Anyway reviewing code carefully because we are, I mean people move a lot of money with Bitcoin wallet and a mistake could be very very very expensive in terms of reputation and well there's a company behind so probably it could be more than reputation.
So yes, reviewing is a problem.
I cannot imagine if I have to keep track of a collection of pointers.
It could be really hard, yeah.
