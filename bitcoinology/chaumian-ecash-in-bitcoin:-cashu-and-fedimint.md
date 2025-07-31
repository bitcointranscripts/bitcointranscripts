---
title: "Chaumian eCash in Bitcoin: Cashu & Fedimint"
transcript_by: ubbabeck via review.btctranscripts.com
media: https://www.youtube.com/watch?v=VwMzNE1D3so
tags: ["ecash","threshold signatures","coinjoin","multisig","zero-knowledge","schnorr"]
speakers: ["Adam Gibson"]
categories: ["meetup"]
date: 2022-10-19
---

 
# INTRODUTION

Adam: So hello everyone.
So today we're talking about Chaumian eChash.
I'm gonna mix terms up a bit.
You know, Chaumian cash, eChash.
I'm gonna mix up the terms mint and bank very often because I don't know why I just keep mixing them up.
To me, they're the same thing in this situation.
And this is gonna be a rambling talk.
I'll try and limit it to no more than one to one and a half hours.
I'll try and keep it, And as we get towards the end of that time, I would expect more and more of you to ask questions and start talking about it, because I think there's a danger, I'm gonna get quite theoretical in some parts, and the really interesting questions are more about the practicality of this, I think.

Cryptography's fascinating, but I know that's not gonna turn everyone on.
So I think, but everyone should be, I think, interested in the question of is this actually useful?
How is it useful?
So we can start discussing that as we get further into it.
So to start with, we need to have some motivation, I feel like, I just put this little section at the start of my notes.



## What is Chaumian Cash?

Sorry, it's just notes, it's not a proper presentation.
I was just, this is me, result of me sort of reading about this stuff for about one week.
So, you know, I'm gonna make some, probably some mistakes, and there'll be some holes in what I say.
If anyone here does know mistakes, can correct mistakes that I make, please go ahead.
Don't, please feel free to interrupt at any time, or if something's completely like what are you talking about, ask me.


So motivation, what's this for?
Does this make sense to people?
Oh, can you read the text?
Yeah, okay, so assuming your eyesight is normal, which I don't know if it is, then hopefully everyone can read.
So I put three points there.
I don't know if it's a comprehensive list, but what is the motivation for having something like a Chaumian cache system?
Before I'm even explaining what it is, I'm gonna talk about why it might be useful, maybe.

More scalable, faster.

I mean, this probably is something that everyone here is familiar with, is the concept that if we use a centralized system, it's much easier to be scalable, performant.
You know, we can have a single database and maybe it's replicated, like if it's Google or one of these big tech companies, you can make thousands, millions, I don't know how many queries per second.
And everything's fine because it's all, there's no issue of consensus about people falling out of consensus, different numbers, whatever.
So it should be more scalable if we just have a centralized system, So that's the first thing.
I've also written here not enough UTXOs. 
Does anyone know what I mean when I, in my little note there, not enough UTXOs?
What am I talking about?
Yes.

Anon: There isn't enough UTXOs. Is it possible to make enough UTXOs for everyone in the world to have one?
Adam: Exactly.

That's the basic point.
So UTXO, unspent transaction output in Bitcoin, has to be stored in the blockchain.
Has to be stored, let's say every node has to have a database of all the UTXOs that currently exist in order to check whether a spending event is valid or not.
So there are currently, who can tell me, 60, 70 million?
I don't know how many million there are right now, but there's tens of millions of UTXOs right now.
But there are not billions of UTXOs. It isn't really feasible for us to have Bitcoin with billions of UTXOs, we can't all have a UTXO, and given that each person really needs more than one UTXO, and that's kind of a problem, which is one of the reasons why Lightning exists, and Lightning is addressing this scalable issue with Bitcoin in some ways, but it's probably also true that since every lightning channel needs UTXO, you almost have the same problem in lightning.

It's better, it's ameliorated, in the future it could get even better, but it's unlikely we'll ever reach a point where we can have tens of billions or hundreds of billions of lightning channels.
It's not realistic.
So a centralized system can address the scalability problem.
What makes this kind of digital cash system be what we call eChash or sometimes Chaumian eChash is the privacy property though, specifically the privacy property.

So if there's one thing you take away, the concept here is that Chaumian eChash was designed from the start by David Chaum to be something where you could somehow have it be untraceable.
They literally use the word untraceable.
It would be kind of like not politically very convenient to talk to regulators and say, oh, I've invented an untraceable form of digital cash nowadays.
But back in the 80s when he first came up with that idea, that's what he had in his mind.
So it's very strong privacy in the specific sense that the bank or the mints which sort of owns this token can't, either can't easily or we hope can't at all link, like when it sees money coming in, it can't tell who originally created or minted that money, let's say, or who originally got that money issued.
Well, we'll go into all this shortly.
The third point is really like, yeah?


Same or better, maybe, theft security model than TTP, trusted third party, but much worse than a blockchain.
Now, same or better than TTP might be a bit weird to you if you're thinking about this.
You're thinking, well, if this mint is a centralized database, then that's already a trusted third party.
So how am I comparing it with a trusted third party?
Well, what I mean here, this is just brief notes, sorry.
What I meant was, compare it with something like Coinbase, or a company which stores your Bitcoin.
If you literally give your coins to Coinbase, your Bitcoins, they're obviously a trusted third party, because they hold your coins, right?
So this has a similar security model, but it's also a little bit different.
The big difference here is that you actually hold the coins yourself.
But it's a really weird gray area, because think about it.
You go to this mint and say, please give me one coin in exchange for whatever.
They give you one coin.
You hold it literally on your mobile phone or on your computer.
They don't hold it.
But on the other hand, they control like the whole database of the coins.
Right, so they can decide at any time not to accept your coin.
They can decide at any time to make 100 more of the coins which you don't know about.
All kinds of similar shenanigans.
So that's why I say same or better than TTP because in something like Coinbase's case, they're just 100% under the control, owning your thing, right?
But debatable.
Much worse than a blockchain, right?

Because the basic Bitcoin model is that you hold the private keys and because of the distributed nature of the consensus and all the proof of work and blah, blah, blah, you hope, you believe there's some kind of immutability that's being enforced globally.
So there isn't some other person who can just say, no, your coins don't exist, or actually here are a million new coins.
Making sense so far?
Great.
If it's so great, why hasn't it been done yet?
I mean, we might as, oh, sorry, I'm playing with, Sorry, I touched the microphone.
Before I even go into what I wanna say, does anyone here wanna take a stab at answering that question?
If Chaumian eCash is so great, and you could say it's great because it's scalable and private, and maybe it isn't so great with a theft thing, but whatever.
If it's so great, why hasn't it been done yet?

Anon: I would say something like, it's tied to, let's say, dollars or something, or gold, physical assets, but it's how it's been done before.
So it's tied to a real thing which gives it value in the first place, then you have these tokens you can trade around digitally. 
But then that gives you a centralised thing that governments don't like and can come and shut down, which happened with e-gold and the other things.
So what Bitcoin brings to the table is something that has value, but isn't something you can go and catch.
So that's why it's interesting to apply this on top of Bitcoin.

Adam: Right. OK.

Adam: Any other opinions or thoughts?

Anon: I'l stab in the dark something to do with Schnorr signatures and their licensing?

Adam: Oh, OlK.
And actually, as it turns out, it was part of my research.
It's not only Schnorr, but several other cryptographic algorithms, including RSA, had weird patterns around them as well.
Interesting point.
I didn't even think about that answer, but I suspect that's a small part of the story.
But it's not an irrelevant point, isn't it?
That sometimes developing these systems is actually stymied by legal restrictions of patents.

Anon: I'm gonna ask something stupid, but didn't Wasabi use something of this sort in their back end or something like that?
So does it mean it has been done, or people have been using it to some degree?
Or is that?

Adam: Okay, so that's another perfectly valid answer to my question is, don't be stupid, it has been done.
It has been done multiple times in different ways.
I wouldn't say Wasabi was an implementation of eCache, but it was certainly an implementation of Chaumian blinding in a very it is very it's very related It's not just you know is a very valid. You know and not only wasabi, but other things, too.

Anon: Does Mercury also have that?
 
Anon: It has the same token concept. ** Not transcribable  **

Adam: Right, yeah, so there's some gray areas here between token and coin, and there's various different things, we're gonna come on later, we'll see another one as well.
All right, I think we've got a good sort of set.

Anon: What's the answer?
Why hasn't that, is this what it has been done?

Adam: There's no simple answer to that question, we'll keep addressing it as we go along, yeah.
Is it fair to say that it's also, like, it's targeting late, or its use cases are more suitable for later adopters rather than earlier adopters because of this inherently centralized aspect of it?
Well, it's certainly true that the kind of bootstrapping mechanism you have in something like Bitcoin is difficult in systems which are just a simple central.
I mean the classic problem you might think of is I'm gonna make a new proof of stake coin.
Well who has all the coins at the start?
Oops, do I get them all?
That's nice, but it's kind of a shitty system, right?
So centralization doesn't really solve that problem, which is one of the kind of clever things about Bitcoin, but I feel like, oh, that's not good.
It's especially not good if, okay, I don't know the password, so don't let that screensaver kick in, okay?
If that happens, we have to yell.
Yeah, just shout at me.

## History - David Chaum's original papers Blind Signatures for Untraceable Payments


I think we should move on to the, because this is like a sort of motivating question, but I didn't intend to sort of answer it.
It's the start of the story.
Actually, maybe that's just as well because, See, it has a back button.
When I was setting this up about half an hour ago, I started setting up on Edge, and we literally spent 10 minutes trying to find a back button on Edge.
I'm not joking.

Anon: It's under advanced settings.

It's under advanced settings, yeah.
So anyway, history.
So, a proper understanding of anything probably involves studying its history.
I think a lot of people, when they got interested in Bitcoin, they thought, oh, there's actually a whole history behind here.
It's not just Bitcoin out of nothing, ex nihilo.
It's actually, the concept of digital cash goes quite a long way back.
Certainly after the advent of public key cryptography, which you could argue is Clifford Cox and GCHQ, or you could argue is Whitfield Diffie and all those guys and the RSA guys in the 70s or whatever.
But anyway, we got public key cryptography on computers and the whole thing was that you could, because of this asymmetric nature of it, you can create very high strength cryptography primitives without, outside of let's say a military context or a government context because people can share things sort of over the internet without pre-agreeing secret key material.
So I can make my GPG public key and write code and everyone can verify that I wrote the code, something like that.
And it can be very, very strong cryptography.
So this whole sort of flowering of cryptography started in that era.
And Chaum was one of the key people in terms of being a bit of a, a bit, he was a genius, I think it's a reasonable statement in terms of very quickly and in a very visionary way seeing very elegant and powerful ideas that you could come up with to use these new cryptographic constructions and One of a few things he came up with around that time.
So I'm talking about I don't know early 80s, maybe mid 80s I don't really know exactly was What did I just find that paper?
Not that one, is it?
I think it was that link.
Yeah, I can just click the link, but I already had it open, I'll just open it again.
Oh, this is opening the...
Anon: Up there on the left.
Every time it's blind.
It's the fourth time, sorry.
It says blind.
Blind.
Thank you.
Yes, that was that was wrong, wasn't it?
Whoops.
Blind.
Thank you.
You got it.
Yeah, I mean, it's, you know, you know you're going deep in cryptography when you start reading papers that were written on typewriters.
So this one was written on a typewriter.
I do want to say, though, I mean, it's always a bit off-putting, right?
I actually recommend reading this.
It's only a few pages and there's very little mathematics in it.
Most of it is taken up with a description, which I think is really smart.

What he did was he just described his idea in terms of this problem.
He said, oh, what happens if you wanna do an election, so voting over the mail, through the post, as we say here in England, right?
And you wanna keep the property of the election still being a secret ballot.
And so, I'm not gonna describe the whole thing.
It's kind of intuitive when you read it through it.
I think it's like the second and third pages he goes through this.
Oh, I can't remember, whatever, you read it.

So anyway, he goes through it and It's really smart because it explains the concept of blinding and how it solves that apparently really difficult problem of how your ballot can be secret, but yet still be verified to be a valid ballot, i.e. You're an actual correct voter and not just some random person.
You can do that just with carbon paper and envelopes so carbon paper the idea is like there's an envelope and inside you put it paper and you sign something on the top of the envelope and That signature carries through onto the carbon paper inside and it's not just a one-step process He explains it's like three or four steps But then you realize oh, yeah, you can do that And then he says well actually we can do the same thing with mathematics.
And he's very vague, he doesn't even talk about RSA in this version of the paper, he just talks about a function that's one way or a function from this to this.
But the other thing that's interesting about the paper is also at the beginning, he sort of anticipates a lot of the debates that we have because he says, the ordinary user does not want all of their financial information to be exposed.
And he was anticipating, this is well before the internet, He was anticipating that once we start doing commerce over these communication channels, as in payments specifically, we're gonna start exposing tons of information about ourselves to all kinds of people, including thieves, including people we don't wanna know the information, right?
So he really sees, oh yeah, we do actually need privacy in these online payments.

But he also says, and I think it's very revealing, like immediately the next paragraph, he says, oh, but this could also be exploited by criminals, right?
And so then he says, well, these kind of systems can also support auditing.
So he's imagining very much a centralized bank-based system where people are making these payments, they're keeping a high level of privacy, just as they would with cash.
He constantly compares with physical cash notes.
Well, and checks, but especially notes, right?
And he says, we can keep these properties.
We can also have the property that we can make sure that, you know, it's kind of like fantasy in my opinion.
We can also make sure that criminals don't take advantage of these systems because they can be audited.
And there's a very important principle. Whenever you have these privacy preserving systems, you can always insert auditing into them.
You can always say, like a voluntary auditing.

Let's say, if I use a CoinJoin, if I use a Confidential Transactions, if I use a Zcash, if I use a Monero, there's always a way for me to say, oh look, I'm gonna reveal this particular key to you and you can then see the exact tracing of the coins through whatever that system is.
So I think that's revealing because actually Chaum was not one of the cypherpunks.
Do you know what I mean by cypherpunks?
Yeah, I guess most of you heard that term.
The cypherpunks was sort of more the late 80s into the 90s and then maybe even later.
A lot of people, it started out sort of a bunch of futurists basically in California who were very libertarian leaning and were very keen on minimizing state power and seeing how cryptography could help with that goal.
And to them, I mean, they had people like Jim Bell who came up with this idea of an assassination market so you could use cryptography to literally anonymously pay for someone to be assassinated, right?
Like a politician.
He was specifically referring to politicians when he came up with the idea.
Chao was outside of that, and he was in that other camp of the cryptographers who were more, look, this is really going to help the human condition, but I don't want to challenge the state's power.
So they were showing that actually sometimes these things could be done.
It's important to understand that I think because a lot of the early history of eChash was tied up with the cypherpunks.
And he wasn't actually in that camp.
Anyway, so how did the history develop?
I mean obviously it was slow initially.
These things didn't exist, it was just a theory.
The initial sort of presentation of the idea was based on RSA.
I won't go into that, but it's kind of old school cryptography RSA, but basically you can take a signature and multiply it by a number and suddenly it's a random number, it's not verifiable as a signature.
And so you can kind of sign with the randomness added and then you can take that signature and you can unblind it as we say.
So you can blind and unblind.
So we might go into that a little bit later with the schnorr case, but I won't explain it now So this early idea was like RSA blind signatures.
The mint is a trusted It's just when he when he was envisioning it as far as I can tell he meant a bank He was thinking specifically a bank.
Okay, so the mint in the sense that it creates coins, was some kind of bank or otherwise some kind of trusted institution.
And importantly, in the presentation, the idea here is that 

## How does a eCash Mint/bank work?
the transfer, and this is explained, I think, in this picture nicely, which shows one of Aaron Van Wirdum's articles.
I stole it from, so thank you Aaron.
Importantly, the transfers of coins in the system have to be mediated by the bank.
What does that mean?
Well, Your person A, you've got some coins issued.
So you've asked the bank, you said, please give me one eChash dollar.
Of course, to get that, you'd have to deposit something with the bank, right?
So they give you one eChash dollar.
You wanna pay person B, what's that?
Yeah.
Oh, I clicked the, sorry.
Annoying, you want to pay person B, well obviously you can send them that eChash dollar.
So at this point, already be thinking to yourself, ah, this is a bit different, right?
This is not like Bitcoin.
I've got, imagine it like a long string of numbers, it was just a very big number.
I'm literally gonna give that number to another person.
All right, so a has a big number they've got from the bank literally a number we're not talking about like They're gonna give the number to be now.
Obviously, there's a problem with that, right?
What's the obvious problem, you just nodded?
What's the obvious problem?

Anon: This is the number 25.
Yeah, exactly.

I can't give you the number 25 and claim I don't own the number 25.
Of course I do, I already have it.
And of course, not 25 is much more, you can't predict it, but nevertheless I still have it.
So we have the double spending problem.
So all this stuff about double spending that we've heard of in Bitcoin, it all started way, way back at the beginning of the idea of digital cash, because data can be copied.
So this is like an online transfer model, in the sense that the way B actually accepts that number as money is by verifying with the bank.
They send the number to the bank.
The bank checks Well, let me ask you.
What does the bank check?Or the mint? 

Anon: It must have a database that 25 equals one dollar.

Adam: Almost but not quite.

Anon: Like who had it last,so this person haven't happened before.

Adam: Also not correct but an important thing.

Anon:  They've got to verify that the signature is theirs. 

 Yeah, that's fair No, but the reason I'm saying you're wrong is something else. But that's also another correction because I'm presenting a very simplified version of the model to start with but but yeah. My point is that they don't check that the  25 there they check that 25 was never spent before They add it's like the opposite to Bitcoin in the sense that you've got a list of spent coins here rather than a list of unspent coins.
And so what you do is if you verify, whoever said signature absolutely correctly. If you can verify that's a valid number, then you add that number to the list of numbers that have been spent, so to speak.
So that model is fine, but what, mm-hmm.

Anon: But when you say spent, you mean spent as in given back to the man, or spent per person A to person B?

Adam: It means a list of coins, at the start, the list would be empty, right?
A gets issued a number. We're calling it 25, but it's very big number. And there is the issue of it being signed and verified, but we're ignoring that for now.
A is giving B the number 25.

Anon: Does this actually get recorded then?

Adam: Wait, wait, wait, wait.
So A is giving B, A is giving B the number 25.
B takes the number 25 and asks the bank if 25 has ever been spent before.
And if the answer's no, and also if it's a valid signature, if the answer's no, they add number 25 to the list and say, yes, it's valid.
And at that point, B accepts it as money.
Does that make sense?
It's a bit, vastly oversimplified, but.

Anon: So the bank is to make sure that there's no two people that know the same number of valid coins.

Adam: Well, it's to make sure that each coin is only spent once.
It's not about people so much.

Anon: Because we can share it with...

Anon: That's because then it comes rising up the double spending problem, right? So You're stopping double spending by making sure that people know two entities.

Adam: Yeah, but imagine they can't even tell entities apart.
The principle involved here is only that they're going to accept coins to be added to that list that they've never seen before added to the list.
I've really oversimplified it so much, I'm worried that these questions are not getting to the point.
Because there's two other elements, there's blinding and signing involved, which I haven't talked about.
I'm really making it confused.
Anon: This person being out of part, he can't spend that. Like it's now, he's got a number which has been recorded as bad.
Adam: Yeah, so there's the re-blinding thing, yeah, yeah, yeah.
Okay, there's so many elements to this.
Okay, so I actually wanted to just, okay, the reason I wanted to show that straight away is to get the concept of onlineness into your head.
The concept that, without going into the cryptography yet, but the concept that, unlike something like Bitcoin. There is a need to contact someone to be online to actually receive money.
In Bitcoin it's really nice that we don't have to be online to receive money.
Here you absolutely do.
And they recognized early on that that was an issue.
They didn't like that when they were writing these initial papers.
I noted here, I won't pull it up, it's not that interesting, but several years later, Chaum working with Amos, Fiat, and Nauer produced another paper where they were addressing that problem, they were saying, you know what, there's a bit of a problem with this system, it's really cool, but it's horrible that the receiver has to be online all the time.
If he wants to receive money, he has to constantly contact the bank every time.
Otherwise, we have this double spend issue.
So the solution they came up with was based on something called cut and choose, which is a very fancy cryptographic protocol where, I don't wanna describe it, but it's probabilistic.
It involves generating a lot of different possibilities and then just relying on statistics to ensure that the protocol was honestly followed.
The problem with it, being statistical and probabilistic means there's a lot of data.
So there was a lot of interactivity, a lot of data back and forth in order to achieve that goal where in this picture, person B could receive that thing from person A and somehow be assured that they wouldn't double spend it.
But there's a subtlety.
They could never be assured that it's not double spend Immediately at the point of receiving the data no matter what the data is But the idea was that if you use some clever protocol you could get a blame and you could get this thing where?
Suppose a gives that number 25 to be B doesn't check with a bank and just trust A and the only reason they would trust them is this idea that if A then went and tried to double spend, try to spend 25 with C, then in so doing they would actually reveal that they had cheated via this clever cut and choose protocol.
And that's really cool in a way because it enables some kind of offline payment based on game theory.
But it's also really uncool in another way because blame protocol only makes sense if there are individual people as accounts.
If every single spend event is anonymous, you've got no one to blame, right?

So this point will come back again later.
All right, so let's go a little bit into, little more detail, I might answer some of the questions we're having about how this thing works.

Anon: Question, can you use something like lightning ivoices to avoid the need for B to be online? If B were to generate a random number, give a hash to A, advertise a hash to A, then A says to bank to mint that only give this coin to someone who can reveal the...

Adam: No, but then you're interacting with the bank again.

Anon: A interacts, but B...

Adam: Oh, you're trying to make it so that A not B interacts.
Okay, I'm not sure I'd have to think about it, alright?
That's cool, that sounds like maybe your ideas are...

## Blind signing

May well be a good one.
But maybe we'll come back to that later.
I think we need to get the basics first because we haven't yet.
What we've presented so far is a really stupid toy model where A is giving B a number 25, but it's the same number.
Well, that's dumb for privacy, right?
Because what happened, remember, at the start, A got the issuance of the coin from the bank.
If that number, even if it's a very long random number, it doesn't matter, if that number's the same number that B then redeems, then we haven't got untraceable cash, have we, we've got traceable cash.
Because the bank sees, well, the coin that B gave me is the one that I gave to A, so that's traceable.
So that introduces the concept of blinding.
And blinding is basically the idea, it sounds, when you first hear this described, it's so confusing.
It says, okay, we know what signatures are, right?
Everyone knows what signatures are, digital signatures.
If you're in Bitcoin, you know what they are.
But what about a blind digital signature?
And here, the idea is the person making the signature doesn't know what message they're signing.
This is very weird, right?

Because what's the point of a signature if you don't know what you're signing?
Would you sign something if you don't know what the message is?
I mean, it's not a good idea, right?
So, but there is actually, weirdly, an application for this and this is the application, right?
So you don't know the message.
So imagine you're the bank, you're sitting there signing.
You know, maybe you're basing it on each customer that comes along, gives you what, $1.
Okay, you've given me $1, I sign, I give it to you.
You give me $1, I sign.
But what am I signing?
You're hiding what it is that I'm signing from me.
What you actually do, so Tracy comes along, she says, I want $1 worth of eChash.
Tracy gives me $1, and she gives me like a thing, I'm not gonna explain this, I sign the thing.
Think of the thing as being like an actual message which is wrapped inside a container, all right?
So she's got a secret number.
Okay, let's put it like that.
She's got a secret number.
She's wrapped the secret inside an envelope.
She says, if you, I want you to sign this for me, I'll give you $1 for it.
So I sign it, I'm the bank, my key, everyone knows my key, everyone knows my verification key, so I give the envelope back to Tracy, and Tracy then opens the envelope, inside is her secret number that she placed there, but by the magic of cryptography, the signature passed through.
It wasn't just on the envelope, it's still also on that secret number.
So what does Tracy hold now?
She holds a secret number that she never showed me and a signature on that secret number.
And that is her coin, that is her eChash coin.
So that's what blind signing does in this situation.
I'm gonna stop there for a second.
Does that make sense?
Or does it not make sense, I should ask?

Anon: It's like carbon paper.

Adam: Yep, carbon paper, yeah.
That's exactly the analogy that, I was trying to find a good analogy and I ended up using the same one because I couldn't think of another one.
I think it's the right one, isn't it?
But the thing is, the problem with the carbon paper analogy is everyone here is not like 65 years old, so they've never seen carbon paper.
At least I don't think you are.
So yeah?

Anon: That secret key that has been signed, the bank knows how much.

Adam: Right,denomination, right?

## Denominations

Relevant point isn't it?
Because if we weren't thinking about denomination, and then Tracy's sitting here with her secret number that's signed, but what does it represent?
Does it represent 100 eChash domes or one?
So denomination matters.
No, that doesn't matter.
So, I mean, how would you solve that?
I mean, you raised the absolutely valid point.
So, how do we solve that problem?
If we want to build a system?
Okay, everyone seems to, yes?

Anon :Each signature is one.

Adam: Each signature is one coin.
Yep, basically yes, but of course you can finesse that right?
How can you how can you make a more powerful version of that?

Right ones hundreds tens fives whatever you want to do. Yeah, but the thing of course is that each because of this weird property where we're signing something.  We don't know the message.
It has to be that the key defines the denomination alright, so I'm the bank and I have I sit here with my public keys.
I've got my one dollar public key I've got my two dollar public key my four dollar public key my eight dollar actually the most of the original implementations use powers of two.
And so when you want, let's say, 17, you say to me, oh, here's, again, a random secret message wrapped up in an envelope, sign it for me, but it's for the 16, so I'm gonna give you $16, but give me a 16 version of a signature using my 16 key, and then give me another one, we're here for the $1. Give me a token for the one key.
So you've effectively got a single $1 blinded token and then a single $16 blinded token.

Okay, what happens if then Tracy wants to pay 13, but she's only got a 16 coin and a 1 coin. Ignore references to one coin by the way. Are you just get 13 of them, but you haven't got you've only got a 1 and a 16 

Anon: Yeah I have to send you all of the 15 and get back, change, well it's like the UTXO but I have to spend all the, yeah, get something back and then.

Adam: But I think it's important to understand that it's different from the UTXO model, right?
Because the important difference is, I mean, I guess a lot of people who use Bitcoin never even think about the UTXO model, but it's weird because it's a, oh, it's a variable denomination.
Yeah, it's like that, yeah, nevermind, Kato, whatever it is.
It's exactly like cash.
It's like, exactly, it's like physical cash, and it's not like UTXOs in this regard but I mean this these are details I don't know and after all users are not going to have to care about this if they use a eChash system. Let me just I didn't start reading by in second denomination defined by signing keys Globe This is a bit obscure globally known or defined pub keys are important for privacy What I mean by that is that it's important that we all know what the bank's public keys are for the one, the two, the four, and so on.
If they start using different keys, they could tag us.
They could use, that's an obscure point.
A coin's a fixed denomination.
Messages, basically think of the messages as random secrets, but they're important secrets.
They're secrets that protect your ownership of the coin.
You can't just lose them, so there's issues around backup.
We'll talk about that.
A coin is spent when redeemed at the mint and is added to the spent list.
We've discussed that already.
Never forget, we're talking about a bearer instrument here, and this is a bit different from Bitcoin. Now Bitcoin is a bearer instrument but there's a kind of a layer of abstraction there. My my what I hold is my private key or private keys in Bitcoin yeah, And that's the thing I have to be careful about because that controls coins.
But here it's the coins themselves which are the actual value, not the keys which control those coins.
So I mean the distinction may be, I don't know how important that distinction is, but it's important if you're trying to understand the system to see it's different.
Because yeah, because of that second clause, right?
Because if I have a UTXO and I give you my UTXO, I haven't really given you anything, right?
But if I give you my eCash coin, you literally hold the coin now, yeah?
So that's kind of an important practical question.
How okay is it in terms of being a bearer instrument?
Okay, I think we've already covered this.
Online payment.
So, most of the time we're gonna be talking about systems that implemented online payment as we discussed at the beginning.
It's unfortunate, it's not ideal, the fact that you have to contact the mint to make the transfer, but that's mostly in practice how these systems have worked, and even the ones that are being proposed today are basically, I think that's correct, always gonna be doing that.
Splits, we talked about that.
If you got a 16 and a one and you wanna pay 13, you're gonna have to ask the mint to change.
Just like you go to a kiosk or the casino, you get the chips, you change out the 16s for the fives or the fives for the ones or whatever it is, you can do that.
And of course, every time you go back to the mint, you can re-blind, you're effectively, I suppose you have to be reblinding every time. So you give them some some tokens and they give you new tokens and again you only you know the secrets for the new new tokens. 

## Stefan Brands's Paper - Untraceable Online Cash in Wallets with Observers

So that's easy enough to do So as the history progressed into the 90s, Stefan Brands, I'm not very knowledgeable about this at all really.
I've only read a few bits and pieces but basically he, I think the TLDR is Stefan Brands was Chaum's student.
I think that's right.
I might be, I don't know if he was like his PhD student, or probably not.
But anyway, they were related in some way.

Anon: I have maybe a similar anecdote.I know at some point when he was in Netherlands, like even Nick Szabo and all the cool people were actually going in, kind of hanging out and hanging out.

Adam: What's Stefan Brands, you mean?

Anon: Well, I'm not.

Adam: No, you're talking about Chaum.

Anon: Yeah, I'm talking about.

Adam: No, we're talking about, I think you're talking about the story of DigiCash, which we'll come onto in a minute.

Anon: Okay, so sorry.

Adam: Yeah, yeah, yeah.
No, but Brands specifically, he wrote a PhD on this, and by the way, Adam Back will just never stop boring you about Stefan Brands, if you wanna learn all about Stefan Brands, because he loves the kind of ideas he had.
And basically, the TLDR is, Brands did the same thing as Chaumn, but kind of a bit better, at least as far as I can glean from reading these things.
He came up with a system that basically addresses the same points, but it's more elegant mathematically.
For example, I'll give you an example.
I think I've written it here.
One of the things, the way it's different, oops.
What is that?
One of the ways it's different is this.
Let me write this down because I think this works.
It's not too complicated.
Yeah, who's familiar with discrete log?
Well, let's go back a step.
Okay, if I write this, does it mean anything to people?
What kind of signature is it?
Yeah, that's a good point.
I actually meant schnorr, but you're right.
You similarly write ECGSA.
So let's say that's a Schnorr signature.
There's an R component, which is the nonce or the nonce point and there's the S component, which is a scalar.
But who knows, who here knows discrete log contracts?
Discrete being a pun, by the way, for those who are very good at spelling but not very good at humor.
Discrete log contracts, I'm running out of space.
And how does a discrete log contracts change the idea of a signature?
So this is a signature sigma on a message m and a public key p.

Anon: I think pretty much you sign a lot of more. So let's say I can only want to like, bet on something, right?

Anon: Yeah.

Anon: And there's like multiple scenarios.You're saying, you win, I win, or there's a stale.
So in the discrete log, we just sign out, we sign out all the outcomes. All the outcomes. And then we, depending on what happens, or it has to be someone from the exterior who kind of like triggers, depending on what happens, then We publish the correct signature for the outcome.

Adam: Yeah, yeah, yeah.

Adam: And what stops us from publishing two signatures with two outcomes to try and cheat people?

Anon: Kind of like the lightning thing, right?

Adam: You kind of have something to hold the other person accountable.

Anon: They keep the same nonce.
Right.
So instead of this model, we say, I mean, you could say I'm kind of.
The nonce reuse, right, right.
The nonce reuse, yeah.
Yeah, that makes sense.
So, what am I doing?
I'm trying to erase it with my finger.
I was like, what do I, yeah.
So, I don't know why that amused me so much, but a P, R, think of, maybe this is a silly way to say it, but this is how I, in my head, what discrete log contracts does is it makes the public key be that and that and not just that, which means that, oops, I switched, thank you.
It's amazing how technology works.
OK, so and then the signature, let's say sigma is just this, suddenly it's just a number, not a nonce and a number, which means it makes a virtue out of what is a vice.
Usually it's a vice if you reuse a nonce, you lose your private key and you lose all your money, right, if it's Bitcoin.
But here, the idea is that because this is fixed in advance, if that oracle who's deciding the outcome of the bet chooses to make two signatures, they have to do it with the same nonce.
So because they do it with the same nonce, they reveal their private key.
I know that for some people that's already known and a lot of people in this room that is like too hard to take in all at once, I get it.
But my point is that Stefan Brands, back in the 90s, at least as far as I understood it from reading it last week, basically did the same trick but in a much more sophisticated way in this paper.
So he was saying that, remember what we said at the start, like oh, it's really yucky, like how do we deal with this?
We don't wanna have the receiver be online and have to check with the bank every single payment.
But we could make a system where if a person double spends, they get punished, right?

So Brands did that again here in a much more elegant way than what Chaumn did in, or the Chaumn-Fiat.
Now our system did, right?
And he used that trick, basically.
He said, look, if the person tries to double spend, they'll be, it's not actually reusing a nonce, but it's the same algebraic principle, and they'll end up revealing a certain key.
But, clever as that idea was, it had the same basic problem, in my opinion, which is that you can't have a blame protocol unless you know that you're blaming someone, right?
If you know that you're blaming someone, you need a user and a key corresponding to a user.
You have to have users, you have to have accounts.
And a lot of us, I wanna say in the more recent like developments in this field, are trying very hard to avoid having like named users and fixed accounts, right?
So it's very difficult to make good privacy in a system that has all the users are listed.
Of course, going back to the beginning, remember what we said about David Chaumm.
David Chaumm had his mind a bank.
He wasn't like anti-state, he wasn't a cypherpunk.
So to him, and maybe to Stefan brands as well, I don't really know.
This kind of system makes a lot of sense.
Now also, with regard to making it offline, there were a lot of ideas around, as far as I can tell from reading this literature, a lot of ideas around tamper-resistant hardware.
So people were thinking a lot about having smart cards or having things embedded in devices that controlled spending.
And so it would be like, in fact, I think in this particular paper, this one here, In this particular paper, he ends up describing it as a kind of a mixed system where you would have what he called an observer with the wallet, which would effectively control the spending and prevent the double spending, but that if somebody was like a hacker and actually determined to like cheat and they actually hacked the hardware, they would still with this other blame element to it to make sure that they would be found out if they did cheat.
So it would disincentivize them, right?
So all this kind of thing, it's smart, but, and in fact the cryptography behind it, it's like what I just showed you with DLC, that's a very simple version.
He did a much more sophisticated idea of the same thing.
It's smart, but is it really something that people are 

## Real world instantiations / History of Chaums ecash via DigiCash Inc.
interested in?
I don't know.
I mean, I suppose that brings us on to this section, which is about real world, what do we know about actual real world examples of eChash going back in history?
So the obvious one, the one that's most famous and probably for very good reason, I probably already opened it here somewhere, but I'll just open it again, is this one.
Yeah, eCash, so there's a nice little timeline here on Chaum's own website where he goes through some examples of, well you can see the timeline, we're talking about the mid-90s, so DigiCash was an actual company based on Chaum's own paper that I've just talked about at the beginning there.
That's the early years.
Your Nick Zabo reference refers to I think one of the people in a picture later down.

Anon: Was there a Romania flag there?

Adam: There's a lot of pictures there.
I honestly have no idea.
Probably they had some Romanian deal or whatever.
But there's another, yeah, Mark Twain Banks, and there's, I think that's the picture that has Szabo in it.
I think that's Szabo there, if I, it's a very, very bad quality picture, even if you could see it, which you can't probably.
I'm pretty sure that's Szabo.
But Zuko's in there somewhere as well.
Zuko Wilcox Sohoen, right?
Anyway, whatever.
The point is that it was a company, it was set up in the Netherlands, and it was literally what we just discussed earlier on.
It was literally, in the interface, I've seen pictures of the interface, somebody was showing me the other day.
Here are your coins, and it was like, you have 10 two coins, and you have 13 four coins, and so on and so on, right?
Typical, like, really old Java interface.
It was kind of funny.
And yeah, now what happened to DigiCash?
So they set this company up.
They had deals with banks, or they tried to set up deals with banks.
They had examples of people actually buying and selling things with it.
I remember Adam Back telling me how he was really enthusiastic about it at the time and he was actually like trying to buy things and stuff.
So what happened to it?
Why aren't we all using DigiCash?
Does anyone know like what happened to DigiCash?
Got shut down.
I think there's a little bit of a confusion in people's heads between examples like e-gold and Liberty Reserve, which are more recent.
These were not really the same kind of thing.
Those things did get shut down and they were trying to back things with gold.
Was DigiCash more bankrupt?
I think it was more bankruptcy, although technically I don't think they actually ended up going bankrupt because the latest thing I've seen on it was like DigiCash becomes Payconic or something, it's a new company.
This was like in 2010, like years and years later.
But in this particular period, what I recommend you read if you are interested in the topic is that one.
There's a journalist in the Netherlands who wrote a long article here, which is really interesting, about, no, I've got the wrong one.
Oh, yeah, no, that's it.
How Digicash Blew Everything, and this is a translation from the Dutch.
And it's a really fascinating article.
It goes through how, basically, the first half of the article is all about how David Chaumn was a complete paranoid lunatic and like he was constantly scuffering business deals, he was constantly going back on his word and everyone, I mean according to the article, this is a journalist, so this is second hand info, I don't know, maybe it's complete nonsense.
But it's a really interesting recording of what happened.
And essentially it wasn't, legendary suspicion, yeah.
Essentially it wasn't so much like an explosion, like they completely went bankrupt immediately.
And it wasn't that the government came in and said, no, we're not gonna allow that.
It wasn't that at all.
It was, I mean, there's stories here, for example, like a Bill Gates coming to them and making them an offer, and then Chaum would, on the last day, would say, no, I've changed my mind, I want more money, or something like that.
It's really nonsense like that.
And there were huge, really important companies trying to integrate this and use this system.
Then they got rid of, there was literally a revolt in the company, they got rid of Chaum, and we actually had to leave.
And they got a new pair of CEOs or something and it was all just, but the thing is ultimately, you could say it's a failure of centralization anyway.
It's not the one that we think of in Bitcoin.
We think about people, oh, you know, the government's gonna come and arrest us if we do that, or they're gonna just declare it illegal.
It's not that kind of thing, it's just because it's a company.
And I personally, my personal opinion is that money cannot be created by a company.
I think it's just insane.
I think it's just like a completely horrible category error.
And you see it over and over again in Silicon Valley.
I think they think oh, we're gonna make this new Starbucks dollars or Apple dollars or something, but it just it doesn't work.
I mean payments it payments rails is one thing, right?
But actually making an actual currency. Maybe I'm being stupid because this is dollars.
I just realized I'm talking nonsense.

Anon: This is about dollars, but anyways complicated story Gift cards right if cause is a fascinating point.

Adam : Yeah, I've always wondered about that maybe we should have another like talk about gift cards because just think it's a fascinating side economy.
Of course, you've already given us a big talk, but from one angle, you know?
So, yeah.
Yeah, Amazon gift cards.
But in a sense, what your company does is it's a connection between the gift card economy and our economy, right, the Bitcoin economy.
But there's that whole, like, even if you threw Bitcoin out the window and just asked yourself about this gift card economy in the world, it's fascinating.
Anyway, yeah, so what I was saying about currency is nonsense, because this was about dollars.
They were, was it euros?
Oh, the euros didn't exist until 1995.
Was it guilders or was it dollars?
See, I don't know much of the history, but this is fascinating.
Read about the politics of DigiCash, why it all sort of went off the rails.
I loved it.
So I recommend that article.
Also, Aaron Van Wirdum wrote a write-up about sort of the intersection between eChash and cypherpunks.
I think at some point he was gonna write a book about it.
I don't exactly know 

## Laissez faire city / Digital Monetary Trust

What happened with that?
But he's really interested in this whole history as well.
And there are lots of other weird little details, like there's the story of, what was it called?
I've forgotten the name of it.
There's this organization that was set up in Puerto Rico.
Yeah, was it that one?
Yeah, Laissez-Faire City, that was it.
Laissez-Faire City, and this guy is writing a, did that, where did that?
Fourth?
Thank you.
I mean, this is not, I'm gonna go through this now.
But this one, I'll tell you what happens here.
These people are trying to set up a kind of a, what they call a laissez-faire city.
And part of that.
Yeah, part of that was something they called the Digital Monetary Trust, which was an attempt to create a kind of, well an element, a part of it was like an eChash system that was developed by this guy, J.
Allingrab, who has some incredible old writings on the internet, except a lot of them have disappeared now.
One of the articles in particular is called "The End of Ordinary Money",  which I particularly recommend.
And yeah, that all went kind of wrong.
And you often see this kind of story with these little libertarian experiments and they all just kind of collapse.

## Open Transactions

There are several examples of these.
And we've got things like open transactions.
Very few people remember this nowadays, but in the early days of Bitcoin, I'm talking about 2014-ish mainly, several of the prominent Bitcoiners were really interested in trying to create a financial cryptography library so that you could do things like create eChash tokens of the ones we've just described, as well as, you know, move Bitcoin around, as well as have accounts for various things.
And they also talked about Ricardian contracts, so a certain kind of smart contract.
They had, and that project still exists.
I mean, I actually checked last week, and Justice Ranvir is still making contributions to open transactions on GitHub.
So there were other ideas, True Ledger, Bill Sinclair, and there was Luka by Ben Laurie.
And we're gonna see shortly that the idea of Luka is still being, the same kind of idea is still being used today.
All of this stuff was like in the background.
You know, in a sense, if you look at all this history, one of the things you start to ask yourself is, yes, a lot of people have tried this, but nobody's really succeeded, so it comes back to that question at the beginning.
Why hasn't this taken off?
I mean I know people offered answers before but if you want to offer new answers...
I mean, back in the day, this was 1995 or something.
Some of them, yeah.

Anon: You should have needed a massive database to control the coins. And there was no technology at that time for that. Now you have, kind of, a million or something. But it was kind of, and on the other hand, if you were a small shop or something, you need an immediate connection to the central database, right?

Anon: This online and this, yeah, exactly.

Anon: And there was no Internet back then for that kind of traffic.
It should be noted, though, like in that period, if we're talking about let's say, 92, 93 through to 96 or seven or so, that people were already starting to make transactions on the internet, but it was slightly before SSL1, so people were actually doing things like, you know, mailing checks or sending wire transfers and you know, for things like porn, obviously, it was the first thing people paid for on the internet.

Anon: 18, still like connections.

Adam: Yeah, I mean, people could, I mean, I think it was, I think it was mainly things like computer games, porn, and I don't know, very scams and things.
What would you expect, right?
And it was, I can't remember, I think I might have paid for a piece of software over the, like paid a wire transfer or check or something.
But people were doing that.
And then SSL1, I wanna say was like, does anyone know, was it like 96, 97, 98?
Anyway, it was very badly insecure.
But around that time, the financial sort of system started to say, oh yeah, we actually could maybe support credit cards on the internet, actual payments on the internet.
What's my point?
I don't know.
Yeah, so what's the practical reasons why, why do we think all these various ideas, including these early 2000s ideas, oh, we also didn't mention 

## Hal Finney's RPow

How Finney's idea, which was our RPal, which was sort of a step towards Bitcoin, where he was saying, you know what, if we had some kind of trusted hardware thing, we could actually use the work done by the hardware as a kind of currency.
But that's already branching off into this whole direction that Bitcoin ended up with, right?
It was more of a cypherbunk thing, which was how can we make money independent of the state or independent of any company or any centralized entity.
People were trying to figure that out.
But at the same time, people were also trying to use cryptography to make these more centralized systems.

Anon: But is that maybe the main reason that people are centralized?

Adam: Yeah, that's honestly my main sort of takeaway, I think.

Anon: If anything is...

Adam: Centralisation is sort of cancer to this kind of thing.
Maybe, I don't know.
Yeah?

Anon: Could it also be that, just thinking of the counterfactual, how well Bitcoin has done in comparison, that Bitcoin has a sort of inherent bootstrap like dynamic to it, whereas there's no like massive draw to go into this because the whole point is you're getting a token that's exactly equivalent to what you've got.
Adam: It could be already, it could be a dollar, it could be, it doesn't have to be to be clear, all right?
I mean, you could make a token, I suppose I just think there's games you can play.
It depends exactly what is the mechanism by which issuance occurs, right?
But I think your fundamental point is valid.
I think we discussed it earlier, this issue of issuance, which is, if we're talking about a new currency, then we have a real issue around issuance.
If we're talking about just a payment mechanism, then you could still make your point, which is it's still less interesting because it doesn't have any exciting bootstrap element to it.

Anon: You could use it to represent a share in the eChash company, for example, and then you've kind of got a bit of that.

Adam: That's another thing you could do, that's a good point.
Yeah, yeah, I think some of these financial cryptography libraries like True Ledger, I don't remember exactly which ones, but had that kind of idea in it as well that you could...
So, there's a lot of ideas here we could play around with, right?
I mean, it's interesting, Maybe we'll talk about that a bit more as we reach the end.
Like practical limitations, maybe how this might actually work.
I was just thinking, not only side chains, but also lightning have that problem.
They don't have a new thing to issue.
So I don't know how successful we consider Lightning to be, but if Lightning is successful, you have to ask the question, well that didn't have like a cool bootstrap thing, but somehow that is working.
So there's a lot of weird questions, I don't know.
I'm just thinking out loud.
Just briefly.

Anon: So it just doesn't seem to have any of the, or most of the main properties that make, have made Bitcoin successful.

Adam: What doesn't, what doesn't have the properties?

Anon: eChash.

Adam: eChash, right, okay.Yeah, yeah.

Anon: But it had some trade-offs with the privacy and whatever, so.

Adam: Yeah, but I'm saying that maybe it didn't deal because the privacy in and of itself alone was not enough of a value proposition.
I think that's an important observation, isn't it?
Maybe, that everyone likes to champion privacy, but does it, if you make a system whose principal advantage is privacy, do people actually use it?


## Compact eCash

So compact eChash, I suppose this is much later, no, it's 2006, so we got Lissiansky and Kamenich.
So this is, I don't know much about this, I just briefly scanned it, to be honest, but I think this is just another technical improvement where they're trying to say, we can make this kind of system more scalable.
Compared to previously cash schemes, we can make a whole wallet about the same size as one coin.
So I suppose it's an important observation here that I think somebody over here made, that in the early versions of these schemes, could they really have handled millions, tens of millions, billions of individuals of these token coin things?
That would have been very hard to do on a database.
So in that sense, this is a probably significant finding, but here we're starting to use bilinear pairings, which we're gonna mention again in a minute, which is a more sort of sophisticated cryptographic construction.
And for some reason, I didn't actually get into it in the paper, it also uses the strong RSA assumption as well as bilinear pairings, but anyway.
But it's also still in the model of, remember we talked about online and offline and we said you might be able to do offline where you could prove double spending after the fact, but that's kind of yucky because then you need to somehow know who to blame.
So I think they were probably still in that model as far 

## Why you need identities to blame?
As I understood from briefly reading it.
Just to mention, I'm sure most people don't know, but Matt Green is a cryptographer.

Anon: Why do you need to know who to blame?

Adam: Because what does it mean to blame someone if every single issuance and spending event is anonymous?
And I say...

Anon: Just don't know if I have a payment or something...

Adam: Oh, I see.
No, but the problem is that you'd have to be after the fact, right?
Yes, if I pay you with a double spent coin and you've given me the car then you're screwed.
Yeah Yeah, it means there's a consequence exactly but a consequence for who is my point so that the model of the example the adversarial example would be I pay you $10 and then I pay Alex $10 two minutes later for a coffee with the same coin.
He gives me the coffee and then after the fact, maybe 10 minutes later or whenever, I don't know when, he finds out that coin was actually double spent.
Well, it's too late, right?
But if my account is registered, and by doing that illegal event, I've revealed myself.
So I could be private before I did this, but after doing that, my identity is revealed and the connection is made and the bank can say, you're a criminal and block my account.

Anon: But I just published something with my transaction that goes through the global cost of network, and then you see that the coin's in the double spend.

Anon: But there's a bit of conversion.

Adam: You're literally going into a distributed system again, yeah, yeah.
Yeah, you're back to solving the double spend problem in the no trusted third party case, which is exactly what bitcoin is.

## Mathew Green's eCash blog post 2010

Yeah, yeah, yeah.
Okay, good.
So, this is a really good blog, but it's more of a cryptography blog, but at least in this particular, yeah, in this particular post, Matthew Green is a cryptographer at Johns Hopkins, how do you say it?
He goes a little bit through the history of eChash designs there.
So for the more technically inclined people, well you might already know it.
If you didn't know, he does some nice write-ups, very occasionally.
And this was actually written around late 2012, and he was, it's interesting, he goes through the various old eChash designs, and at the end he says, oh, and there's this new thing, Bitcoin, this is 2012, right, there's this new thing, Bitcoin, he says, this is really cool, interesting, But there's one thing I really don't like about it, it's privacy properties are terrible, right?
So of course he's right, and then of course, a year later he's one of the key drivers behind Zcash.
Well, the original paper was called ZeroCoin, I believe.
Yeah, in 2013, and then it developed from there into eventually what became Zcash.
So there's Chaumm again.
Anyway, it's a pretty good article.

Anon: It's supposed to be like an extension of Bitcoin, initially.

Adam: Well, it was built on Bitcoin's code base initially and it inherited many properties, for example, the UTXO model, but obviously dramatically changed because they're using this kind of a zero knowledge, or ZK-SNARK specifically, a zero knowledge proof system to sort of Prove that a coin that is presented is valid but not say anything about where it came from Basically something like that is kind of all right.

## Schnorr Blind Signatures

So what about?
Some this is gonna get a bit more technical now some some problems with these systems Now we talked about RSA and we did briefly talk about Schnorr in the context of brands and stuff.
I think most people here have some idea about digital signatures and about what Schnorr is.
This particular page, I just chose this one because I thought Nadav Cohen, he's got some good, again, cryptographically orientated write-ups, and that's a write-up specifically of the blind signature protocol for Schnorr.
I actually pulled this up because it's from some paper, I don't even remember which paper it was but It's a pretty good Summary of the idea and you know, this is gonna pass a few people by but just just bear with me I know some other people Will be happy with it.
The basic schnor is, where's my pen?
Where's the black pen?
Lost it.
The basic schnor is kind of, in the interactive, in the ID protocol form, what am I doing here, S.
There's a nonce and then there's a challenge and then there's a response.
Okay, I don't wanna go through every step of this, obviously, but the basic idea with blinding it is that you want to make it so that at the end. Yes, it's probably better to go backwards from that from the end to the beginning I just me a finger at the end You want to return something that looks exactly like a Schnorr signature.
But you wanna make it so that the challenge, which is formed from, oh.
The challenge, ah, which is formed from the nonce and the message that you're signing, you wanna make it so that that's blinded.
So see here, C plus Beta means that the challenge in the Schnorr protocol, yes, it's derived from the message, but then we add a random number so that actually when the, well, it says server here, so the signer.
When the server sees the challenge, it can't see anything at all about the message.
Yes, it's the step where you, yeah, instead of handing over your message to get signed, you hand over the envelope, and he signs on the envelope instead of signing the message itself.
Yep, exactly, so that's what's going on there.
So you send this blind, effectively, let's keep it simple, you send a blinded message to the server, the server signs the blinded message.
This is Exactly the formula that we have for Schnorr signing, S equals CX plus R, except these bars indicate that these are blinded values, yeah?
Well, let's say, sort of.
And then, but you know what's interesting about this diagram, is that this illustrates an interactive protocol, right?

In other words, on the left side, just ignoring all the mathematics, on the left side it's user, on the right side it says server.
Now when you pay me some Bitcoin you sign your transaction right?
Do you have to interact with anyone to sign that transaction?
No, you just use your private key.
Right, so the idea is that when you take this Schnorr, let's just call it this interactive Schnorr protocol where there's two people talking to each other.
The Schnorr signature converts that into a non-interactive protocol where you sort of basically you pretend that the other side of the conversation is there when they're not actually there.
And it's really weird.
I know you you basically write, you know this and I'm gonna ignore key prefixing for the for the geeks out there, sorry ignore me so you you this thing here is the e and you calculate yourself without talking to the other side. Yeah, that's the non-interactive version of the Schnorr protocol.
That's what a signature is now. This is different isn't it because in blind signing that wouldn't even make any sense right?
I'm gonna blind sign my own message Huh?
Right you want somebody else to sign your message, so it's intrinsically an interactive thing.
I just realized that like, Tom, you guys literally do blind signing, right?
Please interrupt me if I'm making a mistake, Yeah?
Okay, because honestly, I don't really, I've basically almost spent no time looking at blind signatures.
Just recently I have a little bit.
But anyway, it's intrinsically interactive.
And of course that means it's not the same as a system where if I sign something and give it to Tracy, Tracy can then give it to Alex and it's still the same signature, it's still validatable, right?
That's not really true with a interactive process.
Anyway, maybe none of that is interesting to you, I don't know, but at the end of the day, you end up with a thing, this RS, which is a valid blinded signature on your message M, which you can then unblind, okay?
But in itself, it's just a short signature.
Now, but the interesting thing is that one of the reasons I wanted to mention the technicalities here, maybe that yeah, I don't know whatever one of the reasons I want to mention a little bit the technicalities is because it turns out there's actually some fairly serious security concerns with that.
Do you agree, Tom?
I'm just curious, because I mean, I've obviously just looked at it a little bit recently, I don't really know, but the Wagner's attack and the ROS, more recent paper on it.
Okay, let me just say what I'm gonna say, you can tell me if you have any comments, yeah?

## Wagner's attack & The Birthday Paradox


There is such a thing as called Wagner's attack, which is really like a really clever way Does anyone know what the birthday problem is?
Sorry, does anyone know what the birthday paradox is?
That's a better question.
What's the birthday paradox?
Exactly right so What's the birthday paradox?

Anon: The fact that if you choose a random ten people, out of them there's a high chance that two will have birthday the same day.

Adam: Exactly right.
So this is normally a bad paradox.
Yeah, yeah, yeah, absolutely right.
Yep, true, but no way.
So I'm going to pretend there's 23 people in this room, but I didn't count but it's pretty close If there is 23 people in this room What's the chance that two of them have the same birthday?
What is your what is your intuition tell you?
Right low as in what?
10% 5% any other takers What's that It's around 50% But is that your intuition or is that your knowledge?
It's my knowledge.
Yeah, exactly, right?
Because your intuition tells you you should be pretty low, and your intuition's wrong.
And basically, okay, I'm not going to give a whole like maths lesson about that.
Basically, You should think of it this way. The chance of collisions collisions or matches between things in big groups is more than you think. And it turns out with Wagner's attack What they do is instead of analyze the case of let's find two things that are the same, or another way of saying that is let's find two things A and B such that a minus b equals zero.
It says let's find four things, or five things, or six things that add up to zero.
So we want to find a very simple linear relationship between n things or k things.
They call it the k-sum problem.
And it turns out that the k-sum problem is remarkably easy to solve, even for very, very large numbers, like outputs of hash functions.
All right, So if you want to learn more about this, you can read my blog post here, which goes into it in great detail, maybe excessive detail.
But basically the purpose of this blog post is to go through Wagner's paper.
In 2002, 2003 he wrote a paper explaining how he showed an algorithm for solving that K-sum problem in a surprisingly low amount of computation considering what you might expect.
Now why am I talking about all that?
Well it turns out that you can use that kind of reasoning to attack protocols like this Schnorr blind signature protocol and you can get, you can basically crack keys with it much more quickly than you'd expect but only in a very specific situation which is a situation where you're doing lots of signatures in parallel.
You can easily imagine this case.
Suppose I'm a mint and you're all my customers and you're all sending me blind signatures all the time.
Now I'm not exactly sure how the attack would work, but I'm very vague on all this stuff.
But generally speaking, there's a situation where if lots of these signatures are happening all at once, then it's a lot less secure than you might imagine.
And in fact, this recent paper, no, That's the Wagner's paper.
Where's the?

Anon: It says 2020, so the bottom of your screen.

Adam: There it is, thank you, you're right.
This one here, even goes as far as to say, okay, we took Wagner's idea, we made it even better.
Actually, there's a whole history here.
Schnorr wrote a paper in 2001 attacking his own scheme. But but in in this paper there they claim to be able to attack like full-on like 256-bit security with like 200 parallel signatures or something like it's ridiculously. It's very scary stuff, but only in the condition where you're doing the protocol, this kind of, you know, this protocol, the user server protocol, all at the same time, right?

Anon: Presumably the same property. 

Adam: Presumably, yeah, but In the Mint case, it would literally be as a, yeah.
Good point, I must be, yeah, all related.

Anon: Or at the same time.

Adam: Yeah, good question.
Because if you look at something like this, the basic, I mean, avoiding all the details, basically what you're doing is one side creates a nonce, the other side sends back something in response to that nonce.
So if, imagine, I'm not exactly sure how this works, but imagine this side, yeah, this side must be the attacker.
Yeah, it must be.
This side is the attacker.
They have to produce this.
And this guy's producing nonces.
Now, if he's doing that hundreds of times, so you start the protocol with him 100 times, he's producing 100 of these nonces.
And you somehow arrange this equation.
And specifically, what you're attacking is this.
We'll come onto this in a minute, you're trying to create one more coin than you should.
Because think about it, remember the basic principle of the system is, you don't know what message you're signing, but the fact that you signed it counts as one coin.
And so if I get you to output 101 coins from 100 parallel signing sessions, I've broken the system.
So actually this is not key breaking.
I don't remember the details here, but that's the basic idea.
And the reason, yeah, I don't think this is discrete log break, but I now remember.
Anyway, so that brings us onto, so I wanted to mention that because I think it's really important to understand that some of this cryptography is not trivial at all.
And I think this kind of problem has been understood for many years.
For example, in music, it's been analyzed to death over the last five or six years, this same kind of problem.
And people have known since the early 2000s that there is at least a question around the security of blind signature protocols.
I know, I remember talking to nothing much, the Wasabi cryptography guy, you know, about this.
Yeah, well, X, indeed.
About this and, you know, people are aware of this problem. 

## One-more-forgery EUF-CMA (Existential Unforgeability under Chosen Message Attack)


I'm not presenting some new information here, okay?
But it also brings into focus, before we start talking about Cashu, this idea of what the security is.
So I wanna write that phrase.
Yeah.
Because think about it, right?
What is your principal concern?
One more forgery it says.
What is your principal concern about signatures?
Like if you think a signature is secure or not.
Your main concern is can somebody forge it?
You understand concept forge?
Obviously with a physical signature that's silly because they're just silly.
They're just anyone can copy anything, right?
But with a digital signature we expect that nobody can produce a signature without having the key right?
That's the main thing we're hoping so that's the the concept of forgery and we want we want forgery not to be possible and in fact. In the literature, they really focus on this concept it's a pretty. It's a pretty obscure technical name.
EUFCMA means existential unforgeability under chosen message attack.
Particularly that second part of it, chosen message attack, it's illustrating how seriously they're analyzing.
What they say is, okay, the attacker can actually ask for a signature on any arbitrary set of messages he likes, well, basically.
And even given a bunch of signatures on messages that he's chosen, he still can't make another signature out of all that information.
So we're quite aggressive in trying to ensure that signatures can't be forged.
But with blind signatures, that doesn't make any sense, does it?
Think about what I just said.
We wanna prevent that anybody can create a new signature on a message when they don't have the key, even if they've got lots of other signatures.
But do you see why that doesn't make sense with blind signatures?
That security model?
In a blind signature, can I get you to sign a message, can I make a signature on a message that you haven't agreed to?
Yes, that's the whole point, right?
The absolutely essential purpose of a blind signature.
Again, please correct me if I'm wrong, the experts in the room.
The whole point of it is that you sign a message that you haven't chosen, so this concept doesn't really apply.

So instead, what they come up with is a new security model.
They call it the one more forgery Model and so instead is a similar one for discrete log the one more discrete log problem and the idea here is that. You can I can get you to sign anything I like, but I can't get you to sign 11 Signet I can't get you to make 11 signatures when I only are when you thought you're only making 10 Let me put it like that?
Does that make sense?
Yeah yes, so in a basic signature the problem is you don't want somebody to sign to get a signature on a transaction spending your coins, without you without your key. Here we just want you not to be able to get more signatures than the the signer thinks he's giving you.
Is that the right English?
I think that's the right English, yeah.
Oh. Right, so in your envelope, Mm-hmm, mm-hmm.
You have two sheets in there, and it's sort of a signature.
Yeah, I think that's right.
Yeah, that's a good attack, yeah.
Yeah.
All right, so let's start talking about, maybe that's not a very good lead in, but anyway, let's start talking about these new designs that we've been seeing discussed recently.
Actually, I'm not even sure, maybe I should start with Fedimint and then do Cashu because I don't know, there's no particular logic to this.

## Cashu


I'll just present the information and then you just interrupt me when you like.
So Cashew is actually not using Schnorr blind signatures that I've just shown you, nor is it using RSA, which was the way old thing that David Chaumm originally was working on.
In fact, this is using something kind of similar but also different.
The original, as far as we know, the genesis of this was a post on the Cypherbunks mailing list by David Wagner.
And in the post, interestingly, he says, here is a proposal for basically a blind eChash scheme which doesn't use RSA.
Now, Why did he not want it to use RSA?

Anon: Patents 

Adam: Yeah, surprisingly it wasn't because RSA is shit which may well be a good reason But specifically because he said or there's some ugly patents around Chaum has around RSA so here's a suggestion to do something like this eChash token, but using what's called Diffie-Hellman key exchange.
Do we know what that is?

## Diffie-Hellman key exchange

Yeah, anyone want to explain Diffie-Hellman key exchange?

Anon: Well in a simple way, it's pretty much like, usually you want to, so the thing is like, you are an individual here there and I'm an induvidual here and we want to exchange information right most of the time and the problem is like when we exchange the air between us or the wire or whatever it's kind of it's going to be exposed right so what we do we kind of put a number here in the middle that is public, okay, and everyone knows, like 7 or something, and this is not actually how it works by the way.
And then we have our own numbers, okay?
And we kind of multiply, we each have our own secret number.
We multiply our secret number with this number that is public, and we exchange this.
And kind of like that.
Anyway, the basic idea, from the zero sense, the basic idea is that you have something that's public, and we each have our own secrets.
And with this, we can construct some secrets that we can secretly exchange information.
I don't know if that makes sense to anyone.
That was a very bad way to explain it, I'm sorry.

Adam: It's just, it's hardly easy to explain, is it?
Yeah, I'm, the, you know. We're all used to the idea of Alice has got her private key, she multiplies it by blah blah blah, she gets a public key.
We all know private key, public key, yeah?
So if two people have a private key, public key pair, so Alice has public key capital A, Bob has public key capital B, they either way, they can do an exchange, or it's just gonna be a one-way transfer where B can send or Bob can send B to Alice and Alice can calculate A, B or Alice can send her public keys.
Notice you can send your public key, not your private key, obviously.
And as a result, you can calculate a shared value.
Okay, so that's often called a shared secret.
Notice it's a bit confusing from our framework in our heads of public key and private key.
This is a public key because it's a scalar times a point, so it's actually a point.
But b, Little b times capital A is the same as little a times capital B.
That's the same point because in both cases It's actually little a times little b times g so by the Commutative property of scale of multiplication right That means that's the same as that.
In presenting like that, it's really simple, but it's actually incredibly important in the world because a lot of stuff that goes on on the internet works on this principle because when you set up a client-server relationship on the internet, a TLS client-server relationship, you have to decide on what the secret key is that you're gonna use to encrypt your communication, and you deal with this kind of thing usually.
I mean, I don't think it's always the case, but you usually use elliptic curve Diffie-Hellman, ECDH, if you go into your browser somewhere you'll see a list of cipher suites and it'll say ECDH, blah, blah, blah, blah.
There's a very commonly used protocol and what Wagner was proposing was that you can basically, and I probably don't want to go into the mathematics, right?
But you, oh, you know what I can do?
I can show you the basic protocol summary that was created recently by Calle, the guy, this guy, CalleBTC, who, I've opened everything like four times at this point, but I'm just gonna open it again because it's easier, there it is.

## Blind Diffie-Hellman key exchange

Yeah, this is actually, this notation is actually due to me because Ruben's original description was really difficult to read, so I rewrote it.
So basically, the only difference to what we just talked about already is that the blind, it's the same principle.
You have a secret, just like we said, secret in the envelope, sign over it, right?
You put your secret inside an envelope by adding a tweak, what's called an additive tweak.
We add another point, which comes from a random number R, and that's what you send to the bank or the mint, who in this case is Bob.
Bob then takes his private key, the private key of denomination $1, whatever, oh no, one bitcoin in this case, little k, multiplies your blinded value by that.
So it's not a signature, but it's functioning very similar to a signature.
When you receive it you can subtract off little r times K which takes off the blinding and what you get back is something that's verifiably something that the bank signed, this value Z.
You can work through it, It's very simple mathematics.

And then later, you can take that pair, or the secret, with the Diffie-Hellman key output and give it to the bank as a coin, and it's blinded and he doesn't know that it originally came from Alice because he never knew this value, r.
I don't know why I'm explaining this to you really, it's just this is the same kind of thing, but it's just done differently.
How secure is this?
Well this is based on, this is reducible, I think, to the computational Diffie-Hellman assumption.
Technically, I think it's reducible to one more Elgamal decryption.
One more forgery or one more something else.
We have several of these.
Yeah, we say, again, we can't reduce this and say, this is an unforgeable signature because the whole point is nobody knows what the message is.
What we can do is somehow by various magic try and convince you that if you can create a false coin, in other words an 11th coin from a list of 10, then you can do something similar with an already known cryptographic problem, such as Elgamal decryption is the specific one in this case.
Now, why all this technical stuff?
It Turns out that actually, and this I think is quite interesting even if you don't know the cryptography, that the, well I'm on the wrong page, is that it's actually very closely related to something called privacy pass.

## Privacy Pass


Does anyone know what privacy pass is?
Wow, nobody knows.
I'm surprised about that.
I actually used privacy pass briefly.
If you use Tor, has anyone used Tor for just like generally browsing the internet?
Not just, yeah.
You encounter any problems with doing that?
I'm talking about speed.
There's another problem you encounter if you do that.
Like what?

Anon: The capcha.

Adam: Capchas all the time, right?
And yet you haven't heard of Privacy Pass.
You should have.
Well, because Privacy Pass was an attempt to solve that problem.
I did actually use it for a while, but I don't know how much it's caught on.
And it was, here it is, related Privacy Pass.
So Privacy Pass, This is the paper by Ian Goldberg, but what I really recommend you read if you're interested in this stuff Is this not just for the protocol itself, but for all of these protocols.
This is a brilliant way of explaining it Yeah, I've got it here.
This is a brilliant way of explaining the product I really recommend you read this if you're at all interested in just like learning the basics of the cryptography here?
Okay, what does it do?
So yeah, you're right, I interrupted myself.
So basically, the idea is I have to do a capcha.
If I'm On tor, then websites are suspicious of me and I don't have an identity that they can look up, so they keep asking me to do captures over and over again and I can't even get on with my day.
So the idea here is you do capture sometimes, maybe once, five times, 10 times, I can't remember how many times.
And PrivacyPass gives you a token for having done the capcha.
It gives you N tokens, I can't remember how many, it gives you a lot of tokens.
And you're allowed to then spend those tokens to then view websites in the future.
So they're making a, It keeps your privacy because when you spend those tokens, they're blinded just like these eCash coins are.
But they're supposed to notionally prove that you have actually done those captures in the past.
Make sense?

So you can see that the goal of that system is very similar to eCash tokens, but it's actually slightly easier because they can.
Yeah, you don't have to transfer them, right?
You know, the user never have to transfer them between each other, so they only have to talk to a server.
So it's a really cool idea, and It was implemented as a, literally like a browser extension and it would just do it for you.
You didn't even have to do anything, it was just there.
But the interesting thing about that system is it's exactly the same equations that we've just gone through.
It's a blinded Diffie-Hellman key exchange.
There's like one extra feature, one minor difference, but it's basically exactly the same system.
I've listed like how it's different here, but you probably don't care about some of those details.
So privacy, pass, and Cashu are both based on computational Diffie-Hellman.
Again, it comes back to that thing that if you're convinced, which I don't know whether you should be or not, if you're convinced that given that public key, Alice's public key, and it's public, so that's, you know, and you're given Bob's public key, if you're convinced that you can't then calculate the shared secret without knowing one of the private keys, that's the computational Diffie-Hellman assumption.
In other words, the inability to compute the Diffie-Hellman secret from the individual keys.
So if you're convinced that that is a sound assumption, then more or less you're convinced that these are protected against one more forgery style attacks where more coins could be created than should have been created.
But of course, that's only one aspect of the trust in these systems, right?
Anyway, there's some technical stuff there.
So Cashu is like a new project.
I mean, I spent some time talking to the developers this last week, and they're just kind of coming up with it right now, I mean, it's very new, and it's just very bare bones, I would say.
But at the moment, it's just at the level where, as you can see what I'm doing on the command line here, you can just try to mint coins.
Of course, what I haven't mentioned yet is with these new systems, CashU, Fedimint, which we're gonna start to talk about now, what they're trying to do is create a kind of a Bitcoin eCash token.
And what they see is an ability to leverage things like Lightning so that, yeah, you could, and probably you will be able to, mint eCash tokens from a direct on-chain payment, but it will make a lot more sense to mint eCash tokens from a Lightning payment.
So if you send Cashu the instruction mint 420, it will send you back a Lightning invoice, a Bolt 11 invoice.
Then you have things like send, receive, and split command.
We talked about split earlier, so if you have some coins, you can split them up.
You can see, here it says I've got 118 sats in five tokens.
Why did it say, whatever.
Anyway, it's very, very new, okay?
So they're still working through protocol documents and they're trying to figure out how to do it.
I personally think, I mean I don't know how much it matters to be honest, but I personally think they might have been better off just slightly tweaking the construction to be the same as privacy pass because it's a little bit more well analyzed than the system that they're implementing right now.
But that's a technical detail.
I think what they're just going for there is something very simple, where you can just run it easily and connect it with lightning.
But who knows, maybe it might develop into a much more advanced system in the future.

## Fedimint


I think it would be instructive if we then compare it with Fetimint, this is a project that's been going on a lot longer, at least in conceptual phase, by this guy, elsirion, mainly, but I don't know who else was involved in all the setup.
There's a lot more stuff here, right?
There's a website with documentation.
Why have I got all these things open?
There's a website with documentation.
It goes through all kinds of things at both the non-technical level and to a much lesser extent, the technical level.
Actually, getting the cryptographic information about it is not so easy.
But if you're not analyzing it as cryptography, there's tons of information.
For example, here, They go through several possible trade-offs of their system. So I suppose I should now start explaining how Fedimit works, but before I do do people. Anyone here want to take a stab at an outline of Fedimit?
Just general outline of how it works here.

Anon: So that people who are not so acquainted to bitcoin. Can secure their bitcoin though a multi signature. So that they don't have to have too much personal responsibilty.

Anon: Okay, there's a multi signature, yeah. So the 

Adam: Yep, yep, yep, That's the start of it, the multi-sig element.
So Let's just go through, because there's so many parts to this thing.
It's a huge beast.
So at the root of it you have a federation of what are called guardians.
So imagine it's, I don't know, nine people, just for example.
You're gonna have to trust them in the same way right at the beginning of this talk we talked about trusting the mint.
You're gonna have to trust this federation of nine people, but with the caveat that there's a threshold.
So you might have to trust that five of nine of them are doing the right thing.
So if one of them goes rogue, you should still be okay.
Or if one of them goes offline, you should, or dies, you should be okay.
So there's a federation of people, they control the multisig that you mentioned.
The multisig controls the Bitcoin funds, right?
And you will be able to deposit into that multisig, and there's like clever tricks around how you do that, but that will entitle you to get some of these eChash tokens, right?
And then there's these eChash tokens, but actually you're more likely to be paying for it with Lightning.
I wanna mention, maybe it's better to have this picture to start with, yeah.
It's a simple picture, but, oh by the way, D, I hope you don't mind, I copied your, I checked it didn't have any identifying information before I, yeah, yeah, yeah.
Oh yeah, yeah, pay to, yeah, whatever.
So, I mean this is just a very simple web app that somebody threw together.
It's not like the final product.
But the purpose of me showing you this is to say that to the users, however complicated this is, and it is complicated, the interface should not only be simple, but it should also be very reminiscent of using Lightning.
Not only should it look like using Lightning, but also it should be possible, and we were experimenting, me and D and some other people were experimenting with this.
You can send Lightning payments to and from it.
You can send, you know, the idea is it's sort of transparent whether it's Lightning or these eCash tokens.
I mean, whether it's 100% Transparent is debatable whether that's a good idea.
But all right, so let's come back.
So we've got the multi-sig, we've got funds in the multi-sig.
The federation controls it, but they're threshold controlled.
Also, the individual eChash tokens that you're getting issued and then you're sending in this online model that we discussed.
All of that is an interaction with that federation.
So the sort of, actually I think I made a list here.

## Threshold Blind Signatures


The innovation that they're doing, yeah, here we go.
The innovation that they're doing is based around threshold signing, mostly.
It's the most important part because instead of having the mint just receive the blinded message and the signature. It's like five of nine people are doing that so there's some significant extra mathematics involved in getting that right. But they can do that, you do blinding as normal way, but there's another element to this that comes in because it's a threshold now. This is really interesting I think What is the problem?
What is the problem?
If you threshold sign a blinded message, there's actually a reason why, if you just do that without thinking about it, it completely fails, It's insecure.
Remember, the idea here is we sign a message, but we don't care about the message, which is secret.
We just say, oh, the key is for one coin, or the key is for two coins, or the key is for four coins.
So if instead of just me, the mint, signing those and keeping track of how many coins there are, I keep track of how many times I signed a coin, so if somebody tries to produce more than that, I'll say, well, that's not valid, yeah?
You know, the one more forgery.
But what if It's like two out of three people signing.
Do you see the problem?

Anon: Yeah, because I think the way Bitcoin works is you still verify that there are three signatures, and then you sort of use scripting to...Is that that reason why because you can't really. 

Anon: One of them could know either one of them is sort of seeing what's in the sequence there essentially point 

Adam: Okay, this is not that obvious,but I think it's kind of somewhat obvious when I explain it. So suppose you've got a federation with two out of three have to sign everything right in order for it to be valid the user a comes along and asks. Sorry, none the user is not a the federation is a and B and C and the user comes along asks a to sign m1. Careful asks a to sign m1 b to sign m1 and C to sign M2 at the same time.
Okay, so A and B have signed M1, so That's two of three, right?
So M1 is a valid coin.
But C hasn't signed the same thing.
All right, then user asks A to sign M2, B to sign M3, you see where I'm going, right?
And this second step, B and C have signed M3, creating a second coin.
But these two match as well.
So the user has three coins, not two.
So this has actually violated that security promise.
And you can see that the root of the problem there is that we don't have, we don't all know what we're doing at the same time.
We need some kind of consistency, just like we try to enforce with a blockchain.
We know the ordering of events, everyone agrees, this happened, this happened, this happened, this happened.
You need that here too, unfortunately, or at least something like it.
Not exactly what Bitcoin has, but you need some kind of consistency.

Anon: Why is this a problem?

Anon: Since it does matter how many signing evenets occur, because you still got a load of valid signatures.

Adam: Because remember the idea here is that it's not the message that counts is how many times we signed it that counts because every every time two or three people have signed a message, that's counted as one coin.
Now here, we've given the user three coins, but we thought they only asked for two.
There were only two signing events.

Anon: The signing events being people use some money basically instead.

Adam: Yeah.

Anon: Can you turn that into tokens?

Adam: Yeah, well I suppose the thing is, so at the end of these two sessions, so to speak, because this is these two lines of two sessions, user walks away being able at a later time to redeem three different coins, whereas the system thinks that only two coins were issued.
I mean, it depends on the details, but you can see at least it's possible this attack might apply.
So the upshot of that is that the system needs something like a BFT system.
In other words, some kind of consensus system.
This is called Honey Badger Byzantine fault-tolerant consensus.
Okay?
So I don't know how many people here have heard of BFT, but this is a thing that existed way before Bitcoin, you know, like 80s.
I think Leslie Lamport started it all off in the 80s, if I remember correctly.

Anon: Aircraft use the same type of algorithms to synchronize their sensors.

Adam: Ah, right, that makes sense, yeah.
There's any way you need some kind of synchronization across lots of computers, and you can't trust, I mean, some computers might be defective or they might be adversarial and trying to cheat.
So it doesn't necessarily mean like an economic situation where people are trying to cheat.
It might just be you don't trust them to actually operate correctly.
If there's any possibility of people operating incorrectly or if the timing, or I don't know the details, there's a lot of literature and theory around this.
But unfortunately, because we introduced a threshold, we introduced this possibility of a kind of inconsistency which you have to fix.
And they describe that in the documentation.
I should also mention, again, 

## BLS signatures

I'm in danger of boring people a little bit with cryptography, but it's using BLS signatures.
And they're a very different kind of signature than Schnorr. Basically they're based on bilinear pairings and without going into technical details because I would like to but I know it's boring the. The main properties they have is they're kind of like, in theory they're supposed to be very short signatures.
Actually I think they're kind of similar to Schnorr depending on a lot of details.
So we're talking about 30 to 60 bytes, so I don't know. It varies.
Originally there were proposals being even smaller than that but then people analyzed the security or whatever.
They're short but what's really interesting is that they don't use any old elliptic curve.
They have to use very specific elliptic curves to work.
So we can't just do pairings on Bitcoin curve.
It doesn't work.
They have that linearity property, which is really nice.
We use that in Schnorr.
But they're actually deterministic, which means you always get the same signature output for a message.
You can't just keep making new signatures with different values.
It's not usually important, but sometimes it is.
The most striking feature they have is you can just like take a bunch of signatures, multiply them together, and then store that, and then later when you wanna verify, you can just do the verification equation just multiply it together.
So you can you can have a very compact aggregated signature. The biggest negative they have is that specifically the verification Step is a lot more computationally expensive and the reason for that is that a pairing is basically. You've got two curves and you can easily calculate points on curves, we already know how to do that, but to actually do the verification, you have to do something called a pairing, which does a very complicated calculation, mapping from those two curves into a finite field extension.
It's a much bigger object.
And so anyway, there's a whole history of that.
That is, that's the only kind of obvious negative is that the verification is relatively expensive.
However, they are batch verifiable, as indeed is Schnorr.
So that can be useful in certain contexts.
I think I saw elsirion, like a tweet or something where he said, while I was doing performance analysis and I can see that actually there's quite a heavy computational load if we run this kind of system at scale.
I don't remember the details, so maybe you can look into that, it's interesting.
So you can do threshold signing.
What else have we not talked about in Fedimint?
You can see it's a pretty complicated system, but at the user level it's gonna be pretty easy, at least that's their hope.

## Lightning gateways in Fedimint


Lightning gateways, that's important, right?
D, what did we learn about lightning gateways?
Save me from talking so much.
What did we learn about lightning gateways?
In Fedimint?

D: Lightning gateways, I don't know, I can describe where I understand it. So Lightning Gateway is considered to be just like a normal user of the Mint. And they create channels with other users, like the Lightning Channel, I think it's called a Ghost Channel.
So instead of trading Bitcoin on that channel, you're trading these cashier, these tokens.

Adam: Fedi Sats.

D: Yeah, tokens.

D: And they allow you to then, you give a token to them and then they will make the Bitcoin payment on your behalf.
But because it's using the Lightning protocol, it's not like a custodial service where you say, I can please get this payment and they learn who you're paying, it's just as private as any nightly payment.
And I think there was also a relationship with the guardians, but I forget what the detail of that was.

Anon: They need to support HTLCs on the Federation.

Adam: Inside of the, yeah.
Yeah, within the logic of the thing.
Yeah, I was hoping there would be a, because they've got a nice picture that shows all how the pieces fit together, but it's basically like. There's the federation itself, and it has this multi-sig, which is five of nine or whatever it is, and the multi-sig has the BTC, the on-chain BTC.
The Lightning gateway then connects the federation, this is the federation let's say here, connects the federation to the outer Lightning network, other channels and so on.

And you've got the users here, you know, user one, user two, or so on.
And obviously they can request issuance based on paying in lightning or based on paying in on-chain. They can request issuance of tokens.
They get tokens.
They can pay each other with the tokens and or they can pay people outside on the lightning network. So the whole thing is supposed to be like everything can work, right?
Each user can pay each other, each user can pay a Lightning recipient, a Lightning user can pay a user like this as well.
This path is also possible.
I actually looked up the code references, it's on the gits but you don't need to look at it now, but they, as people were discussing here, it requires you to think about how do HTLCs work along a lightning path and then also along into a user like this.
And there's some subtleties there around, you know, the federation has this threshold key, and so, you know, for example, if this user wants to receive a Lightning payment but happens not to be online, then that's another complication you have to consider as well.
So you can see it's pretty complicated, but they're aiming to make it pretty much transparent between trading eChash tokens in their federation and trading Lightning or paying buying and selling.

## Risks and tradeoffs of Fedimint


What about, what about, what are the sort of risks here?
Because I mean, that's the page I've got open here.
What are the risks in this kind of model?
What are the problems?

Anon: The federation itself.

Adam: What about it?

Anon: You can have, I don't know, if it's five or going, you can have five actors.
Adam: All right, so just the basic principle of if a certain number of actors in the federation go rogue or are wanting to, let's say, steal.
I mean, let's be concrete, because there's more than one possibility here.
What could they do?


Anon: They could just stash their own 5 of them, you know, come together and just stash their own wallet.
Adam: The multisig wallet, be specific.
You mean the Bitcoin?

Anon: Yes.
Right.
So first of all, they could just take the Bitcoin directly.
They own the Bitcoin.
So this relationship here is custodial, at least within the threshold five of nine.

Anon: But three of them attack their own means to generate more coins or something like that.
Right.
Adam: So that's the other one.
I made the case on Telegram with some people.
I was saying like, well, actually, maybe, obviously, that's a big risk, right?
They just take the coins.
And just like if you put your coins in Coinbase, they might just walk away with the coins.
But what about if they generate tokens, right?
Inside the Federation, they've got the right to generate tokens anytime they want.
Are you gonna know about that?
So, I mean, I think there's a really interesting discussion there to be had about is there some clever cryptographic way to somehow audit the total supply of eChash tokens.
Because what you want in this system, this system is intended so that if there's 10 BTC in here, there's only 10 BTC at maximum worth, should be exactly I suppose, of eChash tokens sitting in user accounts.
But of course, we want all this stuff to be perfectly private.
We don't want the user to be able to know, you want to know how many tokens you too has.
So we have a conflict here, because we want auditability, but we also want privacy.
So how, at the moment, they've just got privacy.
They've got literally no auditability at all.
The Federation can just print infinite numbers of eChash tokens if they want.

Anon: So, yeah, go ahead.

Anon: I think they were trying to do something to make sure the user knows the guardians haven't tampered with the software?

Adam: No, at that level.
So have the software been some kind of constrained device so that it can't be, I know that model, because I remember that is a very interesting model.
I don't personally trust it, but it's a very, possibly it's interesting.
Notice of course, am I right about this?
Liquid has these hardware security models.

Anon: Yeah.
And RSK as well.
Right, so that we often, in fact, Mercury has something with hardware stuff as well, right?
Yeah, yeah, yeah.
Yeah, so we often see this happening in practice, don't we, that these systems, where there is a trust relationship, people try to use some hardware element to try and, hardware, I mean element in the general sense, to control, or to give, let's say, give better assurances that it isn't being abused.
But I personally, I don't know about you, I don't trust those kind of systems at all.
Like at all.
In fact, oh my God, I don't trust that either.

Anon: I have a question.

Anon: Sorry, really quick for example, that these holograms, they're merely to just improve the security of the Federation member.
They don't do any verification.
Right, that's what I was thinking.

Adam: They're just purely signing devices that- Yeah, they're just signing devices.
Just signing.

Anon: The idea is that no one can get a key, but I believe it has a box and you can sign over it.

Adam: Right, so there's no control over what is signed, it's just purely, just like an ordinary hardware wallet in that sense.

Anon: Yeah, yeah.

Adam: Okay, interesting.
But yeah, That's a very good point to raise.
Yeah.

Anon: So I was just going to mention, companies like Lennon, the IEO, do things like what people deserve, which is on a regular basis, they have a way to prove their amount of investment. You can use something to verify that whatever your point is, it exists in that proof without revealing it.

Anon: This was done for a long time in the beginning.

Adam: Yeah, it's very old, yeah.
It's a very old idea, but I was discussing exactly that on the telegram with the Fedimin guys, and I mean, they know about these, the old Todd Maxwell ideas of how you can make like Merkle trees with maybe Pedersen commitments and blah, blah, blah.
There's ways you can make it as sophisticated as possible, but it's very debatable how much of that could, I mean, elsirion himself told me that he'd studied it with Provost and Sjors Provost, and they don't think there's actually a way you can do that in this kind of system.
But I still think there might be something we can do.
Anon: That's interesting, I think I asked that question on Twitter.
Adam: Yeah, but think about it, it's not the same, because when you, Is it not the same?
It's a very complicated area.
I don't have answers, but I know it's a very interesting point to raise.
So before we go, because we're running out of time, but yeah, go on.

Anon: So the thing is, what is. The main difference between this and Cashu seems to be that they have the Federation rather than whatever.

Anon: Yes.

Anon: What is the more of a trade-off because, again, this is just for now, this is like just a more complicated Ruge Goldberg version of the other one, but clearly I'm probably just misunderstanding.

Adam: No, it's a fair point to raise.
I think definitely...

Anon: What is the...

Adam: Definitely...

Hang on, hang on.
Definitely it's a fair statement that the main difference between those two ideas is the federation element.
I'm gonna be unfair in not remembering some other differences.
It's a much more heavily developed system.
It has a lot of developers who've been working on it for a rel, I mean it's still very new by the standards of most things, but compared to Cashu, which is just like one, basically one guy plus a couple of other guys over a very short time.
This is a much more developed system.
You mean architecturally?
You mean only architecturally, yeah.
I mean it is a different cryptographic construction.
I think they've worked out a lot of details that Cashu hasn't worked out.
That's the biggest difference I see, apart from the obvious difference, which is it supports federations.
Which sounds like just one thing, but as I've already explained to you with that attack, actually supporting federations in this kind of model is really hard.
They actually had to use a Byzantine fault tolerance system, consensus system to actually make it work.
So, you know, the use of BLS signatures, I don't know, it's complicated.
Don't have a simple answer, sorry.
Yep, it's just a mint at the moment.
I mean, I might change it, but that's all it is at the moment.

Anon: The whole idea is that it will be more scalable than lighting. I'm trying to understand what's the point.

Adam: Well, you might say what's the point, yeah, yeah.
But that's what we were discussing right at the start, wasn't it, remember?
Which is like, what's this for?
So, coming back to our start, it should certainly be more speedy, more reliable, and more scalable to make individual person-to-person payments within such a federation.
But of course, the fly in the ointment is within, right?
Well, I mean, that's part of the whole problem is how do you get the network effective like, and can you get the network effective?
Can these things, can an individual mint scale to a million users?
I think Maybe not, I don't think anyone's figured that out.
Maybe I'm wrong, maybe they have.
It should definitely be more private, even substantially more private than Lightning, but again, within the Federation.
If your Federation has 10 members, you have an anonymity set of 10, it doesn't matter how good your...
And the other thing I didn't actually mention, I should have, is a technical point, but it's something from the very beginning that people emphasized, is that this kind of privacy has a kind of perfect quality to it.

## Perfect Privacy


When you have your public key, or your Bitcoin address, and your private key, your private key is private, right?
It can't be deduced from your address.
But somebody with a powerful enough computer could deduce it from your address.
That's not the case with this.
This kind of privacy is sometimes called perfect hiding or perfect privacy in the sense, the simple example is. I give you a random string and I say I have a secret key and if you X all my secret key with my message, it comes to that random string.
Well, It doesn't matter how many computers you have, you'll never figure out my message.
Because for any particular message, there is a corresponding key.
Think about that, it's not an obvious point.
But, does that?

Anon: XOR, that's what.

Adam: Yeah, but people don't know what XOR or is, right?
So. One time pad.
Yeah, I'm talking about a one time pad, yeah, yeah.
But I'm just trying to explain it in a way that people might understand.
I don't know.
Some people know, but a lot of people don't.
You know, you have a string of random numbers.
Or just think of a random number, and it's, yeah, that's what I should have said, look.
You have your message plus a random number.
Now messages are strings, right?
Hello or whatever, but think of it as a number.
Add it to another number and you get some third number.
I made up that random number, so my message might have been 15.
I might have added 32 and Got 47, so I'm gonna tell you 47 and say find my message find my message. It's not just that you don't have a powerful enough computer.
You could never find my message, because there's an infinite number of possible messages with corresponding random numbers R.
So that's perfect privacy as opposed to computational privacy, because if you run a computer long enough you will eventually find my private key by just guessing because as soon as it goes for private key output correct address you know you've got the right one there aren't any others fundamentally different kind of privacy 

Anon: Yeah well if the random number isn't really random then you've you've you failed, yeah but if it is then you haven't. 

Adam: But also you're assuming a repeated gain model.

I'm not, yeah.
I mean, Fair enough, but in itself, the statement that I made, I think is correct, isn't it?
It's infinite possibilities, therefore you can't.
So, yeah.
Anon: Away from the, I'm talking mathematics, two questions about that. I was hoping, so, one thing I don't understand, maybe you do, about this, is that part of the point is to try and make it easier to custody stuff. Because self-custody is hard. And that's fine, it is hard.
Adam: We can talk about custody, yeah.
That's a good point.
But I don't get about why this is better than that.
Because you still have to custody all of these.
I don't think it is better.
I think fundamentally, I don't think it is better.
I think fundamentally, this is a bearer instrument in a slightly even more extreme sense than Bitcoin is a bearer instrument.
Because not only, like, I don't know if that's fair or not, but if I have like a bit 32 style wallet, I can just store one secret and it can control all of my coins and it can even control all of my history. But here every single coin is its own thing and by the nature of being properly private. It means that if I lose it, I can't go to the bank and ask for a new one 
Anon: That's what I was going to say.
It would work.
Anon: The whole point of Feddy is it's supposed to be a community of people that you physically know so that you...
Adam: That's how they present it.
I can work.
That's what they're pitching it as.
That's what they're saying.
Anon: So you could say, well, if I lose my phone with all my coins in it, I can go and ask them because I know who they are.
Adam: Well, then what's the point of having a...
Then I'm great.
Adam: What's the point of having a cryptocurrency in the first place?
Anon: Maybe that's why they're afraid of it.
Adam: Yeah, it is.
It is.
I know.

Anon: You can go to one of the guardians and then spend some QR code and your wallet will be covered.

Anon: But then it's just all actually working.

Adam: Yeah, but they could use encryption, right?
They could use encrypt, you could encrypt your backup with them.
I think I remember Obi telling me that idea.
Yeah, so I mean, I think it's kind of orthogonal, right, to this whole thing of how these eChash tokens work.
It's certainly true that if you have some kind of trust relationship, you can build better backup model.
I mean, yeah, Obi did tell a lot of things like this to me on the call.
He was saying, you know, he was talking about this classic question which is, you know, what happens when you die?
Are your coins just lost or do you have any kind of backup process?
And if you do, inevitably, he's claiming, it involves some kind of trust relationship.
So we're just, I mean, there's a lot of stuff in Fedimint, or let's say in Fedi as a project that isn't directly related to eChash tokens.
I'm just focused on that because I just find that interesting.
But I do agree that we could have had a two hour talk about that instead, but I personally just think this is more interesting, sorry.
No, it is interesting either way, yeah.
All right.

Thank you.

