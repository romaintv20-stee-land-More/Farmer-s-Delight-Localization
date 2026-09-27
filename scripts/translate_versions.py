#!/usr/bin/env python3
"""Oldest-first, resumable translation of all supported Farmer's Delight versions."""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,concurrent.futures,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from targets import TARGETS,source,native_locales,fallback_folder
import generate_fallbacks as g
import complete_special_locales as novelty
# Prefer the established batched Google Translate UI transport when available.
sys.path.insert(0,str(ROOT.parent.parent/'neoorigins-localization-228-work'/'scripts'))
try:
    from sync_neoorigins_228 import google as ui_google
    g.google=ui_google
except ImportError:
    pass
g.LANG['swg']='de'  # Swabian: provisional German fallback, review needed.
g.UNSUPPORTED.add('tok')  # Toki Pona needs real language review, never a fake proxy.
# Unsupported by the configured machine translator; never silently substitute another language.
g.UNSUPPORTED.update({'got_de','hal_ua','nah','pls','qcb_es','qid','tzo_mx','vro','zlm_arab'})
ORIGINAL_MEMORY=g.build_memory
SPECIAL={"jbo_en","qya_aa","tlh_aa"}
def read(path):return g.read(path)
def all_memory(locale):
    votes=defaultdict(Counter)
    for target in TARGETS:
        base=source(target)
        english=read(base/"en_us.json")
        if not english:continue
        for folder,weight in ((base/"upstream",10),(fallback_folder(target),4)):
            translated=read(folder/(locale+".json"))
            for key,value in translated.items():
                original=english.get(key)
                if original is not None and g.valid(original,value):
                    votes[original][value]+=weight
    return {word:count.most_common(1)[0][0] for word,count in votes.items()}
MEMORY={}
def memory_for(locale,english):
    if locale not in MEMORY:MEMORY[locale]=all_memory(locale)
    known=ORIGINAL_MEMORY(locale,english)
    known.update(MEMORY[locale])
    return known
def novel(locale,english):
    cached=g.load_cached(locale,english,read(g.BASE/"upstream"/(locale+".json")))
    latest_en=read(g.FD_NEW/"en_us.json")
    latest=read(g.FD_NEW/(locale+".json"))
    created=0
    for key,word in english.items():
        if key in cached or key in read(g.BASE/"upstream"/(locale+".json")):continue
        if latest_en.get(key)==word and g.valid(word,latest.get(key)):
            cached[key]=latest[key]
            continue
        if locale=="en_pt":translated=novelty.stylize(word,novelty.PIRATE,"Arrr! ")
        elif locale=="lol_us":translated=novelty.stylize(word,novelty.LOLCAT,"Lol, ")
        else:translated=novelty.upside_down(word)
        if not g.valid(word,translated):raise ValueError(f"{locale}: {key}: {translated}")
        cached[key]=translated
        created+=1
    g.save(g.CACHE/(locale+".json"),cached)
    return created
def one(target,workers):
    MEMORY.clear()  # include all newly completed earlier-version fallback files
    mc=target["mc"]
    base=source(target)
    if not (base/"source_manifest.json").exists():
        raise RuntimeError(f"No pinned upstream snapshot for {mc}")
    g.BASE=base
    g.ASSETS=fallback_folder(target)
    g.CACHE=ROOT/"work/translations"/mc
    g.MC=ROOT/"sources/minecraft"/(mc+"_languages.json")
    g.CACHE.mkdir(parents=True,exist_ok=True)
    english=read(base/"en_us.json")
    locals=native_locales(target)
    if not english or len(locals)<100:raise RuntimeError(f"Invalid source {mc}")
    for locale in locals:
        if locale=="en_us":continue
        g.seed_locale(locale,english)
    for locale in sorted({"en_pt","lol_us","en_ud"}&set(locals)):
        print("SYNTHETIC",mc,locale,novel(locale,english),flush=True)
    g.generate(english,locals)
    pending=sum(x["pending"] for x in read(ROOT/"reports"/(mc+"_coverage.json")).values())
    print("SEEDED",mc,"keys",len(english),"locales",len(locals),"pending",pending,flush=True)
    scope=[l for l in locals if l!="en_us" and l not in g.ENGLISH
           and l not in g.UNSUPPORTED]
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        result=list(pool.map(lambda loc:g.translate(loc,english),scope))
    g.generate(english,locals)
    coverage=read(ROOT/"reports"/(mc+"_coverage.json"))
    remaining={key:value["pending"] for key,value in coverage.items() if value["pending"]}
    report={"minecraft_version":mc,"english_keys":len(english),
      "minecraft_native_languages":len(locals),"upstream_locale_files":
      read(base/"source_manifest.json").get("official_translations",8),
      "fallback_keys":sum(x["fallback"] for x in coverage.values()),
      "pending":sum(remaining.values()),"remaining":remaining,
      "native_review":"not completed",
      "automated_job":result}
    g.save(ROOT/"reports"/(mc+"_translation_summary.json"),report)
    print("VERSION COMPLETE",mc,"fallback",report["fallback_keys"],
       "pending",report["pending"],remaining,flush=True)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--start",default="1.16.1")
    p.add_argument("--workers",type=int,default=6)
    p.add_argument("--seed-only",action="store_true")
    args=p.parse_args()
    g.build_memory=memory_for
    active=False
    for target in TARGETS:
        if target["mc"]==args.start:active=True
        if not active:continue
        if args.seed_only:
            g.BASE=source(target);g.ASSETS=fallback_folder(target)
            g.CACHE=ROOT/"work/translations"/target["mc"]
            g.MC=ROOT/"sources/minecraft"/(target["mc"]+"_languages.json")
            english=read(g.BASE/"en_us.json")
            for locale in native_locales(target):
                if locale!="en_us":g.seed_locale(locale,english)
            g.generate(english,native_locales(target))
            print("SEED-ONLY",target["mc"],flush=True)
        else:one(target,args.workers)
if __name__=="__main__":main()
