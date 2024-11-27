---
title: What’s The Problem With Bitcoin Surveillance?
transcript_by: Stephan Livera
speakers:
  - Chris Belcher
date: 2020-04-21
media: https://stephanlivera.com/download-episode/1955/167.mp3
---
podcast: https://stephanlivera.com/episode/167/

Chris Belcher rejoins me on the show to talk about Bitcoin Surveillance companies, and what risks they present to Bitcoin. We also talk about JoinMarket fidelity bonds.
Stephan Livera:

Chris, welcome back to the show.

Chris Belcher:

Thanks for having me.

Stephan Livera:

So, Chris, I know you have been vocal recently in your criticism of Bitcoin surveillance companies. And I share your views on this. I thought it would be good to just have some discussion from the Bitcoin holder perspective. What are some of the things that we do know currently about how some of these companies operate and what are some of the threats that we might see coming from them? So perhaps we just start with a little bit on what techniques we know that they are already using.

Chris Belcher:

Right. so a big one, well, a big obvious one we know is that they analyze the blockchain. So they have, the blockchain leaks in a certain amounts of information. For example, if there’s address reuse or if there’s the common, if a transaction has more than one inputs, the strong evidence that inputs owned by the same person. That’s called the common inputs ownership Heuristic. And there’s also other, like they’re based on assumptions. Heuristics like you can try and figure out or guess which output is the change output. So analyzing the blockchain is one thing, but they don’t only do that. So this is a point I made earlier that often called things like chain analysis companies. I prefer to just call them surveillance companies because they do, a big part of their job is analyzing the blockchain, but they do other things as well.

Chris Belcher:

They analyze the peer to peer network. They might make, they probably run fake nodes. There was one that was in back in 2015 court’s running fake Bitcoin nodes. They’re trying to figure out the user’s IP addresses and with that they can also, if a node broadcasts a transaction i.e. Send the transactions that it previously didn’t receive with the fake nodes, they can possibly figure out who, who did which IP broadcast that transaction. Another thing they most likely do is run Electrum servers or other servers which serve lightweight wallets because they, the way these wallets work by default is they send all their Bitcoin addresses to the server, and the server days, what the addresses on and sends back the history. And then if your adversary running the server, then they essentially just get all your information. I’m trying to think what else they do. Well, it depends on the company of, I know we try and think of it of what they could do rather than what the specific companies do today. Cause they can always change tomorrow. But probably what they get is, when there’s, if a user gives AML KYC information, it probably ends up in the company’s database. I imagine that would be an obvious thing to track.

Stephan Livera:

And so let’s break some of those down a little bit just to spell that out for the listeners. So for example, if they are, as you mentioned, running the Electrum servers on the public servers. So in this case, the user wants to be able to easily use Electrum wallet to plug in their hardware wallet or, and if they are not running their own Electrum service such as using your Electrum personal server or electrs or ElectrumX, then they are pulling out against the public servers. And as I understand there are some, because Electrum is like a very OG software. So there’s a lot of, there are people who are just running just genuinely not surveillance Electrum servers out there. But there are also likely chain analysis and chain surveillance companies doing that as well. And as I understand, and maybe you can correct me it’s essentially like once you’ve put up like that XPUB, the Electrum server is kind of running against its own filters to kind of send you back the information that you need. So your wallet knows, okay, this is what my balance is, these are my transactions. And basically once you’ve given that up to that chain surveillance company’s server, now they know these balances are linked or these addresses are linked, right?

Chris Belcher:

Yeah. Cause they’ll see, they’ll see not just your addresses, which are used, but they’ll see addresses that haven’t been used yet. So if you receive a payment on an unused address, they will, they will have information, they may have information from the server that’s been synced before. So even if you never use a server again, they still could know about new transactions. Sorry, got sidetracked. What was the question?

Stephan Livera:

Yeah, yeah. No, that’s, that’s it. And, and also I think the other part is if you take these different pieces of information and combine them, that’s also another very insidious factor. Because for example, I think it’s colloquially known that basically when a Bitcoin exchange signs up with one of these chain surveillance companies, there’s also some form of information sharing, as you mentioned with the AML KYC. Right. And so as you were saying, we have to assume that they are using the information that they can. So, for example, if they know, okay, Stephan Livera signed up with exchange A and then that exchange and then say I do a withdrawal from that exchange to this address, then that exchange might well be passing that information. And then from that, what kind of clustering information could they do?

Chris Belcher:

Yeah, so they would know it in that situation they would know this address that you were drawn to is linked to Stephan Livera or whichever information, whichever ID they have. And when they see Bitcoins flowing from there, they can say, okay, now Stephan Livera sent to this, I know this many Bitcoins to this address and the remaining Bitcoins to this address. So they, it’s a really big starting point for them. And then with the other techniques of analyzing the blockchain, they can they could figure out, they could, for example, guess, if that was you making a payment or if it was maybe a sending to your own a different wallets or like if you’re paying many people at once or that kind of thing, they could essentially see all the flows of money around.

Stephan Livera:

It’s like a combo of different factors that will all be used to basically try and destroy an individual’s privacy. And it may also, the other thing is people have not necessarily been very good about their digital hygiene and they might share an address publicly online. And then once they’ve got that entry point into your finances, that can be the string that they pull on to go and find more about you. So let’s say a couple of years ago you were not careful and you publicly posted an address and then they could sort of trace from that point onwards and say, okay, where did all that, where did it all flow from there, right?

Chris Belcher:

Yeah, exactly. So it’s, I suppose a good analogy might be if someone’s trying to, if you’re a scientist trying to figure out how some system works, then you attack it from different angles. You say, what if I measured the temperature? What if I measured the pressure and, and all the things when you combine them together in the same way, they might combine IP, address information, blockchain information and AML KYC information all together to get as good an idea as they can of all your data, all your financial data,

Stephan Livera:

Do you know if any of these surveillance companies have been able to unmix any CoinJoins or anything like that?

Chris Belcher:

I don’t know. I wouldn’t know. I don’t talk to them or anything like that. But they may unmix, there are attacks on CoinJoins that we know. Like for example, there’s often in this, in the equal amounts CoinJoin that are implemented today in JoinMarket, Samourai Wallet, and Wasabi. There’s the CoinJoin outputs, which has equal amounts. And then there’s normally a change outputs as well. And the change output isn’t, it’s not part of the country. And just by looking at the transaction, you can deterministically link it to the inputs. So as an example, if someone had two Bitcoins as an input and then the CoinJoin output was 0.5, there would have to be 1.5 as change leftover, which could be linked. And I’ve seen with that kind of thing, you could analyze, at least that amount going forward, even if you couldn’t the CoinJoin amount.

Chris Belcher:

Now there is a thing you could do that is to have so-called sweet CoinJoins, which is if you have I don’t know, if you have two Bitcoins and you do a CoinJoin which is exactly for two Bitcoins. So there’s no change left at all. If there’s no change that attack vector can’t be used. But from what I’ve seen, it’s more likely that they the exchanges and other users of the surveillance software, they’re just block CoinJoins if they can. So that’s happened or maybe it’s not CoinJoins. It’s only happened to Wasabi as far as I know, but they’ve, there was a case a few months ago with a user of Binance got their deposit blocked because it came from wasabi. And I actually read a few weeks ago, the company Chainalysis had like an annual report, 2019 annual report, which is really interesting if you’re interested in Bitcoin privacy and actually mentioned this incident, right?

Chris Belcher:

Right at the end, like in section seven saying, Oh yeah, this happened that an exchange blocked CoinJoin. And they, I forgot the exact words, but they saw it as a positive development. I think they said it’s a good thing or we hope it continues. We hope the rest of the industry adopts it. So it seems likely that the, the technique won’t be to spy on CoinJoins, but just censor them, block them if they can. And like really if you want to use CoinJoins, I think there’s an answer to that, all you have to do is not use those exchanges. So there’s actually I’ve seen a user called a Reddit user call to cointastical who actually has a whole list of P2P exchanges. They’re the ones you know, so bisq and hodlhodl and local cryptos and loads of others I won’t list. And they, if you use them because it’s peer to peer, then there’s no one your CoinJoins can’t be blocked because they’re going straight to the person.

Stephan Livera:

That’s an interesting debate there and I, my sense of it is so far it seems like it seems like the, those wasabi cases were due to the PlusToken taint. But it could well be that in future other exchanges also start to block or flag a coinjoin user merely for using CoinJoin as well. So I guess if we were to then try and think about what are some of the risks that Bitcoin surveillance companies present to the Bitcoin ecosystem, how, what would you say about that? What risks did they present?

Chris Belcher:

Well, I guess the biggest one is just spying on everyone. Like you. People’s financial privacy is, is a big deal. Like you don’t in the fiat system you don’t, it’s not that your bank statement is open for the entire world, for all your, I don’t know, for just random members of the public to see. So that’s a really big thing is you can’t, there’s all kinds of consequences. Like he might get robbed, you might be a, what’d you call it? You might be overcharged if someone knows exactly what your income is, you might have comments or things like that. So just general privacy is nice to have and using it as a bad thing. Then there’s other things. There’s this idea of fungibility, which is for Bitcoin to be a good money every unit has to be the same as every other units.

Chris Belcher:

So I don’t know when you are, you accept payment, then you shouldn’t have to spend lots of time and energy saying, okay, what if making sure that five hops back to this didn’t come from something, you know, hacked, stolen Bitcoins or something like that. So that could be a systemic risk because we could end up in a nightmare situation where it’s only possible to accept Bitcoins if you have an account at some surveillance company. And you can only accept Bitcoins if you’ve checked that the incoming thing is fine according to the surveillance company. And that would essentially be centralization because that means you can only use Bitcoin if you’re signed up to this one or two companies. What else? So I’m just trying to to list things that like the bad consequences of the fact that Bitcoin’s privacy isn’t perfect.

Chris Belcher:

So there’s a thing that there’s no mechanism for appeal like these the analysis, especially when they’re analyzing the blockchain is based on assumptions or heuristics. And they can be wrong, but if they’ve, if they flagged your transaction, you don’t really have, you can’t appeal. Like if someone blocks you and say, Oh, I think your transaction five hops ago came from someone who stole something, you can’t, where do you appeal to? Where do you, who do you go to you, there’s nothing you can really do. And that seems just not very, I don’t know, not very moral.

Stephan Livera:

Right? Yeah. So the way at least in some of those recent cases like Ronald McHodled and a Catxolotl from there was the Binance Singapore, and I think one was a Paxos case. I think essentially the exchange compliance team would email that customer and say, Hey, we saw you were just, you know, doing a CoinJoin and it went through this address. Tell us why you were doing that, why are you using CoinJoin? And then now the customer is placed in this really awkward position of having to basically say, “no, look, I care about my privacy. I’m not doing dodgy things, but you know, we should be able to protect our privacy.” And that, that’s kind of this awkward spot. And, and as you say, it’s sort of like a black box because there’s all these things happening inside there, but it’s not like the chain surveillance company tools code is all out there and open source and people can look at it and challenge it.

Stephan Livera:

They can only just respond to the customers of the surveillance companies, which is for example, Bitcoin exchanges and the compliance department in those exchanges who is doing the email out to them saying, Oh Hey, you got flagged for doing this, CoinJoin, whatever. And I think another thing that’s interesting to point out as well is that at a protocol level, it’s not like my Bitcoin core node has a black list and says, Oh, these are dirty coins or tainted coins and these are clean coins. There’s no distinction there. Right. So if I’m running BTCPay server or if I’m just accepting a Bitcoin payment, there is no blacklisting of coins. And yet it’s like some of these surveillance companies are in quasi sense reinserting a blacklist.

Chris Belcher:

Yeah, exactly. It’s their reality. They come up with an idea of taint or an idea of a certain number of hops and none of that exists actually in the software. And the only reason they can impose the reality into us is because we use the centralized exchanges. And if people could use, not just peer to peer exchange, if you could use Bitcoin directly, if he could buy things from actual merchants that you want to, that you want to spend money on and actually use your money, then you can get around that. So then you, then it’s much harder to censor you. Really the reason their reality is so strong is because they can censor Bitcoin users by blocking their transactions.

Stephan Livera:

Yeah. Although I think it’s one of those things where for some time people will just be struggling to reconcile the fiat money world with the Bitcoin world. And it’s the hard reality is that a lot of these companies are subject to government regulation and if they want to provide a vehicle for people to put their fiat into to try and buy Bitcoin with it and so on, then they’ve got to be subject to these KYC and AML laws and sanctions laws and all the rest of it. And I think the other point the bears in mind is again, from one of my recent interviews with Rafael Yakobi, where he was basically making the point that it’s not really clear that the law specifies that you must use a surveillance company to be in compliance. It’s kind of, there’s this sense of, as you know, to use the joke or the terminology that he said, it was almost like we pretend to do the work and they pretend to pay us. And so in your view, is it, is it that there’s a kind of “fake it till you make it” aspect here, they’re trying to make this into the inaudible standard that every exchange theoretically has to use some kind of surveillance company? Is that what you’re saying?

Chris Belcher:

Yeah. Yeah, that sounds right. And there’s that point that you you don’t necessarily, you could probably stop money laundering and the other things that the government is interested in without doing the mass surveillance on every single person, even if they’re just using Bitcoin for other things like buying an anonymous VPN. So maybe there is, I mean, I’m not a lawyer or anything like that, but maybe there’s some way you can have a win win where governments really can stop money laundering, but also Bitcoin users can get privacy that they, want, that is, that exists in other financial systems as well. And yeah, definitely the surveillance companies, they have a strong incentive to make themselves out that they are, that the only way you can obey the law is to get an account with them and pay them all their fees.

Chris Belcher:

So, so, yeah. Yeah, I agree with you. Maybe it could be more, we could be more, maybe the community could somehow make it more known how flawed some of these heuristics are. So just today or yesterday, the BTC pays implemented release the version which implemented PayJoin, which is a kind of CoinJoin that’s invisible. It can’t be, it looks exactly the same as any other regular transaction, but it’s actually a CoinJoin. So if they, I mean, they could already be very popular because they’re invisible. We don’t know. But if it was more known that the surveillance companies heuristics are actually flawed or can be flawed, then maybe people would, would realize that they don’t need them and they could maybe follow the law in another way.

Stephan Livera:

The other thing as well in terms of how we think about these surveillance companies, right? It’s not like the way I’m thinking of it is not like, Oh yeah, everyone’s just going to shout them down and they’re going to leave. You know, it’s not like that. It’s more like accepting that as long as it’s possible, somebody will try to exploit that sort of regulatory window to try and make a profitable business out of this. So really the actual response just needs to be more like understand that they’re not your friends. Right. And take actions that will ideally cut against those heuristics to make it at least less feasible and less certain that these coins are owned by X , Y, and Z person. Because, you know, they’ve been, they’re actually the result from a PayJoin or they’re actually coming out of a CoinJoin, et cetera.

Chris Belcher:

Yeah, that’s right. And it’s not just, so we, me and you are focusing a lot on the companies that exist in the kind of America, Europe, Australia sphere. But they’d also like you can imagine North Korea building their own software, like just regular that they get some people to write it or China that has nothing to do with our chain analysis equivalents and the companies we know. But just they analyze the blockchain as well. So yeah, the long term or even short term medium plan has to be to make these companies and make this analysis impossible. Cause yeah, you won’t win by like trying to convince them. Right.

Stephan Livera:

That is also a good point as well to touch on because you may see different regimes with different definitions of who is a terrorist and who is a quote unquote bad person who you’re not allowed to do business with. And so then you end up with this weird scenario where depending on which surveillance company you are subscribed with or which, you’d have different lists based on different countries as well. So that to me seems like a very odd scenario that that’s kind of they implied outcome of, Oh yeah, everyone’s gonna use surveillance companies. Right? What would you say on that?

Chris Belcher:

Yeah, yeah. It goes against the idea of the ideal of Bitcoin as permissionless, as borderless as all these other things that we like Bitcoin for that actually you’d be reimposing these political borders back in that a Bitcoin in China would actually be different from a Bitcoin in Europe or America.

Stephan Livera:

And another point I’ve seen you make as well is around the ability of some of these companies potentially. We don’t know yet to exert influence to block a protocol upgrade. So can you tell us a little bit about that? How might that play out?

Chris Belcher:

Oh yeah. So that was that kind of happened. I mean it’s hard to tell, but they, back in when SegWit was being activated, there was the big politics, a big movement around the UASF. So SegWit was an important update that was necessary for lightning and loads of other great ideas to be implemented into Bitcoin. But a coalition, so a bunch of miners and some other people really didn’t want it to happen. They were the tried to stall it in other ways and then the Bitcoin community did this user activity softball, which made it work. And one of the, it seems one of the people who were against SegWit was, I remember there was a guy called Jeff Garzik and it seemed he had a transaction surveillance company, which I think was called Bloq spelled with Q or something like that.

Chris Belcher:

I’d have to check. And they, he was on record saying, Oh yeah, the blockchains are really great. It’s a really big data set. We’re analyze it, we’ll get loads of information, it’ll be wonderful. And he really didn’t like the idea of lightning because it removes all the information. It means they cannot analyze it because the information is all off chain. And he was a big player in trying to stop SegWit from happening. So in that sense inaudible that kind of already happened, but they, these misaligned incentives made people try to oppose updates that would improve Bitcoin as for how that would happen in the future. I guess the same kind of thing. They’d try to use some kind of political influence to stop it happening.

Stephan Livera:

Yeah. So putting that into real world example, I mean, again, we’re kind of hypothetical. We don’t know exactly how it plays out, but hypothetically, let’s say we get the Schnorr taproot soft fork, let’s say later this year or sometime next year perhaps. And then the, you know, one of the next ones in line that everyone in the community would really is quite excited about is the cross input signature aggregation, soft fork or improvement that, you know, again, that’s, it’s still to come. But that is one of those benefits that would really incentivize a lot of CoinJoin usage because it would then be cheaper to do to use that kind of transaction spend. And so potentially at that point there could be pressure to try and block that upgrade would you say?

Chris Belcher:

Yeah. Yeah. And even Schnorr has all those other privacy improvements for lightning and those kinds of things. So you can imagine people opposing it on that point of view. Although I don’t think it would succeed cause we already saw with the UASF for SegWit that ultimately all the objections didn’t matter. And the most important thing was full nodes and what, what users who able to run their full nodes what they wanted and everyone else, all the miners, all the exchanges and that they have to fall into line eventually. So they can try, they might, they might try kind of fake news thing and like have loads of bots on Twitter and Reddit that spread false information. But apart from that, in theory the update should happen.

Stephan Livera:

Yeah, that’s a good point as well around lightning and so on. Although lightning has its own kettle of fish as well because that can be, that can be other ways of potentially surveilling that.

Chris Belcher:

Yeah. I fully expect that as lightning gets more popular and adopted, I fully expect these surveillance companies to also start analyzing lightning. So maybe they’d run their own fake lightning nodes and try and get you to open channels with them or, or something like that. I don’t know. I don’t want to give them ideas, but yeah, that’ll be, that’s in their purview.

Stephan Livera:

Yeah, that’s right. And so we might see that occur as well if lightning, you know, as lightning grows. And so I think it’s also worthwhile pointing out some of the common practices today that are reducing the privacy of Bitcoin users today. So for example, there is a lot of address reuse. So that’s one example I can, I can think of already where exchanges are commonly just reusing addresses and then that allows much easier tagging of the cold wallet cluster. So exchanges typically have a hot wallet and a cold wallet. And then typically there’s a whole bunch of people who are out there just trying to tag different addresses and saying, Oh yeah, I think this is the, let’s say Bitfinex cluster and this is the Bitstamp cluster. And so on and then then they can sort of try and trace it on the way out as well. So do you have any views on that practice and whether, if you know, that’s another thing that can be agitated for by the Bitcoin community around stopping address reuse as a practice or in your view, would that be not very effective anyway because people would still be able to tag things and so on?

Chris Belcher:

Well, yeah. Well I think it would be, it’s worth a go. Every improvement helps. Even if you, if you can improve a small amount, it’s still a big part of the, of the, you know, the ingredients that make the pie of Bitcoin privacy. But this exchange thing is actually a great example of how it’s not just, it’s not just a Chainalysis companies like doing AML that are, that we have to fear. So you can, I think there’s a common example of there’s a trader who wants to, he thinks the Bitcoin price is going to go down. So he goes, he sends money to an exchange and he has to wait for three confirmations before he can press sell. To get into his trading position. But what happened is if he’s, reusing addresses or if, people can figure out the, his transactions have been sent to the exchange, they’re going to front run him.

Chris Belcher:

So they’re going to say, “okay, look, loads of money just load the Bitcoin just went through this exchange. Someone’s clearly going to sell why don’t I open my position first”. So then what will happen is this trader is going to find the price has gone down already. He’s going front run and he won’t be able to make money from his, his trade. And so that, that’s like a direct financial benefit for having good privacy practices. And it’s, it’s really like part today cause I’ve seen loads of exchanges. They only allow you to make a new address every month or, something like that. I think there’s even BitMex actually uses vanity addresses, so they, so like it’s really, really obvious that this address belongs to BitMex.

Stephan Livera:

Right. And I think that’s also one of the potential benefits there for these people who are doing large volume that they might use Liquid and then Liquid has confidential transactions and so on. And so another practice it, that’s recently as you mentioned, BTCPay Server have got PayJoin support now or pay to endpoint depending which terminology we’re using. So I know you and I believe, I think waxwing might’ve also commented on this as well. I think you were saying it doesn’t take a lot of people using PayJoin the common input ownership heuristic really starts to break down because this breaks that.

Chris Belcher:

Yeah, that’s right. So these PayJoin they’re kind of CoinJoin, so they break their common ownership Heuristic, but they do it in an invisible way. So PayJoins look the same as regular transactions. So if there’s anyone analyzing the blockchain, they can’t exclude them from their analysis. They have to, if they’re following the algorithm to cluster together wallets using this common input heuristic, then they’ll in theory get a huge big cluster that contains the service plus all its users.

Stephan Livera:

And as I understand, and I might’ve slightly misrepresented this in the past, whereas I was saying PayJoin, you generally don’t know that they are a PayJoin. Right? But is that, it might theoretically be in some cases you actually can tell whether it is a PayJoin. Is that true?

Chris Belcher:

Yeah. So there’s some attacks. So for example, it looks a bit like this. Suppose you had inputs which are say they’re 5 BTC, 2 BTC and 1 BTC and you want to make a transaction, which is 4 or 6 BTC. You will have to take your input for 5 or 1and use them together. And if you had if you had a PayJoin, kind of the amount you wanted to send, determine the inputs you have to use. So if you in, if you took the same inputs again, 5, 2 and 1. If you only wanted to send a transaction for 0.5, but then you used all your inputs, used 5 , 2 and 1 together, then that might be a bit unusual because what happened there, your wallet was spending more block space when it could have just been 1 input it could have just spent the 1 which was 1 BTC and there’s attacks there with PayJoin because if you, it can happen, if you look carefully at the amounts you end up in that situation, the analyst could suspect something’s a bit wrong because the amounts are a bit unusual so that maybe the wallet used, it looks like the wallet used more amounts than it needed to, in a way.

Stephan Livera:

I see. Yeah. I believe you’ve called that the unnecessary input heuristic, right? Yeah.

Chris Belcher:

That’s right. The unnecessary input heuristic. Well on the other hand, there’s some wallets which do this anyway. So some wallets want to consolidate their inputs and especially if demand for block space is low, they might use more inputs than they need to just to consolidate them. So it’s another Heuristic as well. Like it might work in some cases, but it could also be this other thing which is completely innocent.

Stephan Livera:

The other cool thing with PayJoin as I understand is that it actually from a network perspective is more efficient in terms of chain space usage because you’re actually using less UTXOs or pieces of Bitcoin. And so as I understand, so for example, the BTCPay Server merchant who enables PayJoin, they would get sort of this like a snowball accumulating piece. I think Waxwing has spoken on this idea. So could you just comment on that? Is that what’s the what’s the relevance of that? How do we see, will we see improved chain efficiency by more people doing PayJoin?

Chris Belcher:

I’m actually, I’m not that, I’m not sure about that. So without PayJoin what you’d have is from the point of view of the merchant every incoming transaction will be one input, which they can, they’re most likely to get them in. So we know demand for the block, demand for block space has a cyclical pattern. So demand’s really high in the daytime, like when it’s daytime in Europe, America. And then demand is very low at night time or other weekends. So normally what merchants do is they get inputs, they get these payments and they do nothing until Sunday nights or that kind of time. And then they consolidate them all into one. So when you have a PayJoin, instead of having every payment being new UTXO, or new input, you have one or let’s say one input which just gets bigger and bigger, it has a, has more BTC value each time you get a payment. So what’s happening today in terms of a block space is the consolidation that used to happen on Sunday night when demand was low. Now happens in the daytime on a weekday when demand is relatively high. So, I’m not actually sure that it saves block space like, but it’s not terrible. It might use a tiny bit more because the demand has shifted around in time, but it’s I don’t know that they, I don’t think it makes it cheaper.

Stephan Livera:

Are you making the argument there that the byte would be lower? The bytes? Literally the bytesize of the transaction is lower but you’d be paying more sats per byte for that transaction because it’s during the peak time. As opposed to the off peak time?

Chris Belcher:

No, I think the bytes is slightly higher. Because these consolidation transactions, the ones that happen on the Sunday night they’re normally very big. They have like a hundred or 200 inputs or going to one output and then then all the cost is because it’s one big transaction. The cost, there’s amortisation savings. And with these PayJoins, they’re quite small. Each individual transaction pays for things like the lock time bytes and the n sequence values. And what else? Some bytes which are constant for each transaction, which to be fair is a very small effect, but I mean this is obviously hard. This is like talking about economics in a way. You don’t really know for sure until you actually try out. And even if they are a little bit more expensive, I still think people will do them because privacy is quite valuable. Like people, if people didn’t want privacy, they might use PayPal instead of Bitcoin.

Stephan Livera:

And another thing on this PayJoin question is the holistic aspect of it, right? So it might be one thing for the merchant to use, PayJoins but then is that merchant then doxing in some other way when they merge those inputs, like for example, that merchant might have a hot wallet cluster inside their BTCPay server or whatever other thing they’re using. And then they’ve now got to spend that out into the cold storage or, right. They might be periodically flushing that out into their cold storage or they might be paying their suppliers. Are there impacts there that you can see that well they have to sort of holistically also do CoinJoins on the way out of that receipt of all those PayJoins, if you understand what I’m asking?

Chris Belcher:

Yeah, I know what you mean. It’s the same if you didn’t use PayJoin. So if anyone sends you a transaction with or without and they know one of your Bitcoin transactions and they can later watch where that goes and they could see it goes to your supplier or something like that. So PayJoin doesn’t change it in that situation. So really the important thing about the threat, more different threat models and what PayJoin and actually does. So the way I like to explain it is Payjoin is a customer and a merchant together protecting both their privacy and their threat is a third party who analyzes the blockchain. So within a PayJoin the merchant doesn’t get privacy from the customer and the customer doesn’t get privacy from the merchant. So they both know, for example, the amount being spent and PayJoin, doing stops the third party viewing them. So that means from the merchant’s point of view, if their customer is a threat then PayJoin, doesn’t help them and yes, then they have to do a regular CoinJoin when they go and pay a supplier for example.

Stephan Livera:

Yup. So essentially then it means they need to just think about doing CoinJoins after receiving all of that before spending out into their cold storage cluster or spending to their supplier or whatever, depending on how much of a threat they view that as.

Chris Belcher:

Yeah. But then yes, that’s right. And there’s also this effect that if PayJoin becomes so popular that the common ownership heuristic is essentially broken, then they can maybe get away with not using CoinJoin because it’d be hard for any adversary to make any assumptions at all about the blockchain.

Stephan Livera:

Yeah, that’s a good point also because the whole point is to break the heuristic and then once the heuristic has been broken, then you can now sort of play with that a bit. And use on the other side and actually use that make use of that factor rather.

Chris Belcher:

Yeah, there’s two points that it’s, one effect is generally like a positive externality, breaking the heuristic for everyone, for all Bitcoin users. And another effects is improving privacy of the customer and the merchant. Those two things are separate and they, I’d imagine that at the beginning the improving the privacy of the customer much and will be why people do it. And as a nice side effect, everyone will gain privacy because this heuristic will be broken.

Stephan Livera:

Fantastic. Let’s talk a little bit about one angle of criticism that occasionally Bitcoin people will receive. And that is typically from the ‘just use Monero’ crowd. Now I want to talk a little bit about why, whether or not you believe that’s a good answer. And so there are different concerns that you could raise about the use of Monero. I think, I guess just high level, I could summarize a few of them, right? So you might have a concern around the scalability. Monero is commonly hard forking. There is kind of that still that need to pass through from a liquidity point of view as well around how many people are actually using Monero. And then also how do you actually get into and out of Monero because you don’t, if you don’t necessarily want to store your value inside Monero that’s a factor as well. But yeah, could you just give us your high level thoughts is that, you know, the quote unquote just use Monero is that an answer?

Chris Belcher:

Yeah, no, I agree with you. So the, for me, scalability is a really big thing there that Monero uses. It’s less scalable and okay, well why do we care about scalability? We care about scalability because that’s decentralization that gives us security. Scalability means that the full nodes have to use, they have to have much more processing power than an equivalent Bitcoin full node. So for example, Monero can’t be pruned in the same way that Bitcoin can. So Monero has an ever growing list of all transaction outputs and it doesn’t know when they’ve been spent. So it can’t delete them in the way that Bitcoin does, which means disk space gets bigger, much quicker than in the Bitcoin case. Another way that scalability is hurt is the cryptography used. So they have the confidential transactions and bulletproofs and all that kind of thing and ring signatures.

Chris Belcher:

And I remember Greg Maxwell, I remember him commenting that if he did the calculations for if you scaled up Monero to have the same number of transactions per seconds as Bitcoin, then a Monero full node could not run on regular hardware, it could only run on like really beefy servers. And that’s directly because of all the extra CPU and that kind of thing being used. So the, the kind of, the analogy, not the analogy, but like the concrete sort of argument I like to use is, okay, if you want more privacy, why don’t you use DigiCash? So for people that don’t know, DigiCash was this digital cash starts up from the 90s, and it was a company and it’s implemented a Chaumian e-cash. And that’s this privacy protocol that’s been known for decades. And it has complete, it has perfect privacy information theoretic privacy.

Chris Belcher:

So it means even if you had an infinitely powerful computer, you could not break that privacy. So what doesn’t it exist today? Well, it doesn’t exist because it was centralized. So the company like went bankrupt one day and the whole thing shut down. So you can’t tell people to go use DigiCash cause it had no security, it wasn’t decentralized enough. And when people say, Oh we should use Monero, I kind of see it in the same way that they’re trading away security in order to get some privacy. And I think that’s a really bad trade off that maybe it’s a bit ironic that I mostly work on privacy, but I think Bitcoin security is way more important in that sense. Cause once you have Bitcoin that exists, that can resist attack, then you can build privacy on top. You can build it into the system more. Well, if you’ve started a system that already has poor security, you can’t really ever fix that, like security should be the top priority.

Stephan Livera:

And it’s also fair to point out that Monero does often hard fork. What risks do you see with a protocol that often hard folks?

Chris Belcher:

Yeah, that’s right. A heartful, well hard forking is essentially, it’s it’s centralizing around developers. So there’s a bunch of developers on the guitar or however they organize and they say, okay, we should have just hard fork. We’re gonna do it. And a few weeks or months or whatever and everyone, the entire economy’s just going to swap over. And that means the whole Monero ecosystem has to follow. Their github past to make sure that, you know, checked out, deploy the code and that kind of thing. And that, that also isn’t scalable. I know in Bitcoin there’s lots of Spanish speaking users who don’t speak English. And that kind of thing would never work for them. They’d have to if you want, like the whole point of money is so people can treat it across different languages. And so it can be permissionless and all around the world. And if you actually centralise on one github, around one group of developers that goes against that.

Stephan Livera:

And the, I believe the, so I don’t know the detail, but as I understand, I think the Monero crew, the Monero people basically have a different philosophy around ASIC resistance as well. So it might be that potentially it leads to a less secure network against a more well funded attacker. What’s your view on that?

Chris Belcher:

There’s I haven’t done much research on this, but I’ve, I remember a great PDF written quite a few years ago now called something, I think it was just called ASICs.pdf. I can, I can link it to you to have in the show notes. But it was, it made the argument that what you really want in ASIC to them be simple enough that anyone could produce them. Not anyone, but like anyone with enough technical skill cause produced them. And what can happen with you if you’re constantly hard forking, to get a new proof of work algorithm. Then you’d be, you make it harder and harder to make an ASIC and then that increases. That means you like anyone who wants to make an ASIC have to have, they to have more startup capital costs than it would. It’s essentially another way of centralization. It means only the most well capitalized funds can make an ASIC. And ideally you at least what we hope in Bitcoin, I think we’re moving towards that is that ASICs become, the knowledge of how to make a Bitcoin ASIC becomes spread far and wide and many, many people know how to make one and that ultimately secures our the centralization of mining.

Stephan Livera:

And also it’s worthwhile. We’re talking about, well when we’re talking about privacy, a common concept here is the one of anonymity set. And when a person is trying to get into and out of Monero, they still have to find a way to do that. And that still requires people going across a liquidity set if that makes sense. Like they might have buy it Monero on some exchange or they might need to use perhaps one of those swap services as well. So do you have any comments there in terms of comparative analysis there of Bitcoin and Monero from a, you know, anonymity set of the liquidity analysis?

Chris Belcher:

Yeah, that’s right. So I think Monero has, I think it was 50 times less or a hundred times less. I should, I should check the numbers, but it’s that kind of, let’s say a hundred times less transactions per second than Bitcoin. And when you’re checking this, you should check, cause Monero blocks have a different interval to Bitcoin blocks. But if you compare like for like then whenever it has way fewer transactions than Bitcoin and that means you have anyone who wants privacy has less of a crowd that they’re hiding in. And that comes back to the point I was making about scalability and security and that Monero can’t really increased their transactions per second because they’re full nodes that resource cost is much higher because those transactions, although all have to be verified by people, CPU’s. And then that isn’t scalable.

Stephan Livera:

Another point that is worthwhile discussing is what are the dark net markets using? So as I understand it’s still mostly Bitcoin. But I hear rumours is that there are some that are switching to try and use Monero or I think in practice they use a combo of both. But I think there are some, or one at least that came out going only Monero now in the spirit of intellectual honesty and so on. We, we can’t just deny that. Right. That is a fact. And it’s sort of like, is that a competitor to Bitcoin from a privacy perspective? And how are you thinking about that point?

Chris Belcher:

Oh I think I might be the wrong person to ask, but I don’t know too much about the details of dark net markets and like the ecosystem. I’d guess it will be interesting to see which if there’s a market which uses both, it might be interesting. Maybe someone could ask the vendors or something like that. How much volume do they get for Bitcoin and how much do they get from Monero? I’d like to see how much, because there’s a big difference between offering something offering to accept this coin and people actually using that coin.

Stephan Livera:

Right. And it’s, I mean there’s so many different factors that could go into there because it could be that it’s denominated in something in one currency, but the actual payment rail used is Monero or something else. So that’s another factor to consider we have to also think about like which one is likely to be the economic winner, right? Like Bitcoin with its kind of certain culture and so on of everyone being so set on the limit of 21 million and being so focused on that and focused on, as you mentioned, the broader security element of having enough people being able to run it versus say Monero which is in a more narrow sense, more private but potentially less secure in a macro global sense.

Chris Belcher:

Yeah, exactly. There’s that network network effect thing that that people like if someone, I don’t know from the point of your developer, if they want to make a difference, then they’re going to go for the biggest, most used currency, which we Bitcoin like I know for my kind of privacy research, I’ve always been focused on Bitcoin because that can, it seems like it’s the most scalable and the most secure. And you can make the most difference from that. And I imagine it’s like if there’s a vendor who wants to accept the cryptocurrency, they’ll go for the one which has the most users. And so yeah, so network effects will always be a big advantage to the Bitcoin into the most dominant currency.

Stephan Livera:

Right. And I mean, I guess I can imagine a parallel world. So let’s say you know, a couple of years ago Roger Ver was going on about, Oh my God, the Bitcoin dominance is dropping, right? And he was saying, Oh look, people are using altcoins. We need to blah, blah, blah. And that was part of the argument. And I was like, Oh, this is why we need to have big blocks and scale on chain and so on.

Chris Belcher:

Yeah, well that dominance, that Bitcoin dominance metric is completely like, it’s fake. It can easily be manipulated. So I mean it’s based on market capitalizations and you can very easily fake that. Like I could make an alt coin now call that Chris coin and have 1 trillion units and then I sell one of those units to you for $1 and they’re no, look, I’ve got a coin at $1 trillion market cap. Look how great I am. Bitcoin’s dominance is 0 or 0.1 so really you’re not, that’s not the thing. You should be looking at adoption. How many people use it. How many, not just how many transactions there are, but what the demand for block spaces. So it’s easy to get loads of transactions if they’re all free. But what we see the Bitcoin is there’s transactions which actually pay a significant miner fee, which means Bitcoin really brings value to people. Like they’re willing to pay this, which means they find it useful.

Stephan Livera:

Right? And so it comes down to ultimately what are people willing to pay for. And so I guess the point I’m getting at there, obviously I’m not a proponent of on-chain scaling or Monero but I could imagine a parallel world where someone tries to make that argument of, Oh look, Monero use in dark net markets is rising, therefore, you know, Bitcoin needs to do this, that, and the other to do privacy. Right. You could imagine that parallel?

Chris Belcher:

Yeah. You know, I can understand that. And I think Bitcoin will get there. There’s lots of privacy ideas like this PayJoin thing we were talking about. And there’s a few things like coin swaps and coinjoinXT and loads of other, we have loads of ideas of how to improve the whole thing without completely creating a whole new currency like Monera and even with lightning. So all these things, all blockchains have the scalability problems and we have lightning as a big step forward for that. So you could imagine even Monero could say, okay, we like, we’re not very scalable, we’ll just adopt lightning and that would be private. But really you lightning on Monero would have the same kind of privacy as lightning on Bitcoin. So you may as well just use lightning on Bitcoin if you want a scalable payment rail that’s really private.

Stephan Livera:

Going back to just the PayJoin aspect and I coming to the question of adoption and use of it. So it sounds like obviously the BTCPay Server of a inbuilt wallet obviously has PayJoin support now or Pay to endpoint support and the Blockstream guys were mentioning that it will be coming to Blockstream green, which is a smartphone, Bitcoin wallet. I believe BlueWallet are looking to adopt it also. So Chris, what’s your view on their Bitcoin ecosystems adoption of pay to endpoint? Do you see that happening and becoming the standard or what’s your view there?

Chris Belcher:

Yeah, I hope it does. I mean this stuff has, it’s another network effect argument that this stuff has value in every wallet and every service can adopt it. Like it can send and receive these transactions. So I hope they do. And, if you know, like a message to your listeners if your wallet doesn’t in six months or yeah, if your wallet doesn’t adopt this kind of PayJoin and you can’t pay people on BTCPay Server, then just get another wallet. One which does. Yup. So if people want it, it will be adopted I reckon.

Stephan Livera:

And also your thoughts on competing standards because it may, I guess it’s one of those things where Samourai wallet as you know, have Stowaway which is their version of PayJoin basically. And it’s at this point, it’s not looking like they will be necessarily compatible with the BTCPay Server to endpoint version. And so do you have any thoughts on that and whether it’s better to see sort of competing visions of how to do a PayJoin?

Chris Belcher:

Yeah. Well, they’re slightly, they’re slightly different. The two things, right? So Samourai Wallet’s one, okay so BTC Pay Server’s one, there’s actually a connection between like a TCP connection between the customer and the merchant. And over this connection, they send information back and forth and Samourai Wallet, so obviously that doesn’t work if you’re paying someone who has another smartphone, then you can’t connect directly to them like that. That’s much harder. So the Samourai Wallet one’s work is it has QR codes and the two, if you’re paying another Samourai Wallet user and you get, I think you get the two phones together and they show each other the QR codes and that’s the way of transferring information across to make PayJoin. So if you think about it, they work in different cases.

Chris Belcher:

This BTCPay Server one works when it’s merchants which have, they’re always on, they have a website, you can always connect to them. They’re not behind a firewall or anything like that. And Samourai Wallet’s one is, it seems to be designed for two different smartphones. So, for example, if you’re trading Bitcoins for cash, like in a physical meetup so they don’t actually, they don’t contradict that much. Like they’re for different uses. So I could imagine in the future that Samourai implements both this the one for paying, if you’re paying a BTCPay server and they keep them on with the QR codes and they’re both PayJoins.

Stephan Livera:

From a JoinMarket perspective, if you want to do PayJoin, would the JoinMarket version be compatible or would you be looking to make it compatible with the BTCPay Server Pay to endpoint?

Chris Belcher:

It’s not compatible today, but it’ll be definitely a good idea to make it compatible like to implement it so you can pay this kind of the protocol, that BTCPay Server uses. So if there was a PR open for that, I’d gladly review it and test it. I don’t have much time these days to do that, but yeah, it’ll be good if it was done. I’ve got nothing against it, let’s put it that way.

Stephan Livera:

Fantastic. So look, let’s talk a bit about JoinMarket then. So obviously you are the JoinMarket OG I know you have been discussing and working on this concept of fidelity bonds. So what is a fidelity bond and what’s it used for?

Chris Belcher:

So fidelity bond is a, generally speaking. It’s a way that someone can sacrifice value in a way that can be proved to a third party. So for example there, these are ideas going back here. As you could imagine if there’s an internet forum and it’s got loads of spammers there’s people going on posting as a spam essentially. So one way to stop the spam is to add some kind of cost. And you can do this anonymously without requiring any ID if you use Bitcoin. So like one way to use fidelity bonds here, you would require each new account to sacrifice some Bitcoin, like sends, I don’t know whatever, 0.00001 to a burner address. And that’s associated with that account. And that means if you’ve, your forum can’t be spammed, because the spammer would have to be burning loads of Bitcoin, but regular people, they still don’t need to sacrifice a small amount to get access to the forum that they’re doing. So in general, these fidelity bonds can be useful as a way of stopping the Sybil attacks or all that goes. For example,spamming forums and they are they, the crucial part is there a sacrifice which can be proved. So it’s a lot like proof of work for Bitcoin. If you have a proof of work hash, you can prove it to someone like to anyone essentially they can check it and they can, you can really prove that like this much hash power has been put into making this proof.

Stephan Livera:

Awesome. And so can you shed a little light for us on how fidelity bonds would work in JoinMarket?

Chris Belcher:

Yeah, so JoinMarket has this liquidity market where there’s market takers, we call them, who wants to make a CoinJoin right now. And they pay a small CoinJoin fee on the other side. There’s market makers and they’re willing to make a CoinJoin whenever and in return they earn this CoinJoin fee. So the way for those who bonds would work is that we’d code a routine and the taker, which means it would preferentially choose makers who have more valuable fidelity bonds, which means that there’ll be a market pressure for makers to have fidelity bonds and add it to their bot. So their bot would as well as announcing how much CoinJoins there, like they’re willing to make and what their fee is. They’d also amount, they also announced this proof. So let’s say for example, it will have a UTXO.

Chris Belcher:

So which is a time locked Bitcoin which can, I don’t know, it’s locked for six months and it’s worth, I don’t know, 0.1 Bitcoin. And then the taker would from that, calculate the value of the fidelity bond and say, okay, this both sacrificed a lot, this sacrificed like nothing. I’m going to go with the bot that sacrificed a lot. And the effect there would be that in the same way it will be much harder to Sybil attack JoinMarket would mean if someone wants to make lots of fake bots and JoinMarket to try and be all the makers at once, it would cost them a lot of money.

Stephan Livera:

So help me understand here. Is it sort of like your locking it, you’re time locking your own Bitcoin and you’re sort of proving to other people, Hey look, I’ve locked up a lot of Bitcoin and I actually can’t use it for this six months or forever, however long you’ve done the time locking and then you would still get it back. But then you might recommit to that again because you want to keep being a JoinMarket maker. Is that, am I understanding you correctly though?

Chris Belcher:

Yeah, exactly. So that’s a, there’s two ways that I know of to make, to make this kind of sacrifice. So one way is just to burn the Bitcoins, to send them to an unspendable address. And then the sacrifice is, like if you’ve sent like one Bitcoin to, if you’ve burned one Bitcoin, your sacrifice is one bitcoin another way is to look, you can use the OP code, Check Lock Time Verify and lock the Bitcoins for some time in the future. And then your sacrifices, a time value of money cause you’d get the Bitcoins back at the end, but you wouldn’t get them today. You’d get them in six months or a year whenever. And I’d expect in practice people would be doing this by time locking their Bitcoins.

Stephan Livera:

Awesome. So in terms of fidelity bonds in JoinMarket, how far along is the idea? Have you already like started coding for it or is this like a concept?

Chris Belcher:

I’m making, so right now, today I’m working on the wallet, like the JoinMarket wallet, which can support these time locked addresses and also burner like burner outputs. I’m coding that. Cause it’s there’s lots of, there’s economic reasoning as well. That be really cool to see how this works in practice. Like it’s an experiment as well as like as well as making it work.

Stephan Livera:

You were touching on this earlier, is there a way to quantify the Sybil resistance provided by people doing fidelity bonds in JoinMarket?

Chris Belcher:

Yeah, that’s a really important part of it. So we know in Satoshi’s white paper there’s a whole section on on how you would attack this, this mining proof of work thing and essentially comes up with a 51% attack there that if you have like hash power bigger than everyone else in the entire network, you can make, you can do a SYbil attack. The way you do it in a, in these fidelity bonds is so a really crucial part of the argument is that the value of the bonds is, I’ve called it V Squared. So if you sacrificed 2 Bitcoins, the value of the bond is actually 4 because 2 x 2 = 4. And if you had 5 Bitcoins, the value will be 25, which is 5×5. And that gives an incentive for people to only run one bot because it means if they have a certain stash which they want to use for fidelity bonds, they’ll get the most value.

Chris Belcher:

If they lump it all together, if they split it up over many bots they’ll be at a disadvantage. And that gives preferentially helps honest bots who wants to just make money cause they’ll just run one inaudible. But if you’re a Sybil attacker who wants to, who wants to spy on people, you have to run loads of bots because CoinJoin have like 10 or 8 or how many other users in them. So if the Sybil attacker wants to attack someone who’s making an 8 party CoinJoin, they have to run 8 inaudible and this V Squared term will make them have like a disadvantage. Now the way you work out the actual numbers is, so there’s a document I’ve written called the financial mathematics fidelity bonds and they use draw probability tree diagrams. It’s this thing, if you like, it’s schoolboy maths.

Chris Belcher:

Essentially like there’s a, a tree and you repeatedly choose from a set without replacement and that’s you can I cook that up and post them to figure out to put numbers on it essentially. So there’s a good, I’ve written down some numbers so you can get the idea. So suppose we have honest makers and they have a fidelity bond value of 10 and then there’s two Sybil makers and they have each have a fidelity bond value of a hundred. So a hundred times more. And our taker is making a 3 party CoinJoin, so himself plus 2 people, and then we can work out what’s the probability that the Sybil attackers will win, that there’ll be both of the makers and therefore they’ll be able to unmix the CoinJoin. And it turns out that so just to repeat the numbers again, the honest maker has a value of 10 and the two Sybil have a value of a hundred and it turns out the Sybil attack will fail 24% of the time.

Chris Belcher:

So about 1 and 4, which I find really surprising because the Sybil attackers would sacrifice a hundred times as much value as the honest makers. And that, that you can compare that to to how proof of work works, which there’s this 51% attack. But if the other story has more hash power than everyone else put together, they’ll win. And then the fidelity bond system, they don’t just mean they didn’t use the 51%. They need way more. So I’ve I’ve worked out the numbers and I’ve take it so I’ve used realistic numbers, so I’ve taken from, from JoinMarket all the Bitcoin’s being advertised today for CoinJoins and said, what if all these people just locked them up for six months and use them for those big ones, what would it cost to Sybil attack such a system? And it turns out the adversary would have to they have to lock up 50,000 Bitcoins for six months, which is today’s price it’s about 350 million USD, or they’d have to send about a hundred Bitcoins to burner address and that would give them a, that would allow, that would give them a 95% chance of successfully Sybil attacking the system. So 19 times out of 20. So I think those numbers are quite good, which is why I’m quite excited about the whole thing.

Stephan Livera:

Right. And so as you’re saying, it’s the idea is to try and is to use that asymmetric idea of making it more costly to attack than to defend. And so I guess just summarizing the idea is when you’re in a CoinJoin you, one of the fears or risks is that the other parties in the CoinJoin are actually one person and then they, through the process of elimination, know what your coin is post mix or in the mix depth, right. And so they would say, I know that this output is actually Chris Belcher’s output. Whereas if you are CoinJoining with honest participants only I think in the JoinMarket model was, is it the taker who knows the mapping, right? And so that’s kind of the difference there. And so in terms of how it might look for the user who wants to do a CoinJoin, would they be individually selecting participants and then saying, Oh, okay, look, participant A has a V Squared of a 100 and participant B has a V Squared of 150, so I’ll go with participant B or like how would that work?

Stephan Livera:

Or is it, I mean, I presume a lot of this is just being automated, right?

Chris Belcher:

They could choose if they wanted to with JoinMarket today, you can choose, but it can also be made automated. I think that’s a better user experience that they use or just click send and then every it will happens behind the scenes and after the other end you get the CoinJoin, which like has all the, you know, has really good privacy. So how it would work as the, the taker, like just the wallet would ask the user what’s the maximum they’re willing to pay for a CoinJoin fee and then all the bots, which are cheaper than that. It would choose from them randomly, but it would have a, you’d have a greater chance to choose people to choose box which have a greater fidelity bond value. So their fidelity bond value will be their probability of being chosen. And the Sybil resistance comes that if there’s even one bot who’s honest, then that will introduce uncertainty into the coinjoin. And it’s essentially that’s why it’s why the system is so costly to attack because the honest makers, if they get chosen they only need to get lucky once for the Sybil attack to fail and the Sybil attackers, they have to get lucky every single time. So if the taker is choosing eight other bots the Sybil attack has to get lucky all those eight times and have their own bots be chosen. And if even one honest maker comes in, then there’s uncertainty added.

Stephan Livera:

One other question I had around the JointMarket model and just in CoinJoining in general is obviously it’s ideal to do remixing. And so how does remixing play into that idea? Because if you, so hypothetically let’s say you are concerned that there might be some Sybil attacker in the pool of participants, how does remixing play in and help you avoid or help you mitigate that risk?

Chris Belcher:

Yeah, so remixing is just doing multiple CoinJoins, doing one and then doing another CoinJoin. I know another one these calculations I mentioned, they’re just for one single CoinJoin. So I’ve been using the figure of 95%. Like that’s a good success rate to aim for. And that’s equivalent to 19 out of 20 times. And if you do, if you did 5 CoinJoins, that’s the calculation days. 95% raise to the fifth power. So 95% times by 5, times by 5. And that’s, I can’t do it in my head, but the probability of a Sybil success gets lower and lower each time. And that’s, that’s doing remixing as you call it, doing multiple CoinJoins is built into the JoinMarket scripts, which is called tumbler and yeah, that’s what it at. You start with some Bitcoins and it does many Coinjoins to try and make that trace disappear.

Stephan Livera:

And so one other question around the tumbler and the multiple mixing aspects or multiple rounds of mixing. Does it matter? I guess it does matter the order, right? So would it, or maybe it doesn’t. So let’s say you were doing five rounds of tumbling in JoinMarket and you got, does it matter whether you got successfully Sybil attacked on the first round or the fifth round. Does that matter? Or is it just like if you got Sybil attacked on the first round, but then you actually ran through another four rounds, not Sybil attacked, you’ll find now, right?

Chris Belcher:

Yeah, that’s an interesting question. So I guess I’m just thinking out loud now. If you got Sybil attacks on the very first CoinJoin, then the Sybil attacker could see the source. Like they’d see the coins you started with and they’d see your, the destination of that first CoinJoin. And then the other, the other 4 or 5 CoinJoins, if they’re not Sybil attacks, then they’d still add privacy. So yeah, I guess it would be fine that, and if you’ve got Sybil attacked on the last CoinJoin, then the Sybil attacker would see, yeah, they’d see your destination going to your cold wallet or something like that. But they couldn’t look backwards. They can look back in your source because the other four CoinJoins earlier would, would be genuinely private. So yeah. Yeah. I think that for the Sybil attacker to see they’d have to Sybil attack, all those, all the, all the five CoinJoins or however many did. So tumbler by default, it’s around that number, but no, about 10 or 15.

Stephan Livera:

Gotcha. So basically it’s a good defense because it means they need to successfully Sybil you, 10 to 15 times in a row.

Chris Belcher:

Yeah, yeah, Yeah, exactly.

Stephan Livera:

Yeah, that’s a good way to put it. Okay. And so we’ve spoken about some of the benefits. What are some of the downsides or are there any unsolved problems that you can see with fidelity bonds?

Chris Belcher:

Yeah, so one of them is, I suppose it’s not necessarily a downside and I think it would be fine, but it’s it would make the CoinJoin fees go up because there’d be probably be fewer people, JoinMarket would be more capital intensive. And the only way the market could support that as if CoinJoin, if they earn more money, fees go up. So right now they’re really cheap. This like a 100 Satoshi or maybe 500 Satoshi or it depends. It can be really, it can, some people have zero or 10 satoshi. So I don’t think there’ll be a problem because it’s really cheap compared to miner fees or other costs of using Bitcoin. So I’m not, we find another problem is just locking up coins is, might be kind of annoying.

Chris Belcher:

The makers might not want to do that, but they get paid for it. So I’m sure they’ll do it. But the biggest thing that kind of worries me is, so I mentioned this, this V Squared thing, which gives an incentive for people to only run one bot and not spread out their coins over many bots like, they won’t make more money doing that. That also gives an incentive for multiple people to put their coins into one bot, if you see what I mean, to combine their coins, even though they’re different people. And that would look like, that would look like people renting out fidelity bonds. So you could, you could imagine a situation where there’s some service and it says you signed up, so lock up your coins at a time locked address and then send me the signature and I’ll give you some associates for that.

Chris Belcher:

And they’d make more money because of the V Squared thing, which gives incentive for lumping now some solutions to that is, from what I’ve thought of is you can make the takers only accept one single UTXO not accepts 5 different new inaudible. So as the fidelity bond, but just one. And that means that people couldn’t just lock up coins in their own hardware wallet and send the signature because it would invalidate the others. But that could still be broken. If you have multiparty compute, multi-party ECDSA computation, so you can have a, it would work. This is the kind of, you know, worst case, nightmare scenario, but there’d be this, this maker, which one, which is takes other people’s fidelity bonds and they have a special wallets and you send your Bitcoins in that and it has a pre-signed transaction, which returns your Bitcoins to you.

Chris Belcher:

A bit like a bit like in lightning network. Then your coins will be in this fidelity bond locked up for a few months and you could always get them back, but they’d be, they’d be actually contributing someone else’s fidelity to someone else’s, bot someone else’s bonds. And so that, that could happen. You can’t stop this from happening. And I kind of expect it would be, I don’t think people really do it because they’d, they’d have to get that whole, it’s like all that, you know, the hard earned the Bitcoin savings and they have to put them in a really exotic kind of wallet, which does multi-party ECDSA computation. I don’t think people do it. We’d also, we’d also see adverts everywhere. Like you’d have to see Google ads or ads on Reddit or Twitter saying, Hey, you could get extra money if he gives you, if you put your Bitcoins in this fancy new wallet.

Stephan Livera:

Oh, I’ve never seen those ads before.

Chris Belcher:

Yeah. And that would be an indication that the system is broken.

Stephan Livera:

No. I mean, I’m just referring to the scammy ones.

Chris Belcher:

This is really, the scammy ones are, they’re custodial, so they can literally steal your money. And in this one, because of the cryptography, they wouldn’t, they wouldn’t be able to steal it, but the wallet software would be, it’s any use for this and it probably wouldn’t be that well reviewed.

Stephan Livera:

Right. I see. Yeah. Yeah. So it would take a lot of collusion or as you said the, the renting concept. Yeah. Okay. I guess just with JoinMarket more broadly, do you have any views around ways to make it easy for people to use? I know some of this I’ve discussed in my earlier interview with WaxWing but I’m curious what your thoughts are on this question because it seems to me like JoinMarket is one of those things where you have to be more technically competent to use it. And so do you have any thoughts around that or do you believe it’s just the nature of the thing that only more technical people can use it.

Chris Belcher:

No, I don’t think it has to be only for more technical people, but it’s kind of inevitable. But for now it will be. I think a good analogy is a bit how when between Windows and Linux at least 10 or 15 years ago and at least in the beginning of Linux was really hard to use, that you had to compile your own kernel and do lots of stuff on the command line yourself. But you have the benefits that Linux was really good in than Windows but when Windows is much easier to use, right? And I think there’s a similar kind of thing that JoinMarket has this open source model that it’s decentralized. It doesn’t like it doesn’t take fees or like none of the fees go to developers or anything like that.

Chris Belcher:

So it develops very slowly and people develop things that interest them most in a way. But I think it will improve slowly. So now Linux today is much easier to use than it was when I first started using it. So I know recently WaxWing like there was a nice development. Waxing found a way figured out, or fix the thing where you can have JoinMarket in an app image. So you could download this file and you don’t have to install anything. You just double click it, and then JoinMarket opens up. And that’s like a small step to making it easier to use. And I think small incremental, it’s a progress. Like that could mean that in a few years or so then JoinMarket will be as easy to use as something else. But you can see the incentive thing because the other things like Wasabi Wallet and Samourai Wallet, they directly get money from their customers. So they can employ developers and make things really easy to use. Like windows is, and I think that’s fine as well. Like they that the two kind of, not business models but the two ways of operating are all legitimate and they like, you know, Windows and Linux coexisted fine for ages.

Stephan Livera:

Right? Yeah. And so in terms of contributions or support for JoinMarket is there anything you would like to shout out? Is there anything that you would like to request from the listeners?

Chris Belcher:

Yeah, so my JoinMarket and my research and all of that is only supported by donations from the public. So they if your listeners are interested in supporting this stuff, if they want to help, Bitcoin privacy and that kind of thing, then they should give the JoinMarket project a donation. So the URL it’s bitcoinprivacy.me/joinmarket-donations . And you can find an address there to donate to.

Stephan Livera:

For listeners who want to find you online, where can they find you?

Chris Belcher:

So I have a Twitter, which is @chris_belcher_ . I’m also in Github. github.com/chris-belcher/. I’m on Reddit, which is /u/belcher_ where else? There’s an email address if you want to email me, which is belcher at riseup dot net. I know just about wraps it. There’s also the, the Bitcoinprivacy.me site has on the main page has a bunch of ways to contact me as well, and the other links to some of my things I’ve created.

Stephan Livera:

Awesome. Well, thanks very much for joining me today, Chris.

Chris Belcher:

Thanks for having me.
