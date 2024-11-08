---
title: Intro to W3 Blockchain Workshop
transcript_by: Bryan Bishop
speakers:
  - Doug Schepers
date: 2016-06-29
---
Blockchains and standards

W3C Workshop

29-30 June 2016

Cambridge, Massachusetts

Doug Schepers <schepers@w3.org>

@shepazu

<https://www.w3.org/2016/04/blockchain-workshop/>

irc.w3.org #blockchain

<https://etherpad.w3ctag.org/p/blockchain>


My name is Doug. I am ostensibly the organizer. Along with my chairs, Neha, where are you? Please stand up so that everyone can embarras you. She is with DCI here at MIT, the Digital Currency Initiative. Daza, also with MIT, he is the guy who grbabed the space for us, and he is going to do video stuff later. Daniel, where are you? He's from Microsoft. We have a bunch of program committee people here, notably Christopher, who is an adhoc chair for the thing he has been helping us organize things, and he will be helping us to facilitate things.

My name is Doug. My twitter name is shepazu. You can email me at schepers@w3.org. So the purpose of htis meeting, of this workshop, is collaboration and technical discussion. Technical discussion. If you want to talk about other things, that's great, but don't distract people who are trying to have technical discussions. Feel free to socialize, but let's keep it focused on technical stuff. Please don't dominate the discussion. I have a tendency to do this myself. If I am dominating a discussion, please shut me down. If you have something off-topic, if you find out something you are talking about are going beyond the scope of the areas of we suggested, we can find some place for you guys to talk, Daza or myself can help find you a place. Meetings outside should be quiet. Best to keep discussions towards our doors or keep quiet conversations over here. We just don't want to interrupt our neighbors.

Lightning talks. This is the first thing that we're going to be.... this is the first introduction to each topic. These are adhoc. Some of you emailed me, oh am I going to be doing a lightning talk? Well, maybe. We didn't want to give anyone too much sage on the stage as Christopher has said many times. We don't want to give anyone too much promising on the lightning talks. If you said you were interested in doing a lightning talk, then I will introduce you to the facilitators come talk with me.

There are four different topic areas. If you are interested in giving a lightning talk, come talk to us and we'll try to work you into the schedule. I didn't want anyone to prepare too much. Not too polished. 5 minute each. They are intended to be fire starters, to start conversations and then to lead into topic tables. If you are giving a lightning talk, talk about ideas not about products. Everyone here has their own product, but we're here to talk about use cases, requirements, ideas, technical topics.

There are four main areas of lightning talks. The first one is going to be about identity, this includes rpeutation, personal data, KYC, various things about identity, Marta is the host of this section. I don't see Marta. Marta is meant to be the facilitator. If Marta is not here, I will cover this. The second one is provenance, this is things like licensing of IP, assets, and services. Neha is going to be the host for that one. Blockchain primitives and APIs, this is anything that might be in a browser like features, wallets, consensus protocols, common data formats, hosted by Dazza. The kitchen sink is everything else, which will happen tomorrow.

Anyone can propos ea topic table on anything. After we do the lightning talks, someone might say they want to organize a table on blah, these tables will move around. You will not stay at the same table the entire time, we will reconfigure them for the dfferent topics. We might pull tables together if there is a popular topic. For each of these tables we will have a number eventually, and you will see how this is going to work. Christopher is going to MC the first session.

If you would like to do a lightning talk for one of these other sessions, then I will hook you up with the right person. You will vote with your feet and your ears. If you are nterested in a topic, then go to that place. If you are interested in another topic, then go to another table. If you're not interested, then go to something else, we want you to be engaged as much as you can be.

Christopher Allen is going to lead us in the first breakout exercise. Lightning talks, then table breakouts which each has an instigator person, a faclitator and also a scribe. We are asking everyone, we are self-organizing these, this is more of an unconference than anything else, the instigator is going to be talking a lot, the facilitator is going to have a speaking stick, it's a 3 minute timer. Everyone has no more than 3 minutes to talk. We want to give everyone a chance to talk. You have 3 minutes. If everyone is really interested in what you are saying, you can ask for more tme and they might give you more time to speak. This is a way to give quiet people a time to talk, and so that people like me wont talk.

Each session is going to be 20 minutes of talking, then for the second 20 minutes it's going to be, we're going to focus on the three most important takeaways that you had from the 20 minutes. Then at the end of that 40 minute period, we are going to report back on 1 of those takeaways. This will all be handled by the facilitators. If you are interested in being a facilitator or scribe for a topic table, .... a scribe does not have to write everything down, they have to just get the main points.

We have a graphic facilitator thanks to Blockstream. She is going to capture the key ideas. There is going to be a breakout session. She is going to capture stuff for the plenary session. Media, privacy, etc. We are going ot have some video recordings. If you don't want to be on video, then don't get in front of the video recorder. Avoid being recorded on your own. The podium will be the only place recorded. Dazza might do some lttle interviews, if you're interested in that then please talk with Dazza.

Bailey, are you here? She is going to be here. She is a reporter. She has done stuff for Coinbase? American Banker? She is a freelance... Coindesk, thank you. She's probably going to be doing a couple of interviews. If you are interested in being interviewed, then you can talk with her. She has made sure that she will not quote anybody unless they give her permission to be quoted.

Speaking of quoting people, the hashtag for this event is #blockchainweb. Please do not quote people out of context, this gets you in trouble and gets other people in trouble. Let people know that you plan on tweeting about them. If you hear someone say something, then please ask them before you tweet it. Follow the golden rule, tweet others as you would like to be tweeted yourself. Be careful that the things in here don't spread out of context elsehwere. This is obviously a public event, and it's meant to be public, but we don't want to have people have to defend themselves with things said in this room in the larger media stage.

W3C would like to know if there's anything ready for standardization. Is there any way in which the blockchain can help the web and web standards? or vice versa. There might be other collaborations that might come out of this. That's great, we're glad you're here.

Someone asked me to talk a little bit about standardizations and values. How do you go about standardizing things? Wendy is going to talk about the process a little bit more. When is something ready for standardizing? Is there a clear problem statement that this would solve for a significant number of people? is there a good start ing point? Is there a spec, clear solution, or is there a set of competing solutions? Do we have the right stakeholders? Are the right people ready to come to the table at that time? Are they ready to write things, test things, are they ready to deploy this thing? If none of these things are true, then it's probably not ready for standards. If all of those things are ture, then it might be ready for standards.

W3C focuses on client-side features, browsers, markup languages, user-facing features, javascript, APIs. This is what most of our stuff is. Interchange formats, ontologies, vocabularies, languages to manipulate data, etc. Just as a caveat, a lot of the browser vendors steer far clear of these things. If you want to get involved with those, you have to talk with browser vendors first to figure out if they are interested in this. If it's something that is going to touch on browsers at all, it's important to get browser vendors involved earlier. It's not that eveyrthing has to touch the browser.

Usually when there is a client side API, for example WebRTC there's client-side APIs and protocols and usually we partner with the IETF for that. Will all the W3C staff stand up? Jeff is here, he is our CEO. We have our bizdev guy, if you want to join or give us lots of money then he's the person to talk with. Then there's someone working on formats. And head of technology standards domain.

I would like to thank our sponsors, Dazza and Neha at MIT Media Lab, Sandy Pentland is providing this space. NTT. Blockstream for the graphic facilitator. Other generous W3C members. We have meals for everyone. Can everyone give the sponsors a hand for proviing food? Good. We tried to get meals for everyone. If you did not register in time, then you might not get a meal. If you do not have a badge, then repsectfully please make sure that people who put effort to get involved earlier, please make sure they get their food. Please do not take food that you didn't ask for. Vegetarians, everyone eats it, so don't take one of the vegetarian boxes unless it's clear that all the vegetarians have got all their food. I will eat humans, I am a vegetarian, if it comes down to it, I will eat humans so don't push me. If we're not able to feed you, we apologize. There are food trucks just around the corner and it's pretty good. We probably have food for everyone. I just want to make sure that the people that get food first are.... Apparently, there was some food in the outside area, please do not take food from out there. All of our food will be in here. The food outside is for a set of other people. All trash, there's 3 bins in the back, for trash recycling and compost. Please bus your own tables. If you make trash, please put it back there. That's it. Thank you for attending. Treat everyone respectfully. Have fun, or don't.

If you have any problems, call me 919-824-5482
