---
title: Bitcoin Core GUI introductory meeting
transcript_by: Michael Folkson
tags: ['bitcoin-core', 'ux']
date: 2020-08-20
aliases: ['/bitcoin-design/2020-08-20-bitcoin-core-gui']
---
Topic: Agenda link posted below

Location: Bitcoin Design (online)

Video: No video posted online

Agenda: https://github.com/BitcoinDesign/Meta/issues/8

The conversation has been anonymized by default to protect the identities of the participants. Those who have expressed a preference for their comments to be attributed are attributed. If you were a participant and would like your comments to be attributed please get in touch.

## Bitcoin Core PR review

There seems to be a lot to learn about the background of Bitcoin Core, how work gets done, what it should be, what it is right now, why it is the way it is right now. I am curious to learn more there.

A lot of links are about reviewing, how to review and all of this stuff. I feel that as a designer I cannot help with that as much as I’d like to. I don’t even know what I could do there. I totally understand the need and that that is a priority for development but personally I can’t really help there.

I can see why you think that and for some PRs and Issues I am sure that is the case depending on how technical you are. However there have been discussions in the past where one reviewer has been like “I like this” and the next reviewer has been like “I don’t like that, I like this” I think that that is when someone with a design background who can go away and ask people and come back with a view on what’s best for a certain user group would add value to that discussion. Even if you aren’t technical, I don’t know how technical you are I still think there are going to be certain issues and certain pull requests where you can add value to those discussions and to those reviews.

For things that are directly UI related for sure. From reading through these documents there is a lot of heavier coding work where reviews are needed. That should be prioritized in terms of review work. The UI work was fairly minimal in comparison.

Review is the only way that things can be implemented in the code.

In terms of technical savviness I don’t know how to locally build the wallet and run a branch on my computer. Reviewing for me is typically screenshots that somebody shares. There’s a technical gap for me.

I’m reasonably technical, I do want to play around with building it. I am not sure if I want to contribute in that way. There are a lot of issues open at the moment which are easy to shed new light. I was looking at one now that fanquake put up, make an Tor icon for an active and non-active state and push it into the repo. Pretty easy without having to fully compile the Qt locally and run it.

What I like is that in Figma or Sketch or whatever design tool we have there is a one-to-one reproduction of the actual live software. You do a design first ahead of development and by the time development comes around all the UI issues are discussed and resolved. It simplifies the development because you don’t have to build the UI one way and then redo it again. You have already resolved a lot of those things. What they should be called, where they are located and all this stuff. It does require a whole bunch of coordination because in the initial planning and discussion phase, that’s where you do initial styling and design. It is more planning work and coordination work at first but then the implementation becomes easier. That makes it easier for designers to collaborate to.

## Designing for multiple operating systems

As a coder how are you as designers going to support multiple… the same UI for MacOS, Windows, Linux?

I just started on making a Figma file, that is a way to show what elements fit where. I have a session for Mac, Linux and Windows. I have been importing the designs of the current GUI and remaking them in Figma. Having those reusable components so when people start working on designs they can make designs using the current operating system elements.

There is a historical context. Before designers were involved in the Bitcoin Core GUI development there were discussions in the Bitcoin Core repo about the GUI style. Should it be a single style for all operating systems or should it be native for each system? The consensus is that the native style is preferred. Core in MacOS looks like any other MacOS application. Core in Windows looks like any other Windows application. Is it the correct way? Should we have a uniform style for any platform? Is it easier for a designer? If yes the coders should implement customized styling in the code first.

There are some elements that are very easy to make them look like your native operating system. A button, change the font size, change the font color. Aren’t there some fundamental differences between Windows, Linux and Mac that cannot be so easily localized by changing colors, outlines, backgrounds or typefaces? Does it look and feel native everywhere or does it feel a little bit off? It cannot be fully adjusted. How good is this localization, I guess that is the question.

I’ve been running the GUI on Mac, Linux and Windows and I definitely think there are some inconsistencies across the three platforms. They are definitely native but there are some things that are quite native. To be honest the Linux version probably looks the best which is surprising. Usually it is Mac or Windows.

You feel like if you pull it up on Windows it feels like a Windows application? Do you get that feeling?

I would personally prefer to have one design across all platforms. I am not into a Mac feeling or Windows feeling, I just care that it looks nice, feels nice and does what it is supposed to do. They do feel like a Windows application or a Linux application or a Mac application. Is that what people want? I personally think one implementation would be easier from a design perspective.

Even the onboarding process for Mac and Windows are different for the Bitcoin Core GUI.

It is the same. On MacOS, Windows and Linux the onboarding process is the same.

I tried to run a Bitcoin Core GUI on a Windows and looks wise it was different from Linux and Mac. It might have the same steps but visually I think it looked different.

Bitcoin Core GUI uses the multiplatform framework Qt which was chosen because of its multiplatform nature. It was a long time ago. If I remember correctly Wladimir van der Laan who implemented the GUI in Qt the first time. The Qt framework, it was a good choice for that time for multiplatform support. We have support for any platform, Windows, MacOS, ARM, Linux any. Styling in Qt has options. The default option is to inherit native OS style. Most Qt widgets have an ability to be customized. That ability is not used now.

That’s only for the onboarding? When you get to the actual GUI you aren’t using the default templates right?

## Making changes to the Bitcoin Core GUI

There is feature development, there is the visual styling layer and then there is the improving or working on the interaction layer. Onboarding flow that doesn’t add any features but makes the interaction nicer for new users to set things up. Then just now we were talking about visual styling. Personally my impression is that the visual styling is much lower priority than the feature level and some of the interaction level. The feature level is creating new things and in the interaction level I would include introducing some functionality that exists in the API or the command line and bringing that into the GUI. Include that in improving the interaction model. Is my assumption there accurate?

I agree. Onboarding interaction was discussed many times in the Bitcoin Core repo. How could it look? How should it look? What steps should be included?

I think that is definitely something the design community can help with.

The Bitcoin Core repo works in small steps much better if implemented. I can suggest a first step of onboarding using a wizard and choosing language. These steps will allow us to add additional features to onboarding interaction. The first stages are quite simple and could be implemented in the code quickly.

It is fairly easy to design this in Figma. You can plan for the future, the next five or ten steps. Then you pick one for the first implementation and maybe you get some momentum with other people helping and more steps get added. It helps with design when you know roughly what you want things to be like in the future.

On onboarding what I had in mind was focusing on what is quick to do and doesn’t involve a lot of technical hurdles. Choose your language on the first screen. Second screen a section about the node, what exactly that is, what is pruned node and what is a full node. Having those as onboarding steps I think would make a big difference. Then going into a version 2 of the wizard, making it more fully fledged, add the ability to create a wallet in the onboarding wizard rather than having to get a diff on wallets randomly created without any notification in the GUI. That is quite confusing at the moment. Obviously that is a higher technical hurdle, better to take some baby steps. That’s the approach I was going for, slow versions rather than presenting a fully fledged wizard with different Create Wallet, Load Wallet and different flows. That would be more overwhelming for the Core contributors to look at. Do it in small components.

There are constraints. I’m not entirely sure what those constraints are because it is a project managed by consensus. We can go to one person and ask what the constraints are and they might give a slightly different answer to if you asked someone else. I’d like to nail down what we think the constraints are so we can work within those constraints. The one thing I would say about the baby steps is even on the back end stuff they have had an overarching vision of where they are trying to get, it is just that the PRs they introduce to the project are baby steps. There’s nothing wrong with saying “This is where we’d like to get to as a destination but we need to introduce it into the codebase gradually so people can get comfortable with it.” You can have best of both worlds.

I think the constraints are mostly technical. For example the Qt implementation, the GUI interacts with the core with signal and slot systems. Even improved Qt signal and slot systems sometimes silently fail. The user has no correct information about core data or has wrong information of core data. He cannot distinguish is data true or did the signal, slot system silently fail. It requires much real testing. Currently Core has multiple unit and functional tests. Anytime we build and compile we run tests to guarantee that everything works fine. The GUI has no such automated functional tests. Manual testing is required. Constraints exist and these constraints are mainly inherited from the Qt framework and inherited from security of Core.

I would be happy to help testing if I could just get the development stuff running on my computer.

I think it is plausible to get you up and running doing that. I don’t think it is hard to build PRs. Going back to the review discussion you don’t have to sign off on everything. It is not like when you do a review you need to say “This code is fine. There are no bugs. I have looked at every aspect of this PR and it is all fine.” You can just pick one aspect and say “On the design question I think this but I haven’t reviewed the code, I haven’t done this.” Review is really important and whatever value we can get from whatever skillset somebody has the better. There is certainly value you can bring with your background.

## Getting consensus for GUI changes

On consensus, when I worked on the Monero GUI what would often happen is that I would suggest something to the developers and they would say “Don’t tell us, tell the community.” So I posted on Reddit with 150,000 people. With bigger features, newer things the first step was to throw it out to the public to see what everybody thinks. Then afterwards only later would the team work on things. They could give their input but the idea was to put it into the public space. There was a process where the ideas were first tested in a public phase and the good ones were adjusted. At some point later they trickled into actual development. A small thing might be developed or the whole thing, maybe it took half a year or so. It was a pretty slow process. If you look at it on a longer timeline it is much easier for many people to think about it and build consensus on something. Consensus doesn’t happen at the PR and Issue level but it is a longer process. Is there anything like that happening?

I haven’t seen that happen on Core apart from a big soft fork consensus change. Something like Taproot coming up, it is really important there is community engagement and community support for it because it is a consensus change to the code. Generally for everything else it is the developer community around GitHub discussing what is best. Obviously design is a little different in that back end decisions are different to what is best for this type of user. I can’t speak for everyone, I can only speak for myself but I would guess that whatever process you are happy with in terms of how you get feedback from your future users could be used within this process. If you don’t want to go to Reddit and have discussions with hundreds of random strangers to get feedback on the design changes you want to make you don’t have to. It is down to how you work and how you best like getting feedback on which design decisions should be made.

On the core developers having different ideas on constraints and what works and what doesn’t work, share it in the Bitcoin subreddit and gets hundreds of replies and feedback. That can be used to convince the developers as to why you are trying a certain design. Rather than saying “I’m a designer, this is good” and sit around and bikeshed, worrying about small details. I think that this would be a good idea for doing work on the GUI.

I think any good designer will go and get feedback. I’m not saying a designer makes all the decisions in their head. Part of the design process is to get feedback from your potential users. What I’m saying is whatever is preferable to you in terms of how you work for getting that feedback I think would be fine within this Bitcoin Core project framework. I’m not saying don’t get feedback, I’m saying get feedback in whatever way you are comfortable. The only thing I’m concerned with on the Reddit like approach is often on back end stuff rather than design stuff someone will open an Issue and say “This survey had 50 percent liking this so we should implement it on Core.” Everyone on Core would be like “We don’t care if it is popular, that would require so much work on Core to get it done.” It is not democracy, it is people who have a really strong understanding of how the project works and have wrestled with the code over many years, their say means more than someone who may have never even used the Bitcoin Core GUI. Them saying I’d like this feature over this feature isn’t going to convince a core developer to make that change if the core developer thinks it is a bad change.

It is a sensitive thing. When I posted things on Reddit I would always include the design and a screencast of a video where I talk about it for five to ten minutes. I can clearly narrate what the thinking behind it is and how it relates to the current one and what is different. When you just post an image people will just start looking at a button or so, look at the wrong things because there is no guide on what this change means and why it was done. It really comes down to how those posts are written in order to get really good feedback. It takes effort and it can go horribly wrong.

If you like doing that then do that. If you don’t think that is the best way to get feedback then do whatever is most productive to get feedback before you go to GitHub and say “I think this is best because I got feedback in this specific way.”

It could be that the ten step wizard lives in the public space and gets discussed a lot while the first step is being implemented. The rest is still being discussed and by the time it comes to implementing Step 2 or 3 then there was already a lot of discussion.

## Designers interacting with Core developers

I have a question on interaction between designer and coder. I saw sketches on Figma but as a coder I need window size and pixels. Is the window fixed? I need font names, font size. How do these interactions work? Should a designer open an issue in our repo to describe these elements the coder should implement?

I think it depends. In Figma on the top right hand side there is a Code tab. If you click that one everything that you select in the UI will show… If you double click on a text field it will tell you what font it is, how big it is, what font size it is.

Should I be signed in in Figma?

I can share my screen here, I will show you. Somethings Figma is good that but there is never a replacement for talking to each other. Here on the top right you see this Code tab. Whenever I click on this text field here it will show me the font family, the size. If I hover over another element then it tells me what the distance is to that other element. If you look at this one here, on the left you will see this is purple and it has this icon here. It means that it is a component. I can go to the main component here. Figma also has a component system where any change I make to this main component gets inherited by all the instances of that component. I create some instances here. If I make the main component yellow the instances will also inherit this. When I look at the code of an instance it tells me what the main component is. There’s a whole bunch of stuff like that in Figma. If the design is set up that way then as a developer you can always look at the main component and see how it works. As a designer you can’t do all these unique special things in every place because it is automated. There are fixed properties to all the elements that you use. That’s the same with colors here, these are all the colors used in the interface. You can do the same with text styles. As a designer and a developer you always have to communicate with each other but if you have a good set up like that it makes design development easier because there is a shared language of text styles, components and what they look like. You know what the restrictions are. You don’t have to check with every button what the color is because it is always the color of the main component. There are a few things like that in Figma that are really helpful. There is a bunch of interest in the design community to have a Figma crash course. We did one a month ago but there is more interest. We just to need to organize that and talk about collaboration, what designers can do and what they can’t do.

One thing I am noticing is that there is a gap between the coders and the designers. One thing we might need to develop more are the coders that are interested in this project. If all we have is designers and we don’t have anyone to code then we won’t get anywhere.

Would having a design system set up, documentation that specifies all this be something that guys would want? Instead of having to go into Figma and look at the style guide… In BTCPay it is not finished but they have a design system that specifies all these kinds of things. We follow those guidelines in our Figma designs. When we share videos you know that we are following these specifications. It makes it easier rather than having to go into Figma and look at it.

Do the core developers work on everything or are there one or two people that just work on the GUI, one or two people that just work on security or is it pretty mixed?

It is personal, it depends on the person. People work on whatever their expertise is. Some developers have expertise in security, in consensus code, some developers have expertise in the GUI code. I could list the developers. Promag, Sjors, Luke Dashjr, fanquake.

If we were to present a design to the community and then ultimately to these developers do you think they would be interested in not only providing feedback but also writing the code for this?

I am personally interested in writing code from designer suggestions.

Fanquake does a lot of work on the build system, Luke does a lot of work outside of the GUI. I would guess that out of those individuals that you named they probably wouldn’t be interested in coding up a whole new design. They would look over PRs that are opened but I would guess most of those four if not all of them wouldn’t like to take a design and code it all up themselves.

What happened in Monero was interesting. I had just a design for fun, I posted it on Reddit. A developer who had been wanting to help on the Monero GUI, he picked it up and said “I want to implement this.” For him it was an opportunity to join the project because that was his interest but he didn’t have something to work with. We matched up on this design. It was his way to get started. Maybe if there were some interesting things out there that are open and up for grabs then maybe there is someone who is interested in coming in. Putting things out there sometimes is all that is needed. It is not guaranteed. I also have a design in the Monero repo that has been there for one year and nobody has done anything with it which is fine too. Sometimes it can work out that way.

## Targeted users

On the current Figma designs ([here](https://www.figma.com/file/FJ02rY3m8V9ZCDvoXjW39W/Bitcoin-Core?node-id=281%3A0) and [here](https://www.figma.com/file/FJ02rY3m8V9ZCDvoXjW39W/Bitcoin-Core?node-id=462%3A655)) what kind of user did you have in mind for this?

On the call we had the other week we discussed that the GUI is generally used by power users, people who know a decent amount about Bitcoin and not generally beginners. The rough goal we had in mind is we want those beginners to come onboard so more people run nodes and stuff like that. Whilst designing that I had a pretty broad view of the user base, catering for anyone from beginners to power users. There are technical elements in here that will cater exclusively to power users. When designing the guts of the GUI there is more of a focus on whether it is for power users or beginners. Having an onboarding process I think caters to any individual. I think it helps explain things, gives some context and understanding into what exactly they are doing.

Would it be possible to introduce optional versions? A GUI for beginners, a GUI for power users. Is there a way to separate the GUIs depending on who the GUI is.

I am not sure on the technical side. I think that would be a lot of work. I think one design can cater to all audiences. More complex features can be tucked away behind the scenes only to be accessed by those who need them.

In the Monero GUI, I was against it, but they decided to have a simple mode and an advanced mode. The advanced mode had mining, it had message signing, it had a merchant page, a point of sale type of thing. There were a bunch of other types of settings. When you launch the application it asks you a few things. If you want to bootstrap a remote node, simple mode or advanced mode and then the interface got adjusted. I think Bitcoin Core has less functionality, it doesn’t have mining for example or a merchant screen. My hunch right now is that it is not necessarily needed but maybe later it might be something to think about.

More advanced features are used in wallets like coin selection.

It is going to be a lot of work but I think there are going to be ways to implement these more advanced features like coin selection in a user friendly way. I think it would be possible to do that. I would rather go down that route, having something easy with stuff tucked away. The face of the GUI targeting beginners.

On localization is there a localization effort?

Do you mean translation?

Yes.

Bitcoin Core has translation with Transifex. It pulls translation from Transifex. Bitcoin Core translators are another community like the designer community and developer community.

Any language that you use, the translation community might already have some guidelines on what to call certain things. It might be worth checking when you are writing copy.

Any translation which is added to the project page on Transifex automatically adds as a stage of the release process.

It would be good to see an open issue on the repo on onboarding with a link to the Figma sketches. Let’s bring Figma to our repo to start work on coding.

I’ll do a prototype and a video as well so there is a visual people can watch. They can use Figma to look at the guts. A video seems to communicate what is going on a bit easier.

Just a link to the Figma sketch is enough for a starter.

Figma files can get massive and super confusing. What about any other calls? Design jam sessions, Figma crash course, anything else that would be helpful or useful to do? Or stick to GitHub and Slack for now?

I’d probably attend a Figma crash course. I’d like to understand exactly the changes, right in the guts of what you did on the Monero GUI given that it is Qt just like Bitcoin Core. I think that is a really interesting case study and how you worked and what you needed from other people. I don’t know whether that is a call or a presentation or a discussion or something we can put on YouTube or something. Something so that we can learn as much as we possibly can from that project. I think there will be similarities.

Bitcoin Core uses Qt widgets whereas Monero uses Qt QML which have very different design constraints. I think QML that Monero uses is a lot more flexible and easily customized whereas widgets is a little bit less customizable.

A big thing with Monero was that there was a super motivated developer who really wanted to make this happen. He really pushed this through. I as a designer wouldn’t know where to start coordinating people. He followed up with me on different things and we had a good back and forth. His communication and energy really helped. He also applied for funding, Monero is all community funding. “This is what I want to do. Give me this much Monero” and people donate. He was able to work on this full time. That made a huge difference.

Maybe we need this overarching project. The concern from a Core perspective is that we have this new Bitcoin Core GUI [repo](https://github.com/bitcoin-core/gui) and all the existing contributors are going to forget about it and we aren’t going to get any new contributors on the GUI. It will just sit there and not get the interest or the eyeballs it would have got if it had stayed in the main Bitcoin Core repo. Perhaps an overarching project to revamp the GUI will attract more people to contribute and review PRs and bring attention to it.

Just a handful of motivated people can make a really big difference.

Do you think there is enough to discuss on Monero in terms of lessons or changes that could be replicated on Core?

I don’t think it would be easy. Monero is using Qt QML but Core is using widgets. They are so much different. Bitcoin Core has a [pull request](https://github.com/bitcoin/bitcoin/pull/16883) to switch to QML. It does not have much support. I don’t know why. A lot of review on it is required to switch from widgets to QML.

I cannot speak to the technical challenges of how complex everything was. Maybe we could get the Monero developer in to talk about that side. I can only speak on the design side. The Monero developers are on IRC all day long and I don’t know how they do that time wise and attention wise. I don’t know what all the challenges were and how all that panned out.

There is interesting context here on this PR. With this [process separation](https://bitcoin.stackexchange.com/questions/98398/what-is-the-motivation-behind-russell-yanofskys-work-to-separate-bitcoin-core-i) there is going to be more experimental ambitious GUIs being built that can connect to Core. People can work on both. They can work on the solid standard Bitcoin Core GUI and more experimental GUIs as well if they can’t get it into the Core codebase.

Shall we have another call in a couple of weeks?

I will try to organize a Figma crash course but it won’t be focused on the Core GUI, that will be for anyone in the design community.

In the Figma file I want to have some contributing guidelines for designers that come onboard and also give some context to the developers on the process the designers go through to create designs. If more people join the project will be important to have workflows so things don’t get messy.

