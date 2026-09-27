# Translation and gameplay QA queue

Source-key and packaging audits are structural only. They do not certify natural language quality or real Forge/NeoForge loading.

## Outstanding specialist-language strings

- 1.15.2: jbo_en=144, qya_aa=144, tlh_aa=144
- 1.16.1: jbo_en=150, qya_aa=150, tlh_aa=150, tok=32
- 1.16.3: jbo_en=198, qya_aa=198, tlh_aa=198, tok=34
- 1.16.5: jbo_en=243, qya_aa=243, tlh_aa=243, tok=16
- 1.17.1: jbo_en=236, qya_aa=236, tlh_aa=236, tok=27, zlm_arab=236
- 1.18.1: jbo_en=236, qya_aa=236, tlh_aa=236, tok=27, zlm_arab=236
- 1.18.2: jbo_en=258, qya_aa=258, tlh_aa=258, tok=2, zlm_arab=258
- 1.19.2: jbo_en=267, qya_aa=267, tlh_aa=267, zlm_arab=267
- 1.20.1: got_de=429, hal_ua=429, jbo_en=429, nah=429, pls=429, qcb_es=429, qid=429, qya_aa=429, tlh_aa=429, tok=134, tzo_mx=429, vro=429, zlm_arab=429
- 1.20.4: got_de=286, hal_ua=286, jbo_en=286, nah=286, pls=286, qcb_es=286, qid=286, qya_aa=286, tlh_aa=286, tzo_mx=286, vro=286, zlm_arab=286
- 1.21.1: got_de=479, hal_ua=479, jbo_en=479, nah=479, pls=479, qcb_es=479, qid=479, qya_aa=479, tlh_aa=479, tok=188, tzo_mx=479, vro=479, zlm_arab=479
- 26.1.2: got_de=479, hal_ua=479, jbo_en=479, nah=479, pls=479, qcb_es=479, qid=479, qya_aa=479, tlh_aa=479, tok=188, tzo_mx=479, vro=479, zlm_arab=479

## Release blockers

- Native review for all generated and dialect-proxy translations, including Pirate Speak, LOLCAT, RTL locales and regional dialects.
- Authentic versions of specialist-language strings rather than unrelated language substitutes.
- Start and test the exact original Farmer's Delight dependency on every matching Forge/NeoForge client.
- Confirm the original mod's translations retain priority, every format variable displays, and Chinese 1.20.4 recovery works.
- Check GitHub Actions outputs and mod-loader metadata for every version before stable release.
