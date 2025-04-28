---
title: Building and download Bitcoin software in 30 years
tags:
  - bitcoin-core
date: 2025-02-26
---

* Would be disappointed if told 10 years ago that today there would still be one single software project providing node and wallet and gui
* Ideal would be modular code, core would provide consensus library, there could be multiple nodes, wallets, guis built on top
* For example, there is not just one browser or operating system, but multiple projects, different languages, approaches
* Does not make sense a change to gui code goes through same process as change to consensus code
* Another downside of monolithic project is doesn’t encourage domain expertise, have to know everything to be productive
    * Shouldn’t have to know about p2p to be a wallet developer for example
    * And developers are usually not great at UI development, GUI experts not consensus experts
* Multiprocess project and kernel project should enable modularization
* Multiprocess can be seen like plugin system for alternate wallets/miners/p2p implementations
* Other work making code more modular: originally net code called consensus code, wallet code directly, now is split up
    * original net split was more event ambitious, substituted libevent implementation, could be generalized
* questions
    * what is ideal future?
    * should bitcoin core be one projects? or multiple?
    * should there be multiple outside implementations of projects?
    * how do we personally use bitcoin software?
    * how do we think regular users use it? should they be running full nodes? using electrum-type solution? lightning?
* software usage
    * one ideal is everybody can run full nodes if there is server software not requiring maintence, providing bitcoin node and other functionality
    * another idea is ZKP makes it unnecesssary for most people to run full nodes, light clients are possible with high level of security
        * kernel is to be compatible with zk toolchains and enable this
    * alternately lightning, layer 2’s could become main mode of interaction, bitcoin is lower level
* project organization and scope
    * could bitcoin developers write new p2p implementation in rust as part of this project? should it be a separate project?
    * modularization enables writing new software not just breaking up existing software
    * things like netv2 encryption could be separate plugin that do not require modifying core software
    * when do we remove things? would we drop windows support? drop gui? let different implementations focus on different cases?
    * could project shrink down to being a small well maintained kernel library everything else spun off?
        * how would decisions be made in that case? would forks be more likely?
        * group of developers actively working on this would be much smaller
        * would website host other projects? where would line be drawn?
        * would group of core developers be less defined, not contributors to particular piece of software but a collection of people more like a political party?
    * even stratumv2 mining project raises same questions, should that be distributed alongside bitcoin core?
