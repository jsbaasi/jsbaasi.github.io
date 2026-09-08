---
layout: post
title: Python notes
date: 2026-09-08 12:25:44 +0000
categories: development
permalink: /python-notes/
---
# pathlib
```
from pathlib import Path

# Read entire file as a string
content = Path("data.txt").read_text()

# Read as bytes (for binary files)
raw = Path("image.png").read_bytes()
```

```
Path("output.txt").write_text("hello world") Path("output.bin").write_bytes(b"\x00\x01\x02")
```

```
with Path("big.txt").open() as f:
    for line in f:
        process(line)

# or writing incrementally
with Path("log.txt").open("a") as f:   # "a" = append
    f.write("new entry\n")
```

```
p = Path("some/dir/file.txt")

p.exists()        # bool
p.is_file()       # bool
p.is_dir()        # bool
p.name            # "file.txt"
p.stem            # "file"
p.suffix          # ".txt"
p.parent          # Path("some/dir")
p.read_text(encoding="utf-8")  # explicit encoding
```