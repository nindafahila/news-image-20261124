// news-image-20261124 entry (Node 22, standard library only): the image is
// entry.png beside this file, drawn by draw_entry.py (Python/PIL) from the
// verified world news of Tuesday 24 November 2026, and the program copies
// it to /output/entry.png. The gate takes a whole PNG or JPEG of at most
// 1 MiB and 1024 by 1024 pixels; this file is 1024x1024 and ~124 KB, and
// the copy is byte-identical on every run, so both grader runs match.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
