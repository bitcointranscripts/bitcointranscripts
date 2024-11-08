---
title: Unwinding Bitcoin Coinjoins - Tumblers, Wasabi, JoinMarket
transcript_by: Stephan Livera
speakers:
  - Ergo
date: 2020-06-09
media: https://stephanlivera.com/download-episode/2153/179.mp3
---
podcast: https://stephanlivera.com/episode/179/

Stephan Livera:

Hi Ergo, welcome to the show.

Ergo:

Hey Stephan. Thanks for having me back.

Stephan Livera:

It’s great to chat with you, and I know you’ve been doing a lot of awesome work, so I’m really excited to get into it and discuss with you. So I know you’ve got two reports that you have put out recently with OXT Research. So let’s start with the China and North Korea one. So it’s called the North Korean connection. What spurred this analysis?

Ergo:

So I guess in early March, the the IRS, the DOJ and the FBI took some legal action against two Chinese nationals. And as a part of the legal actions, they published some relatively detailed chain analysis. We saw this go by in a couple of news articles. We got our hands on the, you know, official court documents and kind of took it from there.

Stephan Livera:

It mentioned the Lazarus Group. So who are they?

Ergo:

The Lazarus group is I guess, a somewhat infamous North Korean hacker group. They’re allegedly behind a lot of malware incidents, hacks, thefts and other kinds of issues. We’ve seen, you know, multiple hacks of South Korean exchanges in, I don’t want to say recent years, maybe not since 2018 or so. No, that’s not true. 2019. we had one as well, but we’ve seen multiple you know, exchange hacks you know, in South Korea.

Ergo:

And they’re usually we’ll see a news report go by that attributes, you know, possibly to Lazarus group. We don’t usually get much details. It’s usually behind probably, you know, the government security services. But in this case we finally started to get a little bit more details on that. So, you know, in the Lazarus group report you know, like I said, we, we saw the the news reports go by and we got our hands on the actual, you know complaint filing you know, on first reading. There was a couple of things that we noticed that were, you know, either admitted or, you know, kind of stood out to us as something that we probably wanted to check on. So, you know, the first thing that stood out to us was the use of the term peeling chain.

Ergo:

You might see us use that from time to time and reference to just sort of a typical Bitcoin transaction graph. And for kind of the listeners that aren’t familiar with that terminology you know, a peeling chain typically has is a string of multiple transactions, typically with one input and two outputs. And depending on the size of the outputs, you can sort of get an idea of which output was the change based on some common heuristics and which output was the payment. So this report, which was allegedly filed by, which was filed by the DOJ, the IRS and the FBI this was the first time that we’ve seen them use this somewhat technical kind of Bitcoin transaction graph term. And that kind of immediately stood out to me. I know that the IRS cyber crime investigation unit was involved in this a lot of these organizations, they have access to the mainstream chain analysis software, but you know, that terminology sort of really stood out to us. It either means A) they’re more advanced than we, you know, kind of assume, or they’re getting help from the chain analysis firms. And I’m fairly certain it’s combination of both. They’re very likely even if the chain analysis firms aren’t doing the actual analysis, it’s very likely that they’re at least aiding the government agencies, you know, via consulting or some other type of you know, assistance.

Stephan Livera:

Right. And as I understand even companies like chain analysis and, you know, these chain surveillance companies or surveillance companies are some of them have government contracts and it may well be that they had a contract to teach government employees about chain surveillance, right. And how to, you know, what is a peel chain, what is, you know, a CoinJoin and all these terms. So, so with bringing you back to this particular complaint in the document or in your report as well, you mentioned about how there were these, what they call virtual currency accounts. So can you tell us a little bit about that and where did those accounts come from?

Ergo:

So the complaint formally, it names two Chinese nationals but it claims forfeiture of assets, belonging to virtual currency accounts. That includes, you know, anywhere from, you know, Bitcoin addresses or ETH addresses to accounts directly held by the you know, associated entities at major exchanges. So the complaint seeks forfeiture of those direct accounts. The complaint also references the virtual currency exchanges as pseudonyms. It doesn’t directly name who was hacked and any of the other exchanges that were involved instead, it, it just uses numbers. I think it uses VCE one virtual currency exchange one, or the exchange one to reference, you know, who was hacked and sort of where funds went. So you know, after our first, you know, perusal of the paper we wanted to figure out, you know, who was hacked, you know, what does the complaint attribute, you know, to who and then where do the funds go to try to, you know, get behind some of these pseudonyms?

Ergo:

So as far as hacked exchanges I think we were looking at Upbit let me actually pull up the report.

Stephan Livera:

We’ve got Youbit, Coinrail and Bithumb.

Ergo:

There we go. Exactly. and some of those are, you know, major Korean exchanges update you know, and Upbit Bithumb and Coinrail was one that I had actually never heard of at the time and seemed to be sort of more of an all coin smaller hack, but, you know, the complaint goes into various details about, you know, the process of how the hack happened at each exchange. And for the most part what it alleges is social engineering attacks, you know, emails were sent to exchange parties, malicious links were opened and the hackers apparently gained access to the exchanges, private keys and were able to extract funds.

Stephan Livera:

Right. And so I guess if I had to just summarize what’s going on here, it’s essentially that this hacker group called the Lazarus group. It seems the story seems to be that they have found ways to hack some of these exchanges over the period of 2018 to 2019. And then they typically lie in wait for some time, right. It’s like, they’re a hacker, they’ve stolen some Bitcoins and then they wait and then they’re looking for a way to launder that money or sort of send it through an exchange and then try to pull it out as Fiat. Would you say that’s kind of a high level that’s what’s going on here?

Ergo:

Yeah, that’s a good overview. And what we saw generally in the complaint was this basically happened in three phases, which you sort of just described you know, number one is the initial hack followed by what looked like peel chains to various intermediary exchanges. You know the peel chain, you know, they, they obfuscate slightly the transfer of funds and what they do at least, you know, in our opinion and basically the opinion of whoever authored the complaint is that these are ways of circumventing you know, the exchange compliance software rather than depositing, you know, all 1000 stolen Bitcoin in one transaction it’s done over, I don’t know you know, a few dozen in smaller amounts. This will sort of avoid some of the the flags that might get raised from you know, exchanges.

Ergo:

So they’ll, you know, do the hack peel to a first round of exchanges. In our opinion they treat the second round of exchanges sort of as custodial tumblers. They used, you know, the exchange has operated a shared wallet, funds will go in, you know one address or one wallet and might leave from another. And it’s very hard to keep track of you know, funds from that point on since the exchanges are operating shared wallets. So after the funds are withdrawn then they’re peeled to a third round of exchanges where it looked like the conspirators were trying to cash out, you know, either Fiat or gift cards.

Stephan Livera:

Yeah. That’s really fascinating. It’s very mysterious story. Right. So, so let’s, I guess, dive into a little bit further detail on what’s going on here. So perhaps first, maybe you could just explain the difference for the listeners. What is the difference between a custodial tumbler and then, you know, what we know as the non-custodial coinjoin, if you could explain that, please.

Ergo:

Yeah, so we’ve blurred the lines between the difference between a custodial tumbler and a non-custodial Coinjoin. The term mixer has become, you know, used generically for both both terms, but they are, you know, inherently different. And like you had said tumblers were some of the first obfuscation techniques that were available to Bitcoiners, and these were custodial, they took control of users private keys. They effectively operated a shared wallet and they dispersed funds at some irregular interval after the initial deposit.

Ergo:

So again, you know, tumblers are custodial, they take control of the user’s private keys, and they can get a little bit creative with how they disperse the funds whereas a non-custodial Coinjoin, which is, you know, sort of the Samourai Whirlpool, JoinMarket, and with Wasabi wallet, you know, the things that most Bitcoiners are now sort of have become used to over the last, I don’t know, year or so those are non-custodial. And, you know, they have to operate slightly differently because they’re not custodial, typically the the funds in a coinjoin transaction are returned to the user in the same, in the same transaction as a user makes an input. So, you know, a coinjoin relies on math, whereas a tumbler can rely on its custodial properties to obfuscate fund transfer.

Stephan Livera:

Yep. And then in terms of ways that someone like yourself, a white hat chain analyst can attack, or, you know, try to unmixed or unwind a tumbler, is it essentially relying on things like timing analysis to see that okay, 1000 Bitcoins went in and 1000 Bitcoins came out or what, what are some of the ways that you would try to assess this?

Ergo:

Yeah, so depending on the tumbler, each one sort of operates a little bit differently. You know, funds aren’t necessarily returned to the user and the same transaction, like they are in a coinjoin. And that’s what we mean by, you know, a custodial tumbler can offer some better privacy than you know, a traditional Coinjoin if kind of done properly. You know, in a coinjoin we know that the funds are returned in the same transaction. So we can just monitor, you know, the outflows from that transaction to try to correlate the user, whereas a custodial tumbler, you know, we’re looking at potentially any number of transactions in the future that could possibly be you know, attributable to the original deposit.

Stephan Livera:

Yup. And I guess just one other point I wanted to touch on just with the peel chains as well, because I think that’s it’s useful to go over that as also, I think this is one of those dynamics where for some time before chain analysis became a thing, people thought they were able to obfuscate just by doing these sort of less sophisticated obfuscation techniques. Right. And using I think you’ve used the term previously is like self shuffling or and just kind of this idea of splitting off and carving out little chunks of your Bitcoin. And then like those little babushka dolls, every little piece becomes smaller. So it’s sort of like that’s kind of like what the peel chain is. And essentially these you know, the Lazarus group guys and potentially other people are using peel chains thinking they’re being more anonymous or more private. But I guess the reality is to a more sophisticated analyst, they can pick that apart, right?

Ergo:

Yeah. I mean, that’s correct. If you or an analyst kind of sees a large volume, you know, starting transaction, you know, originating from an exchange you know, depending on how many transactions are done if you just follow the end of that peel chain and you see where each of those outputs goes along the way you can start to kind of come to the conclusion that this is the same entity sending coins to the same place. And, you know, with just looking at a standard block explorer it becomes more difficult to see. You might see a reused address as, as one of the payment, you know, destinations. But you know, when you take a look at this as a transaction graph you know, on OXT, and of course a lot of the the mainstream chain analysis firms have something similar the peel chain becomes even more obvious where you’ll, you’ll see a very clear you know, small, you know, chipping away kind of as you described. And so, you know, for a period of time when these chain analysis firms likely didn’t exist, you know, maybe this could have been used as a technique to, you know, try to obfuscate funds. But now it seems that analysis firms have gotten, you know, a good bit more you know, in tune to what, you know methods Bitcoiners can use.

Stephan Livera:

Yep. And so with the understanding which exchanges it’s going to, and I presume that’s also because people have different goals when they’re using Bitcoin, right. And so some people using Bitcoin don’t care about privacy, that’s just the straight reality. So there are some people who will not be using these kinds of STONEWALL spends and so on, and it may not be possible to do these kinds of spans for large wallets. And so I think that’s why the reality is many. They have like a known cold wallet and that can be tagged and clustered. Would you say?

Ergo:

Yeah, that’s correct. I’m sure, you know the mainstream chain analysis firms are, if they’re not directly working with exchanges, getting provided information, they’re going out and they’re seeding entities. And what I mean by seeding entities, you know, creating an account at, you know, XYZ KYC light exchange to try to tag their clusters there. You know, so if they aren’t collaborating, there are certainly ways to try to get labels on a lot of these exchanges.

Stephan Livera:

Right. And I think it may well be that even just with publicly available information, in some cases you can see, Oh, this, or if you received a payment from somebody, and then you can sort of start to see, Oh, okay. This came from the Binance. Like if I trace this back enough, this came from Binance or this came from Coinbase or whatever exchange. Right. And so I guess just for listeners in your mind, understand that when you send a Bitcoin transaction, you’re sending that to a particular address, but then if the analyst is able to trace it back to see what was the source of that money, or where did it eventually end up, then that’s the way that these clustering behaviors can be done to try and understand. Oh, okay. That’s kind of the layout of the land that, okay. This little area here, that’s the Coinbase cluster and this little area there that’s some other exchange cluster, right?

Ergo:

Yeah, that’s correct. Yep.

Stephan Livera:

All right. So then I think the next question people would have is how, how was it that you were able to tell the money, once it went through the custodial tumbler? So I think that’s coming back to what you were saying around like timing analysis and so on, because normally people would say, okay, once you’ve kind of gone inside the exchange, and then they went back out the exchange, you would have lost the trail then how did you trace it through there?

Ergo:

Well, so, you know, there there’s we haven’t quite gotten to the custodial tumbler part of the Lazarus group, analysis yet. You know, we’re sort of documenting the phases that the IRS describes in the complaint, you know, so phase one was hack and peel to a first round of KYC kind of light exchanges. You know, they then use those KYC light exchanges as, you know, basically custodial tumblers, and then peeled for a third time to you know Fiat off-ramp exchanges. And so, you know, I don’t know exactly what the IRS did to acquire, you know, the information of how they went from, you know, KYC light exchange to you know their fiat exit. I’m going to guess that, you know, they have labels on, you know, the KYC light exchanges and they, you know, serve some subpoenas or, or, you know, reached out to these exchanges and asked for information.

Ergo:

They certainly have in the complaint, they certainly have account names, email addresses, pseudonyms and a other, you know, identifying information that they could only really get from directly from the exchange. So I’m assuming that they reached out to the exchanges from there and said, okay, you know, we saw that these funds went in you know, these transactions were associated with the original hacks, are these transactions that associated with any, you know, ID those ideas were provided, and then they watched the the funds move to the, you know, the Fiat exit and they’ve likely basically repeated the same process.

Stephan Livera:

Yep. I see. And so essentially the IRS, or the DOJ, or FBI would have gone and asked that exchange saying, Hey, you know, X, Y, Z exchange, we know this address at this time, it came in. Who was that deposit for? Do you have an ID underlying that person on your exchange? And then they would ask for that info.

Ergo:

Yeah. Correct. And you can even see in the complaint, they have some of these ridiculous KYC, you know, fake photos with the, you know, the alleged conspirators basically used doctored photos you know, fake passports, fake t-shirt models with the same t-shirt, but a different face. You know, so, you know, there’s certainly a ways around KYC that you know, these guys are aware of and they certainly do. But you know, when sort of all said and done the complaint documents, you know, the hacking process, it documents you know, how much Fiat that they were able to cash out, you know, at the attributed you know, second phase of exchanges. And then from there, the complaint mentions only once another cluster that did not get sent to an exchange.

Ergo:

And instead what they say is, you know, the funds were mixed and, you know, that was basically the end of that sort of paragraph or that portion of the complaint. So, you know I then followed the funds from the cluster that was mentioned into Chipmixter mixer the custodial tumbler which is one of, probably one of the more well known and more used tumblers. And from there, you know, we can circle back to, okay, how did I, how did I track funds across Chipmixer? And you know, we have already sort of given that, that little bit of background about the difference between a Coinjoin and a custodial tumbler the custodial tumbler won’t necessarily return funds you know, in the same transaction that a user you know, has an input.

Ergo:

And so there’s a second hop, you know, at least in the way that Chipmixer works where, you know, the initial transaction and Chipmixer, they’re trying to make look like a fake coinjoin they’ll take, you know, a handful of inputs and then they’ll spit them out. And in certain denominations they’re all, I think factors of two, I think some base 256 number. I can’t remember which ones exactly, but they, they effectively they look like coinjoins, but they’re not you know, so they’ll, there’ll be a second you know, transaction after the fake kind of Coinjoins in Chipmixer in which the funds are then returned to the user. And so what I saw was that there was about 160 Bitcoin that was sent to basically all to the same mix and all originated from the conspirators, you know, premix cluster.

Ergo:

And, you know, there’s a difference between one other difference between a custodial tumbler and a non-custodial coinjoin is that, you know, obviously there’s the risk of fund loss associated with a custodial tumbler. So users aren’t likely to keep their funds on a custodial tumbler for a very long amount of time. They likely are trying to get in and out as quickly as possible. And so what I saw was you know, a significant volume basically heading out from the same transaction as the funds came in you know, just one hop removed because of the custodial nature. And from there, I was able to follow the funds to various destinations.

Stephan Livera:

Yeah. That’s really incredible stuff. And so it, it sort of comes to that idea of you’re kind of using logic to understand, well, okay, this is a custodial service. These people do not want to leave funds on there any longer than they must. So they’re going to try to pull them out. And then as I read from your report, you’ve leveraged some additional metadata things, like, as we mentioned earlier, the volume correlation aspects. And then also there were certain common inputs and destinations, and then those were what enabled you to tie these together and understand that Oh this looks like it’s actually the same actor, even though there’s some obfuscation going on on the chain.

Ergo:

Yeah, that’s correct. I mean, there’s, there’s a couple other things that can done it can be done to de anonymize the flows across either a Coinjoin or custodial tumbler, the worst being is the combination of basically premixed funds and Post mix funds. And I saw that here as well. It was, you know, in one small occurrence, but, you know, it’s sort of, kind of tied a lot of the picture together. Okay. This is very likely the same entity that controls funds on both sides of this Chipmixer.

Stephan Livera:

And so just for listeners who are unfamiliar, I guess that concept of pre-mix and post mix. So pre-mix is basically your wallet that you were dealing with before trying to go through all this mix stuff. And then what’s happened in this case, is withdrawing it out from the custodial tumbler actually came back, which is like post mix that actually came back into that pre-mix cluster. And that’s what you’re saying enables you to tie it together, right?

Ergo:

Yeah. Correct.

Stephan Livera:

Awesome. and then so in terms of the context, just for the numbers, it looks like the complaint says 67 million of withdrawal from the noted exchanges to Chinese banks. And additionally, another $1.5 million in iTunes gift cards using Paxful peer to peer exchange. So that’s interesting, isn’t it? And I think it’s funny that people try to say like, Oh, you know like if there are people who speak bad about say coinjoining, but in reality, people can still sort of use exchanges almost as a custodial tumbler of sorts, right?

Ergo:

Yeah. I mean, that’s correct. And so, you know, the, the, the complaint kind of fingers peel chains as the obvious location technique. And while that certainly wasn’t obfuscation technique used, I mean, as we’ve sort of discussed, and as you know, the IRS clearly shows you know, peel chains are easily trackable, you know, if you’re going to sit down and take the time to do sort of a more in depth analysis. So, you know, in our opinion the sort of the KYC light exchanges were served as more of the general obfuscation technique. You know, they basically acted as custodial tumblers on chain and they required the IRS to go out and start knocking on doors and asking for additional information if they wanted to continue this tracking process. And I guess it’s also worth noting that you know, some of, one of the major destinations of these coins was Huobi, where the the conspirators were effectively trying to cash out into Fiat. We keep running into Huobi and a lot of our analyses.

Stephan Livera:

Yeah, you definitely have to ask that question. Right. so in this context, what does KYC light mean?

Ergo:

You know, so there’s always, well always try to advocate for, no KYC and if there’s, there’s sort of no such thing as no KYC, you always are dealing with some kind of a counterparty you know, even if you’re just trading with your friend they know that they sold you coins you know, but on the complete opposite end of the spectrum, you have sort of the Coinbase where they’re, you know, taking your picture of you holding your driver’s license, your bank account information social security number. And they’re, you know, basically now using all of that to sell to the government and everything in between, you know, sort of falls on some kind of a spectrum. And so some exchanges, they don’t require anything from users, all they need is an email address.

Ergo:

You know, that might be, you know, considered KYC information. And as we sort of saw in this report you know, even just the you know, having an email address can be sort of used against people. You know, but what we mean by sort of KYC light is you know, an exchange that doesn’t require you to give passport driver’s license, you know, bank account, kind of any other information. The KYC light exchanges tend to be exchanges that, you know, they’re basically shitcoin casinos, you know, they don’t, they don’t have Fiat banking ties. You know, so they’re not required to really take any of that information.

Stephan Livera:

I’m also interested to talk a little bit about some of the different approaches that these people are using. So as we’ve discussed, they used Chipmixer going through Huobi, and it looks like they’ve also used Wasabi. So can you tell us a little bit about their efforts there?

Ergo:

Yeah. So, again where the complaint kind of leaves off. It identifies you know, several hundred Bitcoin in a cluster and then effectively says the coins were mixed and the report basically stops. You know, I just described the process of the mixing through Chipmixer. But what we’ve also found was that funds from the conspirators cluster were merged with a very large separate entity’s, cluster which has been providing a significant amount of liquidity to Wasabi for, you know, basically since the end of last year. You know, this was sort of the first hint at you know, an identification of who this entity might be. We have a couple of ideas based on some of the information that was provided in the report or in the complaint about what the entity might be. But, you know, basically from there, you know, we got our first kind of idea that you know, these guys may also be using Wasabi.

Stephan Livera:

And if they’re using Wasabi what are some of the techniques that they may be using and what are some of the ways that you were essentially able to tie them together?

Ergo:

Yeah, so, you know, again, and a lot of you know, the attacks on coinjoins tend to be based on volume and timing. You know, the problem with sending such a large amount of volume, you know, through you know, a relatively small volume you know, coinjoin is that you tend to stand out. And so, you know, that tends to be one of the biggest thing that these guys do wrong, you know, what we saw with plus token. And it’s kind of what we see again here. You know, an entity depositing several hundred Bitcoin within the space of, I don’t know, a day or two and then withdrawing them all effectively to the same place is kind of what we see. You know, one of the other issues that I’ve sort of, you know for the first time was able to document in this case was you know, the address use that these guys have been basically suffering from in the Wasabi mixer, is pretty, pretty bad. And what I’ve seen for the first time was able to see was a, you know, an unmixed change output, basically get paid to a mixed address, which effectively deanonymises the post mix spend without the user having to do anything.

Stephan Livera:

That’s very unfortunate. And it also impacts the privacy of the other people in that mix, because now that’s, you know, there’s less entities who are unknown, right. Because some of them have been tied together.

Ergo:

Yeah, that’s correct. And, you know, it’s not just you know, these guys shouldn’t have been reusing addresses. I doubt that they were trying to demonize themselves. But you know, it sort of happens and it does affect kind of everyone.

Stephan Livera:

So these are some of the, I guess, design flaws that you’ve called out here in the report around Wasabi. So you’ve mentioned the peeling style peel chain the address reuse and then also the post mix spending tools, or rather the lack of post mixed spending tools. So what are you getting at there with the lack of post mix spending tools? Why is that important?

Ergo:

Yeah, so, you know to document at least a little bit of what the process was that I saw here again is you know, the, the entity mixes their coins, they get a bunch of mixed outputs and whatever the current denomination is, you know, some flavor of 0.1 0.2 0.4, et cetera. And then they’re returned a change output and that kind of same same transaction. And if the change output is paid to the same address as a mixed output, it effectively deanonymises that mixed output. You know it’s pretty simple. Then that change output will be remixed and kind of continue on and hopefully not get sucked into any more address re use. But, you know it’s technically not a cluster in sort of the formal sense, but, you know, when a change output is paid to a mixed output address, it’s basically a cluster precursor.

Ergo:

And then, you know, the cluster will sort of survive on the way out of the mixer. Just based on normal kind of post mix spending habits where people will tend to consolidate, you know a couple of mixed outputs at the same time. And so when we say, you know, kind of post mix tools how important those kinds of can be you know sort of formal post mix tool that would break that cluster, you know, would at least make that, you know, somewhat more difficult to track at least the cluster hopefully wouldn’t grow in which case it sort of does here.

Stephan Livera:

Okay. So just want to make sure I’ve understood you correctly there. So essentially what we’re talking about here is once you’ve gone through the mix, you’ve got your coins sitting on the other side, and if you don’t have the right tool set, when you’re spending out of that, you may inadvertently join the wrong pieces together. And is that also related to the concept of an input merge?

Ergo:

Yeah, it’s kind of related. So you know, an input merge sort of goes back to the traditional terminology for a cluster the common input ownership heuristic, where, you know, for the majority of you know, Bitcoin’s history you know, spends that you know, included multiple inputs can basically be assumed to be the same entity. And again, this is a heuristic. But you know, when we say, post mix spending is then merging multiple inputs on the way out of the mixer we’re then sort of formalizing that cluster by kind of the common input ownership heuristic.

Stephan Livera:

Gotcha. And you also noted here the use of multiple mixing clients with Wasabi. So what’s the implication there for users?

Ergo:

Yeah. You know we had seen sort of at least kind of two phases that might be attributable to the conspirators one in which they were running up to, you know, kind of six mixing clients at the same time. And you know the second phase, which was I think at least two. And so, you know, just sort of based on the way that Wasabi operates, their fee structure what this, you know, number one does, is it inflates everyone’s fees you know, fees are calculated proportional to the number of participants you know, or in this case, the number of mixing clients. And then, you know, so users were basically paying an inflated price for a somewhat lower quality mix, especially if then those coins are then merged on the way out and attributable all to the same entity.

²Stephan Livera:

You also note here around unequal amounts. So I guess for listeners who may not have used Wasabi the idea is if you have put in. So I think the typical, like the typical minimum amount is 0.1 BTC or 10 million sats. But if you put in more than that, it will then progressively sort of cut that down into unequal sizes. So is there a problem there in terms of unequal amounts mixing in your view?

Ergo:

When we think of mixing, you know, Wasabi was one of the first to kind of popularized the term anonymity set, you know, that’s the number of identical outputs you know, after the mix has been completed. And when we say kind of unequal mixing amounts, you know, what we’re kind of referring to is on the input side you know, an entity that’s obviously depositing, you know, a very large amount directly into the Coinjoin transaction will tend to stand out. And then you know, based on the actual unequal mixing denominations that Wasabi sort of you know, imposes a there’s a 0.1 0.2 0.4. And so on, that will double depending on, you know, the size of the inputs that are available. And what you’ll kind of see is that, you know, on the, on the higher end of those outputs those are almost always attributable to only a handful of entities on the input side. And that’s what we mean by kind of you know, the unequal mixing amounts being a problem,

Stephan Livera:

Right. I guess, put, in other words, it’s simply that there are just not that many kind of rich entities who are putting in, you know, 10 BTC inputs. And so because of that, it really dramatically reduces your actual anon set of how many people are able to deposit that kind of size in. And then that is kind of the clue or the string that you can pull on to understand, Oh, wait, this might be this, this particular entity or this conspirator, for example.

Ergo:

Yeah, that’s correct. That’s exactly what we mean.

Stephan Livera:

And also you, you mentioned here this concept of structural liquidity enforcement, so what are you getting at with that idea?

Ergo:

So there is no effectively no structural liquidity requirement to trigger a mix at least in Wasabi and I think even in JoinMarket as well. And what I mean by that is that you know, there’s, if enough people get together, the mixed will basically trigger. It doesn’t need to be new incoming liquidity into the mixer. It could basically just be recycled liquidity which will sort of transition us to kind of you know the next report you know, but the way that Wasabi at least works is there’s you know, a timer, if the timer goes off the mix triggers, regardless of whether or not there was, you know, new liquidity inbound or not. And again, you know, kind of the same sort of philosophy applies to JoinMarket.

Stephan Livera:

Yep. And I guess the other rejoinder maybe that you can remix the unmixed change, and I guess some of this is spilling over into the second report. But yeah, maybe, maybe we should discuss the second report and then discuss this general idea of unmixed change and how do we deal with it. So you’ve got this other report here called the Toxic Recall Attack. So what’s going on here? What is Toxic Recall Attack?

Ergo:

So you know, a few weeks ago we saw you know, an old Reddit post kind of get recycled for the first time in a few years. And so, you know, we dug a little bit into the Reddit post. Apparently a user claims to have had their web wallet hacked. The coins were removed from their web wallet to, you know allegedly you know, a wallet controlled by, you know, the hackers the coins, again, sat for, I think, a year and a half or so, and that eventually were mixed through JoinMarket. And so, you know, the the entity mixed two separate two separate UTXOs, one was for 45 BTC. The other one was for 400 BTC. And you know, the way that this sort of the way to kind of describe unmixed change is that, you know, on the input side of a transaction you know, JoinMarket or Wasabi will allow the user to directly deposit into kind of that directly into the mix.

Ergo:

You know, so for example, if, if we have 45 BTC entering, you know, the entering a JoinMarket mix you know, the mixed denomination is,1 BTC. You’ll the 45 BTC input, we’ll get a 44 BTC unmixed change output and a one BTC, you know, mixed output. So when we’re referring to unmixed change, we’re referring to that kind of monotonically decreasing you know, unmixed change output. And what we can kind of see is that over multiple transactions you know, that monotonic decrease will kind of continue as the unmixed change is sort of, you know, peeled through through the coin.

Stephan Livera:

And so I guess what you’re getting at here is also the use of, so in the Samourai Whirlpool model, you’re getting at this idea that the tx0, that sort of pre-mix step is what helps get rid of that problem. Right.

Ergo:

That’s correct. Yeah. I mean, that’s, that’s basically exactly what it does is it, it creates those sort of homogenous or relatively homogenous inputs. You know, at least in the tx0 model the, the pre mixers, they, they’re a little bit larger inputs than the pool denomination because they’re paying the the miner fee. It’s technically impossible to have identical inputs on the input and output side of a coinjoin transaction. Someone has to pay the minor fee, but at least, you know, with the tx0 model this this unmixed change problem is removed directly from the mix. The exchange gets kind of kept separate and, you know, in the pre-mix wallet.

Stephan Livera:

Right. And I suppose someone could put potentially the rejoinder might be something like, well, that’s more costly because you’re having to do an additional transaction. And I presume the response would be basically well stiff. That’s the only way to do this. Right?

Ergo:

Yeah. It’s you know, it’s the closest thing that we have to an ideal coin join you know, and you’ve got to wait and you’ve got to pay. Gotta pay to do it.

Stephan Livera:

Yeah. So, yeah, so you’re right. That would be, so it takes a little bit longer to do it because now you’ve got to wait for this tx0 to clear through, and then your Coinjoin, your actual Conjoin can occur. So that’s, again, that’s kind of comparing some of the different models in terms of a coinjoining. So I guess bringing it back to this JoinMarket case study, so there’s a user gridchain, so they did a Reddit post saying, Oh, look, I lost 445 BTC. I’m offering a bounty if you can track it down. And so in this story, it looks like those BTC were sitting for 1.5 years. So, I mean the common story with some of these hacks is they they’ll do the hack. And then they’ll just sit on the coins for a little while before then they try to run it through a mix. And so in this story, it looks like they tried to go through JoinMarket for their mixing, and then your analysis was essentially able to try and unwind some components of the mix and understand where did those coins end up afterwards. So can you tell us a little bit about how you, how you did that and what was the story there?

Ergo:

Yeah. you know, so we sort of described the peeling nature of unmixed exchange. You know I gave a little bit of an example and I said, you know, two separate UTXOs were mixed allegedly mixed from, you know, gridchain’s original holdings 45 BTC you know, UTXO and a 400 BTC UTXO. Now the 45 BTC, UTXO doesn’t stand out quite as much as the 400 BTC UTXO and that sort of presents problem number one you know, that’s a very obvious peel chain when you have, you know, 400 BTC on the input side you have a 1 BTC mixed output and, you know a 399 BTC change you know, this sort of becomes obvious. And I’m trying to, you know, describe a visual process, which is the transaction graph and how the 400 BTC will slowly get chipped away at over time or as mixes continue.

Ergo:

So definitely go check out the report. The visuals will absolutely help help this explanation. You know, so we followed the 400 BTC input basically across the mixer as it was slowly peeled down and mixed. And what we saw was there were you know, sort of two separate or three separate regimes of kind of mixing you know, the first where the 400 BTC input was acting as a as a maker, a market maker in JoinMarket providing liquidity. They were getting a lot of, you know, much smaller outputs, you know, in the order of 1 BTC and then a period where they began to act as the taker to try to at least based on what I could tell, try to mix their coins a little bit faster.

Ergo:

And so instead of offering liquidity, they began taking liquidity and they began taking liquidity in a very kind of very large amount you know the average mix output before and after the, well before they, as they were acting as the maker, I think was around 5 BTC or 9 BTC as they were acting as the taker it jumped to around 25. It’s just to kind of show the difference you know, in regimes there and during the taker regime there aren’t that many people that are offering that kind of liquidity. And so what we saw was the same, you know, handful of outputs that were capable of providing liquidity that the alleged thief of gridchain’s coins was demanding in the taker model. And so we saw basically the recycling of the same coins that followed along with the unexchange and that sort of introduced us into the, you know, the Toxic Recall Attack.

Stephan Livera:

Yeah. So it’s a really fascinating story. And I think it’s really, really cool analysis that you were able to do, because it sounds to me like no one else has done this up until recently. I think yourself, and I think LaurentMT also mentioned some of this stuff on when I saw some of your earlier discussion on Twitter saying, Oh, hold on a sec, this, there might be a bit more to this story than we first thought. And actually you can de-anonymize some of that.

Ergo:

Yeah. So I mean the hard assumptions here that, you know, kind of kick off the analysis are number one, I’m looking at a JoinMarket transaction, right. That may or may not be the case. There’s ways to confirm that, you know, you can go and you can check the order book, which at least is what we saw on the Reddit post users going, yeah, we confirm this, I see these mixes go by in my order book. And then, you know, kind of the next level of assumption is that I know how the mixer works and I know what it’s doing. And what I mean by that is I know how it treats unmixed change. I know how many inputs from a previous transaction it will accept into a following transaction. And you kind of also have to make the final assumption, which is that, you know, the user is only operating one mixing client.

Ergo:

And from there that sort of opens the door for the toxic recall attack which basically takes that kind of unmixed peel chain. And it says I know that the owner of the original 400 BTC input is now the owner of this unmixed change output, you know, a half dozen transactions later. And if I know that, and I know that mixed outputs from a previous mix are also sent to that unmixed change output, then I can by the process of elimination, go back a couple of transactions and eliminate, you know, the mix outputs that get sent to that unmixed change. And the logic being that the recycled outputs that follow along that unmixed change don’t belong to the entity that controls the unmixed change. And you can sort of do a process of elimination attack where you had maybe five, six, seven, eight, you know, mixed outputs, and depending on how many outputs follow along with that unmixed change even one or two or three or four transactions later, you can, you can cut down the number of possible mixed outputs from a previous mix that could be controlled by that entity.

Stephan Livera:

So it’s sort of like a process of elimination. And so I think the question would also be around remixing or in the JoinMarket model. That’s, the tumbler script that you might do multiple rounds of mixing. So how does that concept play into this does basically, basically the question is, does doing lots of rounds of tumbling, make it harder for this attack to be successful?

Ergo:

So, as you know, as long as there is a unmixed change, kind of present in the mixer, there’s a risk that this attack is possible. And again, you know, the attack, at least from, you know, this one specific case study, it ranged from, you know an anonymity set that was, you know, minus one from the original to, you know, completely de-anonymising an output. And what we saw was that at least in this case, the de-anonymized output was remixed. Even though it was a later, you know, eventually likely sent to the same destination. But you know, kind of the point to circle back to is that as long as the unmixed change is present, you know, this attack remains possible. And again, there’s a severity scale of what the attack will actually kind of accomplish. You know, but so how do we get to kind of mitigating this attack, at least in the current kind of coordinator model that JoinMarket has.

Ergo:

And, you know, number one is to, you know sort of use, I guess, the pre tumbler script, which will, instead of taking that 400 BTC input and peeling it directly through JoinMarket, will split it beforehand and make it, you know, at least a little bit less obvious. And what this will effectively do is hopefully reduce the number of unmixed change outputs that are attributable to that entity. You know, there still is unmixed change present, but instead of 400 BTC, it’s only five or one, you know, and they are only a few peeling chains each as each input is sort of mixed that will reduce, kind of the the likelihood of this attack happening. And then, you know, you get to the actual remix portion. I think the tumbler script for JoinMarket defaults to anywhere from seven to 15 remixes. And what we saw was that this entity was not remixing their coins. Well, I shouldn’t say not remixing. They were likely participating in two kind of at most, in the critical part of this attack remixes. And what remixing will do is it will just, again, further reduce the likelihood that you’re going to be affected as severely by this attack.

Stephan Livera:

Can we just walk that through one more time, just with the 400 BTC essentially you like a pre tumbler script. So what would that, what would be occurring at that stage? Like, theoretically, this is an idea, right. But what would be occurring at that stage to help reduce the possibility of the toxic Recall attack?

Ergo:

Yeah. And I think that this actually exists in JoinMarket. You know, somebody will correct me if this isn’t true, but I’m fairly certain that I’ve heard this mentioned before that, you know, something like this does exist. And I don’t know if it’s part of the actual tumbler script or it’s called something slightly different or pre mixed tumbler. But anyway, what, you know, the theory would be that before you entered the mix, you basically engage in a bunch of peeling chains that will take your 400 BTC and slowly split it, or split it across multiple transactions and whittle down from that instead of 400, you know, direct deposit into the coinjoin the 400 BTC deposit. At some point, you’ll get to some smaller output amount, let’s call it 20 BTC. And that will then eventually be sent into the mixer. And what I mean there then is that if you have only 20 BTC, then you’re sort of in this more high liquidity regime you’re less likely to have a very long peel chain it’ll be shorter and sort of the, you know, that wil mitigate some of the you know the risks of this attack.

Stephan Livera:

I see. Yeah. And so, I guess you’re also getting at this idea that, so similar to what we were saying before, how many people have 400 BTC to mix? Well, not as many as would have 20 BTC to mix. So there’s a bigger group of people who you can, because ultimately it’s about hiding in a crowd, correct?

Ergo:

Correct. Yeah. I mean, and it sort of gets to this idea of you know, how homogenous are the participants of a mix, you know, how similar are they the inputs and the outputs. And as you get sort of towards that more liquid, you know, range, you know you tend to blend better with the crowd.

Stephan Livera:

I see. Yeah. and so I guess part of this just relies on the analyst having knowledge of how the coordinator works and then sort of thinking through the implications of that, and then, you know doing this kind of analysis. And so you’re also talking about kind of understanding how the coordinator works what sort of changes, if any, could be done to how the coordinator works or to how the model works?

Ergo:

You know, and so I sort of explained that, you know, as long as the unmixed change is kind of present this attack is possible, but, you know, things can be done to mitigate that. And like we said, there’s the remixing, the you know, the premixed tumbling. But there’s also one other thing that the coordinator can do, which is to limit the number of previously seen inputs. And what I mean by that is that if we participate in a mix with five outputs and then, you know, have another mix later, only one of the mixed outputs from the first mix is allowed to go to the second mix. You know, that that will also help sort of mitigate this kind of attack. It doesn’t totally eliminate the chances of this, but it will reduce, you know, kind of the risks, again.

Stephan Livera:

As I understand of the Samourai Whirlpool model, there are certain rules in place around how the mix may take place. Right. And there’s, it’s sort of, I think there’s, I can’t remember off the top of my head, but I know TDev often tweets this out. So talking about how no previously seen that’s what you’re getting at here. Right?

Ergo:

Yep. Limited to one. You know it changes the transaction graph somewhat significantly you know, and reduces kind of the the chances of this attack. You know, there’s a couple other things that can be done. And you know, we talked about this a little bit earlier, which is liquidity enforcement. You know, and again, I keep coming back to the Whirlpool model because it’s one of the only other models that’s somewhat different from the JoinMarket and the Wasabi model and for just sort of users or listeners comparison in Whirlpool there needs to be at least two, but up to three new inputs that haven’t been mixed yet that are required to trigger a mix. And that’s what we mean by structural liquidity enforcement. Those two or three new inputs are from a fresh tx0 are from a new user who just deposited coins into the mixer. And that’s what we mean by structural liquidity enforcement is that we need to have new funds coming into the mixer in order for the mix to trigger, instead of just recycling kind of the same volume, which is what kind of led to this attack, or at least made it worse.

Stephan Livera:

Right. And another question I have on this structural liquidity enforcement, if we consider just broadly, if so in the Samourai model, for example, you need typically it’s three new mixers and two people who are already in the pool and they’re just remixing. Is there or as I understand, I think the Samourai guys have mentioned how they might occasionally switch that the other way to say, okay, we’ll allow only two new people and then three remixers. Is there some kind of implication there that it’s kind of difficult for the whole ecosystem to move through? Obviously not the whole ecosystem, not all of Bitcoin is going to move through Samourai Whirlpool, right. Obviously, but it makes it difficult for there to be mixes taking place. If you’re requiring a high number of those people to be quote unquote, new mixers, do you get what I’m trying to get at here?

Ergo:

So if you go back and you read some of the anonymity and mixer research there’s, you know, debate about the term latency, which is kind of what we’re getting at here you know, latency is, is how long you know, do you have to wait, you know, to really get the privacy that you want. And, you know, this kind of comes back to the Whirlpool model, which is that, you know, we really want to prioritize that privacy as much as possible. And that means, you know, you might have to wait for the new liquidity to come because we’ve deemed that, you know, a structural necessity for providing, you know, what we consider to be sufficient anonymity, sufficient privacy. You know, it certainly is a cost, you know, people certainly do have to wait at times.

Ergo:

You know, but when the liquidity is there the mixes trigger very quickly. So yeah, I mean, we’re not going to have all of you know, Bitcoin users shoving themselves through Whirlpool mixer anytime soon. But yeah, you know, it is a challenge for users who have kind of been trained you know, to get everything that they want kind of here and now you’re sort of dealing with this new problem that a lot of people aren’t used to, you know, they’re used to you know, picking up their phone and logging into Twitter and getting what they want kind of immediately, you know, if you throw Tor into the mix, you might have to wait a little while, wait for you know, the relays to open. And but you know, even that still very low latency compared to some of this mixing technology. And so, you know it is important. You know, because it’s not just about, you know, the time that we’re kind of used to, the minute to minute it’s about, you know how many transactions are coming in, how quickly are blocks being processed. You know, users kind of have to get used to you know, waiting a little bit,

Stephan Livera:

It’s sort of like there might be a certain population within the Bitcoin world, let’s call it 5 or 10% of them who really, who actually care about privacy. And then for those people, they’re sort of having to wait for some new, new fresh blood, if you will they’re having to wait for new coins to come in before they can actually get their mix done. But I suppose over time, there’ll be enough of a flow of people kind of moving through the mixer and then doing whatever it said they wanted to spend. And then now they want to come back through, or the other person, they spent to, they want to go through the mixer so that you sort of have to wait for that flow to come through. Right?

Ergo:

Yeah, exactly. And you know, I know Whirlpool was designed with sort of a mobile first kind of approach you know, its got you know, five participants in each mix you know, hopefully that should, you know, kind of help trigger mixes you know, a bit more quickly. But the other thing people can do is, you know a lot of people, they’re not really in a rush to spend at least not yet you know, so you can queue up your coins and, and just wait and let them mix and let it ride you know, weighted out the mixes are happening, they’re happening you know, new record liquidity kind of every month. You know, so it seems to be growing pretty organically. I at least see the number of of people, you know, looking into telegram groups, at least in my opinion, seem to be complaining a little bit less about having to wait. You know, as you know, mobile mixing has come out liquidity is definitely improved.

Stephan Livera:

Yeah, of course. And do you have any thoughts on, at what point it makes sense to switch over from having three, like enforcing three new participants in that mix versus having enforcing only two new participants in the mix? Do you have any thoughts on when is a good time to switch over for that, or is that just kind of like a subjective judgment call?

Ergo:

I don’t know how it’s configured at the moment. I’d have to ask TDev and see what’s the current requirements are. You know, I don’t get too hung up on, you know, three versus two, you know, right now, as things are sort of still developing you know, we’re still trying to observe how users are behaving how they’re interacting with the service before we kind of get some of these finer details, I guess ironed out

Stephan Livera:

Just another point that a skeptic listening might think, well, hang on, you’re part of the Samurai team, and you’re just throwing shit at the competitors. I mean, you have a motive to play up what you feel design flaws. What would you say in response to that?

Ergo:

You know, I guess first off is I think that we’ve pretty clearly demonstrated what the flaws are. You know, this has been present in the original coin joint technology for some time. You know, and I encourage users, developers and anybody else to take a look at the work that I’ve done. Peer review is certainly welcomed. Waxwing has been asking Laurent and I a couple of questions on Mastodon, and we’ve been happy to kind of walk them through our thought process. You know number one is, don’t take my word for it. I’d be happy if you go and try to invalidate the analysis, invalidate the attack that would be great. But I think it’s valid. I don’t think I’m playing up the the implications here. If you read the report, you’ll see that there’s a range.

Ergo:

It’s not the end of the world. So I don’t think that we’ve played up this attack as much as you know, maybe some people will think and, you know just to definitely reiterate the dream market team, you know, Chris Belcher and Adam Gibson, you know, they’ve done a lot for Bitcoin privacy. And they’re obviously very competent devs. And, you know, they wouldn’t have gotten involved in Bitcoin privacy if they didn’t deeply care. You know, so I think that those guys they’re certainly they’re certainly willing to take a look at some of this stuff and make the changes that they can or propose, you know, something else that hopefully will take care of some of these issues

Stephan Livera:

Also unsure if you’ve had a chance to look much into CoinSwap and whether you believe that would improve the situation?

Stephan Livera:

Yeah. And I know you were going to ask I’ve given it a read through you know that we’re still sort of at some of the conceptual kind of architecture phase but you know, it’s very exciting tech. It, you know it’s different from Coinjoin. And at least in my mind, and I don’t want to brutalize this too much, as I know Chris Belcher is in the process of sort of, you know, getting this kind of worked out. But in my mind, it sort of operates as a a non-custodial shared wallet, sort of similar to a tumbler. You can basically do whatever you want. And it will sever the transaction graph, something that’s not possible with coin join. You know, so I sort of look forward to seeing this as it gets you know, developed further.

Ergo:

One of the questions that I at least do have, and hopefully we’ll see it get addressed. And, you know as this thing gets unrolled out was you know the implication that this somehow scales better than traditional Coinjoin. From my first read of the paper, it looked like there were multiple parties taking part in multiple transactions with multisig inputs and multisig outputs. And to me that doesn’t pass the major scaling smell test. Maybe there, I’m sure someone will tell me, you know, will run me the math by me and explain how this will be better by, you know, 50% or something along those lines. But I don’t see it being you know, an order of magnitude difference between kind of a traditional Coinjoin. But, you know, as I said, you know, this is sort of a, in the conceptual phase, and I’m really looking forward to seeing how things develop.

Stephan Livera:

Right. And it could be also, well, potentially Taproot may make a difference there as well in terms of the costs in terms of chain space.

Ergo:

You got to read the, I think you’ve, I’m sure you’ve read it, but at least my interpretation was that Belsher was looking to use ECDSA multisig and not move to taproot. And I, at least from my interpretation of you know, my reading of the the proposal was that ECDSA has quote unquote higher anonymity set, you know, because right now we’re sort of starting at, you know, taproot doesn’t exist yet. And we’ll have to eventually grow into adoption and, who knows what that adoption will look like. So it sounds like he’s planning on going with ECDSA, which won’t get quite the scaling benefits.

Stephan Livera:

Of course, agreed there. And so thinking about this more broadly what are some of the implications of this recent chain analysis work for the future of Bitcoin privacy? Are we all screwed?

Ergo:

Yeah. You know, we’re at the point where the Monero maximalists will put pause on the podcast and quote tweet this and say, “Haha We told you”. you know, but, you know, privacy will kind of continue to be an uphill battle for Bitcoin and Bitcoiners. You know, every day privacy gets harder. It’s not just in Bitcoin. You know, but again, you know, we the chain is entirely transparent. You know, we can’t assume that we are the only ones that know about these flaws. And we have to have to assume that you know, chain analysis and their ilk also doing the same things. And it’s very certain that they are you know, so, you know, the things that we can do you know, basically do nothing and continue, you know, using the systems that we have dealing with some of the shortcomings and trying to do our best, or we can use the better solutions that are out there, or, you know, continue to improve as, as we sort of talked about with basically Coinswap you know, there’s things that can be done.

Ergo:

You know, certainly still here, I’m not giving up, you know, and that someone who actively does these types of analyses.

Stephan Livera:

Great. and also, I think there’s an interesting implication coming out of some of your work here where it’s sort of like exchanges kind of being used to quote unquote whitewash or bless and cleanse the so called dirty coins of large exchanges. And in some ways a skeptic of the chain surveillance companies might say, well, are they kind of selling snake oil here because they’re the ones who were meant to be catching this stuff. And their tools sets were meant to stop this sort of behavior, and yet it has happened, right?

Ergo:

Yeah. you know, as long as we still live in the real world there will be people that will need to cash out to Fiat at some point and, you know the surveillance firms you know, they like to push the concept of taint, 6102 has done some great, great infographics on team that everyone should go check out. You know, but you know, I consider taint to be, you know, snake oil. It’s a scary term that, you know, again, some of the sort of privacy maximalist types will cling on to, and say, you’re going to get tainted coins. If you use Coinjoin, or you use you know some type of, you know, some type of service. And, you know, I think that we’ve done a pretty good job of, or at least 6102 has done a good job of documenting how that’s, you know, basically a flawed concept, but, you know, kind of at the end of the day, you know, whether or not taint is kind of a flawed concept is, you know, these surveillance firms, they’re applying, you know, these, these proprietary risk scores to transactions, you know, to and from different services.

Ergo:

Regardless of the concept of taint, you know coins that come in and out of certain services are gonna get a higher subjective you know, risk score and you know, the way that they sort of you know, carry that risk across, you know, subsequent transactions is something that, you know we don’t entirely know how that’s done. You know, we can listen to, you know their webinars. We can listen to some of the information that they’re put out there and, you know, kind of keep the caveat in the back of our mind that this is, they’re not incentivized to be open about what they do. You know, this is kind of an information war where, you know, we in the open source community are at a disadvantage because all of our technology, all of the software that we use it’s accessible to anyone.

Ergo:

And, you know we’re bumping up against the kind of legacy system, which is, basically being built with this proprietary risk scoring. You know it certainly is an issue you know, what these guys are trying to do. Absolutely. I agree that they’re sort of you know, creating their own problems that they can solve. You know, it sort of seems that they’ve been hinting at kind of recently this new kind of concept of you know last known origin or last known destination where, you know, coins are basically given some type of a blessing if they come from some kind of a trusted exchange and, you know, a trusted exchange and exchange that, you know, likely works directly with whichever surveillance firm or, you know, isn’t part of whatever kind of network of surveillance firms that shares information and everywhere else has sort of given this, you know this non you know, non blessing, I guess maybe as a way to put it you know, we’ll have to see how things sort of progress from here.

Ergo:

But I mean, I’ve noticed a lot of their surveillance firm’s recent reports have been absolutely pushing KYC pretty hard you know, a lot of the themes of their, their research, you know, almost always circles back to, well, you know Local Bitcoins is bad or OTC is bad. You know, everyone needs to use a KYC exchange that we can prevent money laundering. And I don’t see that letting up anytime soon.

Stephan Livera:

Right and so listeners who are, I guess, well, first off take your unblessed coins elsewhere you pleb!

Ergo:

Yeah.

Stephan Livera:

That’s that’s kind of the mindset that we’re getting from them. And so listeners make sure if you haven’t already go back and listen to my episode with Rafael Yakobi, where we talk about some of those concepts as well. I’m also interested to get your thoughts on whether we might see, well, let’s say, okay, so the, you know, analysis is getting better and better, but also are criminals going to get better. Are they going to start using Samourai Whirlpool? And are they, you know what’s going to happen? Is it a matter of time in your view until let’s say some scammer criminal goes and uses Samourai Whirlpool to try and mix their coins?

Ergo:

Yeah, I kinda think it’s a matter of time. I mean, we’ve seen them use you know, Wasabi we’ve seen PlusToken go through Wasabi and our latest report, we talk about, you know, the conspirators or at least someone likely associated with the dark net market, you know, has been providing a lot of liquidity to Wasabi. You know, you kind of have to, look at it from at least here’s the way I look at it, which is that, you know, if Bitcoin and Coinjoins don’t provide sufficient privacy for today’s labeled criminals I worry that, you know, it won’t be able to provide, you know, the privacy that even normal people that aren’t looking to break the law, you know, in the future, the kind of privacy that they need, you know, today right now they might not be labeled as generic criminals.

Ergo:

You know, but with some of the recent turmoil that we’ve seen kind of across the world you know, the term criminal and terrorist has been getting thrown around you know, a lot, a lot more liberally than it used to where people are sort of, or government agencies are basically now sort of unilaterally deciding who is a criminal, who is not a criminal, you know, so just because, you know, right now we might consider, you know, dark net market vendors criminals you know, those people feel like they’re not getting the privacy and the censorship resistance that they need, you know, from Bitcoin, they’re ultimately gonna move somewhere else. So if those people start using or continue to use non-custodial Coinjoin services, I think that’s a good sign. It means that Bitcoin is providing the censorship resistance that they need

Stephan Livera:

Bullish on Coinjoins hey? Lastly I was also keen to ask. This is kind of unrelated, but just out of curiosity, this a crazy 1o1. So for listeners who are unfamiliar recently pre the difficulty adjustments, we had a lot of full blocks because basically blocks are coming out slower, meaning that they were a lot more full. And then the men who stare at the mempool and others who are doing chain analysis were noticing that there was this entity putting out these like really high fee consolidation transactions. And so LaurentMT was talking on Twitter and he named this entity crazy 1o1. So do you have any thoughts on that and have you had a chance to look into that?

Ergo:

Yeah, we’ve started looking into this entity a little bit you know, ziggamon had brought this to our attention. You know, as you had kind of laid out we recently had halving, we saw a significant amount of you know, hash rates sort of come offline as unprofitable miners returned off. And right around the same time we saw an entity that was you know, doing these massive consolidation transactions and paying very high fees. They were taking one of one multisig inputs and consolidating them you know, into, you know, transactions typically with three outputs and paying, you know again, a very high, very high fees. And for, you know, I think a lot of you know, your listeners will be a little bit aware of the purpose of multisig.

Ergo:

You know, I don’t really know of a purpose of a one on one multisig. I can’t think of very many reasons that that would be used you know, for anything. So, you know they sort of were creating you know, expensive transactions very expensive transactions. And, you know, over a couple of week period, it looks like they paid about a hundred BTC in miner fees, which is, you know, that today’s prices, what a million dollars you know, all from a single entity. So, you know Laurent ran a little bit of a custom algorithm to try to get a handle on a cluster of a crazy 1o1. And, you know, we’ve seen some, some links to some exchanges. Some of the typical, you know people that, typical entities that aren’t really very good stewards of the block space.

Ergo:

You know, but we’ll have to dig into it a little bit further to try to figure out, who and why this was going on. I mean, you know, it would almost seem like, you know, some type of you know, custom script that, you know, gone had gone awry, but you know, if something like that had happened, you would figure that after they realized how much they were paying in miner fees, they would have shut this thing down. But, you know, it continued for several weeks and, you know, again, a hundred BTC in mining fees from single entities is pretty crazy. You know, so we’re not quite sure to make out of it yet. It’s an interesting case that we’ll be taking a look at.

Stephan Livera:

I guess the miners are happy, right. That’s more money for the miners. So a silver lining there for the miners that is. So I guess, actually, is there anything else you’re kind of watching closely or what are you sort of looking at in terms of research?

Ergo:

You know, I keep seeing you know the Ponzi scams keep coming up from some of the mainstream chain analysis firms. I may have to do another report on Plus Token and some of the other you know, recently rediscovered scams, like Wo token you know, we saw in the CipherTrace report that was released for Q2 about a week or so ago. They had some mention of Wo token and they provided a transaction graph that, you know, was very I guess again, another term for these types of analyses that we see from the mainstream is opaque. It was basically just a transaction graph. It didn’t even say which which coin it was, you know, was Bitcoin, or was it a Ethereum? Was it something else? And they were implying that these coins were still sort of moving.

Ergo:

You know, so I keep seeing this sort of clickbait junk go by from the mainstream. So I think probably my next report will be on, you know, a little update on plus token and talk briefly about some of these other Ponzis and you know, then we’ll sort of just keep it kind of opportunistic. I mean, we didn’t expect to see the IRS come by with you know, something that we, we could kind of sink our teeth into, but, you know, as this stuff kind of comes up, we’ll we’ll be around to take a look at it.

Stephan Livera:

That’s awesome. I think you guys are doing great work. I really enjoyed reading these two reports that you put out recently and of course enjoyed discussing with you. So Ergo, where can people find you online and where can they get the report?

Ergo:

Yeah, you can check out research.oxt.me. Which is where all the reports are available. Again, check out OXT.me or our block Explorer users, normal users would would do well to take a look into some of this stuff to learn about, you know, kind of improving their own privacy. And other than that, I guess you can give me a shout on Twitter I’m around and that’s about it.

Stephan Livera:

Fantastic. Well, thank you for joining me Ergo.

Ergo:

Thank you, Stephan.
