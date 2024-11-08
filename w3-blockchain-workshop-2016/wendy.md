---
title: Intro to W3C standards
transcript_by: Bryan Bishop
speakers:
  - Wendy Seltzer
---
https://goo.gl/3ZqAuo

We are working to make a web that is global and nteroperable and usable by everyone. If you have tech that you want to work on a global working basis, and distributed manner, then the web is the platform on which to do that. W3C is the consortium and standards body that works to help keep the web open and available. We don't have police power, ew don't have police power to compel web standards, we build consensu sthrough W3C process and our open royalty-free patent policy to invite people to work together.

We hve more than 400 member organizations, we have thousands of participants and interest groups to work together and we have a relatively small staff to work wit heveryone. We have about 65 members on our staff to work to facilitate that consensus. We work in working groups. These are the groups that develop the recommendations for the track standards. We also have interest groups and community groups that work in the earliest stages of use-cases and requirements to incubate people. We are governed by ... work and bring people together. We rarely take votes. We much more often are engaging large groups in debate and discussion to figure out what can we live with that will enable ... a rough and readable ... brainstorming, thinking about what does the web need? What does the tech need? Where are places that are public that our membership can work together with the help of our technical staff so that we can facilitate working together and possibly out of that comes the formation of a working group. Possiby out of that comes great conversations that start up around tables here to form tech startups, or go off and incubate in industry or in public interest organizations.

One possible development though after that incubation happens after people say, you know what we really need to work together is a common interface, a common API, when we have that level of clarity, we might form a working group. Working group iterates on the proposed standard and sends it out for public comment and invites comment from its participants, moves up to the recommendation track, and after  consensus has reached in the working group and among the wide review from the public that might be published as a w3c recommendation. Thta's not saying, again, that we know of any particular recommendation that might come out of here, if we find something, that's whree it will go.

So what are we tthinking of more particularly with the blockchain and the web? There are two different ways that blockchain and web standards can work together. What does the web need to add in order to support blockchain better? That's possibilities like crypto, formats, APIs that could be added to the web to make it easier to access the distributed ledger universally any place that you have a web browser. Easier for the web to interface with those distributed ledgers. And then, conversely, there are opportunities in how can the technologies of blockchain support the web. For example, distributed ledgers supporting certficate transparency? Which is an effort at IETF at the moment, to store the record of certificate issuance on a ledger, publicly transparently so that anyone can check for certificate misissuance.

As Doug mentioned, some things are right for standards. Some things are too early or not yet standard ready. Standards are great for improvement, harmonization and improvement and consensus. If there are already mutliple examples of the ways that something might be done, then we might need to fit three or four of them together into the same framework. When they are already working examples from which to derive a consensus, patterns to match to bring a standard reportoire. Standards are less well suited at the beginning of the innovation process, there's lots of new ideas going on. We don't want to lock anything into a standard. We're not ready to say yes this must be the block size. Or yes this must be the format in which things are expressed. While innovation is running, that's the great time to be incubating possible standards and identifying places where you might need coordination. Not yet the time to write it into this is a global recommendation for the web.

So I wanted to briefly mention some of the work that the W3C is already doing that might be relevant to work that you're looking at. In security and privacy, we have been working in web authentication, web crypto, web application security, web payments, privacy IG, HTML (web platform WG), web performance, CSS, HTML media, WebRTC.

Web authentication is one of the newer pieces of work that came over that came over to W3C from Fido Alliance. Username and password is a terrible way to auhtenticate, yet it's done everywhere on the web. HOw can we get beyond that? The web authenticaiton working group is building the web APIs to act as the interface between the local authenticator, the web client, and the reliant party, the big arrow between your local client which might be a web browser on a client, and the website which is relying party. This will be one module of a larger authorization framework that we are building a way to do strong authentication from the web client.

Another piece of work is PKLjs. It's in the candidate recommendation stage, the Web Crypto API. Instead of inviting every web developer to write his or her own javascript crypto libraries, we're building an API standard across the browsers, rather than, building the implementation, we're standardizing what that API looks like so that a call to encrypt or decrypt, or verify,

This is something that a ... move forward to a recommendation, but the API is extensible and if there are additional algorithms needed, then this is a good place to build for those. Lots of work in our WebAppSec working group. If you're building web applications and want to assure that others are not injecting cross-site scripting attacks (XSS) and data theft attacks, and various APIs design in WebAppSec help to secure web applications, make it easier for the authors of webapps to deploy securely and rely on the transport layer security of HTTPS. And places to think about if you're developing applications in the browser, looking into webappsec APIs and designs.

Again, support for encryption everywhere because we believe that a strong web is one where people can rely on end-to-end security and integrity protection. We support HTTPS with browser-side features.

We have web payments work that is building up a payment request API. That's looking across payment types. If you're here because you're interested in bitcoin or cryptocurrency, then look into the Web Payments work to see whether that is extensible in the ways that you would need to work to support alternative currencies, whether it's by default the protocol will support payment and does it include the payment features or is it extensible to include the payment features that you might need for a cryptocurrency? Along with the basic payment request API, there are payment method identifiers and basic card payment in progress on payment applications to support that API.

I'll put this up on the web with links to the various pieces.

w3.org/security
w3.org/TR/WebCryptoAPI/
w3c.github.io/webauthn/
w3.org/community/hb-secure-services/
w3.org/Payments

Most of all I want to invite you to share ideas and thoughts about work that might be pre-standards phase right now, but think about W3C as a big tent in which you can have conversations about that work and come back to our recommendation track down the road when you have something that look standards-ready. So thanks very much and thank you again for coming to share your ideas at this workshop.

