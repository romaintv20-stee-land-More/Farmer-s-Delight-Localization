# Supported Minecraft versions

One development JAR per Minecraft version. Only Minecraft-native languages for that exact target.
Original Farmer's Delight translations always take precedence. Structural coverage does not guarantee native linguistic quality.

| Minecraft | Loader | Java | English keys | Minecraft locales | Missing-key fallbacks | Structurally covered | Specialist keys pending |
|---|---|---:|---:|---:|---:|---:|---:|
| 1.15.2 | forge | 8 | 144 | 122 | 14,995 | 118/121 | 432 |
| 1.16.1 | forge | 8 | 150 | 125 | 16,044 | 120/124 | 482 |
| 1.16.3 | forge | 8 | 198 | 125 | 20,522 | 120/124 | 628 |
| 1.16.5 | forge | 8 | 243 | 125 | 22,842 | 120/124 | 745 |
| 1.17.1 | forge | 16 | 236 | 123 | 21,567 | 117/122 | 971 |
| 1.18.1 | forge | 17 | 236 | 124 | 21,447 | 118/123 | 971 |
| 1.18.2 | forge | 17 | 258 | 124 | 22,051 | 118/123 | 1,034 |
| 1.19.2 | forge | 17 | 267 | 124 | 22,695 | 119/123 | 1,068 |
| 1.20.1 | forge | 17 | 429 | 143 | 40,840 | 129/142 | 5,282 |
| 1.20.4 | neoforge | 17 | 286 | 143 | 27,749 | 130/142 | 3,432 |
| 1.21.1 | neoforge | 21 | 479 | 143 | 45,701 | 129/142 | 5,936 |
| 26.1.2 | neoforge | 25 | 479 | 143 | 47,628 | 129/142 | 5,936 |

Inherited English variants are counted as structurally covered, not translated.

## Specialist language translation queue

- **1.15.2:** jbo_en (144), qya_aa (144), tlh_aa (144)
- **1.16.1:** jbo_en (150), qya_aa (150), tlh_aa (150), tok (32)
- **1.16.3:** jbo_en (198), qya_aa (198), tlh_aa (198), tok (34)
- **1.16.5:** jbo_en (243), qya_aa (243), tlh_aa (243), tok (16)
- **1.17.1:** jbo_en (236), qya_aa (236), tlh_aa (236), tok (27), zlm_arab (236)
- **1.18.1:** jbo_en (236), qya_aa (236), tlh_aa (236), tok (27), zlm_arab (236)
- **1.18.2:** jbo_en (258), qya_aa (258), tlh_aa (258), tok (2), zlm_arab (258)
- **1.19.2:** jbo_en (267), qya_aa (267), tlh_aa (267), zlm_arab (267)
- **1.20.1:** got_de (429), hal_ua (429), jbo_en (429), nah (429), pls (429), qcb_es (429), qid (429), qya_aa (429), tlh_aa (429), tok (134), tzo_mx (429), vro (429), zlm_arab (429)
- **1.20.4:** got_de (286), hal_ua (286), jbo_en (286), nah (286), pls (286), qcb_es (286), qid (286), qya_aa (286), tlh_aa (286), tzo_mx (286), vro (286), zlm_arab (286)
- **1.21.1:** got_de (479), hal_ua (479), jbo_en (479), nah (479), pls (479), qcb_es (479), qid (479), qya_aa (479), tlh_aa (479), tok (188), tzo_mx (479), vro (479), zlm_arab (479)
- **26.1.2:** got_de (479), hal_ua (479), jbo_en (479), nah (479), pls (479), qcb_es (479), qid (479), qya_aa (479), tlh_aa (479), tok (188), tzo_mx (479), vro (479), zlm_arab (479)

## Verified source policy

Farmer's Delight is pinned to its original Git commit per target. Official Minecraft language lists come from SHA-1-verified Mojang asset indices.
Minecraft 1.20.4 upstream Traditional Chinese (zh_tw) has a missing comma after line 312; its original strings are recovered into the fallback so they remain available.
