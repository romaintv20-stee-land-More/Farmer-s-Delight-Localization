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

## Pending

The remaining Minecraft targets are still awaiting equivalent in-game smoke tests:

- Forge: 1.15.2, 1.16.1, 1.16.3, 1.16.5, 1.17.1, 1.18.1, 1.18.2, 1.19.2, 1.20.1
- NeoForge: 1.20.4, 26.1.2

Minecraft 1.20.4 must additionally verify the recovered Traditional Chinese fallback because the upstream `zh_tw.json` is malformed.
