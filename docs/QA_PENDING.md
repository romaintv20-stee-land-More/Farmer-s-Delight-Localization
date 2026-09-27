# Translation QA — Minecraft 1.15.2 (development)

## Measured structural coverage

- 122 official Minecraft locales, including en_us.
- 144 original English keys; eight original upstream locale files retained.
- Original upstream translations: 1,134 entries across non-English locales.
- Missing-only fallback translations: 14,995 entries.
- 118 of 121 non-English locales covered, including the expected English-inheriting variants.
- Lojban (jbo_en), Quenya (qya_aa) and Klingon (tlh_aa) remain incomplete: 144 strings each, 432 total.

Do not represent the incomplete novelty languages as translated. Minecraft's standard en_us fallback remains available until genuine strings can be reviewed.

## Provisional variants

Pirate Speak has 50 style-generated entries and seven newer upstream same-key values. LOLCAT has 72 style-generated entries and three same-key values. Upside-down English has 144 algorithmically flipped entries. These values need linguistic review.

Hawaiian was generated against the actual Hawaiian language target. The automatic translations and any proxy-language translations remain unreviewed by native speakers.

## Testing still needed

Load the development JAR with Minecraft 1.15.2, Forge 31.2.12+, and the original Farmer's Delight. Verify real client loading, key display, font support, formatting and upstream translation priority.

Source-key and JAR audits passing is not a substitute for native linguistic review or in-game validation.
