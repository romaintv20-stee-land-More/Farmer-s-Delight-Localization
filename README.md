# Farmer's Delight Localization

Independent client-side localization companion for Farmer's Delight by vectorwing.
Adds **only missing translation keys**; the original mod's complete or partial official translations remain unchanged.

## Supported versions

Version-first development is implemented for **12 Minecraft targets** from 1.15.2 Forge to 26.1.2 NeoForge.
Only the official Minecraft languages for each version are supported; custom extra languages are not added.
Each build is one JAR containing its version-specific fallback translations.

| Minecraft | Loader | Java |
|---|---|---:|
| 1.15.2 | forge | 8 |
| 1.16.1 | forge | 8 |
| 1.16.3 | forge | 8 |
| 1.16.5 | forge | 8 |
| 1.17.1 | forge | 16 |
| 1.18.1 | forge | 17 |
| 1.18.2 | forge | 17 |
| 1.19.2 | forge | 17 |
| 1.20.1 | forge | 17 |
| 1.20.4 | neoforge | 17 |
| 1.21.1 | neoforge | 21 |
| 26.1.2 | neoforge | 25 |

Full verified counts and unfinished specialist languages: [Version and coverage matrix](docs/VERSION_MATRIX.md).

## Dependency

Install the matching original Farmer's Delight build for the selected Minecraft version. This mod does not contain the original mod's gameplay.

## Rules

- Use each upstream release's exact English key inventory; keep its own existing locale files authoritative.
- Reuse newer official translations or Beyond & More only when the original English meaning and formatting match.
- Add fallback strings for missing keys of Minecraft-native languages only.
- Validate JSON, formatting variables, version-specific resources and the mod JAR for each target.
- Do not distribute fabricated translations for specialist or novelty languages that require human expertise.

## Development preview

All 12 version inventories are prepared and automatically audited. The 11 earlier targets build locally with JDK 21; Java 25 for Minecraft 26.1.2 is built on GitHub Actions.
Full native-speaker review and in-game testing are **not yet complete**. Automated builds are not a claim of stable release readiness.

## Build

Use Python 3.12+ and JDK 21 (JDK 25 to compile the latest target):

    python scripts/audit_targets.py --all --strict-available-locales
    python scripts/build_all.py --all
    python scripts/audit_targets.py --target 1.21.1 --jar dist/farmersdelight-localization-0.1.0+1.21.1-neoforge.jar

GitHub Actions runs a separate job per target and uploads a version-specific JAR.

## Source and attribution

Original mod: https://github.com/vectorwing/FarmersDelight ; MIT license.
See docs/ATTRIBUTIONS.md and licenses/FarmersDelight-LICENSE.txt. This is an unofficial project.
