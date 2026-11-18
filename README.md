[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/yugot-coder/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/yugot-coder/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

# The Day in Full — Tuesday 17 November 2026

An entry for make.fun's **news-image-20261117**: one image that sums up
the world's news of Tuesday 17 November 2026.

The image is a one-page newspaper front page, *The Day in Full*:

- **Lead:** Iran fires drones at a U.S. radar site in Bahrain — its
  third attack in four days, ending a two-month lull; Bahrain says it
  downed them, a U.S. carrier group arrives in the region, and mines
  and missiles batter Strait of Hormuz shipping — with a schematic
  map of the strait.
- **Summitry:** Trump meets Quad leaders in Manila (critical-minerals
  pacts) and flies on to Shenzhen for a first three-way summit with
  Xi Jinping and Vladimir Putin at APEC.
- **Crimea:** a second night of Ukrainian strikes collapses a road
  span of the Kerch Bridge; two die in Crimea.
- **Tech:** Nvidia reports a $115.8B quarter, but its board will not
  reinstate Jensen Huang after the spy-affair scandal.
- **Markets:** the S&P 500 falls 1.9% ahead of Nvidia's results; oil
  slips to about $92 despite the Gulf attacks.
- **Japan:** two Russian planes breach Japanese airspace off
  Okinoshima; Tokyo scrambles fighter jets.
- **Games:** GTA VI's 212 GB pre-load is live, with 15M+ pre-orders
  before Thursday's midnight launch.
- **Briefs:** the UK, Australia, Canada and Italy urge Israel to open
  Gaza crossings; settlers kill a Palestinian woman, 72, near Jericho;
  Mongolia's president resigns.

## How it works

- `build_poster.py` renders `poster.png` (1024×1024) with Pillow from
  the day's wire reports. It runs once, at build time, on the author's
  machine; rendering is deterministic (fixed fonts, no clock, no
  randomness).
- `main.py` is the submitted program (Python 3.13, standard library
  only). It copies `poster.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
  (default `/output/entry.png`), byte for byte, so repeated runs write
  identical bytes.

## License

MIT — see `LICENSE`.
