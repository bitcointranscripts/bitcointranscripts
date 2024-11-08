---
title: 'How can we get 10x the number of "core" contributors?'
transcript_by: Bryan Bishop
tags:
  - bitcoin-core
  - career
date: 2015-09-13
---
10x the number of core devs

Objectives:

* 10x would only be like <1000 bitcoin developers
* 7000 fedora developers
* how do we grow developers?
*

how many tor developers? how many linux developers?

poaching from each other is not cool

There's not enough people with the necessary skills. There's no clear way to train new people. Apprenticeship works, but it scales very very poorly. It's better than a static fixed number of developers. In the linux industry, started in linux at a time when nobody took it seriously. It was this toy operating system made by a bunch of volunteers and tiny companies that tried to compete with UNIX which was this expensive thing you buy from these massive companies if you wanted to do anything serious on a server. I think that the story of how linux overcame that and entirely replaced that formerly $100B+ industry, coming from a space where it was laughed at, that we can learn from. I think the best way to understand this is that there are a lot of parallels where there are volunteer hobbyists doing it because it is interesting to them, or they use it themselves, and they know how to code and they can make improvements to it. The very first people who contributed to bitcoin like linux were software developers, comp sci people, and also math nerds and cryptographers because the type of engineering you have to do for consensus is very difficult compared to other engineering.

People were doing this as a hobby at first, and other people joined because they saw the possibilities, the money aspect, they were technologists who thought it was really cool. Up until a certain size, an open source project can get pretty far with only volunteers, but volunteers only do what they want to do, You have to do heavylifting to fix major problems, but nobody else is accountable to engage with them and review their code, and to double and triple check that no mistakes were made and that progress was slow. That describes where we are coming from.

It's clear that the parallels between the linux story and bitcoin story are astounding. There are non-developers who will be able to contribute and grow the system. They are equally important. Understand ways in which non-developers can join the community and be helpful. We're this really tiny industry, and we're fighting each other instead of the major trillion dollar banks. Why are we fighting each other?

One problem is that the outside environment now is that there's a startup culture, silicon valley. For a developer interested in bitcoin-like thins, spending their time doing core development is unprofitable compared to taking a job at a startup where they will have zero time on hobbies.

Developers turned off by politics of open-source. Smaller projects are nice, we should keep small projects, we should have parallel communities going, like litecoin and ethereum and XT.

Ecosystem companies in the linux industry hired developers to work on common infrastructure. It's their job to respond to new people that ask questions about getting involved, it's their job to respond to code review when other people try to contribute if they have an idea, it's their job to fix things even their competitors to help because they rely on the same common infrastructure. That started informally at first. This evenutally grew into the Linux Foundation. They are seen as very professional and neutral.

How does the Linux Foundation operate? We have tried foundations in this space before and it did not work out so well. They focused almost entirely on dev and not politics. The money came from member companies. How are they governed? Who resolves disputes? The foundation itself is not in charge of decisions in development projects. They help facilitate cooperation between companies that each financially support developers on their own staff who have developers whose jobs it is it ow ork on common infrastructure.

How many developers were involved in linux when it was small to big? In terms of venture capital, there were 100x more developers. The reason for that was the extreme scarcity of our particular industry. Early 2000s is when Linux began to be taken seriously in the enterprise.

The big UNIX vendors like IBM they were the ones who would be replaced by Linux, they saw the writing on the wall, then they decided to invest $1B into linux engineering. They replaced over time hteir hardware and servers with competencies in Linux. The ecosystem companies have to understand to the shared thing that they all depend on, so one example of this that sounds great but would be hard to do, Pindar is from Hong Kong and has ecosystem relationships with miners, he got the chinese miners to agree in principle to hire an independent developer between them to communicate in English and Chinese and smart enough to become a core developer to help represent the Chinese interests shared between the miners and exchanges and to keep good lines of communication with other developers.

When comparing to Linux, one of the reasons they had more developers, it was much more modular from the beginning. Not every developer is a cryptographer. If we become more modular, we might be able to get more people to participate and so on. There should be more opportunities for people with other talents to move in.

A major effort in Bitcoin Core has been to split the really dangerous to change parts of consensus into a library, so that everything else can be easier to change by other new developers. What's the timeline on that? Review is very important.

There are a few companies that are paying for Bitcoin Core engineering. Blockstream is another. MIT DCI is another one. There are some smaller companies that have been doing it for a long time (Chaincode Labs, ....).

Ecosystem companies are relying on this infrastructure, when you invest in something you can have more influence on it. Why aren't companies investing in infrastructure? At least 350 startups doing things in the bitcoin ecosystem. But which large bank is funding Bitcoin Core?

Red Hat had hired a bunch of the original Linux developers; so it was that the experts all ended up at Red Hat, and everyone who needed support had to go to Red Hat because Red Hat had already hired all of them.

CEOs had never talked with the developers or the miners. Developers read the emails just fine. It's far too easy for people to be angry with each other. Sometimes there's no substitute for talking with humans. CEOs should be reading bitcoin-dev email.

UNIX had 40 years of professors teaching it in their courses. Informal instructional courses. People who write compelling text, the smart middle cool students and smart high school students, they shouldn't have to wade through a bunch of debate. More writers?

Hire technical writers to summarize bitcoin-wizards logs. Hire some technical writers or scifi authors. Giant book. Dev guides were good.

Younger people will work for vision and impact more than money these days, as long as you are not rude.

Lots of repetitive questions; it's not easy for new people to realize that there 100 times that the same idea was brought up. It's a knowledge accumulation problem.

Intimidation factors. Mentorship/mentors/buddy system for introducing to open-source projects. This may be less intimidating.

Use altcoins as false flag projects for recruiting.

Google Summer of Code, mentorship plus summer funding.

There's both a supply and demand problem. Maybe if you made it clear that there is demand, then there was supply.

Needs to be more manifestos sharing the vision.

$1B bitcoin infrastructure project- but why put in $1B if you see the market size is $4B. Also, gavinandresen is paid only $200k and sort of sets an upper bound on developer salaries because it's hard to argue beyond that- although not impossible of course. There's an inherently adversarial nature to some of this.

Developer sponsorship

Measurements/metrics

apprenticeship system, inherently scalability limits

poach linux kernel devs

API service provider companies- but this sort of hides bitcoin from the developers.

Regularly scheduled small developer group meetings, geographically dispersed.

Someone should manage mentorship availability and filter good students to those mentors.

More clarity of status and next steps on pull requests.

Technical writers are easier to hire than bitcoin developers. Target starving artists. If the companies aren't willing to hire new people to become core infrastructure developers, then have them hire technical writers to summarize old IRC logs.
