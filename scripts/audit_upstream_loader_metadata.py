from pathlib import Path
import urllib.request,re,json
branches=["1.15.2","1.16.1","1.16.3","1.16.5","1.17.1","1.18.1","1.18.2","1.19","1.20","1.20.4","1.21","26.1"]
out=[]
for b in branches:
    choices=["src/main/resources/META-INF/mods.toml","src/main/templates/META-INF/neoforge.mods.toml","src/main/resources/META-INF/neoforge.mods.toml"]
    text=None;path=None
    for rel in choices:
        u=f"https://raw.githubusercontent.com/vectorwing/FarmersDelight/{b}/{rel}"
        try:
            text=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"FDLocalization-audit"}),timeout=25).read().decode();path=rel;break
        except Exception:pass
    if text is None:
        out.append({"branch":b,"metadata":None});continue
    loader=re.search(r'loaderVersion\s*=\s*"([^"]+)"',text)
    mc=re.search(r'modId\s*=\s*"minecraft"[\s\S]{0,350}?versionRange\s*=\s*"([^"]+)"',text)
    neof=re.search(r'modId\s*=\s*"neoforge"[\s\S]{0,350}?versionRange\s*=\s*"([^"]+)"',text)
    forge=re.search(r'modId\s*=\s*"forge"[\s\S]{0,350}?versionRange\s*=\s*"([^"]+)"',text)
    out.append({"branch":b,"metadata":path,"loaderVersion":loader.group(1) if loader else None,
                "minecraftRange":mc.group(1) if mc else None,
                "neoRange":neof.group(1) if neof else None,
                "forgeRange":forge.group(1) if forge else None})
print(json.dumps(out,indent=2))
Path(r"D:\ssd\Autres\farmers-delight-localization\project\reports\upstream_loader_metadata.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
