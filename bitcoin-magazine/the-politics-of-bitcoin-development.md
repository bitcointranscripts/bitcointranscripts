---
title: 'The Politics of Bitcoin Development'
transcript_by: 'markon1-a via review.btctranscripts.com'
media: 'https://www.youtube.com/watch?v=NrrD6ufaSrM'
date: '2024-06-11'
tags: []
speakers:
  - 'Christian Decker'
---
## Introduction and Rusty's Proposal

Shinobi: 00:00:01

Hi everybody, I'm Shinobi from Bitcoin Magazine and I'm sitting down here with Christian Decker from Blockstream.

Christian Decker: 00:00:07

I am.

Shinobi: 00:00:08

So Rusty dropped an atom bomb yesterday with his proposal to turn all the things back on just with the kind of VerOps budget analogous to the SigOps budget to kind of rein in the denial of service risks as just a path forward given that everybody's spent the last few years fighting over their narrow little change they want to get in.
How do you feel about this potentially as a path moving forward?

Christian Decker: 00:00:43

I got extremely lucky that Rusty proposed it because otherwise, my talk on the frustrations of as a BIP editor would have been kind of even more depressing than it already was.
And so I saw his presentation and was like, I need to change my slides now.
Because you're right, we have been trying way too long to be clever in as much that we try to sidestep the discussion of whether we want covenants, what kind of covenants we want, or introspection as we like to call it.

## Challenges in Bitcoin Development

Christian Decker: 00:01:26

And it turns out that all of our cleverness wasn't enough for us to actually sort of sneak our little change through, right?
That was always the goal.
We wanted to get here, but to get here, we needed to have this intermediate step, essentially activating a small soft-fork that would enable us to build whatever cool stuff we wanted to build on top for our users and for ourselves of course.
And so everybody was sort of hung up on this activation of the enabling step there.
And since nobody wanted to have the discussion about, hey, do we want covenants?
What covenants do we want?
Are they safe?
We tried to make our proposals so specific that everybody needed a different one.
And so since the review cycles in the Bitcoin community are rather limited, the people that can actually look at a proposal and say, yeah, that's safe or it is not safe, are very few indeed.
And so we ended up in a situation where you'd actually have to badmouth other proposals in order for your proposal to grab the attention that is needed to get your proposal through.
And that never really worked.
It also feels really bad to have to essentially badmouth somebody else's proposal just because you needed it to work, right?

## The Need for Honest Dialogue and Cooperation

Christian Decker: 00:03:03

And then as a compounding factor, we found that many of the proposals that we tried explicitly not to make into Covenants ended up enabling Covenants anyway.
And so not only was it sort of futile, but it also ended up creating this huge tension and frustration among developers and among users, because you actually had to involve users in your propaganda to get your proposal, give your proposal traction.
This felt very much like a liberation strike.
It felt very much like something where we could say, okay, let's approach this as engineers, which is what most of us are, and not as propagandists or salespeople trying to sort of, just get your stuff done.
Let's put this on a more fundamental level.
Let's restore the script we had in the very, very early versions of Bitcoin without the issues, of course.
But let's re-enable that functionality.
Let's give everybody the tools to build whatever they want.
Let's not be patronizing them.
And essentially give them the tools to show their work, show that it is working, show that there is interest in the wider community, and that it is actually being used, right?
And so it might be inefficient, the way that you can do arbitrary things, but you can at least show your work and you can show it works.

## Restoring Early Bitcoin Script Functionalities

Christian Decker: 00:05:04

And then once that is done, then it's the time to actually optimize.
Because then everybody is interested in actually optimizing those use cases.
It's not a use case you're interested in, but it is taking up a bit of blockchain space.
So by enabling more efficient opcodes based on our prior experience, we can then all have the upside of the performance improvement.
I think that is a much more honest dialogue to have.
And it's also a much more, much less noisy sort of way of working towards a common goal, which is enable programmable money on Bitcoin.
I was incredibly happy when Rusty came up with his presentation and I sort of tweaked my presentation because it was sort of this light at the end of the tunnel for me.
And it felt good seeing that there is this possibility of getting back the script and its flexibility in the way it originally was, and as well solve some of this friction we have inside of the Bitcoin developer community.

Shinobi: 00:06:32

And I think you make a really important point as far as the involvement of users.
I think regardless of whether this actually moves forward and it's the direction we choose to go in, if it's just seriously discussed, I think that can be an incredibly healthy thing for the larger and wider ecosystem's involvement because the way a lot of people approach these discussions when the actual subject matter is above their head is just looking at like associations that people who are pushing for a specific thing have and is that a good thing to be associated or a bad thing and then just transitively apply that to whatever proposal they're pushing for.

## The Impact of Enabling Diverse Tools

Shinobi: 00:07:17

Whereas if we move in a more cooperative direction where everybody just openly discusses the complete set of things that we want enabled, and you know, is this good, is this bad, is the good worth like taking some of the bad for the gains we can get from it?
That makes it a lot more difficult for, outside of observers to just associate a single aspect of something and go, well, this person does this thing that I don't like, so therefore I don't like that proposal, because everybody would be just working towards that singular consensus view on things rather than the politicking we've been dealing with.

Christian Decker: 00:08:00

Yeah, absolutely.
It's obvious that we need to defer to experts.
I'm not an expert in some subject matters and I will defer to those experts.
But if those experts are themselves incentivized to present a one-sided picture, because it's holding up their progress, it's holding up the possibility of actually getting their application working.
Then the community as a whole also gets a very, very skewed image of what is actually going on.
In Bitcoin, until now, you always had to be very loud, you had to be very salesy, and you always had to present this, this is the upside of mine, but there's the downsides of everybody else, right?

## Moving Away from Propaganda and Infighting

Christian Decker: 00:08:51

And so you never had an incentive of being honest when talking about the upsides but also downsides of your proposals because whenever you mention a downside it could be twisted in this marketing machine against you.
And I find that just very dishonest.
And why did we do that?
Because ultimately it's the community that gets to decide.
It's everybody put together that gets to decide.
And you had to do marketing at that point.
I'm not a marketing person.
I like to discuss downsides as much as I like to discuss upsides.
I think with a more objective approach to the tradeoffs that are involved, we can make better progress, we can come to proposals that are ultimately better engineered, that had more review, that are safer than if we all try to do some piecemeal little changes.
Because as much as we try to bolt those down, the combination of multiple of these very targeted changes could still open up functionality in their combination.
And so it's a very nuanced discussion to have.
And if we throw propaganda in the mix, then all we get is noise at the end.

Shinobi: 00:10:28

So overall, you feeling positive about the directions things are going?
Like this might actually kind of set us back on course to being more productive rather than the infighting?

Christian Decker: 00:10:41

It feels very much like a breath of fresh air.
We were entrenched a lot over the last years.

## Final Thoughts and Future Prospects

Christian Decker: 00:10:52

We had a lot of infighting and like I said in my talk, I'm not that good with conflict.
And it also affects the individuals that are having these conversations, that are having these discussions.
And it just feels good to have a perspective that we could make progress soon again and get everybody on at the table and give them a voice and be able to have the technical engineering discussions rather than the propaganda discussions that we've had for the last couple of years.
So it's very refreshing.

Shinobi: 00:11:39

All right, well, I'd like to thank you for sitting down with me, Christian.

Christian Decker: 00:11:43

Hey, thank you so much, Shinobi.

Shinobi: 00:11:44

All right, and I hope everybody enjoyed.
