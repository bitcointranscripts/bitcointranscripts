---
title: How To Get Bitcoin
transcript_by: Bryan Bishop
speakers:
  - Balaji Srinivasan
---
Preliminary notes:



Contact me- <https://twitter.com/kanzure>

How to get bitcoin

Balaji Srinivasan

My talk is going to be pretty different from the others. I will try to make this relevant to the blockchain database technology attendees. We're going to talk here today what we call the machine web. It's a web where machines earn bitcoin on each HTTP request. Who here knows what an HTTP request? Every time you load a web page, you make a lot of HTTP requests. So if you are earning bitcoin for each HTTP request, that coud be a lot of bitcoin.

We think that... what we mean is that, there are two webs. There's the world wide web where you have documents hyperlinked to each other. And you got the social web where you've got links between people with likes and tweets and hooks and things like htat. We think there's going to be a machine web where the links are the payments between machines. It's the machine payable web or machine web.

Why would we want something like that in the first place? The reason is because paywalls are a lot worse than you think. By paywall I mean, by analogy you have seen this on the Wall Street Journal website... oh sorry, Paul is in the audience, that's his article on the slide. SWell you paste this url into Google and os on, you are not paying the Wall Street Journal, you are paying google with micropayments in the form of an ad that you are viewing. This is how we monetize content on the web. This is the ad based micropayments paradigm.

If you are talking about machines as a developer, you only have the options of using paywals. If you are a developer, then you have heard about Amazon AWS. Signing up for Amazon AWS is like the WSJ paywall... you have ot put in all your information. There's really no zero-friction process for click and rent a machine without authorization. The way we are thinking about this, just by analogy, if every website has a paywall with a lock in front of it, we wouldn't have the web. Instead it would be omre like television where you have subscriptions to a few key channels and then after that you won't have... you're not going to click on a thousand links if you have to pay for each with a paywall. You would probably just visit a few websites where you have subscriptions.

Machine APIs are left in this quadrant where they can't sign to each other, there's no circulation or anything. They are stuck there. The reason why this is there, and this is an interesting and subtle point, the way that content is monetized is that you have human and they are all over here, and they take content, but 99% of them escape and don't pay. 1% of them might pay 100% of the time. Monetization models are about the humans... distracted by an ad, and then they have gone away, a situation where their monetization event is marginal. Machines don't get distracted.

The machine over here, you might set a table up over here and they pay, but if you put an ad here, they are never going to be distracted from the goa. Machines don't even click ads. Because of this, to have this machine web, we need a way for machines to pay other machines. For a machine web, you need a machine currency. We need bitcoin. ((applause))

Now that we have motivated htis, let's talk about what we're going to do with bitcoin. We built 21 Inc. It's a free piece of software, which allows you to buid the machine web. Any linux machine, any macosx machine, soon any windows machine, the software can run and earn bitcoin and also connect to other machines that spend and receive bitcoin. 21 basicaly makes bitcoin a currency available to the machine web.

There's 3 key features. The first is that 21 allows you to ver yquickly put bitcoin on any device. You install 21, you can mine, earn, sell, or start using programs. 21 also allows you to add bitcoin micropayments to your app in one line of code. You put this in front of any API. If you want 5000 satoshis per API cal, you can pass pricing information, surge pricing for APIs, that's pretty sophisticated, you can retrofit old applications to use bitcoin without knowing anything about bitcoin.

Once you have got your bitcoin, now we have basically a marketplace where you can exchange bitcoin for things on the machine web. You can earn bitcoin with each HTTP request. This coud end up being a lot of bitcoin. Let's get a feel for each feature.

First you get bitcoin on the device. this is the fastest way to get bitcoin. You don't need a credit card. You don't need a bank account. Just install 21 and go. To install 21, you just do this. "curl 21.co | sh" ... you can install this immediately, it installs dependencies which will let you setup servers. If you forget the https it will prompt you to use https. It's aware of errors. Once you install 21, we have 5 different ways to get bitcoin on your machine. You can mine bitcoin, you can buy bitcoin with coinbase, you can get bitcoin from our faucet, you can earn bitcoin by doing microtasks for 21 or for others, and you can also sell your machine resources kind of like an airbnb for machines.

When you are talking about mining in bitcoin, if you have the mining chip enabled, then you can start imning and your bitcoin counter will go up. If you want to buy bitcoin, you can buy bitcoin over here, and then we can deposit it to your wallet, that's easy to do. If you want to get to bitcoin without signing up, and if you're lazy, we will have a faucet. We rate limit this in a bunch of ways, don't abuse it, you can curl 21.co on any machine and get some BTC and start playing with it. You can earn bitcoin. This is kind of new. When people talk about a bitcoin economy where people are paid, well we pay bitcoin in small amonuts to people. If you invite people, they get paid more, especially if they have an institutional email address as opposed to your fake email address. Finally, you can boot up a machine service, 21 burn command is putting labor in and getting back bitcoin. 21 has a really easy way to-- install it, then get bitcoin. Okay.

Once you have this concept seling and getting bitcoin, you might want to build your own not just the ones built-in. We can add 21 to any app. Here's how, it's a flask app over here. Importantly, that can be an arbitrary function. Request a price over there is something which can be an arbitrary function that takes an HTTP request and returns a price, you can offer surge pricing, you can have a higher price for your friends, you can do dynamic pricing in real-time.

The third thing that we give is the ability to eanr bitcoin on every HTTP request, it's a way to monetize online with each micropayment and each HTTP request. Once you add the one line of code to the application, you can do "21 publish" and submit this to the marketplace. It's a discovery point or index point, it's like ebay or whatever, it's a marketplace for people ot discover each other. Discovery is useless wihtout community, so we have profile pages and such. We also have a slack community. That community is going to expand because of this 21 software.

So you have this free software, but what happened to your bitcoin computer? We have now made every computer into a bitcoin computer. We took our bitcoin computer and turned every computer into a bitcoin computer. You can go to 21.co/diy and we have full instructions for how to turn anything into a bitcoin computer. Just put it on your shelf and it makes money in the background. The third thing is embedded mining, but we haven't forgotten about it but we might not have time to mention it here.

In summary-- we launched this software that basically builds a third web, a machine web, it lets you make bitcoin the currency of the machine web. You can add bitcoin to any app. You can earn bitcoin by just running this software.
