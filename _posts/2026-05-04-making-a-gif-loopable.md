---
layout: post
title: Making a GIF loopable
date: 2026-05-04 14:06:09 +0000
categories: development
permalink: /making-a-gif-loopable/
---
https://www.w3.org/Graphics/GIF/spec-gif89a.txt

Looking at the GIF grammar in the appendix:

```
Legend:           <>    grammar word
                  ::=   defines symbol
                  *     zero or more occurrences
                  +     one or more occurrences
                  |     alternate element
                  []    optional element

<GIF Data Stream> ::=     Header <Logical Screen> <Data>* Trailer

<Logical Screen> ::=      Logical Screen Descriptor [Global Color Table]

<Data> ::=                <Graphic Block>  |
                          <Special-Purpose Block>

<Graphic Block> ::=       [Graphic Control Extension] <Graphic-Rendering Block>

<Graphic-Rendering Block> ::=  <Table-Based Image>  |
                               Plain Text Extension

<Table-Based Image> ::=   Image Descriptor [Local Color Table] Image Data

<Special-Purpose Block> ::=    Application Extension  |
                               Comment Extension
```

The application extension is what we're looking for here, which is defined as:

```
0  |     0x21      |  Extension Label
    +---------------+
 1  |     0xFF      |  Application Extension Label
    +---------------+
 2  |     0x0B      |  Block Size
    +---------------+
 3  |               | 
    +-             -+
 4  |               | 
    +-             -+
 5  |               | 
    +-             -+
 6  |               | 
    +-  NETSCAPE   -+  Application Identifier (8 bytes)
 7  |               | 
    +-             -+
 8  |               | 
    +-             -+
 9  |               | 
    +-             -+
10  |               | 
    +---------------+
11  |               | 
    +-             -+
12  |      2.0      |  Application Authentication Code (3 bytes)
    +-             -+
13  |               | 
    +===============+                      --+
14  |     0x03      |  Sub-block Data Size   |
    +---------------+                        |
15  |     0x01      |  Sub-block ID          |
    +---------------+                        | Application Data Sub-block
16  |               |                        |
    +-             -+  Loop Count (2 bytes)  |
17  |               |                        |
    +===============+                      --+
18  |     0x00      |  Block Terminator
```

So going back to the GIF grammar,

```
<GIF Data Stream> ::=     Header <Logical Screen> <Data>* Trailer

<Logical Screen> ::=      Logical Screen Descriptor [Global Color Table]

<Data> ::=                <Graphic Block>  |
                          <Special-Purpose Block>

<Special-Purpose Block> ::=    Application Extension  |
                               Comment Extension
```

We find the end of the header (bytes 0-5 in my case), end of logical screen descriptor (6-12), if there's a global color table then we jump to the end of that as well (probably will be in optimised GIFs) (global color table size field was set to 7, so size is $3 * 2^{7+1}$, so 13-780). Then we insert our application extension block `21 FF 0B 4E 45 54 53 43 41 50 45 ` at 781st byte (0x30D).