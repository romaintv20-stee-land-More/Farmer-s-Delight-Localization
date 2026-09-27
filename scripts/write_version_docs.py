#!/usr/bin/env python3
"""Generate accurate user-facing documentation from pinned audit reports."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from targets import TARGETS
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def save(p,lines):p.write_text("\n".join(lines).rstrip()+"\n",encoding="utf-8")
reports=[]
for t in TARGETS:
    v=t["mc"];q=load(ROOT/"reports"/(v+"_translation_summary.json"))
    n=q["minecraft_native_languages"];complete=n-1-len(q["incomplete_locales"])
    reports.append((t,q,complete))
matrix=["# Supported Minecraft versions","","One development JAR per Minecraft version. Only Minecraft-native languages for that exact target.","Original Farmer's Delight translations always take precedence. Structural coverage does not guarantee native linguistic quality.","",
"| Minecraft | Loader | Java | English keys | Minecraft locales | Missing-key fallbacks | Structurally covered | Specialist keys pending |",
"|---|---|---:|---:|---:|---:|---:|---:|"]
for t,q,complete in reports:
    matrix.append("| {} | {} | {} | {} | {} | {:,} | {}/{} | {:,} |".format(
      t["mc"],t["loader"],t["java"],q["english_keys"],q["minecraft_native_languages"],
      q["fallback_keys"],complete,q["minecraft_native_languages"]-1,q["pending"]))
matrix+=["","Inherited English variants are counted as structurally covered, not translated.","",
"## Specialist language translation queue",""]
for t,q,_ in reports:
    if q["incomplete_locales"]:
        matrix.append("- **{}:** {}".format(t["mc"],", ".join("{} ({})".format(k,v)
                 for k,v in q["incomplete_locales"].items())))
matrix+=["","## Verified source policy","",
"Farmer's Delight is pinned to its original Git commit per target. Official Minecraft language lists come from SHA-1-verified Mojang asset indices.",
"Minecraft 1.20.4 upstream Traditional Chinese (zh_tw) has a missing comma after line 312; its original strings are recovered into the fallback so they remain available."]
save(ROOT/"docs/VERSION_MATRIX.md",matrix)
readme=["# Farmer's Delight Localization","",
"Independent client-side localization companion for Farmer's Delight by vectorwing.",
"Adds **only missing translation keys**; the original mod's complete or partial official translations remain unchanged.","",
"## Supported versions","",
"Version-first development is implemented for **12 Minecraft targets** from 1.15.2 Forge to 26.1.2 NeoForge.",
"Only the official Minecraft languages for each version are supported; custom extra languages are not added.",
"Each build is one JAR containing its version-specific fallback translations.","",
"| Minecraft | Loader | Java |",
"|---|---|---:|"]
for t,_,_ in reports:readme.append("| {} | {} | {} |".format(t["mc"],t["loader"],t["java"]))
readme+=["",
"Full verified counts and unfinished specialist languages: [Version and coverage matrix](docs/VERSION_MATRIX.md).","",
"## Dependency","",
"Install the matching original Farmer's Delight build for the selected Minecraft version. This mod does not contain the original mod's gameplay.",
"",
"## Rules","",
"- Use each upstream release's exact English key inventory; keep its own existing locale files authoritative.",
"- Reuse newer official translations or Beyond & More only when the original English meaning and formatting match.",
"- Add fallback strings for missing keys of Minecraft-native languages only.",
"- Validate JSON, formatting variables, version-specific resources and the mod JAR for each target.",
"- Do not distribute fabricated translations for specialist or novelty languages that require human expertise.",
"",
"## Development preview","",
"All 12 version inventories are prepared and automatically audited. The 11 earlier targets build locally with JDK 21; Java 25 for Minecraft 26.1.2 is built on GitHub Actions.",
"Full native-speaker review and in-game testing are **not yet complete**. Automated builds are not a claim of stable release readiness.",
"",
"## Build","",
"Use Python 3.12+ and JDK 21 (JDK 25 to compile the latest target):",
"",
"    python scripts/audit_targets.py --all --strict-available-locales",
"    python scripts/build_all.py --all",
"    python scripts/audit_targets.py --target 1.21.1 --jar dist/farmersdelight-localization-0.1.0+1.21.1-neoforge.jar",
"",
"GitHub Actions runs a separate job per target and uploads a version-specific JAR.",
"",
"## Source and attribution","",
"Original mod: https://github.com/vectorwing/FarmersDelight ; MIT license.",
"See docs/ATTRIBUTIONS.md and licenses/FarmersDelight-LICENSE.txt. This is an unofficial project."]
save(ROOT/"README.md",readme)
changelog=["# Unreleased — 0.1.0 development preview","",
"- Prepared 12 chronological Farmer's Delight source baselines and respective native Minecraft language inventories.",
"- Added version-specific translation fallback resources without overriding valid original upstream keys.",
"- Added source-language memory reuse, automated translation, formatting audits and per-version JAR checks.",
"- Added Forge/NeoForge CI build matrix: one JAR per supported Minecraft version.",
"- Fixed outstanding Tatar and Latin formatting gaps and restored original Traditional Chinese strings from malformed 1.20.4 upstream JSON.",
"- Tracked authentic specialist-language translations as unfinished work rather than silently using unrelated proxy languages.","",
"Native-speaker review and in-game testing are still required before a stable release.",
"See VERSION_MATRIX.md for all counts and the detailed outstanding queue."]
save(ROOT/"docs/CHANGELOG_DEV.md",changelog)
qa=["# Translation and gameplay QA queue","",
"Source-key and packaging audits are structural only. They do not certify natural language quality or real Forge/NeoForge loading.","",
"## Outstanding specialist-language strings",""]
for t,q,_ in reports:
    if q["incomplete_locales"]:qa.append("- {}: {}".format(t["mc"],", ".join("{}={}".format(k,n) for k,n in q["incomplete_locales"].items())))
qa+=["","## Release blockers","",
"- Native review for all generated and dialect-proxy translations, including Pirate Speak, LOLCAT, RTL locales and regional dialects.",
"- Authentic versions of specialist-language strings rather than unrelated language substitutes.",
"- Start and test the exact original Farmer's Delight dependency on every matching Forge/NeoForge client.",
"- Confirm the original mod's translations retain priority, every format variable displays, and Chinese 1.20.4 recovery works.",
"- Check GitHub Actions outputs and mod-loader metadata for every version before stable release."]
save(ROOT/"docs/QA_PENDING.md",qa)
print("Updated README, coverage matrix, changelog and QA for",len(reports),"versions",flush=True)
