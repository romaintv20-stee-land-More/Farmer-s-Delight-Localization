# Development changelog (unreleased)

## 0.1.0 — first target: Minecraft 1.15.2 / Forge

- Established the earliest Farmer's Delight localization baseline at upstream commit 4e67d3281a3ccb19594773ba6a186b6c66440eef.
- Indexed all 144 original English translation keys and the eight upstream translation files.
- Pinned Minecraft 1.15.2's 122 officially available language codes to Mojang's verified asset index.
- Added translation-memory reuse from later official Farmer's Delight translations and the author's Beyond & More project, only when English source values match.
- Added resumable automatic translation for missing strings, explicit review flags and validation of formatting placeholders.
- Added a standalone client-side Forge mod JAR builder targeting Java 8, with no upstream mod code bundled.
- Added checks that official translation keys are never overwritten or supplemented by unsupported language codes.
- Added automatic GitHub Actions structural audits, build and JAR inspection.

The 1.15.2 build is a development preview until all languages are fully translated, reviewed and tested in game. Later Minecraft branches will be added in chronological order.
