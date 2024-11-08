---
title: Day 1 Closing Panel
transcript_by: Bryan Bishop
tags:
  - lightning
speakers:
  - Elizabeth Stark
  - Peter Todd
  - Jameson Lopp
  - Eric Voskuil
  - Alex Petrov
  - Roman Snitko
---
Closing panel

<https://twitter.com/kanzure/status/1043517333640241152>

RS: Thanks guys for joining the panel. We just need to get one more chair. I am going to introduce Alex Petrov here because everyone else was on stage. The closing panel is going to be an overview of what's happening in bitcoin. I want to start with the question I started with last year. What is the current state of bitcoin compared to last year? What has happened?

ES: Last year, I was sitting next to Craig Wright. His name tag said "Craig Wright". It was petertodd. I've been in the weeds of the lightning world. There's the concept of hodl to buidl. We've seen so many developers coming into the community with so much excitement saying they were interested in bitcoin and building applications and web development and lightning was something that got them interested in bitcoin. Getting people excited about this stuff has been incredible to me over the last year. Also, this year was way less dramatic. Do you guys remember about a year ago Breaking Bitcoin Paris was the height of everything going on with No2X and the community prevailed. Bitcoin was not successfully attacked at the end of the day. Bitcoin is not ruled by any one party and it wont be successfully attacked by people in a hotel rooms trying to make deals. There's cool new tech like graftroot and taproot. This has been a year of building technology.

JL: Bear markets are great for developers.

ES: I agree.

JL: I remember the last bear market was when I went full-time at Bitgo. It was shortly after the MtGox crash and there was despair there. I didn't have any money there, thankfully. People were questioning whether bitcoin would be around in a few years, and whether this was the end and we were grinding down into nothingness. This bear market has its fair share of despair and few people who might come up with various reasons to believe that there will another be great bubble again and what not... but with the latest hype cycle we have caught a lot of interest and people have stuck around and people who have looked beyond price and exchange rate have realized there's a lot going on. Developer momentum has continued or accelerated at least in part to lightning and the ecosystem growing and jobs. One of our biggest challenges at Casa is just going to be hiring.

EV: About a year ago, people were talking about splits and forks and how mayhem was going to ensue if someone was going to run their node differently and force others to do the same. But now we can keep writing code.

PT: In probably the past hour, between the last time I was on stage and an hour ago, I probalby have done more bitcoin transactions than I did in the whole past year. I was sitting on yalls.org reading articles and paying with lightning and it's magic. It's a new experience. It lives up to many of the expectations that people go have. There are other aspects of lightning that I consider dangerous to bitcoin. But the user experience aspect of it works, and it's incredible to see something go from prototype to something you can actually run on a phone and is actually instant. It shows what you can do when you build on bitcoin. I think bcash is wonderful for bitcoin because it's split and now all these people can go away. That's a wonderful outcome. Let them do their thing and not bother us. They can say anything they want on r/btc and bcash twitter and it's really not our problem.

AP: I would like to be short. First, they ignore you. Then they ... then they try to fight you, and then you win. What state we are? I think we are between fighting and winning. There are 75 forks right now of bitcoin. None of them have value. The forks offer different solutions. They are trying to prove they are more capable and more quick. Bitcoin is still number one. Check the source code for most altcoins- they all copying bitcoin directly. They are trying to get faster transactions and to do a lot of things but what most of them are missing is the brilliant equilibrium of what bitcoin is. Bitcoin exists from 3 different points- it's a technical solution, it's an economical solution, and social equilibrium. It's building an absolutely new dimension of how the economy is working. It's practically changing the old-style economy from two-dimensional to three-dimensional. This is why a lot of dimensional guys are making their mistakes; they try to make an analogy but bitcoin doesn't have analogy. It's an evolutionary monetary tool.

RS: I want to talk about lightning. Elizabeth, you talked positively about all the changes and adoption happening. What are the current changes with lightning? Are there any issues that you think are important and hard to solve maybe at this point?

ES: When we released mainnet beta, we intentionally did not have a UI for that because we knew this was an early beta and it's not done. Jameson had a good tweet about this- when would lightning be ready? As long as bitcoin is in beta, lightning will remain in beta. This is not done, it's an on-going process. There have been bugs. We've had incredible testing from the community. Please do not put $325,000 on the network from your own pockets. Some people have tweeted that lightning is unusable and nobody would ever use it, but it turns out they are using it already. One problem is getting funds into and out of lightning. If the blockchain is a decentralized bank, lightning is like a decentralized checking account with instant payments. With the typical lightning apps except for htlc.me is they are non-custodial, and there's a key management problem. If we want to get users that aren't familiar with these concepts, we need to work on thos echallenges and the intersection of security and usability. Also, the concept of channels should be eliminated for user interfaces. If you're advanced, you can go into advanced mode and look at your channels. We're not there yet. It's awesome that petertodd is using an app and buying on y'alls. We don't have watchtowers yet- you can only receive, not send. We're very early, we're in the mid 90s of the internet world, we have not yet had the advent of the mobile phone in 2007. I think a lot of this is going to be hard work, getting watchtowers up and running, getting a good UI, and there's a lot of challenging work left. I think we'll get there. It wil take time. People want it to be already done. We're just not there.

PT: I've deliberately made a choice to use eclair with default settings exactly like other users would use. I'm not using lightning through a node I run. I'm not using eclair with my own payment channels setup. I want the most obvious thing. I want to see that experience.

RS: You said lightning wallet was unusable, then some months passed and it became usable. Do you see that progress continuing all the time?

PT: Not only did it go from completely unusable to something that works....but last time I tried eclair, every payment worked instantly.

RS: You might be hapyp to hear there's a lightning machine in Kyiv accepting lightning payments. Do you have any thoughts on lightning network and whether it's usable?

AP: To create mass adoption and usage, you need documentation. Bitcoin and lightning is still missing documentation. There's a reason why it doesn't have documentation, it's still in development. Why is there a coffee machine in Kyv? They are developers. They can understand it. They know what needs to be changed to make it really useful. They feel they understand it. But they also need to create more developers. Without developers, it's very hard to adopt any technology. They need good documentation. We need to self-organize and create the foundation maybe separate community of who will constantly train how to use the technology and constantly create documentation.

RS: I have some questions about lightning. Does lightning help with anonymity and resisting state actors and bitcoin being black market money? Does it help or not help?

JL: It helps because lightning has privacy by default. It's possible to retain privacy on bitcoin mainnet but it takes a lot of work. Whereas lightning, while bitcoin was originally thought of as this anonymous money I don't think it was really developed with that in mind. It was always pseudonymous. Lightning has been developed with strong privacy in mind. There will probably still be privacy considerations in terms of on-chain privacy vs open-closing channels... hopefully that will take advantage of on-chain privacy especially as we get better coinjoins and aggregatd signatures baked into the blockchain. I'm hoping to see the merging of better on-chain privacy to complement the off-chain privacy.

EV: I tend to not work on lightning and I don't want to comment on protocols I haven't implemented. Generally, from a crypto economics standpoint, I think layering makes sense. What you want to avoid in scaling is reducing the security of the base layer. By allowing people to make local security tradeoff-- a person-to-person transaction can be done with less security and therefore more performance. You're not destroying the security of the underlying layer. I assume that lightning is making that tradeoff in a reasonable wa.y

RS: I think some people came here to learn how to use bitcoin in their own business. Most of the people here are from the US. Alex is not.

ES: Peter is Canadian.

EV: 51st state.

RS: What is the best location to start a bitcoin company today?

PT: I did a talk on this. You need to start it near earth because otherwise as you get far away, the time dilation screws everything else. But quite seriously, there aren't that many governments that are against bitcoin. Uniquely you can just take the risk and be careful about who you deal with.

ES: Venuezla though.

PT: There are a few places that are all screwed up. Probably most of the people in the audience are in an okay location to start a bitcoin business. I would rather focus on what are you actually doing. What is your actual business plan? You will have to talk with laywers. Do you have an actual community and can you go meet people? Nobody in my city does much bitcoin stuff.

ES: With Lightning Labs, we're based in the US but we have folks around the world. There's these big tech companies where you had to be in Silicon Valley. We don't have that anymore. We will hire people anywhere. If we only stuck to one location, finding bitcoin developers is really hard. There are many jobs out there. Go take Jimmy Song's seminar and read up mastering bitcoin and lots of online resources. There's no dirth of jobs in this area anytime soon. From my standpoint and our standpoint, the Berlin hackdays just sprung up because my friends were excited about lightning it's not because we told them to go do this. Custodial businesses will have regulatory concerns. If you're just building software and ways for people to own their own funds, then you don't have to be in the old traditional place.

AP: I would like to turn the question. I'm not going to run any business in North Korea. In China, also not looking like a good place but at least you can get some pro's and con's. Georgia and Malta.. they also start to educate people. This is the greatest point, because you are giving resources. There are many developers in Ukraine and Belarus. There's developers in San Francisco but the price is too high there.

PT: One of the most interesting bitcoin meetups I've ever been to is Nairobi, Kenya. They had actual use cases for bitcoin. Depending on your temperament and what kind of business you might run... maybe moving to Venuezela and go help people smuggle money might be the best thing you could go do for yourself. Might not be the safest thing. Bitcoin is not a replacement for fiat if the government is trustworthy. Bitcoin starts to look attractive where you can't make that assumption, such as Venezuela.

ES: 20-30% of the world is blackmarkets. Go break the law, it's a blackmarket money.

AP: Only less than 7% of the population around the world have access to the banking system. The example of Africa is that they force the fall to push forward adoption for bitcoin because it's quite easy to use bitcoin it doesn't need any banks it just needs a mobile phone and they have mobile phones. It's almost like 68% of global population that has mobile phones. You need to provide them a usable coin. Bitcoin+ with lightning can be exactly this.. solution altogether. They will push these togethers. It will be very simple tool really allow them to perform payment and probably say also from configuration and the regulated government or dirty government wit hjust sting money and doesn't do anything.

RS: Final question because everyone is tired. You guys are going to be on the record. I want you to make a prediction. Any prediction. We'll come back next year and see if this materialized or not. What's going to happen in bitcoin in 1 year? It could be anything, stupid or not.

JL: I think that bitcoin is going to remain a top contender. I think that we have sufficient network effect, interest, developers, and investment, that I would bet against any kind of flippening of any kind.

RS: What about bcash?

JL: I'm optimistic about a lot of things, but not bcash.

EV: Prediction is hard, especially about the future. I predict that half the predictions will be wrong.

PT: I better go predict that I'll go ship a robust calendar backup system for opentimestamps and make my rust proof system public. I'm way late on this. You can make fun of me next year.

AP: I don't want to predict the price or what will happen in the global economy. The global economy will face crazyness in 5-10 years. The bitcoin can be really the savior and it can help reload the economy. But what will happen in years is a lot of altcoins will definitely fall down because they don't have real economy. By definition, the real economy, if you're providing, then you're using, like the currency for real deals for buying or selling services. Most of altcoins right now are like plato, on the exchanges, it doesn't have the real use case in real life. All the people are gaming through irrigation of face. Right now they are trying to understand what the blockchain what the altcoin what the bitcoin is. And south daniel will fail. Just like the ICO. It's a great tool. But right now they steel how to use it. And this is an educational face. On the next level, the real valuable state and the false value will fall down.

RS: Elizabeth?

ES: I am going to predict we will have a Schnorr implementation by next year, I really want that to happen. A lot more people will be using lightning on mobile phones once we have watchtowers running because we want people to both send and receive. A lot of forkcoins were 51% attacked and mining attacks and double spending attacks. We're going to see those with other coins especially as the cost to attack them decreases. These are things that we have talked about for years, I think we'll see more attacks in the coming year.

RS: Thanks everyone, let's give a huge round of applause.


