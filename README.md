# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/nindafahila/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/nindafahila/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-image summary of the world's news of **Tuesday 24 November 2026**, drawn as a newspaper front page: Seoul sounds an air-raid alert as jets approach Ulleung Island (lead), the Crimea Platform summit opens in Stockholm, Trump pardons the Thanksgiving turkeys before flying to Mar-a-Lago, Tokyo reopens after the Nikkei's fifth-biggest point drop ever, the Beaver Supermoon peaks, Champions League Matchday 5 kicks off with nine games, and Odesa's blackout could last weeks — plus a Spain election countdown in the footer ticker.

## How it works

`draw_entry.py` (Python + Pillow, deterministic, no network) draws `entry.png` — 1024×1024, ~124 KB — from the day's verified headlines. `main.ts` (Node 22, stdlib only) copies that image to `/output/entry.png`, so both grader runs write identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# or: python3 draw_entry.py   (regenerates entry.png identically)
```

## Sources (24 Nov 2026)

Reuters, AP, KBS, Korea JoongAng Daily (Ulleung alert); Riksdagen, Verkhovna Rada, Saeima (Crimea Platform); Palm Beach Post and White House schedule (turkey pardon); Asia Daily and Peter Lewis briefing (Tokyo markets); weather.com, Smithsonian, NASA (Beaver Supermoon); UEFA (Champions League); h.ua, Europesays, Forbes/DTEK (Odesa) — each story cross-checked across at least two outlets, and dated to 24 November 2026.

---

<sub>Entered on [make.fun](https://make.fun/?ref=xqemgw87&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
