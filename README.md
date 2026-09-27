# Farmer's Delight Localization

An independent client-side translation add-on for [Farmer's Delight](https://github.com/vectorwing/FarmersDelight). The add-on provides only strings **missing from the original mod**. Farmer's Delight's official translations remain untouched and take precedence.

## Oldest version first

The first target is **Minecraft 1.15.2 with Forge**. Its pinned Farmer's Delight branch contains **144 English translation keys** and eight translated locale files. Mojang's official Minecraft 1.15.2 asset index lists **122 selectable languages**; our project includes no languages outside that index.

Following releases will be developed chronologically across the official 1.16.1, 1.16.3, 1.16.5, 1.17.1, 1.18.1, 1.18.2, 1.19, 1.20, 1.20.4, 1.21 and 26.1 branches. Each version will use its own source baseline and its own official Minecraft language inventory. Forge is necessary for older versions; NeoForge support will follow the upstream mod's available loaders.

## Translation policy

- Retain all official Farmer's Delight translations; add only missing keys.
- When a source string is unchanged, reuse official translations from newer Farmer's Delight branches or translations from Beyond & More.
- Translate the remaining strings for official Minecraft locales and validate key coverage, text formatting and packaged resources.
- Mark automatically generated translations as requiring native-speaker review.
- Special official novelty languages (Pirate Speak, upside-down English, Quenya, etc.) need bespoke translation rather than misleading ordinary machine translation.

## Status

**Development build / work in progress:** Minecraft 1.15.2. Current measured coverage: 118/121 non-English locales complete (including English-inheriting variants), 14,995 new fallback entries, and 432 strings still awaiting genuine translations in three specialized novelty languages. Details: reports/1.15.2_coverage.json and docs/QA_PENDING.md. A passing build does not mean that all translations have been native-reviewed or tested in Minecraft. Do not label the add-on a stable release until those checks are complete.

## Build

Requires Python 3.11+ and JDK 21 for the build process. The compiled class files target **Java 8**, as required by Minecraft 1.15.2.

1. Run python scripts/audit.py to verify the translation keys and available official locales.
2. Run python scripts/build_jar.py to create the Minecraft 1.15.2 Forge mod JAR.
3. Run python scripts/audit.py --jar dist/farmersdelight-localization-0.1.0+1.15.2.jar to validate the archive.

The build compiles a minimal Forge annotation class against a temporary compile-only declaration; that declaration is not bundled into the finished JAR. Runtime compatibility and appearance in game still require testing on the real Forge client.

## Translation generation

Run python scripts/generate_fallbacks.py --seed --generate to reuse existing translations and identify missing keys. Use the --translate option only where automatic translation is appropriate. The translator stores its checkpoint in the ignored work directory and can resume interrupted batches.

All files under sources/farmersdelight/1.15.2 are pinned to the upstream 1.15.2 branch; the official Minecraft language lists under sources/minecraft are pinned to Mojang's asset-index SHA-1.

## Dependencies and attribution

Install Farmer's Delight separately. This add-on provides translations, not Farmer's Delight gameplay content. See docs/ATTRIBUTIONS.md and licenses/FarmersDelight-LICENSE.txt. This project is unofficial and not affiliated with the original mod authors.
