#!/usr/bin/env python3
"""Pin the official selectable Minecraft locales from Mojang's versioned asset index."""
from pathlib import Path
import hashlib,json,re,urllib.request
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"sources/minecraft"
OUT.mkdir(parents=True,exist_ok=True)
VERSIONS=("1.15.2","1.16.1","1.16.3","1.16.5","1.17.1","1.18.1",
          "1.18.2","1.19","1.19.2","1.20","1.20.1","1.20.4","1.21.1","26.1.2")
def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"FarmersDelightLocalization/0.1"})
    with urllib.request.urlopen(req,timeout=45) as response:return response.read()
def load(version,manifest):
    meta=next((x for x in manifest["versions"] if x["id"]==version),None)
    if not meta:raise ValueError(f"Official version not found: {version}")
    vm=json.loads(fetch(meta["url"]))
    idx=vm["assetIndex"]
    raw=fetch(idx["url"])
    got=hashlib.sha1(raw).hexdigest()
    if got!=idx["sha1"]:raise ValueError(f"{version}: asset index SHA-1 mismatch")
    data=json.loads(raw)
    locales=sorted({m.group(1) for name in data["objects"]
        if (m:=re.fullmatch(r"minecraft/lang/([a-z0-9_]+)\.(?:json|lang)",name))})
    if "en_us" not in locales:locales.insert(0,"en_us")
    if len(locales)<20:raise RuntimeError(f"Unexpectedly few Minecraft languages: {locales}")
    payload={"minecraft_version":version,"asset_index_sha1":got,
             "asset_index_id":idx["id"],"source":idx["url"],
             "languages":locales}
    target=OUT/f"{version}_languages.json"
    target.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"Minecraft {version}: {len(locales)} official selectable languages, index {idx['id']}",flush=True)
def main():
    manifest=json.loads(fetch("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"))
    for version in VERSIONS:
        try:load(version,manifest)
        except Exception as e:print(f"FAILED {version}: {e}",flush=True)
if __name__=="__main__":main()
