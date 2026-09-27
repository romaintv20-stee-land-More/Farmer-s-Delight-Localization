#!/usr/bin/env python3
"""Strict key-scope validation of all existing 1.15.2 fallbacks and packaged mod."""
from pathlib import Path
import argparse,json,re,zipfile
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"sources/farmersdelight/1.15.2"
LANG=ROOT/"src/forge_1152/resources/assets/farmersdelight/lang"
PH=re.compile(r"%(?:\d+\$)?[sdif]|§.|\\n")
def load(path):return json.loads(Path(path).read_text(encoding="utf-8"))
def main():
    p=argparse.ArgumentParser();p.add_argument("--jar");p.add_argument("--strict",action="store_true")
    args=p.parse_args()
    en=load(BASE/"en_us.json")
    locales=set(load(ROOT/"sources/minecraft/1.15.2_languages.json")["languages"])
    official={p.stem:load(p) for p in (BASE/"upstream").glob("*.json")}
    if len(en)!=144 or len(locales)!=122:raise RuntimeError("Upstream inventory drift")
    if not set(official)<locales:raise RuntimeError("Unofficial source locale")
    fallback={p.stem:load(p) for p in LANG.glob("*.json")}
    if not set(fallback)<locales:raise RuntimeError("Added language not offered in MC 1.15.2")
    if "en_us" in fallback:raise RuntimeError("Never override original English source")
    errors=[];total=0;pending=0;complete=0
    expected={}
    for locale in sorted(locales-{"en_us"}):
        src=official.get(locale,{})
        new=fallback.get(locale,{})
        overlap=set(src)&set(new)
        stale=set(new)-set(en)
        if overlap:errors.append(f"{locale}: {len(overlap)} official keys overridden")
        if stale:errors.append(f"{locale}: {len(stale)} stale keys")
        for key,value in new.items():
            if (not isinstance(value,str) or not value.strip() or
                sorted(PH.findall(en[key]))!=sorted(PH.findall(value))):
                errors.append(f"{locale}: invalid translation or placeholder: {key}")
        expected_keys=set(en)-(set(src)&set(en))
        expected[locale]=len(expected_keys)
        missing=expected_keys-set(new)
        if locale in {"en_gb","en_au","en_ca","en_nz","enp","enws"}:
            missing=set() # English naturally inherits mod's en_us baseline.
        if not missing:complete+=1
        total+=len(new);pending+=len(missing)
    if args.jar:
        with zipfile.ZipFile(args.jar) as jar:
            members=set(jar.namelist())
            for name in ("META-INF/mods.toml","pack.mcmeta",
                "fr/rtv20/farmersdelightlocalization/FarmersDelightLocalization.class"):
                if name not in members:errors.append(f"JAR missing {name}")
            embedded={n.rsplit("/",1)[-1][:-5] for n in members
                if re.fullmatch(r"assets/farmersdelight/lang/[a-z0-9_]+\.json",n)}
            if embedded!=set(fallback):errors.append("JAR translation inventories differ from source")
            for locale,src in fallback.items():
                path=f"assets/farmersdelight/lang/{locale}.json"
                if load_embedded(jar,path)!=src:errors.append(f"JAR mismatch: {locale}")
    if errors:raise SystemExit("\n".join(errors))
    print(f"PASS: 1.15.2; {len(locales)} official Minecraft languages; "
          f"{total} actual fallback translations; {pending} missing; "
          f"{complete}/121 locales fully covered or inheriting English.")
    if args.strict and pending:raise SystemExit(f"Strict coverage failed: {pending} keys still missing")
def load_embedded(archive,path):
    return json.loads(archive.read(path).decode("utf-8"))
if __name__=="__main__":main()
