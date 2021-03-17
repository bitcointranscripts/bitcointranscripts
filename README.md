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

Each transcript is a markdown file, which requires to include the `title` and `TranscriptBy` in the file front matter For example:

```
---
title: Carl Dong Reproducible Builds (2020-11-30)
TranscriptBy: Bryan Bishop
---
```

Note that it is best practice to include the date of the event in the title.

## Attributions

This project was based on [diyhpluswiki](https://github.com/kanzure/diyhpluswiki) and would not be possible without the many years of work by [kanzure](https://github.com/kanzure).
