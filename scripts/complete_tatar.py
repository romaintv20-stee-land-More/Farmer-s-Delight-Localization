#!/usr/bin/env python3
"""Repair three formatting-sensitive Tatar texts that defeated automatic translation."""
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from targets import INDEX,source,fallback_folder
PH=re.compile(r"%(?:\d+\$)?[sdif]|§.|\\n")
CORRECTIONS={
 "block.farmersdelight.cutting_board.remaining_items":"%s калды...",
 "farmersdelight.configuration.debug.tooltip":"§lКисәтү:§r Бу бүлек гадәти уен өчен каралмаган.",
 "farmersdelight.configuration.enableTomatoVineClimbingTaggedRopes.tooltip":
  "Әгәр кушылган булса, помидор үсемлекләре farmersdelight:ropes тамгасы куелган теләсә кайсы бауга үрмәли ала. "
  "Әгәр сүндерелгән булса, бу мөмкинлек әлеге модның үз бауы белән генә чикләнә.\n\n"
  "§lИгътибар: бу блоклар defaultTomatoVineRope параметрында күрсәтелгән блокка әйләнәчәк.§r"
}
def rj(p):return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
def put(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def main():
    for version in ("1.20.1","1.21.1","26.1.2"):
        target=INDEX[version];en=rj(source(target)/"en_us.json")
        upstream=rj(source(target)/"upstream/tt_ru.json")
        path=fallback_folder(target)/"tt_ru.json"
        fb=rj(path)
        added=0
        for key,tr in CORRECTIONS.items():
            if key not in en or key in upstream:continue
            assert sorted(PH.findall(en[key]))==sorted(PH.findall(tr)),(version,key)
            if key not in fb:added+=1
            fb[key]=tr
        put(path,fb)
        print("Tatar",version,"completed",added,"previously missing keys",flush=True)
if __name__=="__main__":main()
