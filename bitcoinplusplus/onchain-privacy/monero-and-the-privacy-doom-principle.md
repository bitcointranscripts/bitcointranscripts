---
title: Monero and the Privacy Doom Principle
transcript_by: Dnsmpr via review.btctranscripts.com
media: https://www.youtube.com/watch?v=yq_cOVHr8Pg
tags:
  - privacy-problems
  - privacy-enhancements
  - altcoins
speakers:
  - David Vorick
date: 2023-12-09
---
I'm a blockchain researcher and developer.
I've built the Sia blockchain ecosystem and I've been in the space for a while and today I'm talking about Monero and privacy models that ended up being explained in analytical techniques that we can use to beat error in privacy.

## The Concept of Privacy in Cryptocurrencies

So my name is David Vork.
I've been in the blockchain space for about a decade.
I've been between researching and launching blockchains, doing a lot of engineering, but I've been in the space for a while and studying things.
And today I was asked to present on some research I did a couple years ago with regards to Monero.
And basically I identified some analytical techniques that could be used to defeat Monero's privacy.
And so essentially I want to talk through my findings and why I believe that Monero is not a safe cryptocurrency.
And I think that this extends to other similar privacy cryptocurrencies as well, such as the Atlantis, but we'll get into all that.
Before we get too much into the technicals, I wanted to talk about what is privacy and what does it mean when a cryptocurrency provides users with privacy.
And basically, The goal of a privacy cryptocurrency is to make sure that each transaction that a user makes on the network is isolated and does not reveal any information about any of the user's other activity.
And so Bitcoin is not so great about this.
When we think about an example where, say, withdraws Bitcoins from Coinbase, then they take those coins from their own wallet and they spend those coins on, let's say, HIV medicine.
And then the HIV company who accepted Bitcoin goes and deposits It on coinbase.
You have this transaction chain essentially, Coinbase to user to HIV company to Coinbase.
If the cryptocurrency is private, Coinbase will have no way of detecting that these transactions are related.
And so the Coinbase will not learn that the user is a purchaser of HIV medication, or has a business relationship, or has a relationship with an HIV company.
If the cryptocurrency is not private, then Coinbase will be able to look at the transaction graph and look at the data on chain and see, oh, this user is, they'll be able to look at that short turnaround and say, yeah, this user probably has HIV.
And so the Coinbase will be able to learn things about the user based on their other activity, even though the user's relationship with HIV has nothing to do with Coinbase at all.
And so we want to make sure that we build, when we say that a cryptocurrency is private, we want to make sure that the user does not have to think about their actions and does not have to control themselves when they spend their money.
If they receive money, they should be able to treat it as theirs.
They should be able to spend it however they want, and then also have the confidence that their spending activities are not going to be connected together by some outside observer.
Someone who's, you know, party to you for one transaction is going to have no idea about everything else that you do with your money.
And from the perspective of the developers, we actually kind of want to look at the user as our enemy.
The user is this naive entity that's just spending money however it wants, potentially in very self-sabotaging ways.
And if we are telling the user that we can protect them against prying eyes, that we can give them a degree of privacy, we want to make sure that we can deliver on that promise even if the user is doing things like spending money directly from Coinbase to an HRV company.
We want to make sure that the user is protected because we told them that they were protected.
So they shouldn't have to think about privacy.
The wallet should just give them that privacy.

## The Stream Payment Model and its Impact on Cryptocurrency Privacy

So to help analyze cryptocurrencies and determine how good the privacy is, I came up with something that I'm calling the stream payment model.
It's an idea of, it's a model of user behavior that is essentially both practical and like believable.
It's behavior that a real user might exhibit.
And it's also incredibly hostile to privacy cryptocurrency.
A user that is doing this behavior is very effectively undermining themselves and opening themselves up to analytics.
And so if a cryptocurrency is private under the stream payment model, I would argue that that's a good sign that it's robust overall.
But I would also argue if it's not robust under the stream payment model, I would argue that the stream payment model is realistic enough that a cryptocurrency which cannot protect users under the stream payment models just shouldn't be used by non-experts for privacy.
If you can't defend, if a cryptocurrency cannot defend users under the stream payment model, it should be labeled as like expert use only.
And we should assume that an average user is going to sabotage themselves.
And so basically, what I'm going to do today is explain the stream payment model, and then show how Monero and Atlantis and some of these other cryptocurrencies fall short of protecting users under the stream payment model.
So the stream payment model is pretty simple.
Basically, we condense everything down to two users, to two parties.
You have the user, you have their income source, and then you have their expense source.
Unbeknownst to the user and unbeknownst to their income source, those two things are actually the same.
So I'm going to build a very simple idea, which is that you have an artist that sells art online, and that's their income.
And so they get all of, you know, they have a bunch of art transactions every week that gives them a pile of money.
And then every single month, they roll up a bunch of these art payments and they pay rent.
And so you have this continuous stream, this is where the stream model comes in, you have this continuous stream of income of the user making money by selling art, and you have this continuous stream of expenses of the user paying rent to a landlord.
So a very practical situation that one might find themselves in.
And then in our model, the landlord and the art purchaser are actually the same.
And so our goal is to make sure that when a user is transacting, there's no way for the landlord to realize by looking at the blockchain that the person they buy art from and the person who pays them rent are the same person.
And so that's the stream wallet model.
So before we get too much into the analytics, I need to talk about blockchain outputs, which I realize a lot of you are probably already familiar with, but I'm going to go ahead and give a refresher anyway.

## Detailed Analysis of Cryptocurrency Privacy Mechanisms

So basically, the way blockchains work is that transaction, you create something called an output, and it's basically evidence that you are associated with this transaction.
Bitcoin's very straightforward, and so every time that you receive money, there's an output.
When you spend money, you have to take money out of existing outputs and create a new output.
And then because, or on the blockchain record, there's kind of evidence that these two things are related.
And so in the stream wallet model on Bitcoin, basically what's going to happen is your landlord is going to buy a piece of your art and then later when they receive rent from you they're going to see a connection.
They're going to see that the same output that they gave you to essentially fund your artwork is also the output that contributed money to paying the rent.
And so the landlord is instantly going to know after a single transaction that this person is actually the same person And so your privacy on Bitcoin is basically immediately unmasked under this model.
Now what privacy currencies do is they use a technique called decoys.
Not everyone calls it that, but effectively all privacy techniques are to create a bunch of decoys.
And so the idea is, I'm going to start with Zcash, which is secure under the stream payment model.
When you spend money on Zcash, you spend money from your real output, and then you also spend money or you present a obfuscation that says maybe it came from my output or maybe it came from some other output and in Zcash you have what's called like a full full a full privacy set and so everyone every single output on the entire blockchain's history is a plausible potential source of that payment.
And so when the landlord receives that payment on Zcash and they look at the history, they have no, absolutely no way of connecting the rent payment to the art payment that they made, because every rent payment they receive plausibly could have come from every single output in the entire blockchain history.
And so Zcash is effectively impenetrable to this type of analysis.
And maybe there are other techniques that could be used to break Zcash, but I'm not aware of them.
And that's also not the subject of the talk today.
Monero uses a partial decoy technique.
And so basically, instead of presenting, when you spend an output, you present 10 other outputs.
So there are 11 outputs total that are potential sources of your money.
And observers don't know which of the 11 sources actually produced the money.
But in the case of our stream payments, the first time you make a payment to the landlord, they're going to be able to look at that output.
They're going to be able to look at the 11 decoys and go, huh, that's funny.
You know, my favorite artist was used as a decoy.
And, you know, at one time, it's already super suspicious.
There are hundreds of millions of outputs available, and you just happen to pick one that includes the landlord's favorite artist.
Maybe a coincidence.
It's already, honestly, it's already enough for suspicion, and maybe the landlord will spark a conversation and start to ask.
But by the time the landlord receives the second rent payment and they see that the artist is in both of the decoy sets, we've now gone very far beyond coincidence and the landlord's almost certain.
So again, under this stream payment model, Monero's 11 decoys basically breaks down after two transactions.
And so you get a little bit further than Bitcoin on Monero, but not that much further.
And we can actually take this technique a step deeper.
Let's say that the user, you know, there's some piece in the middle, they like mix funds with their friends or, you know, they're trading money on the blockchain, some sort of activity happens, and so the landlords aren't payment.
By the time it gets turned into rent, it's maybe three or four transactions deep.
Well, this, you can still do an analytic, you can still do an analytical experiment where you look at, you know, the output is not one layer deep, it's four layers deep.
And so you look at the 11 decoys that were potential spends from the landlord, and you break it back down.
And so each of those 11 came from 11 and came from 11 more.
And so by the time you're three layers deep, I believe it's 1331, about a thousand potential sources of money, 1000 potential sources of money out of 100 million outputs is still not very random.
And so even if the user is doing small amounts of additional mixing from the time they received the art payment to the time they paid rent, the landlord can still look at the blockchain and gain a pretty high degree of confidence that their tenant is the same thing as their favorite artist.
And after one, it's the same thing.
After one transaction, it's a strange coincidence.
After two, it's almost certain.
And after three, it's definitely certain.
And so Monero's privacy breaks down very quickly.
And the same is true of Atlantis.
Atlantis is a cryptocurrency that gives you instead of 10 decoys, it gives you 65,000 decoys.
But in the context of a highly active ecosystem with hundreds of millions of outputs, 65,000 decoys just isn't sufficient to protect you from discovery.
And so Basically, it doesn't matter how many decoys you're using.
If you cannot get to the point where every single output is plausibly part of your decoy set, the way Zcash does it, you're eventually going to break down under the stream payment model.

## Privacy Decay and Statistical Analysis in Cryptocurrencies

And something that's important to remember is that privacy decay is exponential.
And so if something only has a 90% chance of happening, then maybe the first four or five times you pay rent, it's just a coincidence four or five times in a row.
But each time that that coincidence keeps coming back up, even if we can expand the decoy set immensely.
You're going from being revealed after one transaction to being revealed after two to being revealed after ten.
And people don't have control over, like you have to pay rent every month.
You don't have control over like, oh, I paid rent ten times.
I'm like kind of on the limit of I might accidentally reveal myself to my landlord, I have to switch landlords or something.
That's just not a practical way to engineer private money.
You have to be able to have the user make as many payments as they want to the same person as many times as they have to, to make ends meet or to accomplish their goals without having any of those payments start to threaten the privacy.
And So I've developed something that I call the privacy doom principle, which basically says if your user has no control over how many times they're going to make a payment to someone and their privacy platform is not giving them a 100% complete anonymity set on every transaction.
Then eventually that privacy solution will become completely worthless or completely transparent.
And analytical techniques will be able to completely reveal the transaction graph and expose who all the users are.
And this is like one more token of intuition when thinking about how blockchains might be analyzed.
Really, what the landlord is doing this analysis and trying to figure out who their tenant is, who's paying them, what's the tenant's source of income.
What the landlord is looking for is things that are different from completely random.
And so when the landlord receives a payment, they can ask themselves the question, let's assume that my user is not my favorite artist.
If that's true, how likely is it, or how frequently would I see my favorite artist's outputs appear in the decoy graph?
And if they did appear, how deep would they be?
How many transactions backwards would they be?
And so the landlord can build a model of like, if the user is innocent, this is the statistical profile that their decoys would have.
And then you just ask, do my outputs, do my art payments appear in this decoy graph more frequently than this statistical model suggests they should?
And if the answer is yes, then you have a very strong reason to suspect that this person is the same as your favorite artist.
And so basically you can ask questions to the blockchain of like, is this person X, is this person Y, are their funds Z?
And you can just build a statistical graph.
If the answer is no, this is what the statistics should say.
And then you look at the reality of what the statistics do say, and then you can build a very clean statistical understanding of how likely this person is to be in.
And Again, like I said, typically on these things, after three or four payments, the statistics get extremely skewed, right?
The statistics will usually say like five, you know, five layers deep, you would expect one output in one in 1000 cases.
And then you find that there are actually three outputs, five layers deep, and that just is completely unlikely to happen randomly.
And so, yeah, basically the statistics that break Monero come from asking what random looks like, and then proving to yourself that what you actually see does not match what would be random.
And in the case of Zcash, you get this security because every single output is a plausible source of every single transaction.
And so this sort of statistical analysis doesn't work.

## Potential Solutions and Future of Cryptocurrency Privacy

Since I have time, I'll go ahead and talk about a potential fix.
So I think that if Monero and similar cryptocurrencies want to fix what they should do is they should switch to a full decoy model.
If you don't like trusted setup, you can do it with Starks, but they should switch to something like Snarks or Starks and just transition to being full decoys.
But if they insist on staying with ring signatures, what they can do is they can have users obfuscate their transactions by sending the money to themselves repeatedly.
On Monero, you need to do it something like a dozen times.
On the Lantis, it's something like five times.
And the big caveat is that if everyone else is also doing this, then you can actually get to a point where, because a user, by the time a user spends money to the landlord they've kind of recycled it through the output graph a dozen times and all of their decoys have been cycled through a dozen times by everyone else who's doing the cycling.
So as long as the whole ecosystem is continuously doing this cycling you can get to a point where the graph is noisy enough that the analytics break down, but I really don't suggest that as a solution because it hinges on a bunch of assumptions like everyone else has to be playing along.
Everyone else has to still have their wallets running.
If half your ecosystem disappears and only shows up during bull markets, then during the bear markets, the people who are trying to use the platform for privacy are much more exposed because that additional noise factor, hiding factor is not present.
Whereas if you have a full decoy system like Zcash or the StarCore equivalent, none of those contingencies matter.
And so, yeah, in conclusion, you know, it's not a favorite conclusion of mine to deliver because I've been a big fan of Monero for a long time.
They did a, I think they did a lot of things right.
I think they've been very practical about protecting the privacy of their users.
But ultimately, when you boil down to the stream payment model, and again, you can actually expand that and show that Monero is broken under much less restrictive models as well, statistical analysis is just very effective at seeing through the decoy model of Monero.
And switching from 10 outputs to 100 or 100,000 really doesn't make a dent.
The statistics break things down very quickly when you have a smart enough analyst.
And so, yeah, that is my talk.
And I've been sitting on this for like three or four years, so it's great to finally put it out into the wild.

## Q&A

I know that some of it may have gotten a little bit technical, so I'm more than happy to answer questions if anyone would like clarification on anything or just has other questions.

Host:
Yeah, sure.
I'll ask a clarifying question.
So this type of analysis requires like the landlord to be the purchaser or does it?

David Vorick:
Yeah, so for the very basic breakdown we or the stream model do assume that the landlord is on both sides of the equation.
In practice, what it really would probably look like is that, you know, the user collects money for their art through BitGo, then withdraws it from BitGo, sends it to the landlord, and then the landlord sends it to Coinbase.
Coinbase and BitGo share analytics information because they both use, I think they both use Elliptic to do analytics.
And so now the landlord's not the one finding out about the user, it's Coinbase and BitGo that are getting all this information about the user.
But in practice, it's actually the case that you probably have a party on both sides.
It's not the landlord, but it's a bigger service provider that can see everything and is going to be able to figure out that you are both this artist and you pay.

Host:
Second follow up to that is, so as you sort of weaken the anonymity of one person in the graph, like say Alice, and then you say you're like, I'm 25% sure that, or like maybe over 50% sure that these are her transactions, and you also weaken Bob's, and Bob and Alice are in the same, we're in the same anonymity set, then Do the probabilities, like, do they both, are they both weakened even more because you've somewhat learned some information about one or are they like independent?

David Vorick:
Yeah, so that's the other thing that like just makes life really tough for Monero because so in something like Zcash, they are independent, but in something like Monero, I like to think of it as like a giant Sudoku puzzle where as you interact with Coinbase and BitGo and these big providers, what you're effectively doing is you're giving them numbers in a Sudoku puzzle.
And if there's just a little bit, it's fine, right? You have a giant Sudoku puzzle and like four numbers, you're not going to be able to solve the puzzle.
There's a lot of mystery.
But by the time that Coinbase gets up to say 20 numbers, 22 numbers, it's now not even a difficult Sudoku puzzles.
Coinbase can just go ahead and solve the whole thing.
And so they can fill in all the other numbers.
And so, yes, if Alice does something that erodes her privacy by, say, 25%, right, Coinbase only has 25% certainty.
Even that is enough to start to do things that will unmask Bob.
Because Bob was hiding alongside Alice, and the fact that Alice isn't so hidden anymore does impact Bob's ability to hide as well.

Host:
Wow, that's a lot worse than I thought.
It reminds me of the wave function collapse algorithm, which everyone should check out.

Audience:
Outside of being contacted by the feds, how would the average user know whether they have been compromised from a privacy perspective?

David Vorick:
Yeah, so that's the thing.
A lot of times there's no way to know, and especially when it comes to entities, or maybe we should call them adversaries, such as Coinbase and BitGo, not only are they not going to notify you, but also the way it impacts your life is going to be more subtle.
For example, it might just change what sort of ads get presented to you.
It might change.
I mean, if we're thinking like really dystopian, it's possible that things Coinbase knows about you influences your ability to get loans on a house or you know, get insurance.
Coinbase might be able to contribute information to AIG that impacts the prices of home insurance for you if they know certain activities about you that make you a more risky customer.
And so yeah, you're not necessarily going to know, but that doesn't mean that there aren't very real consequences that are actively impacting your life.

Host:
Okay, I think that's it.
Yeah, let's clap.
Thank you, David.

David Vorick:
Absolutely.
Thank you.
