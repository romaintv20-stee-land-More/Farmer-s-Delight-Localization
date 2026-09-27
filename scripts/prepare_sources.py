#!/usr/bin/env python3
"""Snapshot an upstream Farmer's Delight branch and calculate exact missing translations."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
PREFIX=ROOT.parent
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def dump(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def prepare(version,upstream):
    lang=upstream/"src/main/resources/assets/farmersdelight/lang"
    if not lang.is_dir():raise FileNotFoundError(lang)
    source=ROOT/"sources/farmersdelight"/version
    en=load(lang/"en_us.json")
    supported=load(ROOT/"sources/minecraft"/f"{version}_languages.json")["languages"]
    source.mkdir(parents=True,exist_ok=True)
    dump(source/"en_us.json",en)
    official=source/"upstream"
    official.mkdir(parents=True,exist_ok=True)
    for f in lang.glob("*.json"):
        if f.stem in supported and f.stem!="en_us":
            data=load(f)
            dump(official/f.name,data)
    ref=subprocess.check_output(["git","-C",str(upstream),"rev-parse","HEAD"],text=True).strip()
    manifest={"target":version,"source":"vectorwing/FarmersDelight",
       "branch":subprocess.check_output(["git","-C",str(upstream),"branch","--show-current"],
         text=True).strip(),"commit":ref,
       "english_keys":len(en),"official_minecraft_languages":len(supported),
       "upstream_locale_files":len(list(official.glob("*.json"))),
       "upstream_license":"MIT"}
    dump(source/"source_manifest.json",manifest)
    print("PREPARED",manifest,flush=True)
    from collections import Counter
    gaps={locale:len(set(en)-set(load(official/(locale+".json")) if (official/(locale+".json")).exists() else {}))
          for locale in supported if locale!="en_us"}
    dump(ROOT/"reports"/f"{version}_gaps.json",gaps)
    print("GAPS",{"locales_needing_translation":sum(x>0 for x in gaps.values()),
                  "missing_entries":sum(gaps.values()),"max":max(gaps.values()),
                  "upstream_complete":sum(x==0 for x in gaps.values())},flush=True)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--version",default="1.15.2")
    p.add_argument("--upstream",default=str(PREFIX/"upstream-1152"))
    args=p.parse_args()
    prepare(args.version,Path(args.upstream))
if __name__=="__main__":main()
