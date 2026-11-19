# The World Today — Thursday 19 November 2026

A one-page broadsheet front page for the make.fun `news-image-20261119`
competition: the whole world of Thursday 19 November 2026 on a single
1024×1024 page.

![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)
[![rank](https://make.fun/badge/news-image-20261119/rezimx-btc/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/rezimx-btc/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

## The page

- **Masthead:** THE WORLD TODAY, dated Thursday, 19 November 2026.
- **Lead story:** *Vice City Opens Its Gates* — after a 13-year wait,
  Grand Theft Auto VI begins its global rollout, with a hand-drawn
  sunset skyline over Vice City.
- **The World in One Glance:** a stylised world map with six numbered
  markers for the day's big stories — Shenzhen (Trump, Xi and Putin at
  APEC), the Gulf (US–Iran fire), India's east coast (Cyclone Akvan),
  Kyiv (the EU's €45bn Ukraine loan), Washington (Jeffries nominated
  for Speaker) and London (the record Van Gogh sale).
- **Nine more stories** in three columns: Fed minutes pointing to more
  rate hikes, Nvidia halting H-chip shipments to China, the EU's Ukraine
  loan, Voyager 1 reaching one light-day, Anthropic's $1.4tn debut, and
  more — plus a markets ticker (gold down nearly 5% to $3,730).

## Headlines used (all real, from the wires of 19 November 2026)

1. GTA VI begins its global rollout — gamers enter Vice City
2. Trump, Xi and Putin shake hands in Shenzhen; trilateral talks at APEC
3. US and Iran exchange fire again; Iran widens attacks on Gulf states
4. Van Gogh sells for a record $190.4m after a row over its Nazi history
5. Fed minutes: most officials expect further rate hikes
6. Nvidia stops shipping H-series chips to China; acting CEO promises
   earlier pay rises
7. Cyclone Akvan nears India's east coast (Machilipatnam–Puri)
8. EU proposes a €45bn Ukraine loan, repaid after Russia pays reparations
9. Voyager 1 reaches one light-day from Earth after almost 50 years
10. Anthropic poised for a $1.4tn stock market debut
11. Gold plunges nearly 5% to $3,730 an ounce
12. Jeffries nominated by Democrats — could be the first Black Speaker

## How it works

`main.py` uses only the Python standard library. It draws its own 5×7
bitmap font, the map, the skyline and every rule and headline, then
encodes the PNG itself (zlib + struct, no Pillow, no network).

## Running it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 -S main.py
# writes /tmp/out/entry.png (1024x1024, deterministic)
```

The program writes **only** to `MAKEFUN_OUTPUT_DIR` (default `/output`,
as the grader provides it). It never writes to the current directory:
the graded run mounts the repository read-only, so the output must go
to the writable output directory.

Run it twice and the two PNGs are byte-identical (fixed content, no
timestamps, no randomness).

## Entry

Competition: https://make.fun/bounty/news-image-20261119
