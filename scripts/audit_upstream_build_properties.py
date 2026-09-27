from pathlib import Path
import urllib.request,re,json
branches=["1.15.2","1.16.1","1.16.3","1.16.5","1.17.1","1.18.1","1.18.2","1.19","1.20","1.20.4","1.21","26.1"]
out=[]
for b in branches:
    u=f"https://raw.githubusercontent.com/vectorwing/FarmersDelight/{b}/gradle.properties"
    try:s=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"FDLocalization-audit"}),timeout=30).read().decode()
    except Exception as e:s=""
    props={}
    for line in s.splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k,v=line.split("=",1);props[k.strip()]=v.strip()
    out.append({"branch":b,"minecraft":props.get("minecraft_version") or props.get("mc_version"),
                "neo":props.get("neo_version"),"forge":props.get("forge_version"),
                "loader_range":props.get("loader_version_range")})
print(json.dumps(out,indent=2))
Path(r"D:\ssd\Autres\farmers-delight-localization\project\reports\upstream_build_properties.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
