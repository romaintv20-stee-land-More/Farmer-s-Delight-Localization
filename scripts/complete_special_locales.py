#!/usr/bin/env python3
"""Complete old-version novelty variants while marking synthetic text for review."""
from pathlib import Path
import json,re
import generate_fallbacks as core
EN=core.read(core.BASE/"en_us.json")
NEW_EN=core.read(core.FD_NEW/"en_us.json")
REPORT={}
FLIP=dict(zip("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
              "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz∀ᗺƆᗡƎℲ⅁HIſꓘ⅂WNOԀΌᴚS⊥∩ΛMX⅄Z"))
FLIP.update({"?":"¿","!":"¡",".":"˙",",":"‘","'":",","(" : ")",")":"(","[":"]","]":"["})
PIRATE={"your":"yer","you":"ye","the":"th'","with":"wi'","cooking":"cookin'",
  "cooked":"cook'd","baked":"bak'd","fried":"fry'd","basket":"cargo basket",
  "chicken":"chick'n","food":"grub","delicious":"tasty","holding":"holdin'",
  "slices":"pieces","crafted":"made","prepared":"made","roasted":"roast'd"}
LOLCAT={"your":"ur","you":"u","the":"teh","with":"wif","cooking":"cookin",
  "cooked":"cookd","baked":"bakd","fried":"fryd","basket":"bas-kit",
  "chicken":"chikkin","food":"nomz","fish":"fesh","tasty":"nommy",
  "holds":"haz","servings":"servinz","bread":"bred","egg":"eggo",
  "sandwich":"sammich","delicious":"nommy"}
def stylize(source,lexicon,prefix=""):
    mask,tokens=core.protect(source)
    result=re.sub(r"\b[a-zA-Z]+\b",lambda match:
      (lexicon.get(match.group(0).lower(),match.group(0)).capitalize()
        if match.group(0)[0].isupper() else
        lexicon.get(match.group(0).lower(),match.group(0))),mask)
    result=core.restore(result,tokens)
    if result==source and prefix:result=prefix+source
    return result
def upside_down(source):
    units=re.findall(core.PH.pattern+r"|.",source,re.DOTALL)
    return "".join(unit if core.PH.fullmatch(unit) else FLIP.get(unit,unit)
                   for unit in reversed(units))
def fix_placeholders():
    for locale in ("la_la","tt_ru"):
        cache=core.read(core.CACHE/f"{locale}.json")
        for key,value in list(cache.items()):
            if key in EN and "%" in EN[key] and not core.valid(EN[key],value):
                fixed=re.sub(r"%\s*[Ss]",lambda m:"%s",value)
                if core.valid(EN[key],fixed):cache[key]=fixed
        core.save(core.CACHE/f"{locale}.json",cache)
def synth(locale,lexicon,prefix=""):
    cache=core.read(core.CACHE/f"{locale}.json")
    latest=core.read(core.FD_NEW/f"{locale}.json")
    reuse=generated=0
    for key,english in EN.items():
        if core.valid(english,cache.get(key)):continue
        if key in latest and key in NEW_EN and core.sig(english)==core.sig(latest[key]):
            cache[key]=latest[key];reuse+=1
        else:
            cache[key]=stylize(english,lexicon,prefix);generated+=1
        if not core.valid(english,cache[key]):
            raise RuntimeError(f"{locale} invalid placeholder: {key}")
    core.save(core.CACHE/f"{locale}.json",cache)
    REPORT[locale]={"reused_same_key_different_english":reuse,
        "synthetic_unreviewed":generated}
def main():
    fix_placeholders()
    synth("en_pt",PIRATE,prefix="Arrr! ")
    synth("lol_us",LOLCAT,prefix="Lol, ")
    cache=core.read(core.CACHE/"en_ud.json")
    for key,text in EN.items():
        if key not in cache:cache[key]=upside_down(text)
    core.save(core.CACHE/"en_ud.json",cache)
    REPORT["en_ud"]={"synthetic_upside_down":len(cache)}
    core.save(core.ROOT/"reports/1.15.2_special_qa.json",REPORT)
    core.generate(EN,core.read(core.MC)["languages"])
    print("NOVELTY COMPLETED",REPORT,flush=True)
if __name__=="__main__":main()
