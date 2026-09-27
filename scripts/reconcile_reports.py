#!/usr/bin/env python3
"""Reconcile reports with committed sources, never trust partial/stale job summaries."""
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from targets import TARGETS,source,fallback_folder,native_locales
ENGLISH={"en_gb","en_au","en_ca","en_nz","enp","enws"}
def read(p):return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
def dump(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def reconcile(target):
    mc=target["mc"];en=read(source(target)/"en_us.json")
    if not en:raise RuntimeError(f"Missing baseline {mc}")
    manifest=read(source(target)/"source_manifest.json")
    assert manifest,"Missing source manifest"
    native=native_locales(target)
    official={p.stem:read(p) for p in (source(target)/"upstream").glob("*.json")}
    fallback={p.stem:read(p) for p in fallback_folder(target).glob("*.json")}
    assert set(official)|set(fallback)<=set(native)
    summary=read(ROOT/"reports"/(mc+"_translation_summary.json"))
    coverage={}
    for lang in native:
        if lang=="en_us":continue
        sourcekeys=set(en)&set(official.get(lang,{}))
        fallbackkeys=set(fallback.get(lang,{}))
        assert not(sourcekeys&fallbackkeys),(mc,lang,"source overlap")
        assert fallbackkeys<=set(en),(mc,lang,"obsolete key")
        needed=set(en)-sourcekeys-fallbackkeys
        if lang in ENGLISH:needed=set()
        coverage[lang]={"upstream":len(sourcekeys),"fallback":len(fallbackkeys),
                        "pending":len(needed),
                        "english_inherited":lang in ENGLISH}
    report={"minecraft_version":mc,"english_keys":len(en),
      "minecraft_native_languages":len(native),
      "upstream_locale_files":len(official),
      "fallback_keys":sum(v["fallback"] for v in coverage.values()),
      "upstream_keys":sum(v["upstream"] for v in coverage.values()),
      "pending":sum(v["pending"] for v in coverage.values()),
      "complete_locale_count":sum(not v["pending"] for v in coverage.values()),
      "incomplete_locales":{k:v["pending"] for k,v in coverage.items() if v["pending"]},
      "native_review":"not completed",
      "automated_job":summary.get("automated_job",[])}
    dump(ROOT/"reports"/(mc+"_coverage.json"),coverage)
    dump(ROOT/"reports"/(mc+"_translation_summary.json"),report)
    print("RECONCILED",mc,"English",len(en),"MC locales",len(native),
         "fallbacks",report["fallback_keys"],"incomplete",report["incomplete_locales"],
         flush=True)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--through",default=None)
    args=p.parse_args()
    for target in TARGETS:
        if args.through and TARGETS.index(target)>[x["mc"] for x in TARGETS].index(args.through):break
        reconcile(target)
if __name__=="__main__":main()
