# Live Tennis Scores

Type `:tennis` and it expands to a compact one-line summary of the tennis
matches that are live right now:

```
Carlos Alcaraz 6-4 3-2* vs Jannik Sinner · Coco Gauff 2-6 1-1* vs Iga Swiatek
```

Per match: player 1, the per-set game scores (`*` marks the set currently in
play), player 2. Up to 3 matches, separated by `·`. If nothing is live it
expands to `No live matches right now`.

Powered by the [Live Tennis API](https://livetennisapi.com) (ATP, WTA,
Challenger, ITF, juniors).

## Installation

Make sure you have [Espanso](https://espanso.org/install/) installed first.

```sh
espanso install live-tennis-scores
```

## Setup — API key required

This package calls a **keyed** API. The free tier is enough: it includes the
live-scores endpoint used here at **30 requests/minute, 100 requests/day** —
far more than a text-expansion trigger will ever use.

1. Get a free key at <https://livetennisapi.com/subscribe/free> (no card).
2. Make it available to espanso as the `LIVETENNIS_API_KEY` environment
   variable:
   - **Linux**: add `export LIVETENNIS_API_KEY=your-key` to your shell profile
     (e.g. `~/.profile`) and log out/in, or set it in the environment of
     whatever starts espanso.
   - **macOS**: GUI apps don't read your shell profile; run
     `launchctl setenv LIVETENNIS_API_KEY your-key` (repeat at login, or put it
     in a LaunchAgent), then restart espanso.

Without the key the trigger still expands — to a short setup hint instead of
scores — so it never fails silently.

## How it works (transparency)

The whole thing is one shell pipeline you can read in
[`package.yml`](package.yml):

```sh
curl -s -H "Authorization: Bearer $LIVETENNIS_API_KEY" \
  "https://api.livetennisapi.com/api/public/v1/matches?status=live&limit=3"
```

piped through `grep -o` (keeps only the two player `name` fields and the
per-set `games` arrays of each match) and a short `awk` program that pairs
them into `6-4 3-2*` lines. No jq, no scripts, no files touched, nothing
executed beyond `curl | grep | awk`.

API reference for the endpoint and fields:
<https://docs.livetennisapi.com> (`GET /matches?status=live`).

## Requirements

- `curl` (plus POSIX `grep`/`awk`/`sh`, preinstalled on Linux and macOS)
- Not tested on Windows (the pipeline assumes a POSIX shell; under WSL it
  works)

## License

MIT
