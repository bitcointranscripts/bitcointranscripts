## Metadata
A prefixed metadata is usually generated for each transcript, this has been built into the Bitcoin transcripts editor. So contributors don't need to add the metadata by themselves. If a transcript contains slides, there should be reference to the slide in the metadata. The metadata should look like this:

```md
---
title: "Simplicity: Going Beyond Miniscript"
transcript_by: aphilg via review.btctranscripts.com
media: https://www.youtube.com/watch?v=abUF4MQ7j1w
slides: link-to-the-slide
tags: ["simplicity"]
speakers: ["Christian Lewe"]
categories: ["conference"]
date: 2023-03-01
---
```

## Sections
Use level-2 Markdown headings (`##`) for major sections within the transcript to provide structure and facilitate easy navigation.

```md
## Introduction
...

## Key Concepts of the Erlay Protocol
...

## Q&A Session
...
```

## Speaker Segments and Timestamps
Clearly indicate the start of each speaker's segment with their name and a timestamp in `HH:MM:SS` format. Separate each speaker’s segment with a blank line for clarity.

```md
## Key Concepts of the Erlay Protocol

**[John Doe]**: [00:05:23]  

In this section, we explore the fundamental concepts of the Erlay protocol…

**[Jane Smith]**: [00:07:45]  

That's an interesting point. Let’s dive deeper into the technical details…
```

## Presentations and Slides
If the presentation includes slides or other visual aids, include them using a Markdown image format or reference them explicitly.
```md
![Slide 2: Erlay Protocol Overview](URL_to_image)  
_This slide provides an overview of how Erlay reduces bandwidth usage..._
```
