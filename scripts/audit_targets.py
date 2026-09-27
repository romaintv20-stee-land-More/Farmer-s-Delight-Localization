#!/usr/bin/env python3
"""Audit every Minecraft-version-specific localization source and compiled JAR."""
from pathlib import Path
import argparse,json,re,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from targets import INDEX,TARGETS,source,native_locales,fallback_folder
PH=re.compile(r"%(?:\d+\$)?[sdif]|§.|\\n")
NATIVE_REVIEW_REQUIRED={"jbo_en","qya_aa","tlh_aa","tok","zlm_arab",
  "got_de","hal_ua","nah","pls","qcb_es","qid","tzo_mx","vro"}
SKIP=NATIVE_REVIEW_REQUIRED  # Genuine specialist-language translations remain outstanding.
ENGLISH={"en_gb","en_au","en_ca","en_nz","enp","enws"}
def read(path):return json.loads(Path(path).read_text(encoding="utf-8"))
def audit(target,jar=None,strict=False):
    mc=target["mc"]
    en=read(source(target)/"en_us.json")
    official={x.stem:read(x) for x in (source(target)/"upstream").glob("*.json")}
    locales=set(native_locales(target))
    fallback={x.stem:read(x) for x in fallback_folder(target).glob("*.json")}
    errors=[]
    manifest=read(source(target)/"source_manifest.json")
    if manifest["english_keys"]!=len(en):errors.append(f"{mc}: original English inventory changed")
    expected=manifest.get("official_translations",manifest.get("upstream_locale_files"))
    if expected!=len(official):errors.append(f"{mc}: official locale snapshot incomplete: {len(official)} / {expected}")
    native_count=manifest.get("minecraft_languages",manifest.get("official_minecraft_languages"))
    if native_count!=len(locales):errors.append(f"{mc}: official Minecraft language inventory changed")
    for locale,issue in manifest.get("malformed_upstream_locale",{}).items():
        restored=read(source(target)/"upstream_invalid"/(locale+".json"))
        installed=fallback.get(locale,{})
        if not restored or any(installed.get(k)!=v for k,v in restored.items()):
            errors.append(f"{mc}: original translations from malformed upstream {locale} were not preserved")
    if not en or "en_us" not in locales:errors.append(f"{mc}: no official English keys")
    if not set(fallback).issubset(locales-{"en_us"}):
        errors.append(f"{mc}: translations outside Minecraft official locales")
    if not set(official).issubset(locales-{"en_us"}):
        errors.append(f"{mc}: source inventory includes unofficial Minecraft locales")
    missing_by_locale={}
    total=0;original=0;fully=0
    for locale in sorted(locales-{"en_us"}):
        upstream=official.get(locale,{})
        local=fallback.get(locale,{})
        orig_keys=set(en)&set(upstream)
        original+=len(orig_keys);total+=len(local)
        overlap=orig_keys&set(local)
        stale=set(local)-set(en)
        if overlap:errors.append(f"{mc} {locale}: {len(overlap)} original translations overridden")
        if stale:errors.append(f"{mc} {locale}: {len(stale)} obsolete keys")
        for key,value in local.items():
            if key not in en:continue
            if (not isinstance(value,str) or not value.strip() or
                sorted(PH.findall(en[key]))!=sorted(PH.findall(value))):
                errors.append(f"{mc} {locale}: invalid format: {key}")
        missing=set(en)-orig_keys-set(local)
        if locale in ENGLISH:missing=set()
        if not missing:fully+=1
        elif strict and locale not in SKIP:
            errors.append(f"{mc} {locale}: {len(missing)} non-novelty keys missing")
        if missing:missing_by_locale[locale]=len(missing)
    if jar:
        with zipfile.ZipFile(jar) as archive:
            members=set(archive.namelist())
            path="META-INF/mods.toml" if target["loader"]=="forge" or mc=="1.20.4" else "META-INF/neoforge.mods.toml"
            clazz="fr/rtv20/farmersdelightlocalization/FarmersDelightLocalization.class"
            for key in (path,"pack.mcmeta",clazz,"LICENSE"):
                if key not in members:errors.append(f"{mc}: missing {key}")
            if path in members:
                metadata=archive.read(path).decode("utf-8")
                if f'loaderVersion="{target["loader_range"]}"' not in metadata:
                    errors.append(f"{mc}: incorrect FML loader range")
                dep_pattern=(r'\[\[dependencies\.[^\]]+\]\][\s\S]*?modId\s*=\s*"'
                             +re.escape(target["loader"])+r'"[\s\S]*?versionRange\s*=\s*"([^"]+)"')
                dep=re.search(dep_pattern,metadata)
                if not dep or dep.group(1)!=target["platform_range"]:
                    errors.append(f"{mc}: incorrect {target['loader']} dependency range")
                mcdep=re.search(r'\[\[dependencies\.[^\]]+\]\][\s\S]*?modId\s*=\s*"minecraft"[\s\S]*?versionRange\s*=\s*"([^"]+)"',metadata)
                if not mcdep or mcdep.group(1)!=f"[{mc}]":
                    errors.append(f"{mc}: incorrect Minecraft dependency range")
            if clazz in members:
                content=archive.read(clazz)
                major=int.from_bytes(content[6:8],"big")
                if major!=target["java"]+44:errors.append(f"{mc}: Java class version {major}")
                expected=b"net/minecraftforge/fml/common/Mod" if target["loader"]=="forge" else b"net/neoforged/fml/common/Mod"
                if expected not in content:errors.append(f"{mc}: wrong annotation")
            if "pack.mcmeta" in members:
                pack=json.loads(archive.read("pack.mcmeta"))["pack"]
                if pack["pack_format"]!=target["pack"]:errors.append(f"{mc}: wrong pack format")
            packaged={p.split("/")[-1][:-5] for p in members if re.fullmatch(
                r"assets/farmersdelight/lang/[a-z0-9_]+\.json",p)}
            if packaged!=set(fallback):errors.append(f"{mc}: packaged locales mismatch")
            for locale,data in fallback.items():
                path="assets/farmersdelight/lang/"+locale+".json"
                if path in members and json.loads(archive.read(path))!=data:
                    errors.append(f"{mc}: translation mismatch {locale}")
    if errors:raise RuntimeError("\n".join(errors[:30]))
    print("PASS",mc,target["loader"],"MC locales",len(locales),
          "original keys",original,"fallback",total,"fully covered",
          fully,"/",len(locales)-1,"incomplete",missing_by_locale,flush=True)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--target",choices=list(INDEX))
    p.add_argument("--all",action="store_true")
    p.add_argument("--jar")
    p.add_argument("--strict-nonnovelty","--strict-available-locales",dest="strict_nonnovelty",action="store_true",
      help="Fail on missing strings except explicitly tracked specialist languages requiring native review")
    args=p.parse_args()
    if args.jar and not args.target:p.error("--jar requires --target")
    jobs=[INDEX[args.target]] if args.target else TARGETS if args.all else [INDEX["1.15.2"]]
    for target in jobs:
        if args.all and args.jar:raise RuntimeError("Use --target for a JAR")
        audit(target,args.jar,args.strict_nonnovelty)
if __name__=="__main__":main()
