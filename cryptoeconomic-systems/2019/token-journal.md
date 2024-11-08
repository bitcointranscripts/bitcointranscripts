---
title: Token Journal
transcript_by: Bryan Bishop
speakers:
  - Jason Teutsch
---
-- Disclaimer --
1.  These are unpaid transcriptions, performed in real-time and in-person during the actual source presentation. Due to personal time constraints they are usually not reviewed against the source material once published. Errors are possible. If the original author/speaker or anyone else finds errors of substance, please email me at kanzure@gmail.com for corrections.

2.  I sometimes add annotations to the transcription text. These will always be denoted by a standard editor's note in parenthesis brackets ((like this)), or in a numbered footnote. I welcome feedback and discussion of these as well.
--/Disclaimer --

Token journal

Jason Teutsch

We're going to have 4 talks, about 15 minutes each with 5 minutes for Q&A. At the end, there will be a 40 minute discussion about peer review policies we're trying to do for the journal and get feedback on how to shape the structure of the journal process we're going to do. We have four talks in this session.

# Introduction

Glad to kick off the second day here. I want to tell you about tokenized journals. This is a montage of various conversations I have had with people over the past couple years. I may have ommitted some information and possibly some citations so feel free to chime in during the discussion section.

# Token journal

We're all here to celebrate the kickoff of this new journal at MIT so I probably don't have to explain why peer review sets an important standard for communication in building a field of research around cryptocurrency. One of the goals in the token journal inherent is the need for peer review and we want to bring this to the cryptocurrency community.

We want to go a step forward. This is a radical experiment as we'll soon see. We want to use blockchain and tokenization to improve the scalability and effectiveness of peer review for basic research. This is reviewer scalability for scalability solutions. During the ICO bubble, there were more papers coming out faster than we knew how to read. Going one step further, let's experiment with the utility of these tokens as a store of reputation and see how they can serve the purpose of reputation of the academic ecosystem.

# Agenda

We'll talk about the challenges of incentive design, governance. Obviously, governance, if you start off with zero, in order to have reputation you need an editorial board, and then you need adoption this is more of a practical tihng given the current state of academia how would we get adoption for a system like this. From an operational point of view, and then applications. How do we apply this journal and reputation to the larger ecosystem. Whether you're a dean, publisher or a researcher, hopefully there's something here for you to think about.

# Scope

What we see in a blockchain is a lot of information being conveyed through alternative sources instead of just different academic research. There's whitepapers, academic-style research articles, educatoinal and survey articles, software tools and prototypes, youtube videos, websites, and other public media, and even blog posts. These are all things that add value to the ecosystem and we can open our minds to sort of how to incentivize people to contribute in ways that are valuable. And how do we sort thorugh them all?

Obviously we want to create something that is not exactly the same as reddit because we already have reddit and we have severe not invented here syndrome. Different fields have different needs, and we want to connect these with industry. What about a journal that works for industries?

# Protocol: Journal design principles

Let's start off at journal design principles. Anyone can be an author, anyone can be a reviewer, reviews may result in labels other than "accept" or "reject". Reputable editors incentivize appropriate participation and have the capacity to mint tokens. Reputation, as measured in tokens, is non-transferrable. So they are a little bit different. Still, reputation is the currency of academia ((except for money which is used for funding)). You can endorse someone, but you can't hand them your own reputation.

# Structural considerations

A few questions about how this should work. Should authors and reviewers be anonymous? Authors can always deanonymize themselves. If reviewrs are not anonymous, then how to incentivize honest reviews? If reviewers are anonymous, then what to do about flame wars? If the authors are anonymous, then how to protect against plagiarists claiming their work? Who are the initial editors and how is this set updated over time? How can the protocol reduce spam submissions? And how should the journal implement privacy and timestamping?

Processing a large number of articles, you want to somehow want to manage the amount of spam that comes in. We have questions around privacy. If people are privacy, how do we implement that? How do we do timestamping?

# Statebox protocol

<https://journal.statebox.org/> This is a program where you can draw a diagram of what you want your submission-review-publication pipeline to look like and then it transforms into code. You can play around with that software. They have a little journal site setup.

# Store-of-reputation

I want to go a little deeper into the protocol before we drop into operations. This is a generalization of the journal. The journal provides reputation. In practice, the authors publish to increase their reputation. That's sort of a practical aspect of journal publications and they use it tenure review, job applications, and venture capitalist pitches. So your reputation is useful, outside of just sort of this narrow window of being in a journal ecosystem I guess.

Anyone can mint a token. Tokens are not transferable. The reputational value of the token is as good as its issuer. Tokens should not be transferable in the same way that reputation is not transferrable. The reputational value of a token is only as good as its token. This is a zoo, though, a zoo of tokens. Now we have to deal with the processing of this, now there's scalability problems and making sense of these tokens floating around.

# Towards robust reputation (Lewis-Pye)

He suggested non-tradeable store-of-reputation tokens which have two properties. One is rate, here is the rate at which I create new tokens, and then the promote which is the number of tokens required for permission to mint. Say you collect enough tokens, then in this particular system then you have permission to mint your own tokens. Once you have enough reputation, you can endorse someone else. You start off with a trusted genesis set, that's label zero, and then label n+1 users, and so on. For each level, if you receive enough tokens, from promotions at lower levels, then you can go up to a higher level. It should be clear what we're talking about here is not exactly a hierarchy. There really are labels; a label 1 user can receive more label 1 tokens than a label 0 user. So we have decoupled this idea of labeling and creating this system of measures under which circumstances you can endorse other people but then on top of this you can each person or organization can apply their own comprehension measure as to how they want to interpret these massive collections of tokens. If you have 40 from one person and 30 from another person and 500 from a third person... and s oon.

# Karma-based ethics

This is based on Dasgupta. This is what happens when you read an interesting article 10 minutes before your presentation. Karma is subtractable, and aggregatable.

# Compatibility with status quo

How do we manage to kick this thing off in practice given we have to deal with the current status quo in academia? I called this the bootstrapping strategy, based on conversations with Andrew Miller and Koch and Lewis-Pye who all suggested a similar approach. DCI is also on this slide too. We want to make a token journal that should be consonant with the existing academic ecosystem. Authors rely on traditional publication venues to obtain tenure while peer-reviewed journal submissions are pairwise mutually exclusive. So the observation is that preprints (like IACR ePrint, SSRN) and overlays (DCI) do not preclude peer-review submission of an article. So where does preprint end and peer-review begin? You can't publish the same article in multiple peer-reviewed journals, it just doesn't happen.

# Special status of arXiv

This is a theory, based on a conversation with Andrew Miller. He noted that arxiv.org for example sort of has a special status. There are reputational standards for submission; you have to be endorsed somehow. arxiv + reddit != peer review. Papers go on arxiv, people comment on reddit, and yet the papers can still be peer-reviewed and published in journals. So arxiv is non-commercial, no serious typesetting service, and papers are endorsed but not refereed. So which properties are critical? It's preprint, not peer review. Is measuring paper equality with tokens (as opposed to accept/reject) a form of peer-review?

# Operational strategies

How do we actually establish reputation for tokenized journals? How do we get people to use it? We could tag along with an existing conference like Financial Crypto, CESC (which does not have preceedings) or any of your other events. If you want to experiment with this, then the token journal may be part of an optional review process or overlay.

# Conclusion

I want to wrap things up so we have a few minutes for questions. Just to give a recap, I think there's a lot of opportunities for different folks to get involved here. If you're interested in protocol research, then there's possibility to experiment with these journal submissions, this general idea of sorts-- these reputation tokens. Maybe conference organizers, philosophers, or lawyers could define the boundary between peer review, preprints, implementing token-based systems, leveraging this boundary and then we can start to review submissions using journal feedback. If you are higher up in a university then we can start to talk to our faculty about issuing reputation tokens, or using these journal tokens in non-blockchain fields so broader distribution, and also start hiring postdocs based on their token reputation scores. Thanks a lot, I'll stop there.
