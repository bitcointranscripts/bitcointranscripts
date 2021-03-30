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

Each transcript is a markdown file, which requires to include the `title` and `transcript_by` in the file front matter. You can optionally add the speaker's name as well as categories and tags as strings in an array. For example:

```
---
title: Carl Dong - Reproducible Builds (2020-11-30)
transcript_by: Bryan Bishop
speaker: Carl Dong
categories: ['podcast']
tag: ['build systems']
---
```

*Note*: that it is best practice to include the date of the event in the title. (If we can gather enough meta-data, we someday intend on being able to sort transcripts by date.)

## i18n

Spanish and French are [configured by default](https://github.com/bitcointranscripts/bitcointranscripts.github.io/blob/master/config.toml#L11) for [btctranscripts.com](https://btctranscripts.com).

To add a new spanish translation, for example, you need to add an `_index.es.md` file with the proper Spanish title. Then add the transcript file with the appropriate `.es.md` , e.g. `2021-03-30-example-file.es.md`.

This is the same for French (`.fr`).

If you'd like to propose a new language, you can do so by modifying the [site config](https://github.com/bitcointranscripts/bitcointranscripts.github.io/blob/master/config.toml) (this is another [repo](https://github.com/bitcointranscripts/bitcointranscripts.github.io)).

We'd love transcripts in other languages so we've made every effort to make i18n as easy as possible.

## Attributions

This project was based on [diyhpluswiki](https://github.com/kanzure/diyhpluswiki) and would not be possible without the many years of work by [kanzure](https://github.com/kanzure).
