#!/usr/bin/env python3
"""First-generation translation pipeline: reuse upstream, B&M and translate missing strings."""
from __future__ import annotations
from pathlib import Path
from collections import Counter,defaultdict
import argparse,concurrent.futures,json,re,threading,time,urllib.parse,urllib.request,urllib.error
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"sources/farmersdelight/1.15.2"
ASSETS=ROOT/"src/forge_1152/resources/assets/farmersdelight/lang"
CACHE=ROOT/"work/translated"
MC=ROOT/"sources/minecraft/1.15.2_languages.json"
FD_NEW=ROOT.parent/"upstream-261/src/main/resources/assets/farmersdelight/lang"
BNM=Path(r"D:\ssd\Autres\Mcreator\Mods\Steel_and_More\src\main\resources\assets")
OTHER=Path(r"D:\ssd\Autres\neoorigins-localization-228-work\build\marathi-sources\minecraft_26.1.2_en_us.json")
PH=re.compile(r"%(?:\d+\$)?[sdif]|§.|\\n")
LANG={"fil_ph":"tl","tl_ph":"tl","he_il":"iw","yi_de":"yi","zh_cn":"zh-CN",
  "zh_tw":"zh-TW","zh_hk":"zh-TW","no_no":"no","nn_no":"no","sr_sp":"sr",
  "se_no":"se","bar":"de","brb":"nl","esan":"es","fra_de":"de",
  "ksh":"de","nds_de":"de","go_fr":"fr","io_en":"eo","isv":"ru",
  "li_li":"nl","gv_im":"ga","ast_es":"es","cv_cu":"ru","ba_ru":"ru",
  "fo_fo":"da","haw_us":"haw","lzh":"zh-CN","qya_aa":"en","tlh_aa":"en",
  "jbo_en":"eo","val_es":"ca","kw_gb":"cy","ovd":"sv","rpr":"ru",
  "sxu":"de","lmo":"it","vec_it":"it","mi_nz":"mi","szl":"pl"}
ENGLISH={"en_us","en_gb","en_au","en_ca","en_nz","enp","enws"}
UNSUPPORTED={"qya_aa","tlh_aa","en_ud","en_pt","lol_us","jbo_en"}
THREAD=threading.Lock()
def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8")) if Path(p).is_file() else {}
def save(p,data):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+".tmp")
    tmp.write_text(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    tmp.replace(p)
def sig(s):return sorted(PH.findall(s))
def valid(src,tr):return isinstance(tr,str) and bool(tr.strip()) and sig(src)==sig(tr) and not re.search(r"ZXQPH\d|ZZQSEP\d",tr)
def build_memory(locale,english):
    votes=defaultdict(Counter)
    new_en=read(FD_NEW/"en_us.json")
    new=read(FD_NEW/f"{locale}.json")
    for key,word in english.items():
        if new_en.get(key)==word and valid(word,new.get(key)):votes[key][new[key]]+=10
    pairs=[
      (BNM/"minecraft/lang/en_us.json",BNM/f"minecraft/lang/{locale}.json"),
      (BNM/"steel_and_more/lang/en_us.json",BNM/f"steel_and_more/lang/{locale}.json"),
    ]
    if OTHER.is_file():
        pairs[0]=(OTHER,BNM/f"minecraft/lang/{locale}.json")
    for en_path,target_path in pairs:
        en=read(en_path);translated=read(target_path)
        for key,word in en.items():
            tr=translated.get(key)
            if isinstance(word,str) and valid(word,tr):votes[word][tr]+=1
    return {k:v.most_common(1)[0][0] for k,v in votes.items()}
def load_cached(locale,english,official):
    cached=read(CACHE/f"{locale}.json")
    existing=read(ASSETS/f"{locale}.json")
    for key,value in existing.items():
        if key in english and key not in official and valid(english[key],value):
            cached.setdefault(key,value)
    return cached

def seed_locale(locale,english):
    official=read(BASE/"upstream"/f"{locale}.json")
    cached=load_cached(locale,english,official)
    mem=build_memory(locale,english)
    new_en=read(FD_NEW/"en_us.json")
    new=read(FD_NEW/f"{locale}.json")
    for key,word in english.items():
        if key in official or (key in cached and valid(word,cached[key])):continue
        tr=new.get(key)
        if new_en.get(key)==word and valid(word,tr):cached[key]=tr
        elif word in mem and valid(word,mem[word]):cached[key]=mem[word]
    save(CACHE/f"{locale}.json",cached)
    return len(english)-len(set(english)&(set(official)|set(cached)))
def google(text,target):
    data=urllib.parse.urlencode({"client":"gtx","sl":"en","tl":target,"dt":"t","q":text})
    req=urllib.request.Request("https://translate.googleapis.com/translate_a/single?"+data,
        headers={"User-Agent":"Mozilla/5.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=35) as res:r=json.load(res)
            result="".join(part[0] for part in r[0] if part and isinstance(part[0],str))
            if result.strip():return result
        except Exception:
            if attempt==2:raise
            time.sleep(0.8*(attempt+1))
    raise RuntimeError(f"No translation for {target}")
def protect(src):
    tokens=[]
    def sub(match):
        tokens.append(match.group(0))
        return f"⟦{len(tokens)-1:04d}⟧"
    return PH.sub(sub,src),tokens
def restore(output,tokens):
    for i,value in enumerate(tokens):
        token=f"⟦{i:04d}⟧"
        output=output.replace(token,value)
    return output
def batch_translate(words,target):
    masks=[protect(x) for x in words]
    parts=[]
    for i,(word,_tokens) in enumerate(masks):
        parts.append(f"ZZQSEP{i:04d}ZZQ\n{word}")
    joined="\n".join(parts)
    response=google(joined,target)
    spl=re.split(r"\s*ZZQSEP\d{4}ZZQ\s*",response)
    if spl and not spl[0].strip():spl=spl[1:]
    if len(spl)!=len(words):
        spl=[google(word,target) for word,_ in masks]
    result=[]
    for src,translated,(_word,tokens) in zip(words,spl,masks):
        tr=restore(translated.strip(),tokens)
        if not valid(src,tr):
            tr=google(src,target)
        if not valid(src,tr):
            raise ValueError(f"Invalid placeholders for {src!r}: {tr!r}")
        result.append(tr)
    return result
def translate(locale,english):
    if locale in ENGLISH:return locale,0,"english_default"
    official=read(BASE/"upstream"/f"{locale}.json")
    cached=load_cached(locale,english,official)
    missing=[(k,v) for k,v in english.items() if k not in official and
             not valid(v,cached.get(k))]
    if not missing:return locale,0,"complete"
    if locale in UNSUPPORTED:return locale,len(missing),"requires_special_locale"
    target=LANG.get(locale,locale.split("_")[0])
    unique=list(dict.fromkeys(v for _,v in missing))
    batches=[];batch=[];size=0
    for word in unique:
        if batch and (len(batch)>=14 or size+len(word)>1150):
            batches.append(batch);batch=[];size=0
        batch.append(word);size+=len(word)
    if batch:batches.append(batch)
    completed={english[k]:v for k,v in cached.items() if k in english and valid(english[k],v)}
    for i,words in enumerate(batches,1):
        needed=[x for x in words if x not in completed]
        if not needed:continue
        try:translated=batch_translate(needed,target)
        except Exception as error:
            with THREAD:print("RETRY",locale,i,str(error)[:110],flush=True)
            try:translated=[google(x,target) for x in needed]
            except Exception as exc:
                with THREAD:print("FAILED",locale,i,repr(exc)[:100],flush=True)
                return locale,len(missing),"translator_error"
        for word,tr in zip(needed,translated):
            if valid(word,tr):completed[word]=tr
        for k,word in english.items():
            if k not in official and word in completed and valid(word,completed[word]):
                cached[k]=completed[word]
        save(CACHE/f"{locale}.json",cached)
        time.sleep(0.15)
    pending=sum(k not in official and not valid(v,cached.get(k)) for k,v in english.items())
    with THREAD:print("TRANSLATED",locale,"pending",pending,"/ total",len(english),flush=True)
    return locale,pending,"auto_translated" if not pending else "partial"
def generate(english,locales):
    stats={};ASSETS.mkdir(parents=True,exist_ok=True)
    for locale in locales:
        if locale=="en_us":continue
        official=read(BASE/"upstream"/f"{locale}.json")
        cache=load_cached(locale,english,official)
        data={k:cache[k] for k,v in english.items()
              if k not in official and valid(v,cache.get(k))}
        pending=len(english)-len(set(english)&set(official))-len(data)
        if locale in ENGLISH:pending=0
        if data:save(ASSETS/f"{locale}.json",data)
        elif (ASSETS/f"{locale}.json").exists(): (ASSETS/f"{locale}.json").unlink()
        stats[locale]={"upstream":len(set(english)&set(official)),
            "fallback":len(data),"pending":pending,
            "special":locale in UNSUPPORTED,"english_inherited":locale in ENGLISH}
    save(ROOT/"reports/1.15.2_coverage.json",stats)
    print("COVERAGE",{k:sum(v[k] for v in stats.values())
        for k in ("upstream","fallback","pending")},
        "COMPLETE_LOCALES",sum(v["pending"]==0 for v in stats.values()),"/",len(stats),flush=True)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seed",action="store_true")
    p.add_argument("--translate",action="store_true")
    p.add_argument("--generate",action="store_true")
    p.add_argument("--workers",type=int,default=3)
    p.add_argument("--limit",type=int,default=0)
    args=p.parse_args()
    english=read(BASE/"en_us.json")
    locales=read(MC)["languages"]
    if args.seed:
        gaps={l:seed_locale(l,english) for l in locales if l!="en_us"}
        print("SEEDED","pending",sum(gaps.values()),"locales",sum(bool(x) for x in gaps.values()),flush=True)
    if args.translate:
        scope=[l for l in locales if l!="en_us" and l not in ENGLISH]
        if args.limit:scope=scope[:args.limit]
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            result=list(pool.map(lambda l:translate(l,english),scope))
        save(ROOT/"reports/1.15.2_translation_job.json",result)
    if args.generate:generate(english,locales)
if __name__=="__main__":main()
