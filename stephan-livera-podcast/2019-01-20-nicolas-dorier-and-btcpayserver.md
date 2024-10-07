---
title: Nicolas Dorier and BTCPayServer – self hosted Bitcoin and Lightning payments
transcript_by: Stephan Livera
speakers:
  - Nicolas Dorier
date: 2019-01-20
media: https://stephanlivera.com/episode/48/
source_file: https://stephanlivera.com/download-episode/955/48.mp3
---
Stephan Livera: You’re listening to the Stephan Livera podcast focused on Bitcoin and Austrian economics. This is episode 48 with Nicolas Dorier, who started a great project. I wanted to discuss BTCPayServer. Nicolas is also the creator of NBitcoin, a Bitcoin library for the .Net platform in C#. Here’s my conversation with Nicolas. Nicolas, thanks for coming on the show.

Nicolas Dorier: Yeah, thank you for inviting me.

Stephan Livera: Yeah, I’ve seen you’ve been doing so many interesting things and really impressive things really with BTCPayServer. So obviously I had to get you on and get you to tell a bit of your story and tell us a little bit about why you’re doing what you’re doing. So, let’s start with a little bit of when did you into Bitcoin and what was it about Bitcoin that drew you in?

Nicolas Dorier: So what drew me in Bitcoin is basically Mt. Gox when the Mt. Gox crash happened, I didn’t really give any shits, but it turns out that I was very surprised that Bitcoin was not dead after this. I didn’t know what Bitcoin was. For me, it was just a startup money and just a scam. But because it was still living even by people who lost money to Mt. Gox and got curious about it. Well just once you start informing yourself of or Bitcoin, you’re never over and like yeah, let’s say maybe around four years, five years, I’m in this space and I still learning every day since, first question I asked. So yeah, that’s what drew me in by exactly.

Stephan Livera: Nice, nice. And then what was it also that drew you into work in terms of working on Bitcoin? Because obviously I see you doing, you’re working really hard with BTCPayServer. Someone with your skills could easily go work in some large tech company, right? You could go work for a FAANG, your Facebook, Amazon, Apple, Netflix, Google, one of those companies, and probably a hundred, multiple, hundreds of thousands of dollars. Why do you work on Bitcoin?

Nicolas Dorier: Well, because once you discover Bitcoin, everything seems a bit boring. So I am happy where in the case where I can basically find the right mix between flexibility, boredom, and a salary in my wallet. So, yeah, I mean right now everything I’m working, which is not Bitcoin is basically boring. So, I can afford to push that away.

Stephan Livera: Excellent. Okay. All right. Now let’s get little bit into what it was that drove you to go and start BTCPayServer. I’d like to hear a little bit around what it was with Bitpay that irks you.

Nicolas Dorier: Okay. So, basically before the Bitpay episode last year, I was pretty a big fan of what Bitpay was doing. I was using their wallet was Copay, which was one of the best wallets in the market at this time. And yeah, I was pretty supportive of them. I was a bit upset when they start like pushing the narrative that it was a software upgrade instead of a hard fork and tried to push all their merchant to support this new Shitcoin and telling them that is Bitcoin. I thought it was very fraudulent behavior. The people that were behind it didn’t seem to care at all about it and never bothered to apologize for this story. So, yeah, basically I found out that Bitcoin while it might be decentralized at the blockchain level because Bitcoin is hard to program upon.

Nicolas Dorier: A lot of people end up depending on the infrastructure providers, centralized infrastructure provider like Bitpay or like, I don’t know, BlockCypher or like some centralized infrastructure provider. At the end of the day, if everybody is depending on them, then even if you have a decentralized currency, you’re still vulnerable to the kind of attack that Bitcoin is meant to prevent. So yeah, that’s why I started working on BTCPay. I wanted to provide an easy to host infrastructure that everybody can run so they don’t need those kind of third party services to run their business.

Stephan Livera: Excellent. I think Nicolas, it might be great if you comment on perhaps the difference in opinion in the standing of Bitpay back in the early days versus the standing that Bitpay was in sort of towards the end of 2017.

Nicolas Dorier: The difference of what? Sorry.

Stephan Livera: In the standing, the way people looked at Bitpay, the way people would help promote Bitpay back in the early days and then it changed obviously.

Nicolas Dorier: Yeah. So, back in the day, like Bitcoin community was very supportive of BitPay. I think right now, like most of pure Bitcoiners just hate them and prevent and try to avoid merchants that accept payments that are BitPays. So, but on the other hand, BitPay become a bigger company and don’t really care anymore about Bitcoiners, so, I think it goes both way. Well, on my side right now, I’m less worried about Bitpay. One years ago they had lots of people were depending on them, nowadays there is lots of competing payment processors. So not only BTCPay, but also like coin payment and GloBee and many, many others that that start fixing the gap, that Bitpay left in the market. So I think right now they are not really, really events anymore and I think that’s for the better.

Stephan Livera: Right. Now, tell us a little bit about the narrative in a little more detail. Let’s talk a little bit about what Bitpay were trying to do in terms of how they were trying to change bitcoin. Whereas say the Bitcoiner type people, the average individual person was not necessarily in favor of those changes.

Nicolas Dorier: Yeah. Basically I think their main idea was that the merchant that are using Bitpay don’t really care about all the drama of Bitcoin. So they can silently update them without too much resistance because most of them just want to wait to get paid in Bitcoin and don’t care at all about Bitcoins. But well, lots of Bitcoiner we can tell that lots of Bitcoiner are like a stubborn minority in the sense that if it ever happened that Bitpay do this change, then pure Bitcoiner will never pay any merchants with this new coin. So, it means that we have a split and we have a new coin coming along. So, yeah, sorry, I forgot the-

Stephan Livera: I was just mentioning… I thought it’d be good to just touch on how Bitpay were basically providing a different angle than what most Bitcoiners would have agreed with. So they would say things like, “Oh, the network is congested and this is the network fee.”

Nicolas Dorier: Yeah, yeah. I mean, if you’re a merchant and you don’t care about Bitcoin, like you obviously believe what Bitpay is saying. If they tell you that the fee are high, then you don’t complain. You have no way of verifying by yourself and you don’t really care as a merchant, lots of merchant don’t really care at all about Bitcoin. So, well, I understand their position, I understand what they try to do. But at the end of the day, the customers of Bitcoiner will never use such currency that is controlled by a few infrastructure provider. Well, I understand what they try to do, but I think it’s useless as long as people are refusing to, customer are refusing to use this new coins and doesn’t matter what they try to do, it won’t work.

Stephan Livera: Right. Right. I think it might also be good if you just touch on, just tell the listeners a little bit around BIP-70 and some of the contrast and the debate that happened on that particular BIP.

Nicolas Dorier: Okay. So BIP-70 is a payment protocol which aim to remove, have a sort of protocol to pay a destination, which does not involve copy pasting addresses. And that unlock also some capabilities where while I can pay several destination in one payments. So, BIP by itself was, so for lots of reason, it has been specified in a way that is very, very bad. I think it’s very bad protocol, but for purely technical nature of sort of for example, they are using protobuf and it also either dependency at the application level about PKY and infrastructure. So it’s very… for people that want to implement their protocol, it’s like lots of requirements. However, this protocol I think is bad, but like BitPay added somewhere an extension to this protocol actually, which allow the merchant to tell what are the fees to the user.

Nicolas Dorier: I think that this particular feature is not a bad things per se. I think it’s a good idea that the merchant can communicate to the users of fees that he is expecting. It just that the manner they did it, without any once I did away without asking to the community or without asking for feedback or improvements, like threw lots of people off. But I think at the end of the day, having a way for the merchant to tell the fee, these are good things. So just to tell you the problem they are trying to fix and with this new extension that they did. When the network was congested, customer were paying the merchants to a certain rate. The problem is that we in BitPay, if the transaction take more than one hour to get confirmed, then BitPay decide that this transaction is invalid.

Nicolas Dorier: And like, then after, the merchant need to send back the money or BitPay needs to send back the money to the customer. Okay? So imagine that you are in a… when there have been lots of traffic, when the Blockchain was congested, basically lots of customer were paying, transaction were not validated after one hour, then you need to refund all those customers. But because the network is congested, refunding those customers take even more fees. So, they were kind of stucks. So their solution was, well, we might be able to impose to the user which fees they need to pay to prevent this problem. I think at the end of the day, I mean, it’s a good idea, but just the way they tried to push it and like completely removing the address turns lots of people off.

Stephan Livera: Right. Then let’s talk a little bit about some of the troubles that cause people who were trying to pay with Bitcoin.

Nicolas Dorier: Yes. So right now their new payment protocol. Most of the wallets that we’re using today are not supporting it. So, on my side in BTCPay, I made like some tool to translate their protocol to a normal address that you can copy paste on another wallet. The, so LunaNode are using BitPay as payment processor. On their side they are proposing inside their user interface. They themselves could do the piece of code to extract the address from BitPay payment protocol and show it to the users. Like people are doing work around this, and I got lots of merchant that came to BTCPay whose primary reason was we don’t want to deal with customer support that can’t pay our product basically. So, it turns a lot of people off. I think it’s bad decision, but well, it’s good for BTCPay to bring us more people.

Stephan Livera: Yeah, sure. Definitely. So I think the other thing, I think we’ve got to obviously touch on where you famously tweeted, “This is lies. I’ll make you obsolete.” Tell us a little bit about that.

Nicolas Dorier: Well, yeah, so when this happened, basically I understood that Bitcoin was in danger. If everybody keep depending on centralized services. I started developing BTCPay, so, myself as well as a Bitcoiner I’d advise, people to use BitPay to lots of customer and people I know. But basically, if you’re a merchant and you integrate BitPay, you cannot easily migrate to another solution if you don’t have developer in house that can help you to reach this transition. It takes time to test, it takes time to get it up. So my goal was, I wanted to migrate everybody that I advise BitPay to a open source solution without code change on their side. So, I basically replicated the API of BitPay inside BTCPay.

Nicolas Dorier: So, like merchant that are already integrating with BitPay can just seamlessly migrate to BTCPay without any code change to their backend. That was my primary goal. I won’t say I make them completely obsolete yet. Like for example, if you want fiat integration, you still need a payment processor either like BitPay, though I will advise better one, like, I don’t know, GloBee or CoinPayments or like many other that has been created. But in BTCPay later, so I know that Rockstar Dev is working on the fiat features and integration to add changes.

Stephan Livera: Yeah. Yeah. Well let’s start with talk with a bit of an overview around BTCPayServer and how to set one up and then we’ll get into some of the more detailed components of it.

Nicolas Dorier: So, you want me to talk about what about BTCPay?

Stephan Livera: Yeah. Just around how it’s sort of… what’s the process to set one up? How kind of, how tech savvy do you need to be to run one?

Nicolas Dorier: Okay. So good question, basically BTCPay, I took maybe half of my time coding BTCPay and half of my time trying to find the easy way to deploy it. So, when you are… so my background is mostly Microsoft. Okay. I always use Microsoft project. I love what they’re doing. In Microsoft Word, like installing new software is quite easier in general but in the Linux space. For one reason is that in general, Microsoft software come in one big blob of software that you install on your machine. While in Linux in general, it’s very lots of different small tools that you’re gluing together to get something that match your expectations. But average user, you don’t know to properly glue everything together to make it work. You cannot expect normal user to read like 10 page manual on 10 different GitHub pages on how to make those tools work.

Nicolas Dorier: Basically, lots of effort has been to make BTCPay run on one common line. Actually I try to remove this common lines. Even if you are a user that don’t have any technical capability, you can get it running. So at first I was using Azure as a hosting provider and Azure allow you to have a sort of wizard which help you to provision a new VM and install some stuff on it. I was using this, so you got a wizard where you can say, okay, I want Bitcoin, Litecoin and I want lightning network, please create the VM and give me the address. So it was working fine, just that Azure is very expensive and like not very efficient.

Stephan Livera: Yeah. So on that, let’s talk about the range of cost options now that are available to, say I’m a merchant and I want to take bitcoin payments, and I want to self host, I don’t want to use a BitPay, what are the different cost ranges or options available to me?

Nicolas Dorier: Yeah. So right now the most popular one is around nine euro per, no, $9 per month. So when I started doing it in Azure, it was 60 bucks. We managed to find ways to drop it to less than 10 USD per month and it’s really a very simple wizard, you create an account on LunaNode, you fill out your account where… you can fill out your account credit with Bitcoin if you want. Then you just have to go to a certain page, there is a sort of wizard that you can follow up to say, okay, I want Bitcoin, Litecoin, I want the lnd as a lightning network. Please do so you click and boom, like in 10 minutes you already have your BTCPay that is running. So yeah, around 9 euro per month.

Nicolas Dorier: One thing I think I can drop it to $4 with the new offer that LunaNode released recently but I still need to make some tests around this. Also, there is some people that are trying to push self hosting at home BTCPayServer. So, basically you put BTCPayServer on the Raspberry Pi and then you just run it at your home, you just open the wallet as you needed and it just work. If you do this, it’s more technical but you can drop the price to around one or $2 per month. Basically the cost of electricity that it takes to run the Raspberry Pi.

Stephan Livera: Fantastic. I think another thing that’s really great that I’ve noticed with the BTCPay community around it and the slack channel is that it’s very supportive. So, there are a lot of people who are out there creating guides. So I know Bitcoinshirt or I think he changed his name now to Pavlenex.

Nicolas Dorier: Yes.

Stephan Livera: He made a really great guide and you got guys like Rockstar Dev and you’ve got all these other people in the slack chat. Talk a little bit about that community and how they’re helping people set up their own BTCPayServer.

Nicolas Dorier: Yeah. So like it’s a big contributors to this project. So there is Rockstar Dev came first, then there was Bitcoin Shirt that came and these data is also Mr Kukks that is very active. There is also Britt K that is doing lots of translation related work that is very useful. So yeah, it’s growing and Rockstar Dev and Kukks are like developers, they think about the future they want, they just code it. Bitcoinshirt is like trying to tie everything up together. Like trying to document everything, making video of it to advertise it. As equally is like the marketing, the one Man Marketing Team of BTCPay and he did very great work. He did tutorials theory about if you’re a merchant out to create your own WooCommerce, your own e-commerce website or to create your own BTCPay or to plug them together and like everything from scratch.

Nicolas Dorier: So lots of people came on the slack asking questions and we are not a company, which mean that we cannot expend resources to have customer support people. So that’s why we depends on having the slack and the community like replying to each others when there is problems and it’s working fine. When I see problems, like lots of questions, I come backs very often like Bitcoinshirt told me, this particular point lots of people don’t understand it. So on my side I try to fix those codes so there is less questions the next time. It’s an iterative process every two or three days I release a new version and it’s slowly, slowly evolving in the right direction, thanks to all this feedback that we get continuously every day.

Stephan Livera: Fantastic. You mentioned new features there and I think now might be a good time to just talk about this Fiat exchange component. So obviously the easiest way right now is if you just take Bitcoin and just accept Bitcoin. But obviously the reality is many merchants do not have prices denominated for their inputs, the things that they’re buying and not in Bitcoin. So they have to convert it back into USD or whatever other fiat. Talk to us a little bit about what the plans are around that fiat exchange component.

Nicolas Dorier: Okay. So the main developer on fiat stuff right now, it’s Rockstar Dev. As a general rule, I never code something that I don’t use myself. For example, I never sell Bitcoin, I always hold on my side. So like I had no interest in decoding Fiats integration myself. But like Rockstar Dev for example is working on it. As far as I understand, I’m not sure because he didn’t talk to me too much about what he’s doing exactly. But the way he’s thinking is, if you’re a merchant, you buy some stock of Bitcoin on some exchange. So like let’s say you buy like one Bitcoin on, I don’t know, CoinBase and like when a payment is in coming into your store, immediately you sell a bit of this stock of one Bitcoin.

Stephan Livera: Right? So it’s almost like there’s a float maintained on the exchange.

Nicolas Dorier: Yes, yes. So basically when the money is received by the merchants, then the money will be forwarded to his exchange and the balance will be restored to one Bitcoin eventually.

Stephan Livera: Right.

Nicolas Dorier: [crosstalk 00:25:02] What he’s working on.

Stephan Livera: Right. My understanding then would be, this is because again, Bitcoin on chain was not necessarily designed to function as a retail level payments network. Because of these difficulties that you might face around confirmation time, once a transaction is sent, it may not necessarily confirm instantly or it in most cases it won’t. So that’s why we need this sort of a concept of a float held at the exchange.

Nicolas Dorier: Yep. So basically, like I tell you before BitPay, if the transaction doesn’t confirm after one hour, they call this invoice invalid. The reason behind it is, between the time that the customer sends a transaction and between the time that the invoice is created on the merchant side to the time this transaction is confirmed by the network, exchange rate is like changing a lot. So that’s why that BitPay, after one hour, if the transaction is not confirmed, they say, the exchange rate change so much that we cannot ensure about this particular exchange rates. So that’s why our plan is really to do, we receive a transaction, we convert immediate terms of change and then later coins are forwarded to the exchange. So it means it still means that the merchants is taking some risk on one Bitcoin because he has a stock of one Bitcoin with the exchange, but at least it’s calculated risk.

Stephan Livera: Right, and so the idea there, tell me if you don’t know that the detail, but is Rockstar working with any particular exchanges on who he might try to set this up to work with?

Nicolas Dorier: That’s a very good question. I’m not sure I don’t really know. I know he’s working on this. I don’t know if he’s working with a particular exchange. I know that lot’s exchange approached him to work around this. So I would say probably.

Stephan Livera: Okay.

Nicolas Dorier: But I don’t know enough myself about it.

Stephan Livera: Excellent. Well, we’ll have to get him on eventually, but so yeah, go on.

Nicolas Dorier: Yeah. So, but the thing is that in BTCPay is not like there is a specific roadmap, it’s more like different contributor want different features and just like get it done and then we ship it. So there is no real big roadmap. People sticking to it, it’s just like a need and that you just code it.

Stephan Livera: Yeah, sure. No, I totally appreciate that. I mean that’s the nature of open source software. It’s not like a standard company where there’s someone paying you to do a certain function. But I think another area that might be good for you to touch on is just around this idea of getting from the broader Bitcoiner what we might call the Bitcoin Community. Obviously years and years down the line there won’t be a Bitcoin community. But for now there still is. Are you getting a lot of support? Are you getting a lot of people who recommend, who kind of bring you new people who might use BTCPayServer?

Nicolas Dorier: Yeah, yeah. I mean, so BTCPayServer, in one year it developed entirely thanks to the Bitcoin Community we didn’t invest it into any marketing. We didn’t even had the official websites since last months. So it has been anti lead community driven or of like people trying, it’s talking to other people about it. Then at their turn they try it and like it and then spread the virus a little bit more. Even for example, BitcoinShirt that is our main, let’s say marketing guy in the team. He came himself because he learned about BTCPay about, by somebody else in the community and then try it for his own store where his selling T-shirt. He found it very interesting. He’s dedicating lots of resources to help spreading the virus.

Nicolas Dorier: So it has been very organical and like… you know, it’s thanks to the community, and people just spreading the word of mouth. I prefer it to be like this because imagine that we invest in marketing and lots of people come at once because we don’t have any supports team behind it. This will quickly implode. But if the communities keep growing and growing, even if there is more and more questions, it doesn’t matter too much because there’s so many people using it by now that lots of people can reply to questions. So, it’s very organical growth and yeah, I hope it will continue like this.

Stephan Livera: Excellent. Now, the other aspect there is also around hardware. So I know I haven’t looked into it too much, but I know nodl were looking into this idea of putting in BTCPayServer software built into the hardware full node product. Can you comment a little bit on that?

Nicolas Dorier: Well, that is awesome. So there is not only them as well, lightning in a box. There were several people trying to do this. I am very fun of this approach because it means you go further you own your own hardware, you don’t even depends on ones data center and it’s way better for the network. So right now in BTCPay, most people usually LunaNode to host because it’s the simplest one. But what if LunaNode tomorrow go out of business, then we can have a sizable impact. Of course, I can make other tutorial to other host provider. But if people run their own BTCPay in their own home, you completely remove this problem at all. You don’t have a single point of failure anymore.

Nicolas Dorier: The big challenge… So myself and my company in Japan, we will try to do some kind of box like this as well. But the main difficult part in this project is lots of consumer don’t know how to configure their router. If you host a service at home, you need to configure what we call the NAT of your router. It’s quite technical, so it’s not ready for everyone. On top of this there’s lots of internet provider that don’t provide static IP, which mean that you cannot just configure your DNS name to point to your home. There is solutions to this that I’m thinking about, but it’s still a bit messy, I’m still wondering how to make it as easy as possible. And I don’t have the perfect answer yet.

Stephan Livera: Right, right.

Nicolas Dorier: People still need to be a little bit technical savvy to set it up with these boxes.

Stephan Livera: Right. I suppose some of the other difficulties could just be if you live in an area where you don’t have reliable Internet that might drop out or power might out, and then how would you take payments on it? That kind of thing as well.

Nicolas Dorier: Yeah, that’s kind of thing as well. But there is also some people that are asking where they say, “Oh, we don’t really want BTCPay to be accessible from the outside.” So it simplifies some stuff but not everything. For example, if you want to accept lightning payments, you need a public IP and a fixed IP to receive the payments. So yeah, there is still things to think about. Indeed, if for example, you want to accept lightning payments and you don’t have a reliable connection, then you have more problems. So there’s still things to be fixed. I hope to push this push to self-hosting at home. But yeah, there’s some technical consideration around this.

Stephan Livera: Sure, sure. I suppose then the other angle is also as Bitcoin grows up, we’ll see more and more commercialization around some of these things and we may start to see more and more companies and providers who come out and say, “Hey, we’ll set up and configure the BTCPayServer for you.” That kind of a concept. You want to comment on that?

Nicolas Dorier: Yeah, I hope so. LunaNode themselves they created this simple wizard to create your BTCPay. Actually this wizard is open source itself. I think they are using cloud in it. I don’t really know what it is but like for provisioning new VM, they are using this cloud in its tool and they created this wizard where if you are a hosting provider as well using this cloud in it’s stuff, you can just use the stuff that LunaNode did. And it can easily spread that way. But right now I don’t know how interested are other host provider to offer this kinds of specific service.

Stephan Livera: Right. But I guess it all helps out.

Nicolas Dorier: Yeah, yeah. It will help out. But right now I saw only LunaNode are doing this.

Stephan Livera: Got It. I see, I see.

Nicolas Dorier: Yeah. If there is another host provider that is interested into doing this, I wish they’d join the slack and then we can all talk together about it and help them to do it.

Stephan Livera: Okay. Excellent. I think another good point that you were touching on earlier is just around in general the rise of self hosting. So obviously that is becoming more relevant nowadays, especially with this whole Patreon shutdown, more and more people looking at alternatives. What else is required to help people use Bitcoin in a self hosting approach? So, for example, making sure that the servers don’t get shut down or other tech infrastructure, not just the payments component. Do you have any ideas on that?

Nicolas Dorier: Yeah. So it’s very hard problem basically. So, here is the thing, for example, Gab right now is using, Gab.com Is using a BTCPayServer and basically recently they have been targeted by political opponents to try to shut them down even if they did nothing wrong. Basically, the way it works is that they have some services hosted on some IP address. Then people are trying to find who own this IP address and then complain to the owner of this IP address. Then this owner has better things to do than processing the sort of complaint. So they just shut them down, it’s very problematic. The only way to fix this problem is using Tor. One of the ways to, is the simplest way to solve this problem is using Tor.

Nicolas Dorier: If you are using Tor, then you’re fine they won’t manage to shut you down, but like most people don’t use Tor. So you have another option that I will, I think push people to and it’s related to those boxes as well. One solution is you host your BTCPayServer box inside your own data center. Okay? Except that you don’t accept queries directly into your data center. Instead, what you are doing is you set up another server. So for example, very small server on LunaNode on LunaNode you set up some SSH server and you use a system what we call a reverse tunneling. Basically what will happen is that if a user want to go to your website, he will use a public IP of LunaNode and LunaNode will forward the request to your backend server that is on someones IP that you control.

Stephan Livera: Right, an intermediate step.

Nicolas Dorier: Yes, and so basically if there is a complaint, if people complain to LunaNode, of course LunaNode will shut you down, but you don’t really have to care, you just go to another jurisdiction opening a new server and like just resetting this tunneling things and then you’re back on line. So, then it become very unproductive to try to reach those IP owner because it’s so easy to pop up a new service. Because they don’t own your data. It’s only possible because the server, the service provider don’t own your data. Your data is owned by yours. So it’s related as well to the boxes basically.

Stephan Livera: Right. I imagine the other way is essentially if you’re lucky, like say Gab, they managed, I think they’ve managed to find a provider who just is willing to still continue hosting them.

Nicolas Dorier: Yeah. It’s good that they find it, but it will work until one point. We never know when it will break. But well, I guess if it breaks they can jump to another provider as well. As they’re getting more and more kicked and that every time they get kicked they learn more and more about this space and they will become more and more resistant to it. Gab.com before you trying to use BTCPay, like trying many other solution. Basically, they tried every single centralized payment processor that they called and like MasterCard, basically it was like pulling the strings to prevent them to service gabs.com. At the end of the day, they become maximalist because that’s the only thing they… the only way for them to accept money then. They become more and more efficient at it as they can ban them. But at one point they will always come back.

Stephan Livera: It becomes a little bit like the story of the government trying to shut down Torrenting, like say how they tried to shut down the Pirate Bay, but then someone keeps making proxies and re pulling it back up.

Nicolas Dorier: Yeah, yeah. That’s it. I mean, as long as you own the data as long as you own your own data in your own end, then they can shut you down. You just have to find another way to get back online eventually possible. So yeah, it’s no problem, I think about this but well, it’s still right now technically speaking, it’s still a bit hard to do it. I try, I will try to make it easier, but it’s, I always come back in the sense of on my side, I’m always coding on the stuff that I use myself, and myself I’m not targeting that this kind of behaviors. I’m less motivated to work on it that say gabs.com or people like this. If people are targeted and are willing to help me on this, it will be very helpful.

Stephan Livera: Right, right. Okay. Another area, so you touched on this earlier, it was just around the hosted options. So companies like GloBee, OpenNode, CoinGate. Do you have any thoughts on the main trade-offs that a person has to think about when they’re thinking about whether they want to use BTCPayServer, self hosted or whether they would go through one of those other options?

Nicolas Dorier: Well, so the other option are possible depending on where you live, depending on the jurisdiction and depending of your political inclinations. If you are a Gab, like I am in GloBee coin payment or anything else, like eventually we’ll get shut down. There is no question of about this. For people that are not politically targeted, I think they can be good solution, but because of the fact that you don’t control your own key, what you can do with those payment processor or way more restricted. For example, BTCPayServer is not only useful for merchant, actually, it’s very good wallets. You can use it for as a wallets and you depend on your own node. So you don’t leak any privacy, you can do this with coin payment or GloBee or those kinds of services.

Nicolas Dorier: We have other features that are pretty cool. For example, where the point of sales feature where you can very easily create very simple point of sale, very easy to operate and then create invoice out of this, it’s like kind of feature that is possible only with BTCPay not with GloBee. Recently there is Mr Kukks that created a crowdfunding application of BTCPay, I don’t know if you have seen it.

Stephan Livera: [inaudible 00:43:06].

Nicolas Dorier: Yeah, it’s, I can send you the link later but basically anybody can create their own fully customized crowdfunding page and be public and then people can just send Lightning payments, Bitcoin payments to it’s. So it’s fun, it’s kind of fun feature like this that you can not re-do with centralized payment processors and way more fun feature like this will come in the future in BTCPay. So yeah keep tuned.

Stephan Livera: Yeah, it’s a very exciting space. I think there’s a lot of possibilities around this whole concept of self hosting. Have you got anything else that you wanted to bring up around BTCPayServer or anything to look out for coming up or anything else that you want to bring up?

Nicolas Dorier: Well, there is a very interesting thing with BTCPay that because it’s open source, there is some people that are just forking BTCPay, adding their own feature or adding their own design. And like time to time mergings upstream changes. If you’re a business and BTCPay doesn’t have a match yet, it’s that doesn’t have a completely matched what you want to do. It’s very easy to fork and I plan to do it even more easy, easier to fork in the future. That’s kind of flexibility that you can get from open source project but not from other centralized payments, processors.

Nicolas Dorier: For the features to look out, there is the Fiat things that Rockstar Dev is working on. I can’t say myself too much about it because I don’t really know that much about it. There is Kukks that have a pull request about doing permanent invoices. So the idea, so imagine that you are a freelance and you want to request a payment to your customer. The program right now is when you create an invoice with BTCPay, it locks the rates, the rate is locked for like 15 minutes.

Stephan Livera: Yeah.

Nicolas Dorier: If the user don’t pay in 15 minutes, then you need to create a new invoice. It’s not very user friendly. So like Mr Kukks is doing a new feature where it create a simple page of payment, we call that payment request page. So like you send a link to this page to your customer and when your customer want to pay, just click on it. It takes the rate of the day credit invoice and can pay. So it’s like you can pay it is own convenience.

Stephan Livera: Fantastic.

Nicolas Dorier: The last thing I will work is what we were talking about away, so you remember when I talk to you about this reverse tunneling-

Stephan Livera: Yeah.

Nicolas Dorier: … features. That is to prevent people to be shutdown. Actually, it’s not only useful for people that are politically targeted. It’s also very useful for people that want to host BTCPay at home because they don’t have a fixed IP. If you don’t have a fixed IP, with this reverse terminal in solution, you can still create your own BTCPay and have a very easy set up and you don’t have to configure the net, or that kind of things. So like, it started even useful for politically targeted people, but also for people that just want to plug the box at home and like that just work. So that will be what I will work on in the short term.

Stephan Livera: Yeah. That’s awesome. I think it’s really fascinating to see all the ways these different technologies are kind of building out together and interacting in different ways and you’ve got the hardware guys and then you’ve got you guys, and there’s just a really interesting, what’s the word, kind of symbiosis there in the way that some of the different products are kind of interacting together.

Nicolas Dorier: Yeah, it’s always a question of, in open source, people are not paid, which means that they need to find their own motivation to code some features. SO, it can be profit related, like people selling boxes, they hope to make profit with it. People like Kukks did with crowdfunding gap because he himself has cool idea to code and want to raise money by doing this. When people are like customer of their own products give like lots of motivation to code on it. Then as more stuff getting built, some other people say, “Oh, what you do is pretty cool. I want to use it for myself and like, maybe improve it and then little by little, the product become bigger and bigger.” It’s very organic growth and it’s a beauty of opensource.

Stephan Livera: Yeah. I think you make a great point around how many people, they just want to scratch their own itch and then that is what drives people to go and do different projects.

Nicolas Dorier: Yeah.

Stephan Livera: Yeah. Okay. Have you got anything else that you want to get the listeners to know in terms of how they can, if they want to come and support BTCPayServer or anything else to consider?

Nicolas Dorier: Yeah. I mean, a very good way to help BTCPayServer is using it by yourself and see for your own case. Like what is the gaps of features that you will like and just discuss it on the slack and just get some developer motivated to do it or developing it yourself. It’s fun and you don’t have to be a merchant even if you are normal user that just want an easy way to manage your wallet, where you don’t click your addresses to third parties, then BTCPay is for you as well. So yeah, just try it, have fun with it and come on just like sharing your experience.

Stephan Livera: Excellent. Okay. Where can people find you guys and find the slack?

Nicolas Dorier: It’s slack.btcpayserver.org.

Stephan Livera: Okay. Excellent. Also, obviously your Twitter is Nicolas Dorier. I’ll put the link obviously in the show notes.

Nicolas Dorier: There is also the BTCPayServer Twitter accounts as well.

Stephan Livera: Oh, yes, I’ll link that as well. So Twitter for that. Okay. Excellent. Anything, any final comments?

Nicolas Dorier: Oh, yeah, as well. You can also send the link to our YouTube Channel because like we have a YouTube Channel with lots of video to get started, to play with BTCPay and that kind of stuff. So yeah, I will I send it to you by text.

Stephan Livera: Excellent. All right, well look, thank you very much for coming on Nicolas. I hope the listeners found it interesting to just learn a little bit more about BTCPayServer.

Nicolas Dorier: Yeah, I hope so. I think they will.

Stephan Livera: There you go. I hope you enjoyed hearing more about the BTCPayServer project and why Nicholas started it. More importantly, I hope you’ll be interested to go and try it out. So go and check out the YouTube Channel for some how to videos and join the BTCPayServer slack and discuss with the guys links are in the show notes on my website, stephanlivera.com. Lastly, if you enjoyed this podcast, remember to retweet and share with your friends. That’s it for me. Thanks and chat next time.
