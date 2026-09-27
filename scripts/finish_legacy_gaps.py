#!/usr/bin/env python3
"""Finish isolated, low-risk gaps in early official Minecraft languages."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from targets import TARGETS,source,fallback_folder,native_locales
import generate_fallbacks as trans
def read(p):return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
LATIN={
 "You need a %s to eat this.":"Tibi opus est %s ut hoc edas.",
 "%1$s was grilled to perfection":"%1$s ad perfectionem assatus est."
}
def tok_memory():
    votes={}
    for target in TARGETS:
        if target["mc"] in ("1.20.1","1.20.4","1.21.1","26.1.2"):continue
        base=source(target);en=read(base/"en_us.json")
        for folder in (base/"upstream",fallback_folder(target)):
            localized=read(folder/"tok.json")
            for key,target_text in localized.items():
                source_text=en.get(key)
                if source_text is not None and trans.valid(source_text,target_text):
                    votes.setdefault(source_text,target_text)
    return votes
def main():
    tok=tok_memory()
    report={}
    for target in TARGETS:
        mc=target["mc"]
        if mc not in ("1.16.1","1.16.3","1.16.5","1.17.1",
                      "1.18.1","1.18.2","1.19.2"):continue
        en=read(source(target)/"en_us.json")
        folder=fallback_folder(target)
        if not en:continue
        updated={}
        for lang in ("swg","la_la","tok"):
            if lang not in native_locales(target):continue
            official=read(source(target)/"upstream"/(lang+".json"))
            localized=read(folder/(lang+".json"))
            german={}
            if lang=="swg":
                german.update(read(source(target)/"upstream/de_de.json"))
                german.update(read(folder/"de_de.json"))
            added=0
            for key,src in en.items():
                if key in official or key in localized:continue
                candidate=(german.get(key) if lang=="swg" else
                    LATIN.get(src) if lang=="la_la" else tok.get(src))
                if trans.valid(src,candidate):
                    localized[key]=candidate
                    added+=1
            if added:
                trans.save(folder/(lang+".json"),localized)
            updated[lang]={"filled":added,"pending":len(set(en)-set(official)-set(localized))}
        report[mc]=updated
        print("REPAIRED",mc,updated,flush=True)
    trans.save(ROOT/"reports/legacy_gap_repairs.json",report)
if __name__=="__main__":main()
