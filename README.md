# Bitcoin Transcripts Repository

A home for Bitcoin transcripts used by [btctranscripts.com](https://btctranscripts.com).

This does not contain the code to run the site displaying this content, which can be found at the [bitcointranscripts.github.io](https://github.com/bitcointranscripts/bitcointranscripts.github.io) repo.

## Contribution

When creating a new directory or adding a page to an existing directory, please follow the structure like this:

```
├── _index.md
├── page-top.md
└── /level-one
    ├── _index.md
    ├── page-1-one.md
    ├── page-1-two.md
    └── /level-two
        ├── _index.md
        ├── page-2-one.md
        ├── page-2-two.md
        └── /level-three
            ├── _index.md
            ├── page-3-one.md
            ├── page-3-two.md
            └── /level-four
                ├── page-4-one.md
                └── page-4-two.md
```

Each directory requires an `_index.md` file with front matter that will reflect the name of the index page in the menu. Adding `{{< childpages >}}` as the body will ensure that all the appropriate files in that directory will be listed. (See [example](https://raw.githubusercontent.com/bitcointranscripts/bitcointranscripts/master/advancing-bitcoin/2019/_index.md))

The file name will ideally be prefixed by the date (e.g. `2021-03-30-example-file.md`)

Each transcript is a markdown file, which requires to include the `title` and `transcript_by` in the file front matter. You can optionally add the `speakers`' names and `tags` as strings in an array as well as `date`(YYYY-MM-DD) and the video/audio link as `media` if available. For example:

```
---
title: Reproducible Builds
transcript_by: Bryan Bishop
speakers: ['Carl Dong']
tags: ['build systems']
date: 2020-11-30
media: https://www.youtube.com/watch?v=L_sI_tXmy2U
---
```

There is usually some other data that is included at the top of each file like full title and slides. Include what you can. For example:

```
Slides: <https://docs.google.com/presentation/d/154bMWdcMCFUco4ZXQ3lWfF51U5dad8pQ23rKVkncnns/edit#slide=id.p>

```

*Note* that valid markdown has `<>`s around urls like the slide example above.

When a transcript is added, [@bitcoinwritings](https://twitter.com/bitcoinwritings) will tweet for it and tag speakers & contributors  as long as they have been associated with a twitter username at [twitter_handles.json](/twitter_handles.json)

### Transcription Style

For your contributions, please use an "edited transcription" style, which can also be referred to as clean verbatim transcription. The goal of an edited transcription is to preserve the meaning of a text without paraphrasing. Stammering, filler words such as 'like' or 'you know', and unnecessary non-verbal communication can be omitted. Strike a balance between completeness and readability.

Oftentimes, audience questions and comments will be inaudible. Feel free to only indicate when an audience member is speaking if their audio is not clear.

## i18n

Spanish and Portuguese are [configured by default](https://github.com/bitcointranscripts/bitcointranscripts.github.io/blob/master/config.toml#L11) for [btctranscripts.com](https://btctranscripts.com).

To add a new spanish translation, for example, you need to add an `_index.es.md` file with the proper Spanish title. Then add the transcript file with the appropriate `.es.md` , e.g. `2021-03-30-example-file.es.md`.

This is the same for Portuguese (`.pt`).

Each transcript is a markdown file, which requires to include the `title` and `transcript_by` in the file front matter as shown above. We strongly suggest you add the `translation_by` for translated transcripts. For example:

```
---
title: Firmas Schnorr
transcript_by: Michael Folkson
translation_by: Blue Moon
speakers: ['Andreas Antonopoulos']
tags: ['schnorr-signatures']
date: 2018-10-07
media: https://www.youtube.com/watch?v=8TaY730YlMg
---
```

There is usually some meta-data also usually at the top of each file that includes slides link and other data. That should all be translated as well.

If you'd like to propose a new language, you can do so by modifying the [site config](https://github.com/bitcointranscripts/bitcointranscripts.github.io/blob/master/config.toml) and translating the appropraite [i18n file](https://github.com/bitcointranscripts/bitcointranscripts.github.io/blob/master/i18n) (this is another [repo](https://github.com/bitcointranscripts/bitcointranscripts.github.io)).

We'd love transcripts in other languages so we've made every effort to make i18n as easy as possible.

## Attributions

This project was based on [diyhpluswiki](https://github.com/kanzure/diyhpluswiki) and would not be possible without the many years of work by [kanzure](https://github.com/kanzure).
