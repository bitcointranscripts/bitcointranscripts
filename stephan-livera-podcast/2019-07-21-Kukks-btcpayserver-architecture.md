---
title: BTCPayServer architecture and BTC transmuter
transcript_by: Stephan Livera
speakers:
  - Kukks
date: 2019-01-20
media: https://stephanlivera.com/download-episode/1276/91.mp3
---
podcast: https://stephanlivera.com/episode/91/

Stephan Livera: Hi, and welcome back to the Stephan Livera podcast, focused on Bitcoin and Austrian economics. Today, we are carrying on with he BTCPayServer series, with Kukks, a contributor of BTCPayServer. But first, let me introduce the sponsors of the podcast.

Stephan Livera: So firstly, check out Kraken. They are the best Bitcoin exchange. I’ve been consistently impressed with the way they operate, over the years. They also have this incredible strong focus on security. They’re operating Kraken security labs, they are working on various initiatives in the space. They’re one of the longest-standing Bitcoin exchanges. They’re consistently rated the best. They offer some of the best liquidity in the industry. They’ve got high trading volume and no fees. Kraken have 24/7 support, and on the institutional business solutions side, they’re very popular there too. They offer the highest available API rate limits, and there’s also a Kraken OTC desk. Kraken offer five Fiat currencies, and also offer margin and futures trading. So, to learn more and sign up, go to the Kraken link in the show notes.

Stephan Livera: Next up, look into Unchained Capital. They’re a Bitcoin financial services company. I really like working with these guys. They offer a two of three keys multi-signature vault product, and that helps protect you against that proverbial five-dollar wrench attack. And you can distribute your keys, and Unchained Capital will be the third party co-signer. Customers who create this unchained vault also get three free months of access to Saifedean Ammous’ Bitcoin Standard Research Bulletin.

Stephan Livera: Unchained also offer Bitcoin collateral loans, allowing you to get USD liquidity without selling your Bitcoins. So this might be more tax-efficient for you, enabling you to avoid selling. So, while that loan’s outstanding, it’s stored in collaborative custody with Unchained. So, to learn more and sign up, go to the Unchained Capital link in the show notes.

Stephan Livera: So, the interview today is with Kukks. He’s a BTCPayServer developer and contributor. And I really enjoyed this chat, because we really dove a little deeper into BTCPayServer, and we spoke a little bit about the architecture of it, and also this new and upcoming concept of the Fiat Transmuter, which helps merchants take Bitcoin payment, but then actually receive Fiat, through an interface with a Bitcoin exchange. So I hope you guys enjoy this interview. Here it is.

Stephan Livera: Kukks, welcome to the show.

Kukks: Yeah, thanks. Thanks for having me.

Stephan Livera: You’re a well-known team member on the BTCPayServer project. Let’s hear a little bit about your background. How did you get into Bitcoin, and also development?

Kukks: Yeah, so I started coding when I was a teenager. I used to play this game called Runescape quite a bit, I don’t know if you-

Stephan Livera: Classic.

Kukks: Yeah, I played it so much that I eventually started looking to figure out how to be more efficient at it. And eventually I started coding these bots for it, so I didn’t have to play myself. And that pretty much kept me going full-time instead of actually playing the game. So yeah, it just took off from there. Started coding maybe at the age of 13 on that game, and by the time I was 17, I just said, “I’ll just keep on working on this full-time.” You know, as in doing coding as a career. Yeah, that’s how it all started.

Kukks: Eventually, I’ve worked at all sorts of different companies, doing mostly money-related things. So Forex, investments, insurance stuff. iGaming. So, yeah.

Stephan Livera: Excellent. And then, let’s get into the Bitcoin part of it. How did you find Bitcoin?

Kukks: Yeah, Bitcoin. So, it’s actually been a long time since I’ve heard of Bitcoin, and I bought my first stuff. But I didn’t really get into it that much back then. I think it’s been around since the Mt. Gox era, but I didn’t really get into it at all that much at that point. It was very, let’s say, rough, at that age, for me. I think I joined the dogecoin community for a while, but that was just for laughs. I didn’t really understand the tech; it was just fun stuff on Reddit, posting memes and jokes and sending tips to each other and stuff for laughs.

Stephan Livera: Yeah. So, what was it about Bitcoin that appealed to you? Was there anything in particular?

Kukks: Eventually, once you start getting into the tech … So maybe two, three years ago I started reading more about the tech behind it, and actually learning how to code with it, and programming stuff around it. And it starts appealing a lot more to me, it starts appealing a lot more to developers at least, if you actually understand the tech behind it. To me, it really hit the core when I started actually writing programs in it. And that’s how I really got into Bitcoin and fell down the rabbit hole.

Stephan Livera: Nice, nice. Well, okay. Let’s bring it to BTCPayServer then. How did you hear about BTCPayServer?

Kukks: Yeah, so, a few years ago, I was trying to start my own projects, maybe a company. But I was looking to do a crypto exchange, like most people in the beginning want to do. And I’m a C# developer, .Net developer, so obviously I ended up in Nicolas Dorier’s libraries in Bitcoin and his other projects there. And eventually I started coding my own payment processor to accept Bitcoin payments, deposits, and moving money around through that. And eventually, I ended up on BTCPay, because it did exactly what I needed to do. It really fed into all the stuff I needed to work on. And initially, I just started sending some small changes to the project. And it went pretty well, I think. It was easy for me to get into. Pretty much exactly what I needed to do. And it hit me right at the core.

Kukks: Down the line, I ended up spending so much time on BTCPay, just coding unrelated stuff to my own projects, that I just completely forgot about my own project, and just started working on BTCPay. And I really just ended up just staying there, dedicated to it.

Stephan Livera: Where in the timeline was this, in terms of BTCPayServer starting?

Kukks: I would say it was early last year that I actually got into BTCPay quite a bit. So yeah, I think BTCPay started mid-year before that.

Stephan Livera: Sort of August-ish I think, yeah. Okay.

Kukks: Yeah, yeah.

Stephan Livera: And so prior to that, had you met any of the other BTCPayServer team, or spoken with them? Or it was just purely you saw it doing something you wanted?

Kukks: Yeah, exactly, it was just something I wanted to do. I never met any of the others at all. No, I’ve never even met them in real life at all. So I only joined … Well, I started hanging out on Twitter just because the guys told me to, on BTCPay. So I was very disconnected from Crypto Twitter in general, Bitcoin Twitter. So it was all very new to me.

Stephan Livera: Yeah. And at that point, were you still working in your normal job, or had you already quit?

Kukks: Yeah, I was still working on my normal job. I actually quit officially in February this year. So I was actually doing it full-time on the side to work on BTCPay at that point.

Stephan Livera: Yeah. And how’s that experience been, quitting your normal day job to work properly into Bitcoin projects?

Kukks: Pretty great. I mean, I’ve learned way more in the past few months that I’ve been working on BTCPay than I have in my full-time job for the past few years now. So it’s been amazing for me. The community has been amazing. The biggest issue is having money to actually live off, but I had some savings going, so I’ve managed to kind of get myself lean to survive for a few more months. So, so far, I’m still going strong for now on BTCPay full-time.

Stephan Livera: Okay. Great. Let’s dive into BTCPayServer itself. I’m interested to discuss the architecture of BTCPayServer. Can you give us an overview?

Kukks: Yeah, so BTCPayServer comes in three or four parts. You’ve got the core BTCPayServer itself, which has the UI, the checkouts, the store management aspect of it, invoices. The apps, which are crowdfunding and point of sale. Then you’ve got NBXplorer, which is a Bitcoin UTXO tracker.

Stephan Livera: Oh, like a block explorer?

Kukks: Yeah, pretty much. It helps you kind of figure out what money is actually coming to your addresses, and it also helps you generate new addresses, helps you create transactions to spend with also. Yeah. And then there’s also the Docker repository, which is basically our installer, which helps us construct the entire thing on different VPSs, servers, Raspberry Pis. And it works everywhere, globally and universally. Yeah, those are the main parts of it. Because otherwise, there is also the smaller libraries. Well, smaller, let’s say … In Bitcoin and the BTCPay but Lightning integration libraries. Those are used extensively in everything, in the entire stack.

Stephan Livera: And as I understand, it’s not that there’s different BTCPay servers for different devices; it’s just the one BTCPayServer, right?

Kukks: No, no. It’s exactly the same one used everywhere. So we code once and deploy it everywhere.

Stephan Livera: Great. And so a couple of other pieces I was keen to dig into there as well. So, I understand you’ve got the potential to use TOR as part of BTCPayServer. You’ve got Let’s Encrypt and Nginx. And then you’ve also got a database as well, as the pieces that kind of form the overarching puzzle.

Kukks: Yeah. So, for a database, you could use Postgres, that’s the official one that we deploy all installations with by default. But there is an option to use MySQL and some other different types of databases. Let’s Encrypt helps you get HTTPS certificates for your websites, so that your websites are secure. And what was the other one?

Stephan Livera: Oh, just mentioning TOR as well, that you can set it up with TOR.

Kukks: Oh, yeah. So, TOR is actually included by default now, so you don’t even need to do anything. So it’s deployed automatically. If you want, you can opt out, but it doesn’t really bring any value to opt out of it.

Stephan Livera: Fantastic. So, let’s now talk a little bit about the typical ways that a merchant might use BTCPayServer, and how you’ve got ideas around making it more flexible. And how does BTCPayServer help with that?

Kukks: Yeah, so BTCPay, at this point, it’s not just a payment process, because you can do so much crazy things with it, at this point. You can pretty much deploy it and use it for not just to accept payments, but you can also use it to manage a whole system for exchanges, like I wanted to do. For example, you can use it to handle deposits and withdraws and stuff like that. Some people want to use it for, I forgot what they … Integrating it into forums, into their own specific apps. And basically, it’s quite easy to just modify it to show it to be whatever you want it to be.

Kukks: My plans to make BTCPay more flexible are pretty much interlinked with working on the new API that Nicolas announced probably a few days ago. It’s basically to allow people to not be constrained with what we show as a UI, and allow them to expand to use BTCPay as a headless system. What that means is they can roll out their own UI and create their own completely new UX experience. I mean, if you wanted to, you could use BTCPay as a API to create your own payment solution as a competitor to BitPay and CoinGate and all those guys. So it’s quite easy to do this once we have the new API rolled out.

Stephan Livera: Yeah. And I recall, just from the offline chat, you were mentioning the OAuth or OpenID feature. So what’s the interaction there?

Kukks: Yeah, so OpenID is a way to allow users to authenticate, to log in to BTCPay through an API. When you look at some apps, they tell you that you can log in with Twitter and log in with Facebook and all that stuff, and then you click on the link, and it takes you to the Twitter or Facebook, page, and it tells you, “Authorize this application to use.” This is basically allowing you to do the same thing with your own BTCPay instance. So, eventually you’ll have users being able to integrate BTCPay into their apps, or create a whole new surface that adds functionality to BTCPay, and alerts users to just log in with your instance directly. So you can create a whole new API or service, let’s say it adds a new application to BTCPay. So right now, we have crowd funding and point of sale; let’s say you create a more advanced point of sale app that hooks up to BTCPayServer. You can let users to just log in with their BTCPay account, and they can use your new app through it.

Kukks: And the possibilities for this kind of stuff can be quite endless. It’s hard for me to imagine, because I’ve been working with the same apps so often, but it’s quite big.

Stephan Livera: Yeah, sure. So then, if I’ve understood you, just to make sure I’ve got this right, does that mean, then, that similar to when you go on a website and you try to log in using your Google ID or Twitter, it’s a similar sort of thing here, but with BTCPayServer?

Kukks: Yeah, with your own BTCPayServer. And obviously, it’s not just that much. That’s only one of the small features of OpenID. But you can also log in transparently in the background. So you can have machines communicate with BTCPay. It doesn’t need to be a user to actually actively log in. It could just be just a normal API.

Stephan Livera: Okay. Let’s also talk about the Fiat bridge, or what is also known as the BTC Transmuter. Actually, before we get into that, let’s take a step back. The key reason why many merchants look for some kind of payment processing in the first place is because right now their costs are typically denominated in Fiat, meaning, they could accept Bitcoin, but then they would still need to get Fiat, because they’ve still got to pay rent and labor wages and so on. So that, historically, is why they’ve used services like CoinBase in the past, and BitPay in the past, or BitPay even today, and some of these other services. And it helps them quickly translate that Bitcoin into Fiat for them to use.

Stephan Livera: And I understand, BTCPayServer, you guys have got something you’re working on that will do a similar kind of function?

Kukks: Yeah. So, with BTCPay, one of the main features is that the funds can go directly to your cold storage wall, if you configure it that way. That means all the money is never really touched by anybody that handles BTCPay, or even the server admin, if you’re running it on a third party BTCPay host.

Kukks: And because of that, it makes handling Fiat quite hard. At least, converting it to Fiat. Since nobody has access to the money, there’s no private keys available to actually send the money elsewhere. Nobody has custody of it. So what we had to do is we had to pretty much create a separate plug-in that handles this stuff for you. Initially, we wanted to do it so that it would be built into BTCPay, and have a small feature that lets you send Bitcoin to an exchange and just trade it for Fiat. But we started hearing people telling us what the requirements were for them, and it was quite intense. So many different things. Everybody wants to handle their own different exchange, they have their own criteria on how to do it. And eventually, we just had to come to the conclusion that we needed to create this huge flexible system to handle this kind of requirement.

Kukks: And that’s where the BTC Transmuter was born. Me and Rockstar Dev were trying to plan it way back in November, around November last year. And we came up with this idea that we can create a system that allows you to define rules and conditions on how to handle your entire criteria on how to do Fiat settlement. And what we found out when we started building the system is that you can do so much more with it, since you can basically define all sorts of actions and rules. So, you can do spending of your Bitcoin, you can split the money that comes in between different users. It’s quite a big thing. I feel like BTC Transmuter is not just a Fiat bridge, at this point. It’s a way to automate your money. That’s actually how Nicolas put it a few months ago. You can do so many crazy things with it now.

Kukks: For example, a lot of people were asking us to allow BTCPay to send emails to their users once their payment was confirmed. With Transmuter, you just tell it so that once an invoice on your BTCPay store gets confirmed, send an email to the buyer telling him how much money was confirmed at what point. And then you can also tell it so that it sends a command to an exchange that you configure to place a sell order of your Bitcoin equivalent to the same amount that you received, against the Fiat that you want to receive. So you can create quite a lot of different criteria to that.

Stephan Livera: So, as I understand, the basic model is that you are maintaining some sort of float at a given exchange, and theoretically it would be a Bitcoin float at the exchange. And so while you as the merchant receives money incoming into your store, you would then, as those orders come in, or as the Bitcoins come in and hit your BTCPayServer, it’s calling out to the exchange, using, I presume, some API, that the exchange then knows, okay, sell, however many, 500 thousand sats or whatever to get the Fiat equivalent into your exchange account. Is that basically how it works? Or where am I-

Kukks: Yeah, so that’s the most common use case we came up with for how to use the BTC Transmuter to create a Fiat settlement feature. Obviously you can come up with some more crazy ways. Like, for example, you can also send the Bitcoin. So, all the money that comes in through your store can go to a hot wallet that it handled by BTC Transmuter, which then forwards, let’s say, 50% of that money to the exchange that you’re using, and 50% of the rest to go to your cold storage. And once the money is confirmed on your exchange, you can tell it to sell that to Fiat, while you also keep the 50% locally in your cold storage. That’s also another way to do it.

Kukks: So it’s quite customizable. You can create all sorts of different flows. For example, some people accept Altcoins with BTCPay. You can also tell the BTC Transmuter to just grab those Altcoins, send them to an exchange, and dump them straight away to Bitcoin. So you don’t even need to hold them or touch them at all.

Stephan Livera: Right. Yeah. Okay. And so I guess what you’re getting at there is, you can set up different ways. So for example, if you, as a merchant, want to make a decision, “I want to hold 10% of my incoming Bitcoins as Bitcoin, and not Fiat, you can set the settings up in such a way that it would do that. Is that right?

Kukks: Yeah, exactly.

Stephan Livera: Okay. And it’s interesting, then, because I guess exchanges will like this idea, because they will get new customers out of it. So, in the past, where a merchant might have used a BitPay or whoever, if they are now using BTCPayServer and the BTC Transmuter, then the exchange is getting more business out of that. So they’re happier about that, I guess?

Kukks: Hopefully. I think it makes sense for them to actually allow BTC Transmuter to work with them. I think we do have over a dozen exchanges integrated into the Transmuter, so people do have a choice on what to use. I think it should be good business for them. Some exchanges in the past have actually had a similar feature, where they dedicate a specific Bitcoin address to their customers. And once they send money to this address, they would automatically dump it for Fiat. I don’t know if it’s still a feature nowadays, but it used to be something in the past.

Stephan Livera: Okay, great. And you mentioned the 12 exchanges and the Transmuter. Actually, I haven’t had the change to see it yet in BTCPayServer. Is it a typically available option right now, or is it more an advanced feature that you need to dig into to use?

Kukks: So, it’s quite advanced. It’s still an alpha build kind of thing. But it is available as an option when you’re installing BTCPay on the side. It’s a separate UI completely, separate login and everything. It just works on the side. So they are completely separate instances. Since BTC Transmuter does have some handling of private keys, we wanted to keep them completely separate, so we don’t taint BTCPay with any private key storage.

Kukks: The private key storage is mostly there for these hot wallet interactions that you set up if you want to, obviously. But yet, it’s just part of the installer. You just run one extra command, and you should be able to go.

Stephan Livera: Great, okay. Let’s talk about Lightning as well. So, do you want to just touch on any of the thoughts around how BTCPayServer helps emergent tech lighting payment, and then any interaction, if there is any, with Fiat bridge for that?

Kukks: Yeah, so the Fiat bridge actually also handles Lightning, so it supports all the implementations that BTCPay supports. It can detect incoming payments, it can forward payments as well through Lightning. Eventually I want to have one of the use cases to allow Lightning payments to be forwarded to other people, who will swap it for on chain payments. So similar to the Lightning Loop and the other services that have been built around these kind of use cases.

Kukks: So, eventually, I’m hoping that BTC Transmuter will let you offer these services to your customers without needing a specific Lightning implementation. Because Lightning Loop is cool, but I would really like it if everything was agnostic of the implementation.

Stephan Livera: Right, I see. So, let’s talk through just an example for the merchant who wants to use Lightning. So let’s say I’m a merchant, I install BTCPayServer, I install this additional Fiat bridge or BTC Transmuter. I need to set up some Lightning channels, and ideally I need some incoming capacity. So maybe I can, you know, call out to the community and say, “Hey, guys, I want some incoming capacity”, and maybe if I’ve got a few friends, they’ll open some channels to me. And then I’ve got incoming capacity.

Stephan Livera: And so let’s say I start selling stuff, and over time the balance in that channel starts moving to my side, and then those channels start to become exhausted, because all the balance is on my side. What’s some of the options, then, in terms of submarine swaps, loop out. Do you have any thoughts around what that way is of generating the ability for the merchant to keep that flow coming through?

Kukks: Well, in terms of BTC Transmuter, in theory you could have an agreement with another person that runs a transmuter in BTCPay to create a set of rules so that whenever he receives a payment from your Lightning note, he will send you an on-chain Bitcoin transaction to you. So you can emulate the loop in and loop out through BTC Transmuter as well.

Kukks: You can do all sorts of different flows. So that’s the beauty of it. Whatever you can come up with, you can hook it up. And since it integrates directly with BTCPay, you can accept Bitcoin payments straight with it as well.

Stephan Livera: Great. All right. Are there any other ideas that you’re interested to work with on BTCPayServer in the future?

Kukks: Yes. So, one of the things with the BTC Transmuter and BTCPayServer, you have to [inaudible 00:28:17] a lot of people on the Fiat bridge, the Fiat conversion. And a big problem with the exchanges is that

[inaudible 00:28:25]

KYC has been getting kind of crazy. The other day, my favorite exchange … Well, favorite. The one I prefer to use, got this enhanced KYC policy that basically asked me for everything about me, and some more as well, that I didn’t even know what to fill in. So I wish we could eventually find a way to package up BTCPayServer and BTC Transmuter to allow people to offer Fiat and Bitcoin through them. So, for example, somebody starts up a BTCPayServer, they create a point of sale app, and they can offer sending Fiat to them in exchange for Bitcoin sent to them. So that would be a virtual ATM for Bitcoin.

Kukks: So, for example, somebody send you Bitcoin, and you send them back Fiat in some way or another. And vice versa, obviously. So that’s one thing I really want to work on, in the medium term at least.

Kukks: I also want to allow some form of exchange support. As in, running BTCPayServer to fulfill a crypto exchange-

Stephan Livera: To be an exchange, or? What do you mean?

Kukks: Yeah, yeah, yeah. Since BTCPayServer, last year, they had some work done on it to actually allow atomic swaps. So you can actually do that kind of stuff already. So if somebody wanted to emulate a whole new Bitcoin exchange or any exchange that you know at this point, if you just say that you can create BTC Transmuter and BTCPayServer to say, “Okay, every time I receive a payment on this specific store, I will send them X amount of Litecoin or whatever people want to buy.” Because it’s quite possible already to do it. At least it gets people off the whole exchange idea, that they need and exchange to actually do these trades. I prefer having these smaller peer-to-peer trades than having one big massive entity controlling all the money that has the Fiat onramp.

Stephan Livera: Right, I see. Yeah, so, I suppose, yeah, we could see a lot of smaller people offering their own little version of an exchange. And I suppose in some sense, the ATM idea is kind of related to that as well, that it’s more just like a Fiat exchange only.

Stephan Livera: I’m curious, actually, just with the ATM, could you explain a little bit further on that? So, what would the setup be? Would it be, somebody sets up a pice of hardware, or some kind of computer, and actually, it’s running BTCPayServer … Where would the Fiat part come into that?

Kukks: Yeah, so, I was talking mostly about virtual ones, so online. But I’m sure you can come up with a way. I’ve seen BTCPayServer used with vending machines and stuff like that as well. So it can hook up with some dispenser. Of course, you need to add some security sensors catching it, and people are going to try to open it with a crowbar. But virtually, I’m still trying to figure out the right way to handle transfer of Fiat. Because obviously, that’s quite a harder part to deal with.

Stephan Livera: Yeah. Yeah, in many cases, the difficulty is on the Fiat side.

Kukks: So, I mean, you can always do it in a more manual way, where they send you Fiat by mail, if you wanted to, but that’s kind of risky, in any case. So I was thinking maybe you could also, I don’t know if you’ve heard of Revolute and other payments?

Stephan Livera: Oh, okay.

Kukks: Yeah. So maybe you could use their API and have two accounts connect with each other, and then they send money to each other like that. Obviously there’s still trust in between these clients to actually fulfill the order, but as long as they’re small transactions, I don’t think it’s a big issue. And I also think they would be breaking some terms and conditions here and there to actually do these kind of trades. So if I can manage to make this easy enough for people to do, it shouldn’t matter that they just launch an instance, they do a few exchanges between people, and they get reported, closed down, and then they can just reopen one in an hour or two. So I’m hoping I can come up with some idea like that.

Stephan Livera: Fascinating stuff. Also, do you have any advice for any new developers who are looking to contribute to BTCPay?

Kukks: Yeah. Just come to the chat and hang out with us. We’ll pretty much tell you what we want to do, and if you want to do anything specifically, we’ll help you out any time you want. While we do mostly C# coding, there’s all sorts of different languages that you can do. So we’ve got front end, back end, UX work, design, Linux scripts. There’s really a lot of stuff that you can just touch and modify yourself. And if you have no clue where to start, just message us, and we’ll tell you what we wanted to work on in the short term, and we’ll guide you through them.

Stephan Livera: Great. So, are there any examples that you can think of where somebody came through and they were just sort of chatting, and maybe they’re running their own merchant store, and then they ended up contributing?

Kukks: Yeah. Well, I mean, if you look at Pavlenex, he pretty much ended up like that, right? He had a Bitcoin-insured store, and ended up hanging out in the chat so often, and pretty much doing customer support and helping out with all the issues around that, he basically lives there at this point. It’s a great example of a person really getting committed out of just his own use case.

Stephan Livera: Yeah, that’s a common trend I see as well, within the whole world of open source. It’s very much a scratch your own itch, right? So you have some certain problem that you want, and then that is what motivates you to go and work on that problem and collaborate with other people who want the same thing.

Kukks: Yeah, exactly. And that’s pretty much how I got into it as well. I mean, I wanted to do my own cliché thing, started working with the libraries that were offered by BTCPay, and eventually I got sucked down the rabbit hole, and now I just work on just these features, making sure features are growing and getting better every day.

Stephan Livera: Yeah. Did you also have any involvement with the crowdfunding application?

Kukks: Yeah. So, Nicolas actually sponsored me to work on the crowdfunding in December. Yeah, so I spend maybe a month or two building the crowdfunding app. And I think it’s been a great success so far. Plenty of people have used it in all sorts of campaigns now. I do … Yeah?

Stephan Livera: No, I was just saying, let’s dive into the crowdfunding app a little bit more. Tell us how that works and how that works a little differently from what the typical BTCPayServer merchant experience.

Kukks: Yeah. So, BTCPayServer’s crowdfunding app really is a super set of features that BTCPay offers. So it uses the invoicing system that BTCPay offers, and allows users to create an application that groups all these invoices together and creates invoices for that application. So you can say that you can create a … So , I think the last example I saw the other day we managed to create some new luxury shoes, and he needs to raise a specific amount of money for that.

Kukks: You can create perks on a BTCPay crowdfunding app, and say, “If you donate $100, or the equivalent of that in Bitcoin, you can get these fancy leather shoes.” You can have different types of these perks, so $100, $200, $500. Very similar to how Kickstarter and Indiegogo and all those platforms look like. And people can obviously just see everything on our nice and simple UI.

Kukks: The UI is quite a straightforward experience, in my opinion, for users to just edit and just launch. And I don’t think there’s been too many issues around that. Even during the we are all hodlonaut campaign, which used the BTCPay crowdfunding app, we maybe got maybe one or two issues that we fixed straight away on that campaign, and other than that, it was smooth sailing, even for that huge amount of donation volume.

Stephan Livera: Yeah. I think, just to add some context, it might be interesting to talk about the amount of saving that can come from using BTCPay crowdfunding app. Whereas if you go through these traditional providers using standard Fiat rails, you might easily be paying two or three percent per donation. And that can really add up. So let’s say $10,000, that’s now $200 or $300 gone on fees.

Kukks: Yeah. And I think it actually is a lot more than two or three percent, because that’s only for the transaction charge. Then they have administration fees on top, and it can easily go up to 12%, if I remember correctly. So with BTCPay, you save a lot of money. But that also applies to BTCPay in general. Just using BTCPay over BitPay and all the other payment processors that are custodian-based, that take a little hold of your money for a bit of time, they still charge you between 0.5% to, I think I’ve seen it up to 5% sometimes. So there’s savings all around, considering you can host BTCPay for, I think it’s $4 a month at this point.

Stephan Livera: Yeah, that’s an interesting one as well. Because I really from my chat with Pavlenex, he was saying at the start it was something like $60 a month to host it. And then that cost dramatically came down. Why was that?

Kukks: Yeah, so that happened because, initially the official way to install BTCPay was through Azure. And Azure is quite expensive in every regard. So just hosting it there was always going to be expensive. So I think it was more than $60, too. I think it was more like $100 at that point. So once the installer got adapted to be more agnostic of where you’re installing it, everything got reduced drastically in terms of cost. BTCPay can be run on a Raspberry Pi without too many issues, so it’s quite lightweight in itself. You just buy a $30 and you can host it in your own home.

Stephan Livera: And what about trying to make BTCPayServer work with some of the different … As I understand it, there are different web store plugins, right? So there’s WooCommerce and so on. Is there a lot of work that’s required to keep it up to date with those, or is that not a huge deal?

Kukks: I don’t think it’s a huge deal, but the code base that we use for these plugins is actually forked from BitPay, since we actually emulated their whole API. Their code base is not, let’s say, the best, and the most well-maintained, so we do get all sorts of issues with them every now and then. But I do hope that once we get a new API going, I’ll be able to rewrite all of them to a cleaner code base. But yeah, fingers crossed. It’s not a big issue.

Stephan Livera: Yeah. And as I understand it right now, then, there is, I guess, some element of back porting required as well, for now, while BitPay are changing some of their things on their end.

Kukks: Yeah, yeah. I mean, they don’t change that much from their end. And they do have to keep some backwards compatibility, because they have so many merchants that aren’t really willing to change their plugins just for breaking support for old code. So, in terms of backwards compatibility, it’s not that big of an issue from their newer code base, but for us, we do add a lot of stuff to BTCPay, and we have to make sure it stays fitting with the BitPay layer. So that is a bit annoying to do, but there’s nothing we can do about it. We just have to stay careful and kind of handle our code base with more care, just to make sure it stays fitting. I do wish that eventually, once we have the new API and everybody settles in with it, that we can make the BitPay compatibility layer an opt-in thing. But maybe down the line.

Stephan Livera: Right. Yeah. And do you have a sense … So, I know, obviously, this is open source software, we don’t know exactly who’s using it. But do you have a sense of how many merchants are out there in the wild using BTCPayServer? Just even a rough estimate?

Kukks: I would say a few thousand. I can’t really say much more than that, but I would say a few thousand. I do know that some of the volume on some of these merchants is insanely crazy. The statistics regarding Bitcoins being transacted on them is huge. I won’t say numbers, but it’s ridiculous. So it is definitely making an impact.

Stephan Livera: That’s great to see. And in terms of BTC Transmuter, do you know how many people are using that alpha version, and what’s their feedback been so far?

Kukks: Yeah, so I’ve mostly been working with Mike from Coincards. We’re using it obviously in production with him, since he loves to be reckless. But it’s been working great with him. I think so far we’ve only had a few issues, and I’ve been pumping out bot fixes and versions every time we encounter something. And we’re not really advertising the plugin too much right now, because we don’t want people to have a bad experience from the start. But I think in, I want to say a few months from now, it should be nice and smooth.

Stephan Livera: Excellent. Look, I think that’s just about it in terms of questions I had on my list. Did you have anything else you wanted to touch on?

Kukks: Nothing that I can think of directly.

Stephan Livera: Okay, great. Well, look, it’s been fantastic chatting with you, and it’s a lot of context that hopefully any listener who is thinking about being a merchant and running BTCPay themselves can use. And lastly, before we let you go, make sure you tell the listeners where they can find you online, and if they want to chat with you, where can they find you?

Kukks: Yeah, you can find me mostly on our Mattermost chat, so that’s chat.BTCPayServer.org. And Mr Kukks on Twitter.

Stephan Livera: Fantastic. Well, look, that’s been great. Thank you for coming on.

Kukks: Yeah, thank you. Thank you for having me.

Stephan Livera: I hope you guys enjoyed that. I thought it was pretty cool just to get some insight into the way Kukks is thinking about these things, and also the progress on some of these different features, such as the BTC Transmuter or the Fiat bridge. So I hope you guys are enjoying this series. We’ve got one more episode coming soon. And just a reminder, you can subscribe and get the show notes on my website, stephanlivera.com. Share the episodes with a friend, review or rate the podcast. If you want to advertise, you can email me, stephanlivera@pm.me. And similarly, if you’ve got any feedback, you can DM me on Twitter or email me. Thanks, guys, and I’ll speak to you soon.
