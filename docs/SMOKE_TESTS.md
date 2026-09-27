# In-game smoke tests

## Minecraft 1.21.1 / NeoForge 21.1.219 — PASS (2026-09-27)

Test environment:

- Minecraft 1.21.1
- NeoForge 21.1.219 / FML 4.0.42
- Java 21.0.6
- Farmer's Delight 1.3.4 from its official 1.21 development branch
- Farmer's Delight Localization 0.1.0 development JAR

Observed in the live client log:

- `Farmer's Delight 1.3.4 (farmersdelight)`
- `Farmer's Delight Localization 0.1.0 (farmersdelight_localization)`
- ResourceManager reload contains both `mod/farmersdelight` and `mod/farmersdelight_localization`.
- Minecraft reached normal render/resource loading with OpenGL, fonts, sounds and texture atlases initialized.
- No fatal or loading error was attributed to `farmersdelight_localization`.

A warning for the absent JEI development class `mezz.jei.library.load.PluginCaller` appeared because JEI was not present in the userdev run; Farmer's Delight continued loading with EMI/CraftTweaker and the localization add-on.

This smoke test validates mod discovery and resource loading. It does not replace visual review of every translated string.

## Minecraft 1.20.4 / NeoForge 20.4.189 — PASS (2026-09-27)

The official Farmer's Delight 1.20.4 development branch was started with Java 17, NeoForge 20.4.189 and our 1.20.4 localization JAR. Its pinned CraftTweaker runtime dependency currently references an unavailable REI artifact, so CraftTweaker runtime loading was disabled only in the disposable upstream test clone; our addon repository and JAR were not modified.

The live client log confirms the localization JAR was discovered from the mods directory, NeoForge injected its event subscribers, and ResourceManager reloaded both `mod:farmersdelight` and `mod:farmersdelight_localization`. The client reached normal font, sound and texture loading without a fatal error from the localization addon.

The structural audit separately verifies that the malformed original `zh_tw.json` translations are recovered in our valid 1.20.4 fallback.

## Pending

The remaining Minecraft targets are still awaiting equivalent in-game smoke tests:

- Forge: 1.15.2, 1.16.1, 1.16.3, 1.16.5, 1.17.1, 1.18.1, 1.18.2, 1.19.2, 1.20.1
- NeoForge: 26.1.2
