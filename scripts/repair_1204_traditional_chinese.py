#!/usr/bin/env python3
"""Restore original Traditional Chinese strings from a malformed pinned upstream file."""
from pathlib import Path
import json,re,urllib.request
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"sources/farmersdelight/1.20.4"
FALLBACK=ROOT/"src/versions/1.20.4/assets/farmersdelight/lang/zh_tw.json"
URL="https://raw.githubusercontent.com/vectorwing/FarmersDelight/0848f7d3150456dba69a8d6f70606a085b7ad33e/src/main/resources/assets/farmersdelight/lang/zh_tw.json"
def load(p):return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
def put(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def main():
    raw=urllib.request.urlopen(urllib.request.Request(URL,headers={"User-Agent":"FD-Localization-audit"}),timeout=25).read().decode("utf-8")
    try:json.loads(raw)
    except json.JSONDecodeError as ex:
        print("Upstream JSON is malformed as expected:",ex,flush=True)
    else:raise RuntimeError("Upstream zh_tw fixed: review handling before continuing")
    lines=raw.splitlines()
    assert lines[311].lstrip().startswith('"farmersdelight.jei.info.ham"') and not lines[311].rstrip().endswith(",")
    lines[311]=lines[311].rstrip()+","
    recovered=json.loads("\n".join(lines))
    en=load(BASE/"en_us.json")
    existing=load(FALLBACK)
    token=re.compile(r"%(?:\d+\$)?[sdif]|§.|\\n")
    reused={k:v for k,v in recovered.items() if k in en and isinstance(v,str) and
            sorted(token.findall(en[k]))==sorted(token.findall(v))}
    # The upstream resource is entirely malformed; its recovered official values must
    # be present in the low-priority fallback to avoid losing those original translations.
    final=dict(existing)
    final.update(reused)
    put(FALLBACK,final)
    invalid=BASE/"upstream_invalid/zh_tw.json"
    put(invalid,reused)
    manifest=load(BASE/"source_manifest.json")
    manifest["official_translations"]=len(list((BASE/"upstream").glob("*.json")))
    manifest["malformed_upstream_locale"]={"zh_tw":{
        "upstream_url":URL,"error":"missing comma after line 312",
        "recovered_valid_keys":len(reused),
        "reason":"upstream JSON cannot load; mirror recovered originals in fallback"}}
    put(BASE/"source_manifest.json",manifest)
    print("RESTORED",len(reused),"official Traditional Chinese values into the valid fallback;",
          "total fallback entries",len(final),"of English",len(en),flush=True)
if __name__=="__main__":main()
