---
title: Maintaining Bitcoin Core-Contributions, Consensus, Conflict
transcript_by: Stephan Livera
speakers:
  - Jonas Schnelli
date: 2021-01-14
media: https://stephanlivera.com/download-episode/2832/242.mp3
---
podcast: https://stephanlivera.com/episode/242/

Stephan Livera:

Jonas. Welcome back to the show.

Jonas Schnelli:

Hey! Hi, Stephan. Thanks for having me.

Stephan Livera:

Jonas, Its been a while since we spoke on the show and I was excited to get another opportunity to chat with you and learn a little bit more and obviously talk about this on behalf of some of the newer listeners who are coming in and they may not be familiar with how does Bitcoin Core work. So just for listeners who are a bit newer, can you just give a bit of background? Who are you, what do you do in this space?

Jonas Schnelli:

Yeah, sure. My name is Jonas Schnelli. I live in Switzerland. I started getting interested in Bitcoin in 2011 and follow the open source project called Bitcoin back then started to contribute in 2013 and went full time, kind of as my job to work on Bitcoin Core in 2015 and made over a 30,000 lines of code in Bitcoin Core. And before that I worked as a software engineer for roughly 20 years.

Stephan Livera:

Excellent. And so can you spell out a little bit about the role of a maintainer in an open source project like Bitcoin?

Jonas Schnelli:

Yeah, so maintaining or maintainers usually duty. I sometimes call it like the janitor job cleaning up, reviewing making releases, things that needs more attention than just writing features. I think it’s very important to have stable maintainers, people that not come and go that’s what is one of the skillsets you probably need some basic trust from the ecosystem that you’re not maintaining it in the wrong direction and what it means job wise. It means a lot of communication. So when I get out, go to my computer, there’s roughly 150 GitHub comments in 24 hours. I need to skip through those, take the ones out that are in my area, or that interests me. Make sure you give feedback to especially new contributors or give feedback on things that laying around for a long time. So the project can move on. And of course there’s a lot of work around features and pull requests, which means releases, testing, infrastructure, stuff like that. And luckily we’re a handful of people who do the maintaining and ideally there will be more, but it’s kind of hard to get people to commit to that job. So that’s why it’s currently six people.

Stephan Livera:

Yeah, it sounds very much like tough work and sometimes a bit of a hidden or a thankless task in many ways. I think for listeners who might be a little bit newer, they might just be trying to learn about Bitcoin. What does it mean that Bitcoin’s code is open source and that there’s no top down leader. There’s no CEO of the Bitcoin code right?

Jonas Schnelli:

I think that’s one of the big reasons why Bitcoin has developed so stable over the last year since so natural because there’s no leadership. Satoshi disappeared roughly in 2013 compared to other cryptocurrencies like Ethereum Monero. And these was like coin and stuff. They have still all a leadership structure, the founder or in Ethereum as a good example with Vitalik is still there. And this influences that direction in a non-scientific way. And I think that’s a great thing we have at Bitcoin Core. There’s no leadership and open source in my opinion means everyone can change the code towards the direction he or she wants. And of course there is currently a project called Bitcoin Core, which is dominant implementation, but it’s always possible for not in terms of the hard fork of the consensus, but to fork the code and change it in a different direction. At the end, it’s the users. They decide what software they want to run, but I think core has made a good job over the last years. People putting a lot of trust into Bitcoin Core and think it’s a stable environment for development.

Stephan Livera:

From the user’s perspective, I guess. Could you just outline a little bit how developers of Bitcoin Core have to respect the wishes of the users, right? It’s not that you guys are the kind of top-down leaders and you guys set how things go and everyone must use your code. Why is that?

Jonas Schnelli:

Yeah, these ideas or debates come up here and there, I lastrRemember during the hard fork debate, I think it was 17. Or even before when some people said, well, the core people are not doing this. The core people are not doing that. They sit in an ivory tower and decide what they want. Well, first it’s an open source project. Secondly, if you put resources in, you have something to say, you can steer it in that direction and it’s completely open. So everyone can open a pull request. Is it right whoever they can open a pull request and no one will close the pull request because of emotions. That’s really where it’s scientific. So if a big enemy of Bitcoin, whoever that is starts to open a pull request, it will take seriously. If it’s technically feasible, what he or she wrote. And that’s really important to understand.

Jonas Schnelli:

So whenever you put resources into Bitcoin Core, you can steer similar to Linux. That’s also why IBM Redhat adds all these bigger companies into computers. They have their dedicated contributors to the Linux kernel because they have, they want to have a stake in it and they need it for their enterprise solutions. So they have ideas in what direction they want to go. Although this doesn’t mean if a new contributor comes and tries to change, let’s say block size to one gigabyte, there will still be scientific discussion and people will probably neglect to it. And it will very likely not be merged. So it’s still consensus. You can steer it in a way, but there’s no ultimate power you can enforce if you’re just a single contributor.

Stephan Livera:

And I presume as well that as developers, there’s some level of what we might call stewardship. And you’re trying to, in some way, respect the intention of the users and the kind of goals of the project wouldn’t you say?

Jonas Schnelli:

Absolutely. So it doesn’t mean that every developer has its own agenda and goes into like it pulls in each direction. So there’s still, there’s an issue tracker and obvious users who doesn’t have the development skills, they file issues. They all ask for features. Of course, the community as a whole gets respected in the whole development process, reasonable things get addressed. There’s a lot of development or developers. They don’t have a clear perspective where they want to end up. They just want fulfill the needs of the ecosystem. I call myself in that realm and I think there’s very much listening to the users and implementing what they want or what we think they want. Of course, if there’s special needs for enterprise solutions, that’s up to the enterprises to put these resources into Bitcoin Core. Usually if someone comes out, asks in an issue, well, the Bitcoin Core doesn’t work with 1000 wallets, please make that happen. Then usually we say if you need enterprise solutions in Bitcoin core, it’s up to you to find these resources eventually pay for these developers to implement it and maintain it.

Stephan Livera:

Right? And so maybe it’s a good point here just to spell out who are some of the main, let’s call it stakeholders then in Bitcoin Core, because if we’re trying to understand who controls it well, what are the different directions it could get pulled in? So I guess, let me just spell out a few. You might be thinking, okay, well, the miners are a stakeholder in bitcoin people who create software or hardware that interacts with Bitcoin Core. They might be a stakeholder. The end user might be a stakeholder. Bitcoin companies like exchanges and financial services and other Bitcoin companies. They have some interest or stake in what’s going on with Bitcoin Core. Are there any others or do you want to spell out some of the stakeholders in this?

Jonas Schnelli:

Yeah, I think you nailed it pretty much how it is. And I think what still surprises me and we have, like, we had 10 years on the road with Bitcoiners are still only very few companies from those one we see daily doing between business that actually contribute to Bitcoin Core. That still surprises me today. So when we look at what companies are putting resources down, I think the one that leads out is probably Chaincode labs from New York. Alex Suhas’ company, they employ quite a few Bitcoin Core developers and also lightning. So I think at least 10 or around 10 and they have no business. So that’s, that needs to be said they have no traditional business where they want to get something back in terms of financial reward. So this is more of a kind of foundation approach. And on the other hand, there is Blockstream that was prominent over the few over the last few years.

Jonas Schnelli:

Nowadays, think if I’m right, they only have one, or at least two developers working on Bitcoin Core, some on lightning. They went a lot. They reduce their resources a lot over the last years. And of course the new players like, OKCoin sponsoring a few developers, Bitmain was sponsoring, but they stopped last year and miners have a stake for sure. We know that they want their block reward, but on the development side, they haven’t put much resources in, but I think they will come now and take over a lot because they really depend on a great infrastructure.

Stephan Livera:

Right. And I guess when it comes to making contributions, there is a process around this. And so listen as if you’re unfamiliar some earlier, good episodes are the one with John Atack 124, I think. And Steve Lee, Gloria Zhao and John Newbery, some of those are early episodes. You can see those in the catalog. I’ll put links to those Jonas. If you could just tell us a little bit about the contribution process and then what it takes to have that contribution reviewed and then merged. What does that look like?

Jonas Schnelli:

I think if you’re a developer coming from traditional software development process, more in the private sector, it’s like, if you work at Google or whatever, and you come and start to contribute to an open source project like Bitcoin Core, first, you need to adapt your mental set. Because usually when you work in a business software and things go very fast, you write a line of code where you write the change. Maybe someone looks at it, maybe not, and it will be merged in a few days or you, merge it yourself in a few days into the stable master branch in Bitcoin Core, things are really different and we’re good. So if you start to contribute Bitcoin Core, maybe you pick up an issue that someone is requesting a feature or a bug and you start to work on it. It will take at least normal change set.

Jonas Schnelli:

It will take at least two to six months until it gets merged because there’s so many reviewing going on. There’s so much testing going on because stability is the main focus of Bitcoin Core. And this can be hard for new contributors because they wait for things to move on and it takes like weeks until nothing goes. And reviewing is still a bottleneck of Bitcoin Core. So it takes a lot of time. If you want to work 100% percent on Bitcoin Core with all your time, you need to do a lot of changes. And also a lot of reviewing to kind of fill up your schedule because it’s like a lot of waiting for your own changes. But once you have written a such change, you open a pull request and then it’s public. A lot of people will come in and ask for changes, and then you need to be a major enough to accept ratings criticism and approaches or others have, or even if it’s a bad idea and you need to accept that things are not getting merged.

Stephan Livera:

Yeah And so then there’s also this element where in open-source projects there’s often that dynamic, where there are more people who want to write a new contribution, AKA a pull request, then compared to the amount of resources that we have in terms of reviewer time, and then potentially even more scarce is maintainer time. Could you just spell out that dynamic for us?

Jonas Schnelli:

Yes . I think it’s a sentiment we see in most open source project that people are really great in writing features new things, things that are great to write, because there’s a concrete outcome. What we’re actually need is people refactoring the software, making it easier to change in the future, making it more performant, things that are not so fancy to implement that’s not visible, but it helps for scaling it. The next 10 years things are actually the hard part and gladly in Bitcoin Core, we have a lot of developers willing to do that, probably because of the funding. And, but yeah, I mean, reviewing is still what’s missing because there’s a lot of changes and a lot of refactorings written, but no one has a skillset or no one takes the time to actually go step by step through every line of code and verifies it. Of course it’s done over time, but it is still the bottleneck.

Stephan Livera:

And for listeners who might be newer to this, what does the term refactoring mean?

Jonas Schnelli:

Yes, that’s an essential thing that gets pushed away in the private sector, traditional business software development. So when you want to have a software projects. A project succeed over time, you need always to kind of reshuffle the code, optimise the code in a way which is not visible. There’s no outcome in terms of feature, but internally it gets much easier to change things in future like writing instead of one single file of code, you split it into multiple files, makes it easier to read, makes it easier to change, less impact. If you change one thing at the other end, things like that, it’s super important for a cryptocurrency or it’s super important for Bitcoin. And this is also why people sometime think while there’s a lot of development going on Bitcoin Core, like hundreds of comments, but at the end, it still looks the same. So why is that? That’s actually because we’re doing refactoring.

Stephan Livera:

And in the process of refactoring that is potentially an avenue for bugs to happen and guess depending on whether it’s like in most cases, obviously it will be unintentional bugs, but potentially that’s a risk where if someone was malicious and maybe they were a bit more calculated about that, that might be an opportunity for somebody to try to slip a bug into that code. And at that point, we are essentially relying on the skill of reviewers who know the code base. And also to some extent, the maintainers, can you outline some of your thoughts on that idea?

Jonas Schnelli:

Yeah. I think refactorings always have the risks of breaking things. Introducing former bugs or new bugs how counter fight that is usually we have like a test suite that tests everything, or as much as possible, of course we cannot test everything, but there’s a lot of tests testing the software automatically. So whenever you change something, you run these tests and if something is broken. I changed it in a way which changed the behaviour. Of course not everything is tested while there’s still a remaining risk. And we had issues in the past. There was a big bug, the inflation bug that was also due to refactoring. So it is risky, but not refactoring is even more risky because we will end up with software that’s no longer maintainable. And then the ugly box will happen.

Stephan Livera:

Now some listeners might be thinking, but Jonas, I just want 21 million and I don’t want any changes. Can we just have stasis of the code or is it actually that stasis is not an option?

Jonas Schnelli:

Yeah. I mean, Bitcoin was built to resist changes that’s for sure. No one wants to change 21 million cap or similar things because we want the value of the coin and not feature fancy stuff. Right. So I think to keep it stable, you need to at least make sure if you found issues get fixed because otherwise people figure out how to break Bitcoin Core, how to stop it, the peer to peer network from working. So at least that needs to happen. And then scaling the chain grows over time. We also want to make it possible for everyone to verify the chain so they can still run a full node compared to other cryptocurrencies where this is no longer possible. And also I think everyone is okay with improving things in a way which is clearly beneficial for everyone. I’d say privacy is probably in that area. Well, some will probably say privacy is evil, but I think most Bitcoin stakeholders are very much interested in increasing privacy. So that’s why still stuff goes forward.

Stephan Livera:

Right. And perhaps another example of that is over time, things change external to Bitcoin. So an example would be the Tor v2 addresses is being deprecated. And so I know that was also a project recently in Bitcoin Core to have compatibility with Tor v3 addresses. So perhaps that’s also an example where stasis is actually not an option.

Jonas Schnelli:

Yeah. Very good example. And I think there’s a lot around that and HTTP some part of it. We have some API’s that needs to have at least some minimal maintaining. Absolutely.

Stephan Livera:

Gotcha. And so when we’re talking about who controls Bitcoin Core, who has influenced it, some people make a change or some people put in a pull request. Their pull request gets attention and work and other pull requests don’t get attention and work. How does that decision, how does that process happen? Why is it that some get work and others don’t?

Jonas Schnelli:

Yeah, of course there is an emotional element. That’s not possible to hide our contributors that have contributed over the years with stable things. Good example is Pieter Wuille? If he writes a pull request, it just gets attention because he’s the father of segregated witness. He’s the father of Taproot. So I think if you have a good record of well able changes, your stuff gets more attention. That’s just a fact. And there’s also things that no one is interested in reviewing or bring forward. If someone comes with good example is probably, it comes all over time, always in it’s a full address index like Electrum servers usually do, a technical thing, but if there’s changes that have not much interest, it just starts to lay around there and reviewing will not have, but that doesn’t mean that the one that wrote the change and is interested that to get it merged cannot find people willing to review it either on a financial basis or just find people who have the skillsets to review it and comment on it. But usually having some already existing contributor work or help bringing forward your change is super beneficial.

Stephan Livera:

What about if there are, trade-offs involved with a pull request and if there’s some kind of conflict that comes up, how is that trade-off managed and how do you think about that when you’re a maintainer?

Jonas Schnelli:

Yeah, that happens a lot. So if even contributors that have been working on core for years have sometimes different views on the change. If it’s consensus critical, there’s nothing that usually we want that everyone is on board with the consensus change. If there’s loud voices against the consensus change, even if it’s not the majority, it will lead to problems. So on consensus changes, we should really try to have everyone on board or at least most people there is no voting process or anything like that. It’s like to try to form consensus on changes. If there are smaller things that doesn’t affect consensus, and it’s not going too much into the peer to peer network, it might get merged regardless of one or two voices complaining about the negative sides. That depends often on the maintainer and also on the weight of the complaint. Especially like user interface changes. It’s so much a matter of taste. So if you would listen to every voice, you wouldn’t get anywhere.

Stephan Livera:

I see. And just as part of the development process, there’s this thing called the act process. So could you tell us a little bit about what that is?

Jonas Schnelli:

Yes. So whenever there’s a pull request and someone starts to review it, we need an outcome of that review. We have these terms ACK that means acknowledged or accept something like that. So there’s a test that acknowledge a test. That ACK that means you have actually tested the software and you accept it. Or there is the utACK, which means untested, acknowledged.That means I have not tested it, but I have reviewed the code and I accept it. Sometimes people write code review ACK. That means I have done the code review and accepted Ideally, especially for new contributors who start reviewing code. Right? A bit more than just an ack, start to write: What have you tested? What was your feeling about it? What’s the consequences of that change? So people have more trust in that you have actually reviewed it thoroughly.

Stephan Livera:

Yep. So bringing you back to what we were saying earlier, essentially what you’re saying there is that in certain cases somebody could nack something, but if it’s relatively minor than it could still get merged in by a maintainer, correct?

Jonas Schnelli:

Absolutely. Yeah. That happens a few times. And I think it’s also find that I mean, take, for example, a visual change that is a matter of taste and someone says even a long-term contributor says nack, this looks ugly and maybe nine other people accepted. So then it will lead to a merge or someone said nack. And it also happened on consensus changes during the debate of the block size or things got changed regardless of nACKs coming from other sides. It happens. Yes.

Stephan Livera:

Yeah. Another saying that comes from the, I guess computer science and development community is this idea of believing in code and rough consensus. What does that mean?

Jonas Schnelli:

Yeah, good question. I think, rough consensus probably means if, I think the voting process is not some can have in Bitcoin Core when I started to contribute, I thought, well, that needs to kind of a guideline a rule when I can start to merge things or to this, does it mean 5 ACKs or 10 ACKs? Or is there a kind of a ratio I need to, but at the end, it’s a fingertip feeling I was saying in Swiss German we need to have, like, it’s always different. Every pull is different. Every process of marching is different. You need to have these senses what is good or what is not good.

Stephan Livera:

Yeah. And one sense, I get just from following some of the discussion over the years, I’m not a developer myself, but it seems that there’s a bit of a sense that if we’re going to make a change, we kind of want it to be Pareto beneficial. Right. It’s kind of like people only win out of this and there’s no one who’s like a losing out of this change. Would you say that is sort of roughly aligned or how would you respond to that?

Jonas Schnelli:

Yeah, absolutely. I mean, there are some things where we cannot make everyone happy. A good example while it’s very technical, but it’s the new address for the Tor format? You have a you mentioned before of the version Tor on, in addresses, there’s always downsides like other implementations, like btcd in that particular issue had problems with reading those new addresses. So we needed to decide whether we complicated more for a bug that was implemented in another software cannot satisfy everyone. But at the end, what Bitcoin Core tries to do is make the ecosystem as a whole try to work towards the ecosystem as a whole, as good as possible.

Stephan Livera:

Yeah. And while we’re on that topic as well, what about this idea of backwards compatibility or forward compatibility, this idea, the notion that somebody should be able to run Bitcoin Core nodes from one, two, three, four years ago or even more and still participate in the Bitcoin network. What’s your thought on that idea?

Jonas Schnelli:

Yeah, that’s something we take very seriously. So we put a lot of resources in backward compatibility and I mean, where we can’t is when a soft fork kind of gets activated and how we call it a written down to the code. So it’s no longer possible to use the older software for consensus reasons. That’s probably the only place where backward compatibility won’t work. I think older nodes are still on the network. We’re far away from having the newest version, the newest stable version dominantly on the network. So it’s like there’s a lot of old software or old nodes in, on main net. And I think that’s absolutely fine. We think upgrading the upgrading process is something that needs attention and needs to be taken very seriously. That’s also why there is no automatic updates and things like that because there’s always risks involved and people should really be conscious about taking those risks and upgrading.

Stephan Livera:

Yeah. And when we’re talking about influence in this world of Bitcoin Core as you mentioned, if you are a long time respected contributor, your work tends to carry a little bit more heft or weight to it. So I guess for a developer, that’s how you, in some sense, gain influence, if you are a company or a development organization, what’s the way that you kind of exert that influence. Is it mainly by having your paid contributors work into a specific area of the code base? What does that look like?

Jonas Schnelli:

Yeah, I think first there’s two areas. One is the protocol development specification. It’s more in that area where the BIPs are, the Bitcoin improvement process is papers. And the other side is working actually on the core code. I think companies are usually very good in writing specifications. That means writing no code, it’s pure specifications, sometime a little bit of code or reference implementation, but in other areas you can achieve a lot. And if it’s a good idea, if it makes sense, it gets, the implementation gets picked up by other people, or you find people doing the implementation. But if a company wants to work on the core code on the Bitcoin Core code, it’s passed on by either having employees in house that start to contribute, or by funding open source development, either through a vessel, a larger funding organization, or you hire or sponsor your own developers question then is how can you influence these? And I think that’s a good question in general. And if you have them, in-house the problem is the culture is so different. The culture, how you develop in-house business stuff versus working on Bitcoin Core so different. And I would even say a guy that writes, or someone writes code in-house for a company, stuff is not ideally, or you cannot share it between like 50-50 that’s wishful thinking of, it’s so different attention spans and things like that.

Stephan Livera:

Yeah. I see on the question of funding as well, do you see that, like, that could be a negative or a positive, like if somebody, I guess, and theoretically we wouldn’t, we could also not know about it, right? Somebody could be totally a pseudonymous contributor and they may be being funded by our worst enemy, but we wouldn’t necessarily know, and they could just be making so long as the contributions are still being reviewed. Right?

Jonas Schnelli:

I think a good example was when I worked with Bitmain or they started to sponsor my work in 2016 a bit before they went into the rough side of Bitcoin Cash and stuff. So over time I started to question, is that a kind of a good relation or not? On the other hand, they have not influenced myself or any of my work. And I think it’s fine. You know, as long as somebody sees it valuable and pays for it and doesn’t influence it. But of course, no one knows there could be developers being influenced by sides we don’t want in Bitcoin. On the other hand, it’s kind of impossible to wash these outs because its open source, right. Everyone can try to influence it in their direction.

Stephan Livera:

And on the question of funding as well, in many cases, I have seen it done as just kind of a no strings attached a Bitcoin company or exchange or development organisation just says, Hey, here’s the money we want you to just work on Bitcoin Core. In other cases, it’s specific and tied to a certain project or deliverable or something that they want a developer or contributor to achieve. What’s your thought on those kinds of scenarios is one better than the other? Or is it more just like you’ve got to choose the right tool for the job there.

Jonas Schnelli:

Yeah. I think it’s both is okay, because let’s go down the route of you have unlimited funding for whatever you want to do. I mean, for maintenance, there’s a good example. You don’t have an outlined project except maintaining right. So it’s probably an ideal situation where you just have the funds to do whatever you think is necessary. On the other hand, other people perform better. If they have a clear outline, a specific amount of time and money for achieving a goal. On the other hand, it’s very hard to estimate that in Bitcoin Core, because you cannot control the reviewing. You cannot control possible changes. You need to go through because of other contributors have other ideas. So it’s very hard to frame it. I think what’s hard is for company usually has a business interests. They must be financially interested. So why would they sponsor someone working on something they cannot influence?

Jonas Schnelli:

That’s a really difficult question. And I think a lot of companies struggle with that because they cannot throw out money out of the window. They’re not a charity. They need to get something in return, some try to get in return, public relations. So they be part of the ecosystem customer or attracted to that. Some probably write it off as infrastructure needs. Well, you need to have the basic infrastructure to make money on top of it. But I think that’s probably one of the reasons why we haven’t seen or rather there’s still kind of a whole bag of major companies to contribute because it’s so hard to do it in a way which reflects the company’s desires of making money.

Stephan Livera:

Yeah. And maybe they can fund some developers if they want to keep some hardcore maxis off their back, you know?

Jonas Schnelli:

Yeah, for sure. I mean, if you fund in the right direction, people maybe start to be more nice to you because you have a stake in that. But I think in the long run, most people have understand that the core infrastructures it’s necessary to make money on top of it with whatever company. So they see it as, as the base layer, they need to fund.

Stephan Livera:

Others such as Steve Lee of square crypto have commented previously around this idea that maybe in an ideal scenario would be something like a 10 by 10 matrix with many different development organisations, all contributing to Bitcoin in their own way, perhaps with their own different viewpoints and such that in that way that they may challenge each other. And so on. What’s your view on that idea? Are you for that against that? Or kind of neutral on it?

Jonas Schnelli:

Yeah, I think I’d also like to see that. There’s just one thing that always stands out for me that the software is still a monolithic piece of code where we have consensus code in the same repository as the UI of the windows application. As an example, we need to distinct where I’d like to see more people working on it or more happening. I think the consensus module should probably be a separate thing where, where we can have as much as possible influence, but then you can say there’s a lot of code that’s not necessary for Bitcoin to survive. Like the UI. That’s very matter of taste. There we could not see just different influences on core. We could see other implementations. You guys, for instance, when Satoshi wrote yet application the initial application, I think from the beginning, he always mentioned it’s the reference implementation. And I still like the idea, although when it comes to consensus, I’m more I think we should have one single piece where everyone works on it, similar to the Colonel or something like that in the Linux world.

Stephan Livera:

Right. And if I recall correctly, there were some instances where it was actually some things kind of bugs from other systems. And I think this was Pieter Wuille on chaincode podcast. And he was explaining how with the Berkeley DB kind of debacle back in 2013, that it was like a bug from some other area was effectively becoming like a Bitcoin consensus rule because without that you were falling out of consensus. So I guess that’s one of the difficulties.

Jonas Schnelli:

Yes. Consensus. It’s currently, I’d say very hard to impossible to specify just in words, there’s a lot of code and things involved in the consensus layer, even softer external software, like level DB or formerly Berkeley DB. And that’s why I think having multiple consensus implementations might be a higher risk than having one where we work together on a single piece of software.

Stephan Livera:

So when we’re talking about influence and ability to work on different areas of the code, is it also true to say that there are different areas of the code within Bitcoin Core on which people are considered an authority or an expert in that area? Could you spell out what some of those different areas are and how that aspect of this work?

Jonas Schnelli:

Yes, that’s true. The areas are A) consensus, I’d say be peer to peer, see wallet, then user interface, API’s, RPC is a good API, ZeroMQ is another API. And in all these areas, there are unspoken, not written down experts like, John Newbery’s is nowadays and more in peer network. Pieter Wuille Is certainly one that has good insights into the consensus part. And Andrew Chaw of Blockstream is he’s very into the wallet. Yes, your oversight there, but it’s a fluid situation. People come and go, but there’s always someone you like to have for review in that certain area, if you want to move forward. And because they are quite the experts there.

Stephan Livera:

I say it’s kind of like an unwritten rule thing that if you were to make a hardware wallets kind of a pull request or something like that, that it would be nice if Andrew Chow reviews that as an example,

Jonas Schnelli:

Absolutely. It’s not necessary for a merge, but at sometimes the maintainers waits and maybe even asks Andrew, if he’s willing to review the pool requests, because it looks like he has a good understanding there, that’s how it happens. Yeah.

Stephan Livera:

In terms of Bitcoin Core as a code base, I guess, for you as a maintainer, you’re sort of more in the centre and you can’t necessarily go as deep into each of those different areas as compared to the subject expert. Right? So how does that sort of work when you have to be, you’re kind of relying on some level of the review by the, unwritten experts in that area, right?

Jonas Schnelli:

Yes. I think it’s also good to know that the most maintainers have a specific target area. Although it’s kind of, it’s overlapping and sometimes moving, I initially started to be ready to maintain the user interface though over the years I moved more towards API changes and wallets. So it’s like every maintainer has its own area of interest and that’s also where he picks out things he’d like to get merged and move forward. Although things that lay around for a long time gets picked up by maintainers usually working in other areas. And there’s also like we have a project it’s called high priority pull requests where every contributor can put one issue or one change in that list. So these should be reviewed first. And this kind of a rule we try to to maintain and that also helps to review things that are maybe not in your skillset, but you still have the skills to do it.

Stephan Livera:

I see. And how do you, I guess, apportion your time between the different pull requests. Cause I guess there’s be a lot of people demanding your time and saying, Hey, this thing is reviewed. Can you please merge it? And you have to decide, and you have to try to apportion your time. How do you make that decision?

Jonas Schnelli:

Yeah, it’s, that’s really hard sometimes because you want to help everyone at the end. But time is limited. You have your own or in my way from my side, I have my own changes. I want to get forward as a contributor. Sometimes even the review trading happens, that’s funny, but sometimes we trade reviews. You look at my things, I look at your things and together we bring it forward. It’s natural, it’s a good process right now.

Stephan Livera:

So in terms of I’m thinking here of Jameson Lopp’s famous article Who Controls Bitcoin Core? And in that article, he spells out some of the different controls that are in place to make sure that the Bitcoin Core code is reviewed. And also that there are ways that the end user, if they choose to can verify that the software is correctly done. So could you spell out a little bit about your processes that are involved as part of that, as I understand this things like gitian and you’re doing like a compile and you’re essentially saying, yeah, I’ve signed off on this. Could you spell out some of those processes for the listeners?

Jonas Schnelli:

Yes. So I think as an initial or as the most important part in that circle, we use git as a source code, a maintaining system, that’s just for keeping the source code, having a way to verify that the source code is correct. On top we sign every merge. So every March that goes into that gateway repository is merged together with an additional hash. So because git this using SHA-1, which is more or less broken, that’s just for the code. And each merge gets assigned with the PGP key of the maintainer that merged it. So you have at the end, the possibility to verify the whole source code. If there is no merge inside, that’s not done by a maintainer. It’s not going back to the initial comment we had from Sirius or from Satoshi. So it’s goes back, I think to 2013 or 14, but at least you have a certain integrity check with GPG that no one has changed the code in a way which was not intended.

Jonas Schnelli:

And from that code base how do we form binaries? Because most people are not capable to take the source code and make it into running application. That’s still a complex thing for most people, and we still want to ship binaries, double clickable applications. And this is the hard part. How can we form these double clickable applications out of a source code in a non-centralised way? That’s actually a very hard problem and it’s still not solved in most app store cases. So that’s why people came up with that Gitian thing. That’s actually can look at it as a black box where many people can use this black box to turn that source code that’s verifiable into an application. You can double click and that’s also verifiable. So at the end, people who are downloading Bitcoin Core, they have an option to verify that application and look what, how many developers have said that this application is good to run, and this is an important process. If you want to have a critical software pre-compiled.

Stephan Livera:

And just for our listeners who maybe they’re a little bit new, they don’t know what GPG verify as a command does. Why does that help them have additional confidence in the code that they are about to run? If they run GPG verify?

Jonas Schnelli:

Yeah. GPG is a way how you sign messages, sign letters, and everyone who obtains your public key can verify that it’s actually signed by you. It’s called also the web of trust if you include key servers. So what it helps it’s if someone sends me a message, let’s say Pieter Wuille sends me a message. I can verify if that message is actually written by him and not by someone else by verifying with that GPG or PGP key. And the same thing can be done for a commit, for a set of changes for Bitcoin Core. Every maintainer signs it with their key and everyone else who can obtain it publicly on the internet can verify it has been done by Jonas or by Pieter or whoever and not someone else. Or there is no slippery comments slipped into in between that has rough consequences.

Stephan Livera:

Excellent. And I know there is other work being done in this area. People like Carl Dong and guix and this idea of reproducible builds, what does that mean?

Jonas Schnelli:

Yeah, there’s that, or there’s limits to that gitian approach, especially the compiler section at the very beginning, you need to have, at least the compiler you need to trust. You need to download within that process of keys and compiler, that turns source code into binaries. That’s still kind of an element we need to trust within Gideon. And you can break that further down by having just a very minimal layer of trust. Very simple compiler that is even on the machine level verifiable that then compiles and bootstraps, the things you need to compare. So it’s very complicated, but at the end it gives a higher assurance that no one can change things we don’t want. That’s why the guix project is worked on.

Stephan Livera:

Right? Yeah. So, yeah. So for listeners, that’s an interesting one. If you’re interested to go down that rabbit hole, you can go search that and look up this idea of the tool chain and what tool chain are we using to verify things and create things or compile and build. I guess people might be thinking Bitcoin Core. Sometimes the code can take a long time to change because things can be delayed. Why does that happen?

Jonas Schnelli:

Yeah. Sometimes some people tell me, well, it’s super slow how the process happens or how things go. All the people tell me, wow what happened in 2020 was awesome. Like a lot of changes. So it depends also on what you expect. But of course, things can be really slow if you more known to kind of traditional software projects because stability is key. Everything is in every change, the centre is stability. And if stability is not given we cannot add features and that’s why sometimes look slow for most people.

Stephan Livera:

Yeah. And as I understand it, there’s also this thing where if somebody puts in a pull request and then sometimes other things can change around them at the time that they were trying to make that change. And then they will have to now do what’s called rebasing the code, what does that mean?

Jonas Schnelli:

Yes. That’s part of the negative side to work on open source or on things that change slowly assume I try to change the peer to peer network. Like I done for encrypting the peer to peer network first implementation. I wrote three years ago and it has not been merged because very complex, we need to change things. We need to specify things. But I wrote the change three years ago, but in the meantime, there was a lot of other changes merged. So my change is no longer applicable to the current codebase because it changed. So what I need to do is whenever something changes the area, my non-merchant change is affecting. I need to do it again. I mean, not completely, but I at least need to change some things. Sometimes it’s just the line of code that’s shuffled in the wrong way. Sometimes it’s completely different depending on what else have been implemented in the area my change is affecting. And that’s sometimes because things we make daily, sometimes it’s like one week of work is just taking all your contributions, rebase them that’s called rebasing, make them applicable for the new codebase. And sometimes you introduce bugs. Things are different. The concept is different. Yeah, that can be really cumbersome sometimes, but it’s part of the work.

Stephan Livera:

Yeah. And what about if people have just different visions for what Bitcoin should be? Or maybe some people think of it as, okay. It should just be digital gold. It should be 21 million and no more. And then maybe someone else might have a different view where they think, no, I want privacy and I want confidential transactions and they might be thinking, Oh, I want confidential transactions. Even if there is a risk, I think depending on which way you go, either a risk of a hidden inflation or a risk of the encryption breaking down and the amounts actually no longer being confidential. How do you sort of weigh up that difference in clashing visions?

Jonas Schnelli:

Yeah. Especially you mentioned that a lot of consensus things, and if there is an uncertainty in the consensus my take on that is it’s not getting merged. So Taproot is a good example. I mean, it’s not being forked into the chain, but the call is at least now in Bitcoin Core and it’s running on signet and stuff. So I think Taproot has an overall consensus agreement that it’s beneficial for probably most, well, we don’t know. Maybe some voices will come up soon, but it looks like there’s super great support for it where other things, because maybe also because there’s no really hard downsides to it, or we don’t know them yet. So I think that’s also why it has broad support, but some changes have always a lot of positive and negative side effects. So I think that’s sometimes why some changes have harder time to get merged, especially like if you mentioned confidential transactions, they have scalability issues or scalability downsides, at least. So things like that I always think about will be very hard to get the community behind because it’s beneficial for some businesses or some interests, but not beneficial for others. That’s where it makes it makes it really hard. And Taproot, as an example, looks like it’s beneficial for everyone a bit.

Stephan Livera:

I see. So maybe we could summarise it as kind of if there’s gridlock, it’s a no-go it’s just not happening, but if you can essentially get basically everyone to agree to it, then there’s a good chance you can get it in if you have enough review time and work on it.

Jonas Schnelli:

So I think you can say that although segregated witness was also.

Stephan Livera:

Controversial at the time.

Jonas Schnelli:

partially because of the block size . I think everyone wanted segregated witness or a lot of people, but they try to tie it also to block size increase and things like that. We’ll have probably even a harder time now when there’s more eyes on the things. So we’ll see.

Stephan Livera:

Yeah, that’s a tough one. And so I guess it’s ultimately, if people really want something they can fork off, right. That is always an option. And crucially users don’t have to run the code that developers give them, they can go find some other developers and run some other code, but it just essentially you have to move the Schelling point. Basically, if you don’t move the Schelling point, if people don’t go to your side, you’re just creating a shit coin.

Jonas Schnelli:

Yeah. Very important. I think in that sense, these people that have the intention to forecast for a change, they probably are hold back now because of the bad examples that have happened in the past. Bitcoin cash is probably the most prominent example. It doesn’t look like a successful fork in terms of monetisation. And I think because of these examples, people are in the future, eventually trying more to pull everyone into the same direction rather than forking and at the end have a bad out.

Stephan Livera:

Yeah. So maybe we could summarize that as there’s a very, very strong preference, not to hard fork, the Bitcoin economy, because if somebody puts out a change that breaks the consensus, now you’ve got a split in the chain and you cause all sorts of chaos in the exchanges, the wallets, the whole ecosystem, because people, they may not necessarily be on the chain that they want to be on and there’s all this kind of drama about it. And I guess we can summarize that then as saying we very much prefer soft forking for an upgrade.

Jonas Schnelli:

Absolutely. I think the last years show clearly that this is the much better way to go for everyone.

Stephan Livera:

Gotcha. And so I guess bringing it to what’s happening with Taproot and potentially what comes in the future, is it the case that maybe we’ve got a case of 2017 or SegWit2X PTSD and that everyone is kind of worried that it’s going to go down, like what happened in 2017. But potentially the people who were really gonna kick up a stink about this have already had their chance to say their piece and that now, fingers crossed, obviously it looks like most people in the Bitcoin ecosystem today are in favor of taproot. I mean, it looks like that I think it was over 90% of the hash rate effectively the pools that represent over 90% of the hash rate to be a bit more precise. They have come out saying we support Taproot. Basically every well-known developer supports it. What’s your view on where it is currently and the process going forward for that?

Jonas Schnelli:

Yeah. I think there’s a many, or some variables to that calculation. A it’s it looks like I said before, Taproot has overall, it’s more beneficial for all sides or all stakeholders then segregated witness where people, even there it was probably beneficial for everyone, but people didn’t see it back then. That’s side of that one variable in that calculation and B people learned good example is the miners. Miners initially thought they have their voting, which is not a voting on soft forks. They, thought they have more power back then and, trying to maximize their power or maximize their finance opportunities by using that power. But they had to learn it’s actually not power they have. It’s just it was a mechanism to not lose mining power in the network rather than a voting.

Jonas Schnelli:

So they came back to the conclusion, very likely that they have just to stick with majority and make money by the block reward. And by the fees full stop, hence in a way if it’s not beneficial to them they certainly will come together and do something. But things like Taproot, I would be wondering if they would be against it. And and of course we have sown these failed forks of these fail hard forks. And this will also hold people off of doing it again, that’s not a white or that that’s not a free card for every soft fork. I think, especially as if it’s controversial, it will have a hard time, but things that really move forward and are beneficial for everyone. I think it’s right now. It’s a good time to do it.

Stephan Livera:

So in terms, Taproot again, so there’s Bitcoin has no CEO or leader, so it’s not like an authoritative answer, but I guess from your perspective, what does it look like in terms of taproot and the process for proceeding with Taproot in terms of when it’s going into Bitcoin Core and that kind of aspect of it?

Jonas Schnelli:

Yeah. So, I mean, the specification or the discussion around Taproot, are pretty old, probably started with MAST from Johnson Lau back in ’17 or in ’16, it’s a long history of development. And at the end, someone wrote the poll requests to implement it in Bitcoin Core. Most contributors were in favor of getting that into the main code branch at there was a lot of testing. And at some point I think even after one year, it got merged. So it’s now merged and it will be released in version 0.21, which will be released in the next weeks. But that’s only the code that’s really important to know that’s the code, the potential to Taproot by the specifications. There’s no soft fork implemented right now. And usually how it is someone writes an activation for that soft fork proposes. We could do it like this miners need to agree on this and that it could also be different mechanism, like a user activated soft fork.

Jonas Schnelli:

That’s still open. And probably it will be a traditional software where miners kind of signal their readiness. And if someone implements that it will go into the master branch after a review and people will run it when there is a new version and that’s how things change. And it’s not some top-down structure where someone says, we’re going to do that soft fork. It’s like everyone does its part of it. Like you mentioned before the 90% readiness from the miners for tech, how do you measure that? There’s just one guy who set up a project. They collaborated with others to set up a projects asked miners if they’re ready for Taproot and willing to do it, everyone does its part. And that’s truly open source in my opinion.

Stephan Livera:

Yeah. That’s the crazy thing for somebody who’s a little bit new to this space that they might be used to having a guy up the front with a bull horn saying, okay, everybody, this is what’s happening now, but there is no guy up the front with a bull horn. It’s actually just, everyone has to self organise in some way. So that means if you are an end user and you’re running your Bitcoin node, you might want to upgrade to the newest version of Bitcoin Core. And we don’t know yet exactly whether so you might just upgrade to version 0.21, but that won’t necessarily have the like activation aspect of it, but you’ll have the code for it. And then the miners have to get ready for it. And everyone else has to basically make sure all their wallets and things are ready for it as well. So I guess it’s kind of like everyone has to do their part.

Jonas Schnelli:

Yeah, exactly. And I think it’s also really important to know that there is, or it’s impossible to have a clear how you call it milestone plan, what we’re going to do next in Bitcoin Core, because that requires centralised planning. If you want to have a centralised roadmap of things you need centralised planning, and of course you could like try to do something in that area, but usually everyone has its own agenda and its own milestones and own path what he wants to do. And that changes over time and having a centralised planning, we do ACK’s in time. Why that would mean its a centralised plan. And we don’t want that for sure.

Stephan Livera:

Yeah. Okay. So turning to some other areas of Bitcoin, obviously there’s so many different areas but curious to get your thoughts on some of these areas around for example, Bitcoin privacy. Do you see any things coming down the line that might assist people who are interested in using Bitcoin more privately?

Jonas Schnelli:

Yeah, I think the missing privacy in the base layer is still a big issue. I think still one of the biggest problems we have to solve and gladly stuff like Taproot works towards that direction. Of course it’s not enough. There’s other non-consensus changes that helps improve privacy, like the wasabi coin shuffling approach, which is great, but I think can also be dangerous because the anonymity set, is probably still pretty low. What I like to work towards is full privacy for the whole for all transactions in the base layer in the consensus area, that’s where things really get interesting to me. And it will take a lot of time for sure. It’s not something that will be solved in the next two years, but I’m pretty confident it gets solved in the next 10 years or solved improved.

Stephan Livera:

So what sort of approaches do you think would make the most sense there for privacy of the next 10 years?

Jonas Schnelli:

Yeah that’s hard. I haven’t evaluated all the new proposals, but what I know is there’s a lot of research going on in that area with cryptographers working on it. I think right now, all the proposals that have concrete steps, like bulletproofs, confidential transactions they will go through another round of specification overhaul improvement. And I think right now we don’t have a ready to implement technology or ready to state technology that will solve it in a way how we would all like to. So it’s probably another year or two for specification overhauling.

Stephan Livera:

Yeah. Right. So I guess it’s like a confidential transactions, essentially. It doesn’t have the right trade-offs that we want. And maybe in the coming years, there’ll be another breakthrough in terms of how to do it with less bad trade-offs and now maybe people would be more comfortable to have that, I guess the other big one that could potentially really move the needle. There is, again, this is a future potential. It’s not something anyone is kind of working on directly right now as I understand is this whole cross input signature aggregation idea, which maybe that’s an idea that might make coinjoins like make the incentive for coin joining a little bit better. So maybe that’s another angle.

Jonas Schnelli:

Yeah, Absolutely. And also what we have seen over the last years is just how with pure scientific papers, how things got improved much more over the last year. So I think it’s in a great state now that in scientific papers. We can get to a state very much quicker than trying to implement stuff or trying to work on the detailed specifications of it, rather than just coming up with new ideas, sparing each other’s with better ideas. I think that’s, we’re currently in that state, in my opinion,

Stephan Livera:

And from a lightning network perspective, do you play around with lightning yourself? Do you have any thoughts on lightning development or what you would like to see on that front?

Jonas Schnelli:

Yeah so I’m still very interested in having a payment system rather than just a pure store of value store of wealth. I think lightning goes into the right direction. It’s still very early, in my opinion it’s not major enough to be used for the broad masses. On the other hand, we have still that high volatility about, I really like the argument that there is a capable payment system called lightning that can be pulled out as soon as volatility goes down or transactions on a daily basis gets more and more important. But right now I think then the needs for doing daily transactions is not absolutely there, but it will be my opinion.

Stephan Livera:

Yeah. And as a Bitcoin Core maintainer, do you see any, I guess, potential conflict, if there are things that say lightning developers want and do they ever come into conflict with just people who just want to use Bitcoin on chain?

Jonas Schnelli:

Yeah. Taproot is also an example that has a lot of things, lightning people want. And I think there were changes if I recall correctly check long time verify, is also a change that was highly appreciated or wanted by the lightning people that’s been merged a few years ago. I think most Bitcoiners or say Bitcoin developers have, are much interested into lightning to succeed. So I think it’s, there’s no clear the people are sitting in the same boat, I’d say right now. And of course no one would do a trade-off that affects Bitcoin Core as a store of value just in the favor of doing it as a lightning support. I think right now all changes that affect both in a positive way are easy to do?

Stephan Livera:

Yeah. And probably a good example is ANYPREVOUT, which Christian Decker and AJ Towns are putting some work into that and potentially that might be a future soft fork that helps us get to the next level of lightning network, which is the ELTOO that’s ELTOO So maybe that would be another potential future soft fork. Do you have any thoughts on any providers?

Jonas Schnelli:

The thought more have is that there is a lot of things I’m kind of queuing for a soft fork that is one particular example, but also another, and once we set the time for a possible soft fork. I wonder how much other things should be pulled into that soft fork, or should it be one after the other? Because soft forks usually take a lot of time on the heart and our heart to do, if there is an attempt to pull things together into a single software and we will see

Stephan Livera:

Right. Because another one is I can’t remember, I always forget the name, but it’s a Matt Corallo’s or something like great consensus cleanup or something like that one as well.

Jonas Schnelli:

Yeah.

Stephan Livera:

So then there might be competing demands of people who want that, and then people who want ANYPREVOUT out. And then I know Jeremy Rubin has the CTV check template verify that there might be kind of competing demands of what goes next. And if things can’t be done concurrently, that is

Jonas Schnelli:

yeah. And you don’t want to overload soft forks with features because it makes it harder to get to get in and yeah, but you don’t want to make a software every half year. Well need to see what we can combine and makes sense.

Stephan Livera:

Yeah. The other way is potentially if, well, I guess maybe this is a bit magical thinking or kumbaya, but what if let’s say Taproot goes down without a hitch. Everyone is basically everyone is pro Taproot. The miners are for it, the users it, the developers are for it. And then maybe the next few can be done in quick succession. If so long as he ecosystem broadly considered a super majority of the ecosystem is pro those particular soft forks.

Jonas Schnelli:

Yeah. I think that will be the ideal case, although we never should forget that there’s always risks involved with every change, especially consensus changes. So we shouldn’t take consensus changes lightly, even if we all agree that this is a beneficial thing, there should still be precautions around it. And we’re dealing with a very high market value right now. So we don’t want to broadly speaking, fuck it up right?

Stephan Livera:

Yeah. I think the crazy thing is it’s like a, this we’re all in this airplane and it’s taken off and we’re in the air and we’re trying to change it while we’re in the air.

Jonas Schnelli:

Yeah. Sometimes it feels like that. Exactly. But then on the other hand you need to change things or otherwise the plane might lose altitude or even crash. So I think it’s exactly that we have to, but we don’t want to, but we need to something like that.

Stephan Livera:

Right. But the positive side is we’re turning the plane into like a jet plane or a rocket ship it’s like upgrading.

Jonas Schnelli:

Yeah, absolutely. And for sure, it will fly to moon.

Stephan Livera:

Yeah also mining, I think that’s another area we should chat about as well. So I guess there hasn’t been a huge amount of negative pressure on that area, but I mean, people would mention it every now and again, they say, Oh look, 60% of miners are in China. Or there’s talk about, Oh, maybe the miners would start to have to sanction certain Bitcoin addresses or blocks and addresses are there things that the Bitcoin mining ecosystem would need to make sure that Bitcoin sort of stays true to the permissionless ideals of Bitcoin?

Jonas Schnelli:

Yeah. Mining is one of these elements where decentralisation is still a bit at risk or censorship resistant. I think right now we’re in a good state. There is no very major or very high in terms of hash rate pool around of course, a lot of pools come from China, due to probably the cheaper electricity and the closeness to ASIC manufacturing. I think even if there is a pool that gains high amount of hash power, it doesn’t mean it will super problematic short term. But of course it needs to be addressed. And I think right now we’re in a good states, probably the more time goes down, the broader, the hash rate will be distributed. I don’t see a solution how to fix that centralization problem. And I think right now with censorship. There’s no mind there’s doing very few in the past, but non is doing it in a broad scale. Kind of hidings, certain types of transaction. And that’s also why we want to Taproot because things will look more identical. Censoring stuff based on the semantics of a transaction will be harder. And I think we’re on the right way. And miners have just one interest mainly that’s maximizing their profits through the block reward.

Stephan Livera:

Right. And so theoretically, a miner who was trying to censor transactions is effectively giving up income. And so that’s one of the incentives that protects the overall system. I guess the counter angle to that would be something like, Oh, see what if it’s a government who pays for the mining because they want to try and kill Bitcoin. And so, I mean, you can go down these kind of endless rabbit holes.

Jonas Schnelli:

Yeah. But I think it’s senseless because at the end, people will build software around it would change stuff to bypass these preventions. And right now it’s a market. if a miner starts to censor data transactions that just loose money and maybe to get it con to get it confirmed faster, the services need to pay more fee. And at the end, someone will pick it up. Even maybe the ones that we’re not mining these transactions because they it’s lucrative to do. That’s why I think the market will solve it out right now.

Stephan Livera:

Yeah. And also, I guess it also depends on the miner, being able to identify that transaction as one that needs to be blocked. If the person has already used sufficient privacy techniques, they may not be able to identify this is the one that needs to be blocked.

Jonas Schnelli:

Absolutely. I mean, right now lightning transactions are still pretty much visible. So a miner could say, I’m not mining lightning transactions because I fear that the fees go away from the main chain, with Taproot things may look differently because it’s possible to make it look the same. And these things are actually helping also in decentralization of the mining problem.

Stephan Livera:

Yeah. And from a mining perspective, this is another angle of all. What if the fees don’t get high enough in time? So I guess the high one one interesting fact, eh, so listeners, if you check out Clark Moody’s dashboard, I think he says 99% of Bitcoins will have been mined by the year 2035. And so that means we’ve got about 15 years or so. Before basically the fees have to rise or the price has to rise enough such that miners are getting enough of an incentive. Because potentially at that point, if the percentage of the block subsidy is comprised, so the block reward is comprised of fees and block subsidy. So if the block subsidy comes down, then essentially fees need to go up a bit. And if not, we might see this kind of lumpy block reward structure, and that could also be difficult or troublesome if miners have to if there’s like, if that causes funny behaviour in terms of like fee sniping and things like that, I’m wondering what your view is on that. Do you just think overall the ecosystem is just going to grow so much that that doesn’t matter? Or do you have a different thought on that?

Jonas Schnelli:

It’s hard to predict. So it’s, we don’t know what happens during the next 10 years, there’s scenarios. I think one thing that should not be forgetting is that the hash rate can also go down. That’s not a problem. Well, it might get to a problem when there’s a lot of volatility happening on the hash rate market. But right now I think we have way too much hash rate to secure the current network. We have so much kilowatts per hour on transaction. That’s way too much in terms of the security we need. So maybe the hash rate will go down over the years who knows, and miners, are eventually planning even with that their gear will be obsolete in the next five years or something like that. Or even the newer gear they will purchase. It’s hard to play out, but I think it’s always good to know the hash rate can drop. We will need to deal with the volatility with the difficulty, but it’s not required to have a hash rate stable or going up always.

Stephan Livera:

I see. Yeah. And I guess the other, cause again, there’s so many moving pieces here. Another one people could do is not simply, but they could essentially require less, they could require more confirmations on the transaction as they send that’s. That’s probably, that’s also another adaptation that people could do.

Jonas Schnelli:

Yeah. Possible. And I think also over time, we will have more transactions happening on the blockchain, ideally with the same size, but even maybe with a slight increase in size to have more I mean, Taproot is a good example. Schnorr signatures is a good example how to make, get more into the same size of data on the blockchain. So we can actually have more fees without more size that will also work towards getting more subsidize or more fees for the miners.

Stephan Livera:

Also just more broadly. Do you, what are some big risk factors you see for Bitcoin?

Jonas Schnelli:

I haven’t done a clear evaluation, but my gut always tells me the highest risk is still bug in the implementation that’s probably due to on what side I work on. I still think there is when people sometimes tweet and you know, Bitcoin Fixes That, and Bitcoin always goes to moon, Number Go Up technology. It’s all good. But sometimes I remind myself there’s still risks involved. Like in every system I think in gold, it’s probably finding gold somewhere else in Bitcoin. People sometimes tell me, well, it’s the hardest money. Yeah. Maybe it’s the hardest money. I agree. But there are still risks, implementation could be wrong. Cryptography could be overhauled or broken. There are risks on the implement implementation side. And I think these are usually underestimated not saying that it is a problem, but it’s a risk and we should address it always.

Stephan Livera:

Right. And do you see a risk that if people leave their keys on custodians or if people aren’t running Bitcoin full nodes or if they’re not trying to make the system more decentralized, is that a risk in your view or do you see that as, not as much of a risk?

Jonas Schnelli:

Not so much as I saw it in the last year. So custodial services are getting better. It’s now, I mean, during the times Mt. Gox, I don’t want to know but probably a lot of percentage of the wealth holders had had a stake in Mt. Gox, right now it’s more or less distributed. It’s not only going not only Gemini or whatever we want to whatever we want to name here. It’s more broadly distributed. And I still think people should at least have a high amount of percentage of their coins, hold in their pockets and who knows what politically happened in the world in the next years. So it could be that people want to hold more in their own pockets. And I think it’s still the best you can do, but people should never forget if you hold your own coins, you need to be your own security guard. And that can be really hard. You need to make no mistakes.

Stephan Livera:

Do you see an importance in the proliferation of things like multi signature and the accessibility of that kind of technology and software?

Jonas Schnelli:

Yeah. Multisig is a good example. I’m still waiting. I mean, Specter is probably the best example how to do it nowadays, but it’s still a new software. It’s not really thoroughly tested by the ecosystem. I think multisig is great, but the potential to screw up it’s much higher than if you do a single sig transaction. So we need to be really careful stuff needs to be tested better than for single sig transactions. I think it’s a great solution. The protocol layer is perfect. Just the implementation, the usability of it makes me believe it’s not yet there.

Stephan Livera:

And in terms of things like the let’s call them the full node package, softwares the Umbrel, myNode, Raspiblitz RoninDojo. And what’s your thoughts on those?

Jonas Schnelli:

Yeah, I mean, I worked on a project on the BitBox Base. I try to get that onto the market. It’s really a hard market. I think running a full node, in my opinion, it costs you a hundred, 200, 300, maybe a thousand dollars, but you have your own view on the blockchain. You own trust layer, that things are correct. And I don’t know why the market is still not big enough that people want that, but somehow my gut tells me in the future, people need or want to have their own trust layer to have their own view to the blockchain.

Stephan Livera:

Maybe it’s a question of functionality and ease of use, and maybe a once it gets easy enough to have that and run your own store off of that or other things like that or maybe an easy way to run it and then onboard your family onto that as well. So maybe the whole idea of the family node or the perhaps the community node as an idea that maybe that could be developed over the next few years as well.

Jonas Schnelli:

Yeah I tell that since 2015 or 14 and nothing has changed much, and I hope, I mean, it has a bit, but running a full node is still, it’s like, Oh, you’re running a full node. You must be that geek. Right. But it should be like, you plug it in. It’s like a router at home, you plug it in and you have your access to the blockchain in a private and in a trustless wave. But we’re not there yet.

Stephan Livera:

Last question. Do you have any you know, predictions of what happens in Bitcoin over the next say five years?

Jonas Schnelli:

Yeah, I think right now we see a growth in store of wealth, store of value. I think that will continue for probably a few years. But after these five years you just mentioned, I think even before there will be a high demand for also using it as a decentralized system to transport money in a much broader way than we see today.

Stephan Livera:

Yeah. So that means probably a lot more lightning network at that time. So we’ll have to.

New Speaker:

see stuff like that. Well, I think that’s probably going to do it for this one. So Jonas before we let you go, where can listeners find you and follow you online?

Jonas Schnelli:

Sure. So my Twitter is @_jonasschnelli_ or just search Jonas Schnelli . My Github is Jonas Schnelli. You’ll find me there. You can follow me and see what I’m doing on Bitcoin Core. You’re always free to contact me on telegram.

Stephan Livera:

Fantastic. Well, thanks very much for joining me today.

Jonas Schnelli:

Thanks for having me. Thanks a lot.
