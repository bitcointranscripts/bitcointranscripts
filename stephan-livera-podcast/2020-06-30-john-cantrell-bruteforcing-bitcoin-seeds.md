---
title: Bruteforcing Bitcoin Seeds
transcript_by: Stephan Livera
speakers:
  - John Cantrell
date: 2020-06-30
media: https://www.youtube.com/watch?v=wzYqkxBoNhw
---
podcast: https://stephanlivera.com/episode/187/

Stephan Livera:

I’m going to bring in my guest, John is a developer and he’s also known for working on the juggernaut project and he’s got this fantastic article that he wrote recently that I wanted to get him on and discuss. So John, welcome to the show.

John Cantrell:

It’s great to be here.

Stephan Livera:

So John, tell us a little bit about yourself and your background as a developer.

John Cantrell:

Sure. I’ve been doing software development now for almost 20 years. And I’ve spent probably the last seven of it, focused, well, not entirely 7 focused on Bitcoin, but I’m sort of always in the privacy space and more recently in Bitcoin, but I’ve been kind of following along for about 7 years now.

Stephan Livera:

That’s fantastic. Yeah. I really enjoyed your recent article. I thought it was just phenomenal, really clever approach. So I’d love to break that down a little bit. Could you set this up for us? What was the scenario? What was what this giveaway about?

John Cantrell:

Well, I think it was mostly about I will start trying to get some more followers on his different social media platforms, which it seemed like it didn’t really work out so well for him in the end, but that was his plan was, Hey, let’s give away a Bitcoin and see if I can get people excited enough and make them follow me to try to get clues. And he was going to release, you know, a word every couple of days or I don’t know the exact rate, but that seemed to be what he did. And so I think his idea was, you know, eventually there’d be enough words. Well, he was trying to prevent brute forcing actually by, he said he was going to release the last four words all at once because he incorrectly assumed that it would be impossible or it would take a long, like a couple of weeks. I think he thought, to brute force with eight words.

Stephan Livera:

Yep. And I guess just for the setup. Yeah. Just for the setup for the listeners, I suppose Alistair was saying, you have to follow me across all of these different platforms and I’m going to release one word or two words across each of them. So let’s, I guess explain for those of us in new to Bitcoin. So those people who are new to Bitcoin, remember it’s very important. We always talk about learning how to self custody, your Bitcoin. That’s a very important thing in Bitcoin, not your keys, not your coins. Now, typically when you are setting up a new wallet that not all most wallets will give you either a 12 or 24 word seed. And then that is how you back up and protect your Bitcoins. So, John, perhaps you could break that down a little bit for us. What is that seed and how do we sort of generate one and kind of what’s that process there?

John Cantrell:

Yeah, sure. So it’s I can’t say it’s true for every wallet, right? Every wallet can kind of choose to do this however they like, it’s sort of there’s sort of any, there’s lots of different ways you could convert a word into a string of words into a seed, but luckily we have a standard and so there’s these BIP standards there’s sort of Bitcoin improvement protocols. And we have one, I forget when it was released, we can go check, but it’s called BIP39 and it sort of defined a standard for a way to generate a seed from a mnemonic or a string of words. And so at the end of the day, what really is going on here is you need some, you need some randomness or some entropy and how you get that is, is really important because humans are pretty terrible at generating randomness.

John Cantrell:

Like I think there’s something like if you ask people to guess a number between one and 10, like most people say seven or something like that, right. So it’s like you don’t want to be, you don’t want to do it yourself. You want to, you want to offload this one, one nice way that I actually liked a lot is rolling dice. You have to make sure that they’re properly weighted and everything, but that’s a great way to generate a pretty, pretty, pretty random data. I think a lot of the wallets just use whatever kind of system level pseudo randomness is provided. There’s other neat tricks I’ve seen around using hardware on the device, like the accelerometer, like, Oh, go ahead and shake your device around randomly. And you know, maybe that’s good enough for some entropy or move your mouse around on the screen.

John Cantrell:

You might’ve seen, I’ve even seen them on like a banking website or something once. But so basically the idea is you need some source of randomness and in, BIP39, they, you can kind of choose how much you want based on how secure you want it to be in a sense. And so sort of a bare minimum is 128 bits. And that would give you, that’s how you get to the 12 words and that’s the 12 word seed. And so if you see a wallet that uses 24 words, that means you like we have, I think it’s 256 bits of entropy. And so what that means is, or how it works, I guess in BIP39 is once you have those 128 random bits, and however you got them, whether it was through dice rolling or some kind of a random function built into the device, they then calculate a 4 digit check sum.

John Cantrell:

So you get up to 132 bits, and then they say, we want to divide that into a 12 words, right? You need to get this into words. And the reason they do the words is so that it’s easier to memorize to remember for people like an easily, it’s easy to write down. You don’t have to write down this 128 bit string. It’s just these 12 English words or whatever word, you know, there’s different words for different languages actually. Yeah. And so, and too, and what they do is basically they just split that randomness, that random bit strings of ones and zeros into groups of 11 bits. And it could be anything really, you know, if you want, it just depends on the size of the word list. And so with 11 bits, you can represent the numbers all the way up to 2048.

John Cantrell:

And that’s why, well, actually zero to 2047, but that’s why the list has 2048 words on it. And so basically every 11 bits is just mapping into one of these words on the list and that’s all you’re really doing. It’s just kind of like a convenient way or an easy way for humans to write down or even memorize if they want 120 bits of randomness, essentially. And so that’s sort of the first step. I don’t know if you want me to pause there and you have any questions about that, but that’s how it starts.

Stephan Livera:

Right. And I guess maybe just backing up one bit is the, it’s kind of starting out with a big, big number, right? So if you want to think of it more simply, it’s just, you’re starting out with a huge, huge number. And then you’re sort of breaking that into this. Like there’s a method that the BIP39 standard spells out, which is the way by which you break that down into either 12 or 24 words. And that’s what most Bitcoiners know as their mnemonic, which is, I guess, technically it’s different from the actual number, right. It’s just a representation of that, I guess.

John Cantrell:

Yeah, it is. There’s still just the number, right? It’s just the binary number, which you could convert to decimal. It’s going to be some extremely large number. And then yeah, the mnemonic, isn’t really the number. I mean, it is, it’s just a different way of, like I said, it’s breaking it down into groups and then mapping each one of those to a word. So at the end of the day, it is still that, you know, that big number, but then from there. So if we go into, how do you turn that mnemonic string or that 128 bits of randomness into an actual Bitcoin, private key pair, so private key and a public key there’s kind of another process to find. And so I don’t think we want to go into elliptic curve math, but basically there’s some math here that is what, how private and public keys work.

John Cantrell:

So just like the mnemonic, your private key is actually just a really large number really large. And, and from that, you can do math with the curve that Bitcoin uses to get the public key that you can give out and that’s how you can generate addresses and things like that. But basically the issue was 128 bits is too small to be this, to be your private key. And so they have some, some method to basically use a lot of hash functions and make it slow to compute. So this was actually the most difficult and challenging part. But in terms of brute forcing something like this is how do you take this 128 bit mnemonic and get it into the master seed? And so they do this, a lot of websites will do this when you, when you store it, when they store your passwords.

John Cantrell:

So websites don’t actually store it well, they shouldn’t actually store your raw password that you typed in. They usually hash it and store a hash of it so that if the database is leaked, your password, isn’t actually leaked. It’s just this hash that no one can reverse. And I guess we should step back a little bit. And just hashing is sort of used a lot in this process and it’s sort of, you can think of it like a one way function. Basically. It’s easy to go from. It’s easy to take some input and calculate the output, but it’s impossible or theoretically impossible to go backwards. So if you’re given some hash output, you can’t figure out what the input was. And so what they also do is other than checking every possible input, essentially, which is what brute forcing is. And so websites will, they will, they want to make it slow for brute forces to check.

John Cantrell:

And so they, they come up with really slow hash functions or hash functions, just done thousands of times. And so this is where you’ll hear things like scrypt, which is, I think it’s the same script that’s used in Litecoin is a slow hash function. But I think most of the standard on the web these days is something called B crypt. And it just basically makes it so maybe it takes a half second to do one hash. And so as a user logging into a website, when they have to calculate the hash, it only takes a half second, and it’s not a big deal, but if you needed to check a trillion of them, you know, you’re out of luck, there’s no way you’re going to do a trillion and a half second each. And so that’s sort of the same thing that BIP39. It does 2048 iterations of this hash function, a SHA 512 to the convert the 128 bit mnemonic into basically more random data, but it’s now 64 bytes of random data, which is enough to use as your master private key.

Stephan Livera:

Fantastic. So it’s analogous in some ways too salting, which is that practice you were mentioning around like the websites not storing your, you know, your parcel that exactly as it is, but they salt it first, which is the hashing aspect. And I think the other important point that you were pointing out is the asymmetric nature of it. That it’s easy to go one way, but it’s hard to go back the other way. Oh, we’ve just got a comment in the chat. Why doesn’t he sound well? John’s got some voice modifier software, so that’s that’s why John’s voice is a little bit different. But I think it’s a great idea to protect your privacy. So that’s totally fine. The other, so I guess the next step then is thinking about things like derivation paths and so on. So could you tell us a little bit about how you tried to infer, what sort of address, what sort of key path the Bitcoin was stored at?

John Cantrell:

Yeah, I mean, the first question is really, he says, I’m gonna release a couple of weeks. It was generated, always said it was generated using a 12 word mnemonic. And so, but that alone doesn’t necessarily mean it was BIP39. Like I think Electrum, which is another really popular wallet. It doesn’t actually use, they don’t use it. And so, you know, it could have been an Electrum wallet and I didn’t know at the start. And so, and even like LND has its own, like there’s different people have different ideas in different ways and there’s actually are ways to improve it. And so anyways, it wasn’t clear that that was what he was doing, but as the words started coming out, it’s pretty obvious because you can just check it against the word list and be like, okay, they’re coming from the BIP39 English word list, then you’re pretty confident that that’s what it is. I mean, he could have been tricky and like made his own word list, you know, to make it nearly impossible for this to happen. But anyways, I assumed he wasn’t doing anything fancy since he was targeting nontechnical people and, you know, he was trying to use a standard wallet. I was pretty sure. And so I was like, it’s probably just a BIP39 wallet I didn’t want to overthink it too much. But yeah, you go ahead.

Stephan Livera:

Yeah, I was just saying, and then you also figured out that what sort of address and so on, like it was a P2SH pay to script hash nested P2WSH, right?

John Cantrell:

Yeah. So I’m not actually like a expert on all of the wallet address formats. There’s like so many of them, but yeah, the next step was like, okay. A lot of people, when they try to brute force or do wallet recovery, like there’s a couple of services that do this. They, also, as part of its scan, kind of like the store of the blockchain, UTXO set, so that they can be like, let me generate all these addresses and just kind of search. They’re searching to find addresses that have bitcoin in them. And in this case I knew I didn’t need to do that. And it was a step I could eliminate because he gave us the address to start. And so I was like, I don’t really care. You know, I don’t need to do the standard recovery process.

John Cantrell:

And so I just need to figure out how to generate that address from a seed basically, you know, how do I go from that seed to that address and just try every seed until I can get that addressed. And so to do that is goes into this idea of BIP32, which is another improvement protocol and kind of standard for Bitcoin wallets. And it’s really clever and extremely useful. And the main idea there is let’s take one seed and be able to generate nearly infinite wallets from it. And the idea is you can have there’s different. It feels like a full tree of public and private key pairs. And so you can, it manages things like your change addresses that even supports multi coins. If you want, you know, you want to go down that path.

John Cantrell:

You can, you can split accounts. If you want to have one set of addresses for you, one for your wife, or you have a business. And the other really nice thing is that it allows you to generate public keys without needing the private keys presence. So you can actually, if you run a, I assume, a BTC Pay server and things like that, do this, but if you’re, if you’re running a store and you don’t want to have a wallet, you want to receive the bitcoin on, but you don’t want to have your private keys on your server in case it gets hacked. You know, this is a perfect solution where you can generate nearly infinite addresses without needing to expose your private key anywhere. And so it’s a really clever trick.

Stephan Livera:

Yep. So I guess I’ll just make sure everyone can follow along. I want the intelligent layman to be able to follow along how that works. So basically think of it like your Bitcoin wallet actually manages, it’s a key chain. So it manages many, many different address, sorry, private and public key pairs. And so you can think of it like that. There’s a process to go from public key to address, right. There’s like hashing, encoding and so on, but just for listeners, just so you understand what’s going on. Just think of it, like your wallet manages is a key chain and this master public key is kind of like the top level. If you will account and you can set up little sub accounts in there and each of those is you can generate a new address. And in reality, it’s like a private and public key pair, correct?

John Cantrell:

Yup. Yeah. That’s about, that’s pretty much right. I mean it’s a little more complicated than that. It’s more of a tree structure where you can come and keep branching based on the account numbers and things like that. And that was sort of the next problem, right? It was like, well, which account did he use in which, you know, is it the first address? Is it the millionth address? He didn’t give any indication of that. Right. And so that to me was, as I mentioned in the article was sort of the biggest risk of this whole project. Because I didn’t know, so, you know, which derivation path he was using. And so it’s, you know, it’s great. You can go from mnemonic to seed, to master private key, and then you have to pick, you know, there’s only one address for each path.

John Cantrell:

Well, yeah. For each path. And so, and it takes a lot of time. There’s a lot of math and hashing that needs to be done for each address. And so if you’re trying to brute force a trillion possibilities, you’re trying to save as much time as possible. So I was like going to take a risk here and to save as much time as possible, just check one address. And I sort of just assumed in my head, if I was him, you know, what, how would I set this up? And well, maybe not if I was him, but like, if I was just trying to do this as easy as possible, I’m going to boot up a new Trezor, you know, hit, generate wallet, send, you know, it’s going to give me the first address and I’m going to send the Bitcoin to it.

John Cantrell:

And so I sort just assumed that’s what he did. And so in that sense, what Trezor would do is just use the first account and the first, you know, the first address in that account. And so I just assumed that the derivation path was the standard derivation path for the first address, essentially. And so that was the only address I was checking for each mnemonic that I was iterating through with brute force. And so it was a huge risk because if it was the second, if he was like, Oh, I’m just going to do a test address the test first and then generate a second address and move the Bitcoin there. You know, I would have been totally, always screwed or if he was using an existing treasure and you already had a bunch of addresses and accounts, and he was like, Oh, I’ll make a new account, a new wallet in my Trezor and move it there. You know I would’ve missed it. So there’s lots of ways this could have, could have failed. And luckily he bootstrapped a new, a new account. It seems like.

Stephan Livera:

Right. I see. So I guess what Alistair probably did, right. Inferring from what you were saying, and from what you were successful in the end is that he used, let’s say just a typical Trezor or a Ledger, or just a typical BIP39 wallet and use only the first address. And so you were able to kind of look on the common pathway for that type of address, and if he didn’t reveal the address then you would have had to look at across different pathways, right?

John Cantrell:

If you didn’t, yeah. If you didn’t reveal the address, it would have been a lot harder because another piece that we’re not talking about is not just the derivation path, but also sort of what type of address he was using. And so, like an address isn’t just, you know, back in the early days of Bitcoin, it was simple. It was just pay to public key hash. And now there’s a lot of other kind of standard address types. And in this case it was luckily I just opened it in in a block Explorer and was able, they have all the fancy stats now, they show you, you know, what it is. And it was pretty obvious looking at that, that it was this pay to script hash wrapped SegWit address type. And so with that, so basically what my point was one, you know, when you pick a derivation path, even from there, you don’t necessarily get straight to an address.

John Cantrell:

You had to pick what type of output it would have been. So I actually booted up to my own Trezor and took a walk and saw that that’s also the type that was generating like, okay, this is probably it. And so, like the code that I was writing also had to, you know, you had to tell it, which I had to pick, you know, how do I want to encode the the output script when I was generating the address. And so there was lots of things I was kind of guessing at.

Stephan Livera:

I mean, this is phenomenal, rarely. I mean, this is very clever work. Could you tell us a little bit about how you figured out if this brute force attack is feasible?

John Cantrell:

Yeah, that was sort of my first, my first thing. I was like, well, he says, he’s going to release the last three or four.

John Cantrell:

He said in the beginning, he said three or four. So I was like, okay, three seems. I had no idea. Actually. I was like, you know, I never really done this. I never or done any research or really reading into what is feasible today. I always just know everyone’s like, well to 128 bits or 256 bits is a really big number computers can’t do it. You always see like infographic with like the sun and the impenetrable force. And I kind of just take it as like, yeah, it’s probably pretty big. And it’s like, you know, you never really have a sense for how big it really is until you try to do something like this. And for me, that was one of the coolest takeaways was like, wow, this really is impossible. And so that’s what I wanted to figure out. I was like, what is possible?

John Cantrell:

What is reasonable? Assuming I can actually figure all this out and you know, how fast can I do each for each missing word? And so basically what happens is each word that, you know, you can remove 11 bits from the unknown random string, right? So it was 128 bits we’re trying to figure out. And so each word that he releases, you can, you know, 11 bits now you can just fix them, you know, assuming he was releasing them in order, which is another assumption I was making. But and so after the first word, it’s 117 bits left. And then after the next one, it’s 106 bits and et cetera. And and so that kind of tells you how many numbers you have to iterate through. Right? It’s like two to the, whatever is how two to the number of bits that you’re trying to guess is how many numbers you kind of have to iterate and check.

John Cantrell:

And so what I did was wrote a quick program in rust. I wasn’t actually, I’m not a rust developer, but I knew it was supposedly easy to use and fast. And that’s what I was like, I need something fast, you know, like, yeah, I’m typically a JavaScript developer and I know this is not a good idea to do anything that you need performance in general anyways. And so there’s a bunch of libraries already pre-written and rust Bitcoin and rust lightning, which is what square crypto is kind of working on. And so I just used those to make a quick quick test app, just to see how quick the process was, was from going from mnemonic to address. And I just wanted to get a sense for like, could my laptop do 10 words? You know, how would it, would it take a second or an hour?

John Cantrell:

Like, you know, I wanted to get kind of a feel for what I was dealing with and if it was really possible, was it worth even trying this or was it actually just going to be impossible? And so I did my first test with eight words because I assumed he was gonna, he said three or four. So I was trying to prepare for worst case. I was like, can I do it with eight? Like, that’s the real question, because he’s gonna let it sit. He’s gonna let eight words be out there for at least a couple of days. So can I do eight words in one day it was sort of my target. I was like, I want to be able to do it in a day. And when I wrote the program and ran it on my laptop, which was maybe four or five years old at this point it didn’t look good.

John Cantrell:

It was gonna take, I forget what I wrote. I think it’s like 25 years, something like that. So I was like okay, well, my computer’s kind of old and I know I can probably use graphic cards. So anyways, the next step, like I said, was to toss it up, I spun up a virtual server on DigitalOcean with like 32 cores or something like that, just to see it got a little better, but I’m still infeasible. I forget the number, but it was, it was something like a thousand days or something like that, like three years as well as like, okay, I need, or maybe it was 9,000. I was like, I need at least a thousand times performance improvement from this to make this doable in a day. And I wasn’t sure again, I was like, I don’t know if that’s possible, but I know that, you know, in the early days of Bitcoin mining, we quickly transitioned to GPU mining, which is using, is basically calculating the SHA 256 hash and whatever else is needed to mine, Bitcoin using a graphics card.

John Cantrell:

And so I was like, maybe I can do the same thing with this. I mean, this is basically the same thing. Unfortunately it’s SHA 512, which is slightly different algorithm, but I knew that they were a lot faster and I didn’t know how fast, how much I was like, I’m not sure I’m going to a thousand times, but maybe, and so I was like, let’s do it. And so I kinda took, I sort of was hoping that there would be, I knew there’s all these like hash there’s all these apps out there, like hashcat and John the ripper. And it’s for people who try to brute force basically leaked password databases. And so I was like, they already have these like GPU implementations. I thought it would be really easy just to kind of borrow some of those open source code and just get a test out there.

John Cantrell:

Unfortunately, it wasn’t that simple. And so I was like, I’m going to go and learn about programming a graphics card, which I had never looked into before, but it was actually really interesting. And I wrote about some of the high level things I learned, which is like it’s like the graphics card processors by themselves are actually slower than your normal CPU, which is interesting. And it makes sense, I guess when you think about it, but when you used for general purpose programming, at least, you know, doing matrix multiplication, that’s definitely faster, which is sort of its main purpose in AI and video games and things like that. But if you want to write a general purpose program that does whatever you want they’re actually typically slower than your CPU and the real advantage comes in in the sense that they have.

John Cantrell:

Thousands of core, I forget like a Nvidia 2080 TI, which is sort of like the leading edge consumer graphics card, thinking that something like 5,000 cores and my laptop had two or four. And so, you know, I was like, well, right there, that’s, you know, a thousand times more cores, maybe I’ll get a thousand times improvement that I need. And that’s just from one graphics card. And then I was like, you can also scale up the number of graphics cards that you use. And so I kinda went down this rabbit hole of figuring out what I needed to kind of implement to be able to run this on a graphics card and eventually using kind of pulling together a bunch of different open source C projects. Luckily, you know, the programming language you use on a graphics card is actually really similar to normal C programming.

John Cantrell:

And so there’s tons of open source work around this, especially like libsecp256k1, which is the library, the look, the curve, math library that Bitcoin uses. And I was able to find, you know, all the other things I needed as well. And it was mostly a matter of porting them over to actually run on the graphics card, including all the logic to do the enumeration of all the mnemonics and converting to seeds and kind of doing all the steps with this code. And so anyways, at the end of the day, I ran it on a, I got it working and ran it on one 2080 TI that I rented on this site vast.ai, which is a really cool website to where people can kind of rent out their rent out their unused graphics card. So if you have an old mining rig or I don’t know where these people have more, they have eight graphics cards, they play really high resolution games.

John Cantrell:

I don’t know. But you know, when you’re sleeping or they’re just idle being idle, you can rent them out to, I think it’s typically used for AI, hence the domain name, but so when people want to train these models, they need lots of graphics, graphics cards, lots of computing power, to do the training. And so this is kind of a cheap way to get access to lots of graphics cards without having to like, when you typically go to like an Amazon or AWS or Google cloud or all these providers, you’re going to pay quite a bit more to, to run to rent these cards, and it’s actually a lot harder to access them. They make it, this vast website made it extremely easy for me to get access and up and running without really much onboarding at all.

John Cantrell:

I was just going to kind of finish there. When I ran my first test on the graphics card, I saw that it was going to take about 80 days and I was like, well, that’s a lot better than 25 years, but it’s still not good enough. So I would need, you know, but, but if I rent 80 graphics cards, you know, maybe I’d be able to do it in one day. And that was sort of how I found this vast website and realized I was going to have to orchestrate this whole mess of 80 plus graphics cards to get it done in a day. So at the end of the day, it was a multistep process figuring out whether or not it was possible, but I kept having an inkling that it was and kept pushing on physically.

Stephan Livera:

Yeah. Right. And I guess just to get an idea of the numbers, I think from your article, you said you spent about $350 worth of GPU time. And at the time we’re recording now Bitcoin price is around $9,000. Right. So it’s yeah,

John Cantrell:

Yeah, yeah. That’s sort of what I was thinking. I was like, well, I’m assuming my code is right. Assuming that the derivation path is right, assuming this is the address format. And I made a lot of assumptions, but I was like, if my assumptions are correct, then I should be okay spending, I don’t know, at least, I mean, even a couple of thousand dollars, if I was pretty confident I was going to get it. I also assumed, I don’t know if anyone else was out there doing this, but if you were like reach out to me from the chat, but I was assuming there were a lot of people trying to do this. And so I was scared that even if it worked, I would get beat, you know, in a race, someone who had access to, I don’t know, a thousand GPU or something like some of these old miners, right? Like a lot of these people have like these huge GPU farms that they’re using to mine Ethereum and whatever they could have been like, Oh, this is, this is a nice, you know, I might as well go grab this Bitcoin if I had 10,000 GPUs and I thought I would get crushed that way, but that didn’t seem to happen.

Stephan Livera:

Great. And look, let’s chat a little bit about, I guess, just for listeners who might be a bit scared at this point, they’re thinking, well, hang on. Like, does that mean my Bitcoins are unsafe. Can you just outline a little bit around, you know, tips and ways listeners can think about that? And you know, the, the relative levels of safety that we’re talking about.

John Cantrell:

Yeah. So it’s back to this idea that I think it comes up a lot in humans. Like we always think linearly, like even in predicting the future, we’re like, Oh, well, in five years, the last five years, this happened. So in five years, like it’s going to be like this, but a lot of things like technology grow exponentially and sort of the same in this case, like each word or each bit sorry that of, of the seed that gets leaked or is actually like makes it exponentially easier. Right. And so this tip is don’t put your words on Twitter, private sort of the secret, but like, yeah, I ran some numbers afterwards because everyone kept, that was sort of the number one question was like, well, how long would it take?

John Cantrell:

Why don’t you just do it for all 12 words? And you’ll get all the Bitcoin. I was like, Oh, that sounds nice. But it’s something like 400 quadrillion. Like it’s, you know, the universe is probably going to end before I would be able to do it. Not to say that, you know, computing power is not going to continue to increase, but it’s just, it’s so unfathomable to do that with today’s hardware. And so your Bitcoin is safe from this type of attack, at least. Lots of other ways it can be attacked, but but generally it just, I mean, don’t give out your seed.

Stephan Livera:

Yeah. I mean the obvious stuff. Right. and obviously just be worry about, you know, trying to do those. What’s called colloquially scrapping, right. Where you take half your seed and put it somewhere else and things like that. I mean yeah.

John Cantrell:

It’s an interesting debate. I saw Giacomo and some other, I forget who it is, like JW weatherman or something. I don’t know. Anyway, there is some debate on this and I’d like to, I never really thought about it still. I saw people that do it and it depends on, I think it depends on the threat that you’re trying to protect against. Right? Like technically if you just leave all 12 words in one spot and someone gets to that spot, well, now they definitely get your Bitcoin. Whereas if you did split it and they get to one spot, they still probably get your Bitcoin, but always it’s going to take them, you know, a couple of days, if they assume they even can do the brute force. And so I think it gains you something in certain scenarios, right? Like so I don’t know the full argument, why people are so against it, to me, it seems like it, those games get you, you gain something. I don’t really know. Maybe you can elaborate if you know, the other side of the argument better, but I’m not too familiar with it.

Stephan Livera:

Right. Yeah. I think the general argument as I understand is more like, kind of in the direction that people are talking about, say multisig and for other reasons as well of like, when you need to like rotate a key or when you need to like, do a new set up, or what do you do now that you’ve already given those words out, like it’s kind of practical components, the practical management of it, but it’s interesting you have that view as you all, one of the guys who did do the brute force thing. So if anything, you would be one of the people who would say like, look, I just did. But we’ve got to remember again, as you said, it’s an exponential thing. You did 4 words of a 12 word seed, right. When you start talking about, say a 24 word seed and it’s 12 and 12, well, maybe that’s still really difficult. Right. So, yeah. But what I also wanted to chat about juggernaut, so your project I had a chance to just play around with it last night. I think it’s really cool. Tell us a little bit about juggernaut. What is it and why did you make it?

John Cantrell:

Yeah. Also juggernaut is a messaging application built on top of the lightning network. And so I mostly made it as a way to start exploring some of the new technologies we’re seeing, being enabled by the lighting network. So I don’t know if everyone’s familiar with the lightning network, but the way they work is this layer to build on top of Bitcoin where one of its main purposes is to enable fast and low fee transactions because it’s too expensive and slow to do it on dimension. And that sort of was like the core ideas behind it. But recently we’ve seen things like key send payments, be enabled, which is this idea of being able to send a payment sort of like a Bitcoin payment where you have you can send it to someone’s know directly without them having to generate an invoice first.

John Cantrell:

And when you do that, you can also include some arbitrary data in the payload. And one of the LND developers put out what kind of a command line tool prototype of him making these payments through someone’s know, directly in the arbitrary data happened to be a message. And so he sort of was showing how you could build a messaging application that utilized the lighting network’s encryption and routing properties to have sort of a decentralized messaging system. And so I thought that was really cool and something we haven’t really seen before. And I wanted to kind of run with it and explore what might be possible in the future. And so it’s sort of just the prototype and an example of, of what it might look like. It sort of looks a lot like telegram or kind of a messenger app you might be used to. But there’s no telegram servers, there’s no drag or not server, you know, it’s just, it’s literally every message is routed over the wedding network.

Stephan Livera:

Yeah. So I guess the idea is it might offer some level of censor resistance, right? Like it’s difficult for somebody to stop that message theoretically. And so I guess, how should people think about it if they want to think about using the lightning network for messaging versus say signal or wire or telegram?

John Cantrell:

Yeah. It’s, I’m not sure how practical it is at least today. Because there’s a lot to get to get started, right? You need to, you need to have Bitcoin, you need to have a lightning node. You need to have lightning channels open, you need to pay routing fees. Like it’s a lot harder than just like a double click on the telegram app. And there we go. But the main difference is this idea that I keep coming back to, and I talk to a lot of people in the Bitcoin space and I don’t get good answers. But there’s a lot of people outside of bitcoin as well, are doing this, you’ll see all these, you know, all the shitcoins and all these other projects. They’re not decentralized because they’re the ones bootstrapped, like this company is running the network.

John Cantrell:

It’s their node, there’s a couple people running nodes. And so it’s sort of this problem you keep seeing where, like you don’t are you really decentralized? Do you really have censorship resistance. If there’s just three people that someone can, the government can go after it or shut down your project. It’s like, well, not really. And so to me, that’s one of the hardest things to do in any of these new projects is like, how do you bootstrap a truly like censorship resistant network? And it’s one of these things where I don’t know if anyone can do it again. Like it’s sort of like this thing that happened with Bitcoin and it’s sort of this gift we have, I don’t know, no one seems to be able to replicate it. And I don’t know if they can. And so my idea there is like, if we can’t actually bootstrap another network, then we have to build on top of, on Bitcoin and lightning.

John Cantrell:

And so that’s sort of the nice, that’s sort of, for me, the key thing there is that it’s using this, the network exists for a different purpose already, and people are already running these nodes for using Bitcoin or for using whitening. And this app happens to just, I’m not trying to build a new network that I have to convince thousands of people around the world to run my node. We can bootstrap on top of this already existing network. And so that I think is sort of the most important part. To me, it’s like, it’s same with telegram and signal. So if we look at them right they’re end to end encrypted, they’re open source. Anyone can run it, you know? Sure. Like, but there are still telegram runs the main servers and you’re still using them when your messages are routed through them.

John Cantrell:

So they can collect metadata around who you’re messaging, how often your messaging, you know, they can’t see the actual content of the message, but no, one’s really running their own telegram. I mean, maybe some people are doing it, but like most, most people just use the telegram servers. And so I think even, you know, them and signal, everyone just has this problem of like, how do you incentivize someone to actually run your node and build your own decentralized network? And so to me, that’s one of the interesting things about lightning and trying to, trying to explore what apps might be possible to build on top of it, because you don’t have to worry about the problem of bootstrapping a new network. You can just use the one that we already have.

Stephan Livera:

Fantastic, I think it’s very clever because It’s just difficult to get people to run service for something else. Right. If people talk about even getting enough Tor exit nodes and relay nodes. And so it’s a great idea. So listeners, I gave juggernaut a try last night, I found a very simple, I just double click install and then basically I got my LND connect string and then pasted that into juggernaut. And then I found a public key of one of my listeners and did some chat with them and then was able to do payment to them and also payment requests. So listeners definitely go and have a look, give it a try. So John, have you got any thoughts around mobile client and any feedback so far on juggernaut?

John Cantrell:

Yeah. So mobile would definitely be doable. I’ve kind of stepped back a little bit to rethink everything because all the feedback I got was not as easy. It was not as great as yours, just was almost everyone, even people in the coin, like investors in their court and like people building other services, they actually don’t run lighting nodes. It seems like. And so it’s like a lot of people couldn’t even like make it to try and be out because they don’t have the requirements. And so to me, it kind of highlighted that the onboarding to lightning and Bitcoin in general is just, it’s just too hard. And I think this week was actually interesting. We saw Square Crypto, come out with some more grants for a lot of the design and UX work and it’s needed badly. And to me, that’s sort of now what I think might have to become my number one focus is on onboarding and maybe directly onto lightning is sort of where I’m thinking, because you already have, you know, Swan and Coinbase.

John Cantrell:

And a lot of these people focused on onboarding people into Bitcoin. But there’s not a lot of people like making it super easy to, to get onto lightning. I mean, there are a bunch of mobile apps, but a lot of them are making trade offs that I’m not sure again, that you come back to these trade offs, like to make it easier to use. You have to give up some of the censorship resistant and decentralization and control of your keys and everything that we like to talk about in Bitcoin. And so it is really, it’s a really challenging problem, but I think it might, I hope it’s worth exploring. And so that’s sort of, one of my main focuses right now is around that idea is how do you get someone on to lightning even if it’s just like, you know, even if it’s a dollar worth of sats just to be able to then enable these types of applications around messaging or using some kind of decentralized service that communicates over lightning, you don’t need a lot of money on you just, you know, you can send one sat around and you know you work with the services here.

Stephan Livera:

Yeah. It could be that you know, it’s a great idea, but sometimes ideas come a little early and maybe people aren’t ready for that yet. So it’s, as you, as you point out it’s around getting kind of building those other things to kind of as the setup for this to become ready.

John Cantrell:

Exactly. Yeah. It’s like, someone’s got to do it. And so yeah, like all these ideas, there’s lots of cool lighting applications we’re seeing now, but I imagine they’re all having the same problem where like, it’s sort of not worth it. If there’s 10 people that are ready to get onto your app, you need the right person, but it’s sort of also a chicken and egg problem. Where, how are you going to, why is someone going to onboard on lightning? If there’s no apps, it’s sort of the classic I don’t know if you want to call. I don’t, I don’t think it’s a problem, but people like to talk about it as a problem with where other use cases and stuff alone. I think it’s more about the censorship resistant money. Non-Government money, go listen to the podcasts from Vijay on ‘What is Bitcoin’. And you can you know, you’ll have a better idea of the use case there, but anyways, I think it’s an interesting problem and I think it needs to be addressed. And then I was really happy to see square crypto move in that direction, because I think it’s a problem that hasn’t had funding and without funding you know, not a lot gets done.

Stephan Livera:

Fantastic. Well, look, I think that’s going to do it for this one. Thank you very much for joining me, John, where can listeners find you online?

John Cantrell:

Yeah, right now I’m pretty much only on Twitter. So @JohnCantrell97 I’m trying to branch out a little bit, but yeah, just go, just go there and talk to me happy to answer your questions. I’ve got a lot of questions after this article about, you know, how can I do this? How can I do that. And I’m just going to throw this out there. I cannot brute force your the wall, the wallet from, you know, Bitfinex that holds 10 trillion Bitcoins. So stop asking me.

Stephan Livera:

Excellent. Well, thank you, John and listeners, you can find my show at stephanlivera.com. Find me online at @stephanlivera on Twitter. That’s it from us. And we’ll see you guys in the citadels.
