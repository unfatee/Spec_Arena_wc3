# Spec Arena 2.5.7.3 by Fawk

Warcraft III custom map based on SpecArena v2.5.7.2.

The tested release file is:

`dist/SA2573S2.w3x`

In the Warcraft III lobby the map is named `Spec Arena 2.5.7.3 by Fawk`.

## Contents

- `dist/SA2573S2.w3x` - playable release build.
- `source/` - final extracted map files that were overwritten in the MPQ archive.
- `scripts/rebuild-from-base.ps1` - local rebuild helper.
- `scripts/object_tools.py` - helper for reading/writing Warcraft III object files.
- `tools/README.md` - where to put `mpqcli.exe` if you want to rebuild locally.

## Release Info

- Warcraft III build used during testing: `1.26.0.6401`.
- The `SA2573S2.w3x` build was confirmed to open and launch.
- Current packaged map SHA256:

```text
5892BB166EBF4D7B9CDAD49454506242E6F0FD6318FD7A9689B81946A54DA3B2
```

## Main Changes

- Fixed F9/info text and lobby/loading text handling.
- Added `SoakingFawk` to authors/version info.
- San / Fire Skeleton:
  - Fire Breath cooldown 20 sec and intelligence scaling.
  - Fireball intelligence scaling.
  - Fire Aura intelligence scaling and +10 intelligence per level, up to +80.
  - Explode cooldown 30 sec.
- Arid:
  - Shooting switches to ranged forms with attack ranges 300/300/400/400/500/500.
- Earlier balance/fix work is preserved in the included map source files.

## Local Install

Copy `dist/SA2573S2.w3x` to:

```text
C:\war\Maps\Download\
```

Then select the map in Warcraft III.

## Rebuild

The repository does not commit `mpqcli.exe`. Put it here:

```text
tools\mpqcli.exe
```

Then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\rebuild-from-base.ps1
```

By default the script uses the local backup map path from the development machine. You can pass another compatible full Spec Arena MPQ map:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\rebuild-from-base.ps1 -BaseMap "C:\path\to\base-or-previous-build.w3x"
```

## Notes

This repository is prepared for modding/version tracking. Warcraft III, its assets, and trademarks belong to Blizzard Entertainment. Original map authorship is preserved in the map info.

