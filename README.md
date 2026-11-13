# Brushing the Sea

A coolest-art-01 entry for make.fun.

A tiny figure in a kimono gently brushing soft ocean waves smooth with a
large wooden brush — a gentle "impossible chore" done to nature, in
traditional Japanese ukiyo-e woodblock print style.

## How it works

`main.py` (Python 3.13, stdlib only) reads the bundled `entry.png`,
verifies it (JPEG magic, dimensions ≤ 1024×1024, sha256), and writes it to
`$MAKEFUN_OUTPUT_DIR` (falling back to `/output`, which the docker grader
mounts writable).

## Run

```sh
python3 main.py
```
