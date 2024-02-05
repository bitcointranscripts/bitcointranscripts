---
title: "Open Timestamps: Leveraging Bitcoin's Security For All Data"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=hUFNqD3DWWQ
tags: ['proof-systems']
speakers: ['Sjors Provoost', 'Aaron van Wirdum']
categories: ['podcast']
date: 2020-11-06
summary: "In this episode of The Van Wirdum Sjorsnado, Aaron and Sjors discuss Open Timestamps, a Bitcoin-based time stamping project from applied cryptography consultant and former Bitcoin Core contributor Peter Todd. Open Timestamps leverages the security of the Bitcoin blockchain to timestamp any type of data, allowing for irrefutable proof that that data existed at a particular point in time.\n\nAaron and Sjors explain that virtually any amount of data can, in fact, be timestamped in the Bitcoin blockchain at minimal cost because Open Timestamps leverages Merkle trees, the cryptographic trick to aggregate data into a single, compact hash. This hash is then included in a Bitcoin transaction, making all of the data aggregated into the hash as immutable as any other Bitcoin transaction.\n\nTodd offered an interesting showcase of Open Timestamps earlier this week, as he proved that the public key used by Google to sign “the email\" to Hunter Biden indeed existed in 2016. \n\nAaron and Sjors also discuss some of the other possibilities that a time-stamping system like Open Timestamps offers, as well as its limitations. Finally, Aaron provides a little bit of context for the history of cryptographic time stamping, which was itself referenced in the Bitcoin white paper"
aliases: ['/bitcoin-magazine/bitcoin-explained/open-timestamps-leveraging-bitcoin-s-security-for-all-data']
---
Speaker 0: 00:00:07

Live from Utrecht, this is the fanboyroom Shortsnado.
Hello! Hey Shorts.
What's up?
Shorts, today we are going to discuss at length in depth the American political situation.

Speaker 1: 00:00:19

That's right.
We're going to explain everything and we're going to tell you who to vote for, even though this will be released after the election.

Speaker 0: 00:00:26

This is our election special that's going to be published three days after the election.
Exactly.
There was something in the news this week which is mildly, slightly relevant to Bitcoin, and we thought it would be fun to dedicate an episode to it.

Speaker 1: 00:00:43

Yep, exactly.

Speaker 0: 00:00:44

We're not actually going to discuss the politics of the situation, I think.

Speaker 1: 00:00:48

I believe the listeners understand that.

Speaker 0: 00:00:50

What we're going to discuss is open timestamps.

Speaker 1: 00:00:53

Yes.

Speaker 0: 00:00:53

Right?
And we'll get to the reason why it's relevant later.
Or do you want to get into that now?

Speaker 1: 00:00:58

Well, we can say that something was timestamped.
That was at least mentioned in the news.

Speaker 0: 00:01:04

Yeah.
Yeah.
So it's these emails by Hunter Biden, or he received emails.
That's actually the story.
Yeah.
Through timestamps, we can be sure that these emails were in fact sent a couple years ago and they were signed with Google's

Speaker 1: 00:01:20

keys.
Exactly.
Was that term again?
Yeah, they were sent between two Gmail addresses and Google signs email.
So we know that Google signed that email and if they don't lie about the timestamps, which I don't think Google does, we know those emails are real.
What they mean is a different question, but we know they're real.

Speaker 0: 00:01:36

Yes, and thanks to OpenTimestamps, we know that the emails were really sent.

Speaker 1: 00:01:40

Actually, thanks to OpenTimestamps, we know less than that, but we can get into that.

Speaker 0: 00:01:45

Okay, let's get into OpenTimestamps then.

## Open Timestamps

Speaker 0: 00:01:47

So OpenTimestamps, it's a project by Peter Todd, former Bitcoin Core contributor.

Speaker 1: 00:01:52

He likes to call himself a former Bitcoin Core contributor.

Speaker 0: 00:01:56

Yes, and applied cryptographer consultant.
That's what he calls himself.
Okay.
So do you want to explain what it is?
Open timestamps?

Speaker 1: 00:02:05

Well it's basically a way to prove that a given document exists, existed before a certain time.

Speaker 0: 00:02:13

Yeah, before or at a certain time I guess.
Yeah, well if you

Speaker 1: 00:02:18

add one second then you can

Speaker 0: 00:02:19

make it before.
Sure, exactly.
Sure, fair enough.

Speaker 1: 00:02:21

But the idea is you can, you know, you use the Bitcoin blockchain for this because Bitcoin blocks, we know when they were created, roughly, not to the second, but we know roughly when they were created.
And so if the Bitcoin blockchain points to a document, and I say points to in quotes, that means that document must have existed before that part of the blockchain was created.
And that's kind of what OpenTimestamp leverages.
Of course, we don't actually put documents in the blockchain, that would be bad.
We put timestamps in the documents, in the blockchain.
And these timestamps are a hash of the document, or they are a hash of multiple documents.

Speaker 0: 00:02:59

There are actual documents in the blockchain, aren't there?

Speaker 1: 00:03:02

That's correct.
So that's the worst way you can do this.
You can put the actual document in the blockchain and then you can prove that that document existed, you know, very long ago and some people were doing that back in 2011.

Speaker 0: 00:03:16

Yeah, for example, the Bitcoin white paper, I think, is in the blockchain, right?
It could be.
I think so.
But anyway, so there's a better way of doing this.

Speaker 1: 00:03:24

Yes, because a document can be hashed.

Speaker 0: 00:03:28

Yes, so what's a hash?
Is that too much for our audience?
Do they already understand that you think?

Speaker 1: 00:03:36

No, it's good to remind people.

## What Is a Hash

Speaker 0: 00:03:37

Okay, let's get it.
What is a hash?

Speaker 1: 00:03:39

We can teach them something.
The Dutch word for hash is verhospeling.
Not that anyone would ever use that word.
But it is basically a mangled version of the document.

Speaker 0: 00:03:48

Why did you mention that?

Speaker 1: 00:03:50

Because we want to educate our users.

Speaker 0: 00:03:52

We want to teach them Dutch?

Speaker 1: 00:03:53

Yes.

Speaker 0: 00:03:54

For the hospital.
You taught me something, I didn't know that.

Speaker 1: 00:03:57

Well, yeah, because nobody would use that.

Speaker 0: 00:03:59

Right.

Speaker 1: 00:04:00

So the idea is that you take any given text and you mangle it in a way that you get just a number Or you know, it looks like a bunch of letters, but it's just a big number.

Speaker 0: 00:04:11

Yeah.
Well, it's a hexadecimal number, right?

Speaker 1: 00:04:14

Well a number is a number but you can write a number as a hexadecimal.

Speaker 0: 00:04:17

Exactly.

Speaker 1: 00:04:17

So the key there is that if you change one letter in the text, the hash changes.
And so a good hash function is something that takes any text and produces a unique number and does not collide.
So you cannot come up with two different tags that produce the same number.
Right.
Now that's of course impossible to actually prove, but the wizards came up with, for example, SHA-256, and so far it seems to work.
And the nice thing is the Bitcoin blockchain keeps producing blocks, and there's a pretty big incentive to find a duplicate.
So if there is a vulnerability in SHA256 where you could take, you could change the contents of a block and still have the same proof of work, That would be bad, but we'll find out soon enough.

## Benefits of a Hash

Speaker 0: 00:05:03

Yeah, so I guess the benefits of a hash I would describe as you can, if you have a hash of a document and you have the document, then you can prove that the hash of the document is in fact the hash of the document, because every time you hash the document, the same hash comes out.

Speaker 1: 00:05:19

That's right.
And the

Speaker 0: 00:05:20

other benefit is that a hash is very small compared to the document.

Speaker 1: 00:05:24

That's also right.
Or at

Speaker 0: 00:05:24

least it can be very small.
So you can have, I don't know, an entire book, and you produce a hash of it, then you just have one string of numbers.

Speaker 1: 00:05:32

Exactly.

Speaker 0: 00:05:33

So now you can prove that the book is the same thing as the hash.

Speaker 1: 00:05:37

Yeah, and this can be useful for very practical stuff like if you have optical character recognition, so you're scanning a book and you want to make sure that the scan is correct, or maybe you have a checksum, which is also a hash.

Speaker 0: 00:05:50

Right.
Okay.
So that's what a hash is.

Speaker 1: 00:05:52

Yes.

Speaker 0: 00:05:52

Do we cover hashes?
Yeah.
I think so.

## Miracle Tree

Speaker 0: 00:05:55

Now, something we discussed last week is a Merkle tree.
How about I explain the Merkle tree this time?

Speaker 1: 00:06:01

Sounds good.
Go ahead.

Speaker 0: 00:06:01

And then people can tell us who did a better job.

Speaker 1: 00:06:04

All

Speaker 0: 00:06:04

right.
Okay, so we're hashing documents.
We just explained how we're hashing documents.
Now we have, let's say we have two documents.
Each of them we turn into a hash.
So now we have two hashes.
Now we take the two hashes and we combine these and turn them into a new hash.
So now we have one hash again.
Now we have two more documents.
We hash these documents as well.
We have two hashes.
These two hashes we hash again.
So now in total we still have two hashes.
We hash these hashes together and now once again we have one hash.

Speaker 1: 00:06:40

One hash that represents all these four documents.

Speaker 0: 00:06:42

Yes, one hash that includes all four.

Speaker 1: 00:06:44

And This looks like a pyramid, but we call it a tree.

Speaker 0: 00:06:49

Yes, it's a reverse tree.
It's a pyramid.
Yeah, you're right.
That's what a Merkle tree is.

Speaker 1: 00:06:54

So why do we care about Merkle trees?

Speaker 0: 00:06:56

The nice thing about the Merkle tree is that if you have one of the documents that's included in the Merkle tree, you should be able to prove that it is in the Merkle tree to someone who only has the Merkle hash, which was the last hash we ended up with.

Speaker 1: 00:07:14

Exactly.
And they also don't need to know every document in the Merkle tree.
So you can reveal one document in the Merkle tree.

Speaker 0: 00:07:21

Right.

Speaker 1: 00:07:22

By, you know, revealing the right hashes.
Basically one at every level of the tree.

Speaker 0: 00:07:26

Yes, which is called a Merkle root.
Or Merkle proof.
Oh, sorry.
Merkle proof.
So yeah, okay.
Okay.

Speaker 1: 00:07:33

So why do we care about this?
Instead of putting the whole document inside the blockchain in the transaction, we can put a hash of a document in a transaction.

Speaker 0: 00:07:42

Right, which is much more compact, much smaller, and therefore requires less block space and less fees.

Speaker 1: 00:07:47

Exactly.

Speaker 0: 00:07:47

So that's better.

Speaker 1: 00:07:48

And there's a nice way to do that.
This is called OP return, which we discussed, I believe in a previous episode.
It basically tells the node, like everything after this, you can ignore.
You don't have to put this in your UTXO set, which we talked about last episode, takes up RAM.
So you write OP return in the destination of your payment, and then it's followed by the hash.
And then some other software will have to interpret that.
Right.
But it's still a bit inefficient, right?
And that's why we're talking about this Merkle tree.

Speaker 0: 00:08:14

Yeah, you don't want to have to create a transaction for each document you want to include in a blockchain because there's a better way and that's including the Merkle root.
That's right.
I'm confused about terms can you

Speaker 1: 00:08:26

hear?
So the Merkle root is the top of the tree yes or the top of the roots or the bottom of the upside down tree, depending on how you want to look at it.
And the Merkle proof is a way to say that this given document actually is part of that tree without having to reveal the entire tree, but just bits of the tree.
So how do you use this in practice is the question because you might just have one document that you want to timestamp but you don't want to create a transaction for that, but what if people could come together and Yeah, basically have a whole bunch of documents maybe once a day or once an hour, timestamped.
And that is where the calendar server comes out.
So this is a super centralized solution, but that doesn't really matter.
And we'll explain why that doesn't matter.

Speaker 0: 00:09:14

It's a server run by Peter Todd in this case, right?

Speaker 1: 00:09:17

It could be, we don't know, but that's what he says.

Speaker 0: 00:09:19

I trust Peter, don't you?
I trust Peter to run this server.

Speaker 1: 00:09:24

We don't have to.
That's even better.
Yes.
Okay, so what this calendar server does is basically everybody keeps sending documents to it or actually hashes of documents to it of course not the actual document that would be bad and the server basically waits one second and then tells you at the end of that second you know if you were the only hash or if there were other people who submitted something in that second, and it gives you a hash back.
And you then need to call that server again a while later to say, hey, has this thing been included in the block yet?
Because every couple hours, it will take all these hashes and make a Merkle tree out of that and put that on the blockchain inside a transaction.

Speaker 0: 00:10:05

So what the server is returning to you immediately is a hash of the document itself?

Speaker 1: 00:10:10

I think the server immediately returns either a timestamp or maybe the hash of every other document it perceived.
No, probably, I guess a timestamp.
I haven't looked at the implementation, but the idea is that it groups everybody into seconds, so you never have to wait for more than a second.
And then at some point, multiple seconds worth of transactions, multiple seconds worth of documents are put into a single transaction, which is confirmed in a chain.
And then the server will actually give you the whole chain of evidence you need to go from the document you submitted to that transaction and the block.

Speaker 0: 00:10:45

Okay, so that last part doesn't happen immediately.
That last part telling you where to find it in the tree, that only happens when it's included in a transaction.

Speaker 1: 00:10:53

Well, it has to, right?
And included in a block, because you don't know what block it's going to be in when you make the transaction.
But you don't even know what the transaction is going to look like because there's more documents coming in.
So the hash keeps changing.
The hash that goes into the transaction keeps changing as new documents go to this calendar server.
But eventually, at some point, everything it's got so far goes into a transaction, it gets confirmed, and now it has that proof.
So this is where it can be, you know, where you temporarily have to trust it.
But you can see if it's not doing what it's supposed to do.
It could just decide to throw away your document and never include it.
But once it has done that, you don't need it anymore, because you get all the evidence yourself and you can keep it.
And if they somehow censor you, then you just run your own server.

Speaker 0: 00:11:42

Okay, so if I understand correctly, Everyone's sending in documents they want to have hashed, or do they send in the hashes themselves?

Speaker 1: 00:11:49

They send in the hashes.

Speaker 0: 00:11:50

Okay, so everyone sends in hashes of documents they want to have timestamped.
Once a second, Peter Todd returns, or well, the calendar server, whoever operates it, returns either a hash of the document, if there was only one document that second.
Or no, in that case, what do you get back because you're already sending in a hash?

Speaker 1: 00:12:11

I guess it'll just give you the hash back.

Speaker 0: 00:12:13

Okay, so...

Speaker 1: 00:12:13

I haven't read the exact code, but this is probably how it roughly works.

Speaker 0: 00:12:17

Yeah, it's a bit of an implementation detail anyway.
So you send in the hash of the document you want to have timestamped.
Once a second, a hash is returned, which is either then I guess that hash, or if multiple people send in documents, or if there were multiple hashes of documents sent in in the same second, then a Merkle root is returned plus a Merkle path, which lets you find your hash in the tree.
Exactly.
It's like a miniature tree for once a second.
Every second, there's a miniature tree.

Speaker 1: 00:12:51

And this just prevents you from flooding the server with millions of hashes and it having to hold on to that for years.
Now, whatever you throw at it in one second, it can forget after one second.

Speaker 0: 00:13:02

Right.
Now, all of these miniature trees, to call them that, these are all sort of accumulated and turned into a new Merkle tree.
And the Merkle root of that tree is once a while included in a Bitcoin transaction.
At that point, all of the documents are basically time-stamped in the Bitcoin blockchain.

Speaker 1: 00:13:22

Yes, but you still don't have the proof.

Speaker 0: 00:13:24

Yes, and that proof is also sent to you by the server.

Speaker 1: 00:13:27

No, no, no.
The server, you know, it's not, don't call us, we call you.
It's the opposite.
You have to call the server.
So you basically, every now and then, I think there's a way that you can just wait for it if you have a patient computer, but you can also pull it later and say, hey, do you have the full proof of me now?
And at that point, it will give you everything you need.

Speaker 0: 00:13:47

Right, okay.

Speaker 1: 00:13:48

So which to go back is basically you started your document that you gave the hash.
And then the whatever hashes of all the documents in that one second, and then whatever transaction it comes in, and then where that is in the block.
Right.
That's pretty much the proof.

Speaker 0: 00:14:06

All right, so now we've included a document or the hash of a document in the Bitcoin blockchain through this miracle trick.
Now we want to prove to someone later on, it's a year later, we want to prove to someone that a year ago we included this hash into the Bitcoin blockchain.
How do we do that?
How do we prove it?

Speaker 1: 00:14:24

Right.
So first you give that person the actual document, and then you give them this OTS file, which contains the proof.
Basically all these these Merkle proofs that we stored before.

Speaker 0: 00:14:36

Right and then what does that person do with that?

Speaker 1: 00:14:39

They run a command called OTS verify which basically checks the proof so it checks whether all the hashes are what they say they should be.

Speaker 0: 00:14:46

And then

Speaker 1: 00:14:47

it checks against your own node whether the transaction is included in the blockchain.

Speaker 0: 00:14:52

So that requires them to have the OpenTimestamp software, right?

Speaker 1: 00:14:56

That's right.

Speaker 0: 00:14:56

And the OpenTimestamp software uses the Bitcoin blockchain that you have on your node to check if it's really in there.

Speaker 1: 00:15:02

Exactly.
And so it does not need any of these calendar services.
So these are just necessary to store proof, but they can disappear off the face of the earth as long as you keep the file with the proof.

Speaker 0: 00:15:12

Right.
So now in recent weeks we discussed all sorts of pruning tricks, these kinds of things.
What if you're running a pruned node?
Can you still check the blockchain somehow?

Speaker 1: 00:15:22

Yes, because the nice thing is that you can prove that a transaction exists in a block without keeping the whole block.
You can just basically provide a Merkle proof that the transaction actually occurs in the block.
Right.
And therefore the only thing you need is the block header.
And yeah, you still have that.
If you prune everything, you don't prune the headers.
Nice.
So you have a nice chain of evidence.

Speaker 0: 00:15:43

Okay, so let's get to the reason why we're discussing all of this, Jors.

Speaker 1: 00:15:46

Exactly.
So basically there was an email, let's say Alice was asking Bob for coffee.

Speaker 0: 00:15:53

You don't want to trigger anyone so we're just gonna use Alice and Bob.

Speaker 1: 00:15:57

Also don't know the name of the sender.
Let's say Alice was asking Bob for a coffee back in 2015.
And an email circulates on the internet.
But you do see an email, so you might rightfully ask, okay, maybe this email is completely fake.
Right?
But the nice thing is that...

Speaker 0: 00:16:12

You can never trust Alice and Bob not to lie about coffee.

Speaker 1: 00:16:16

Well, or you're not even trusting Alice or Bob because this email just comes out of nowhere.
It wasn't given to you by Alice or by Bob.

Speaker 0: 00:16:23

Yeah, I'm just saying I don't trust Alice and Bob's words for whether or not they had coffee together.

Speaker 1: 00:16:29

That's true.

Speaker 0: 00:16:30

I want cryptographic proof about them drinking coffee or not, Sjoerd.

Speaker 1: 00:16:33

Well, it doesn't prove whether they actually drank coffee, right?
It just proves that Alice asked Bob for coffee.
I'll settle for that.

## Spam and Fishing

Speaker 1: 00:16:40

Okay, so the nice thing is we have this problem called spam and phishing, you know, basically fake emails pretending to be somebody else.
And the way that is partially solved is that mail servers can sign emails for you.
So you don't have to use PGP yourself, although of course you should, but the mail server will say, okay, this email goes to this person and here's the signature, basically testifying to that.
And Gmail does that standard.

Speaker 0: 00:17:07

Right.
So they have a special key to do that.

Speaker 1: 00:17:10

Yeah, exactly.

Speaker 0: 00:17:11

So it's basically in that case, Google saying, yep, this is the real email.
This was the real sender.
This was the real recipient.
It was really Alice and Bob.
And yes, they were really discussing getting a cup of coffee together.

Speaker 1: 00:17:24

Exactly and that of course might be enough but you know because it depends on how much you trust Google of course.
Google signs a couple of fields, which is the sender, the recipient, the time, and the contents of the message, so you know that.
But, you know, we're Bitcoiners, so we want to have more.
And so the thing is that there is actually another email out there which we can talk about which is Greg Maxwell sending Peter Todd a message randomly about some Bitcoin thing and it happens that Peter Todd timestamped that message back in 2016 and that message is using the Google's key.

Speaker 0: 00:18:04

The same key.

Speaker 1: 00:18:06

So now we have proof that not only did Google sign this thing, they used a key that already existed back in those days.
Because we know that key existed.

Speaker 0: 00:18:16

Right, because it was timestamped on the Bitcoin blockchain exactly back in those days.

Speaker 1: 00:18:20

Yeah, now that doesn't really you know matter that this key existed because we already know Google signed it.
If you assume Google lied about the timestamps that'd be weird.

Speaker 0: 00:18:31

Still nice.

Speaker 1: 00:18:31

Yes, exactly.

Speaker 0: 00:18:33

That's a bit of a downer to end the podcast on.

Speaker 1: 00:18:35

Oh, we're not ending

Speaker 0: 00:18:36

the podcast.
Let's give some better examples than why open timestamps is great.

Speaker 1: 00:18:40

Yeah, well, so the caveat is always people get really excited about timestamps and They are quite useful, but they are not magic bullets.
And there's a lot of things they can't do.
So, you know, don't assign magic to them.

Speaker 0: 00:18:53

Okay.
There's a couple

Speaker 1: 00:18:54

of things you cannot prove.

Speaker 0: 00:18:55

So there wasn't enough of a downer.
Now you're going to list more things you cannot do with timestamps?

Speaker 1: 00:18:59

That's correct.

Speaker 0: 00:19:00

Okay, let's have it.

Speaker 1: 00:19:01

The things you cannot prove, you cannot prove, and sorry for all the double negatives, but you cannot prove that a document does not exist.
And what this means is, you can say, hey, I said X back in 2015.
That's what you can prove that.
But you cannot prove that you didn't say X in 2015.

Speaker 0: 00:19:19

You cannot say that you didn't say X in 2015.

Speaker 1: 00:19:23

Right, if I say I never said blah in 2015, there's no way for me to prove that.
Unless I have like 24-hour footage.

Speaker 0: 00:19:32

Right, of yourself.

Speaker 1: 00:19:34

Yeah, for the whole year.
Sure.
But other than that you can't.

Speaker 0: 00:19:37

Okay.

Speaker 1: 00:19:38

The other thing you can do

Speaker 0: 00:19:39

is but someone else might be able to For example with this email example,

Speaker 1: 00:19:44

well, they can if you did say but not what I didn't say So the other thing you can can't say is that there's only one thing that I said.
So I might have said in 2015, Bitcoin is gonna go to 100, and then I would say Bitcoin is gonna go to 1,000, and I would say Bitcoin is gonna go to 10,000, and then, you know, today I released the proof that I set the right price but you have no idea how many other prices I time stamped.
Right.
So that's important to keep in mind when people use time stamps in Magic Tricks.

Speaker 0: 00:20:14

You might have just time stamped every single possible price for 2020 and then come out as a visionary in 2020 because you're only revealing the one you got right.

Speaker 1: 00:20:25

Exactly.
I also can't prove that something is older than the timestamp.
Basically if I timestamp something now then you have no way, I have no way of proving that maybe it was ten years ago.
Yeah.
Right?
So, if you have some sort of magical anti-aging medicine, you can say, oh, look at how I looked in 2016, but actually that was me in 1981 or something.
Sure.
Some more disappointments?

Speaker 0: 00:20:51

Yeah I want another one.

Speaker 1: 00:20:53

If you lose the proof or if you lose the original document well then you're screwed right because if you have the hash you cannot reconstruct the document.

Speaker 0: 00:21:02

Right.

Speaker 1: 00:21:02

And if you just have the hash, I don't think you can still figure out how to connect that to the thing in the blockchain.
You need all these intermediate steps of the tree.

Speaker 0: 00:21:11

Yeah, you need the document in order to prove that the hash matches the document by just hashing the document again.
Plus you need all sorts of extra info to find it in the blockchain.
Sure, yeah.

Speaker 1: 00:21:22

Yeah, that's what you downloaded and hopefully saved in a file.

Speaker 0: 00:21:24

Yeah, okay.

Speaker 1: 00:21:25

And the last thing, that's kind of a bummer, you can't really prove that a website is real in general.
It's very difficult.
So if, let's say there's a tweet, and the tweet has a URL, and if I give that to you, you have no way of...
I cannot prove to you that that URL really contains that tweet.
I mean, you can go to it yourself, but that's the only way you can find out.
And so that's a problem if 10 years from now I want to prove that a certain tweet was real.
If it's still there, then I can prove that it existed.
So I can make a timestamp of the, basically the website

Speaker 0: 00:22:02

as

Speaker 1: 00:22:03

the document looks, and then, you know, today you look at it again and you can see well I'm seeing the same text.

Speaker 0: 00:22:09

So how would you fake that a website existed then?

Speaker 1: 00:22:13

I can just edit some HTML and make a different tweet.
I can make a website that shows a tweet

Speaker 0: 00:22:20

but the

Speaker 1: 00:22:20

tweet could be complete nonsense and so I have no way to prove that but if the tweet didn't change then I can prove it

Speaker 0: 00:22:26

right

Speaker 1: 00:22:27

and but the problem is of course you can delete tweets So that's why you have things like the web archive.
So you can make a timestamp of a tweet on the web archive.
And if the web archive is still out there when you check the evidence, then you can prove that the tweet existed.
But if the tweeter deletes that tweet and gets rid of the web archive, then you're screwed.

Speaker 0: 00:22:49

Yeah, couldn't you make a backup of the web archive yourself?

Speaker 1: 00:22:51

But then how do you prove that that's the real web archive?

Speaker 0: 00:22:54

I don't know.
If you timestamp the web archive and keep a backup of the web archive, then...

Speaker 1: 00:23:00

Well, it depends on when you made it.
So then the question is, when you made that backup, did you have reason, did you already know what things you needed to fake?
Or was it impossible for you to know what things you needed to fake?
So there's still, you know, things you can do if you carefully think about what you have and what you don't have.
But it's not magic.

Speaker 0: 00:23:19

It's not magic.
So what is great about it?

Speaker 1: 00:23:22

Well, that's why we have a list of called cool things.

Speaker 0: 00:23:25

Nice.

## Timestamp Git Commits

Speaker 1: 00:23:26

So one of the cool things you can do is you can timestamp git commits and Bitcoin Core is doing that.
Which is nice.

Speaker 0: 00:23:34

So every time there's a new commit to the Bitcoin Core source code, that is timestamps.

Speaker 1: 00:23:40

Exactly.

Speaker 0: 00:23:41

Right.
Interesting.

Speaker 1: 00:23:41

And we know that all these commits that go into Bitcoin Core are signed by the maintainers too.
So there's two things.
We now, we have these timestamps and assuming somebody stores the evidence, multiple people store that evidence and the signatures are real.
You can go back in time, look at these timestamps and see that the history is indeed what GitHub says it is.

Speaker 0: 00:24:05

Right.
You can trace the entire history, or at least up to a point, of what the Bitcoin Core source code looked like.
Now, if somehow there would be another version of history timestamped in there, then it's either not signed by the maintainers, so it's obvious that's the fake one, or I guess in a worst case scenario, if it is signed by the maintainers,

Speaker 1: 00:24:29

then we know that That particular maintainer has been signing two versions of history.

Speaker 0: 00:24:33

So we know there's a problem at least.

Speaker 1: 00:24:35

Yeah, you might still not know which is the real one, but you know there's a very serious problem.

Speaker 0: 00:24:39

Yeah, interesting.
Okay, more cool stuff.

Speaker 1: 00:24:42

Another cool thing is actually the opposite.
The Genesis block timestamps the times.

Speaker 0: 00:24:48

Yeah, the newspaper, sure.

Speaker 1: 00:24:49

But actually it's, you know, in practice more like the other way around, right?
The fact that the times occurs in the Bitcoin blockchain, that times article from January 3rd, 2009, The fact that that occurs in the blockchain means that the blockchain must be more recent than that.

Speaker 0: 00:25:06

Yes, well the Genesis block at least, yes.
Well, so I guess the whole blockchain, sure.

Speaker 1: 00:25:10

Yes, because everything else came after.

Speaker 0: 00:25:12

Yes.

Speaker 1: 00:25:13

So that's a nice example of how timestamps in the real world, you know, can prove what's going on in Bitcoin.
So I guess you can use some of that magic to triangulate stuff if people put newspaper articles in the blockchain, then you have some extra assurance that this thing is really not older than you think it is.

Speaker 0: 00:25:30

Okay, more cool stuff.

## Limit the Scope of Fraud

Speaker 1: 00:25:31

Well, the last thing is, I guess, more of a general claim is that you can limit the scope of fraud I believe that's how Peter thought phrased it so you cannot necessarily prevent all forms of fraud as we discussed it could be really funky things going on but there's a limit there's a more limited things you can do because these timestamps exist.
You have to be more careful.
You cannot, for example, say, hey, this Google key was recently created by a Russian hacker.
No, we know it was out there in 2016.
So there's certain things you can no longer claim based on these timestamps.
And as we described with the example of the hypothetical evil Bitcoin Core maintainer that changes history, you can then prove that there are two versions of history, and that is something they would have to think

Speaker 0: 00:26:16

about.
Yeah, so what I really like about this idea, so for I think timestamps and these kinds of timestamps and open timestamps, it is, I think, the most interesting and the most important non-monetary use of Bitcoin.
I think it's a big deal being able to timestamp documents in such a very viable way.

Speaker 1: 00:26:37

Okay yeah it's definitely very cool and very useful.

Speaker 0: 00:26:40

You know I've studied history and it's a huge part of a historian's job to find out if documents, if evidence is really as old as it's supposed to be.
A nice example is, I'm sure you've seen these photos of Joseph Stalin, where people are just photoshopped out before Photoshop was a thing.

Speaker 1: 00:26:59

Yeah, exactly.
Nowadays, everybody does that.
But Yeah,

Speaker 0: 00:27:02

back in those days, that was a bit more original.
But these are the kinds of things, like you can imagine how these kinds of trickeries could be prevented with something like Open Timestamps somehow, or at least be made more obvious, or it could be a very useful tool for historians, I think.
The other cool thing, Shorz, I'm going to tell you one more cool thing before we end this podcast.

Speaker 1: 00:27:24

All right, tell

Speaker 0: 00:27:24

me.
I think one of the nice things about Open Timestamps is that it actually resembles the idea that is mentioned in the white paper in the Bitcoin white paper the Scott Stornetta and Stuart Haber if I'm recalling these names correctly they had their own idea for timestamping back in the I think it was either the late 80s or the early 90s.
And back then, Stornetta's idea, his concern was that, as long as we have paper documents, then forging paper documents, is at least kind of difficult.
It's at least sort of like it leaves traces or you can sort of tell that something has been doctored with or messed with, or it's at least sort of possible while if we're moving.

Speaker 1: 00:28:11

And you know how old paper is.

Speaker 0: 00:28:13

Yeah, you can even tell how old paper is in many cases, or at least roughly.
And if we're moving to a digital world, that kind of stuff becomes completely impossible and every document can be altered in ways that are just unseeable.
So He wanted to solve that problem and he and Heber, they tried to solve this problem.
They couldn't figure out how to solve this problem because every solution they come up with relied on some kind of third party to vouch that a document existed at a certain point in time.
And maybe that third party would be checked by another, by fourth party, but there was always some trust involved, and that's what I want to get rid of.

Speaker 1: 00:28:59

Right, and That sounds pretty problematic in the Stalin example you just mentioned.

Speaker 0: 00:29:03

Exactly, yes.
So, ultimately, they thought they were not going to be able to solve this problem, and then they wanted to at least prove that this was an unsolvable problem.
But then while trying to prove that it was unsolvable, they came to the realization that, wait a minute, this is actually solvable if everyone in the world is party of the timestamping process.
So everyone in the world submits their hashes and everyone in this world receives the combined hashes in return.
That way, if you want to forge history, you would have to corrupt everyone or it would be obvious to everyone, like No one's going to go along with that.
That was their solution, and this solution, I think, evolved.
Ultimately, they came up with this idea of including the Merkle route into newspapers.
Then there was a Merkle route in the New York Times of May 22nd, 1996.
So you knew that documents existed back then.
Yep.
And ultimately, their ideas were inspiration for Satoshi Nakamoto.
It was included in the Bitcoin white paper.
And that's interesting because now peter toss came up with a solution to actually implement a very similar solution into bitcoin so we've sort of gone full circle

Speaker 1: 00:30:26

yeah it's great because everybody wants the bitcoin blockchain it's very redundant

Speaker 0: 00:30:32

what

Speaker 1: 00:30:32

it's very redundant basically Everybody has a copy of the Bitcoin blockchain.
So just like that newspaper.

Speaker 0: 00:30:38

Right, pretty much.
Okay.

Speaker 1: 00:30:41

And they have a financial incentive to have this copy.
It's one thing to say everybody in the world must participate and have this hash, it's in order to say, well, if you want to use money you need to keep track of a hash and by the way it also fixes this timestamping problem.
Right.
Okay, I think, I guess that's all we've got.

Speaker 0: 00:30:57

I think so too, Sjoerd.

Speaker 1: 00:30:58

So thank you for listening to the Venn Weirdum, Sjoerd Nadeau.

Speaker 0: 00:31:01

There you go.
The Van Weerdam Shorsnado.
There you go.
