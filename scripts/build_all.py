#!/usr/bin/env python3
"""Build independent, one-JAR-per-version Forge/NeoForge localization companions."""
from __future__ import annotations
from pathlib import Path
from tempfile import TemporaryDirectory
import argparse,json,os,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from targets import TARGETS,INDEX,source,fallback_folder
MOD="farmersdelight_localization"
PREFIX="fr/rtv20/farmersdelightlocalization/FarmersDelightLocalization"
STUB="""package {package};
import java.lang.annotation.*;
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Mod {{ String value(); }}
"""
def find_javac():
    explicit=os.environ.get("JAVA_HOME")
    if explicit:
        name="javac.exe" if os.name=="nt" else "javac"
        candidate=Path(explicit)/"bin"/name
        if candidate.is_file():return str(candidate)
    preferred=Path("C:/Program Files/Java/jdk-21/bin/javac.exe")
    return str(preferred) if preferred.is_file() else shutil.which("javac")
def metadata(target):
    minecraft=target["mc"]
    loader=target["loader"]
    old=loader=="forge"
    header='modLoader="javafml"\nloaderVersion="['+target["loader_min"]+',)"\nlicense="MIT"\n\n'
    body='[[mods]]\nmodId="'+MOD+'"\nversion="0.1.0"\ndisplayName="Farmer\'s Delight Localization"\n'
    body+='authors="Romain and contributors"\n'
    body+='description="Client-side missing-key translations for Farmer\'s Delight."\n'
    if old:
        body+='displayTest="IGNORE_ALL_VERSION"\n'
    deps=[]
    for name,range_value in ((loader,"["+target["loader_min"]+",)"),
                             ("minecraft","["+minecraft+"]"),
                             ("farmersdelight","[0,)")):
        if old:
            deps.extend(["[[dependencies."+MOD+"]]","modId="+json.dumps(name),
                "mandatory=true","versionRange="+json.dumps(range_value),
                "ordering="+json.dumps("AFTER" if name=="farmersdelight" else "NONE"),
                "side="+json.dumps("CLIENT"),""])
        else:
            deps.extend(["[[dependencies."+MOD+"]]","modId="+json.dumps(name),
                'type="required"',"versionRange="+json.dumps(range_value),
                "ordering="+json.dumps("AFTER" if name=="farmersdelight" else "NONE"),
                'side="CLIENT"',""])
    path="META-INF/mods.toml" if old or minecraft=="1.20.4" else "META-INF/neoforge.mods.toml"
    return path,(header+body+"\n"+"\n".join(deps)).encode("utf-8")
def build(target):
    mc=target["mc"]
    javac=find_javac()
    if not javac:raise RuntimeError("A compatible Java development kit is required")
    package="net.minecraftforge.fml.common" if target["loader"]=="forge" else "net.neoforged.fml.common"
    entry=(ROOT/"src/forge_1152/java" if target["loader"]=="forge" else ROOT/"src/neoforge/java")/(PREFIX+".java")
    local=fallback_folder(target)
    if not local.is_dir():raise RuntimeError("Missing locale resources for "+mc)
    langfiles=sorted(local.glob("*.json"))
    if not langfiles:raise RuntimeError(f"{mc}: missing translation resources")
    dest=ROOT/"dist"/("farmersdelight-localization-0.1.0+"+mc+"-"+target["loader"]+".jar")
    dest.parent.mkdir(parents=True,exist_ok=True)
    with TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        stub=tmp/Path(package.replace(".","/"))/"Mod.java"
        stub.parent.mkdir(parents=True,exist_ok=True)
        stub.write_text(STUB.format(package=package),encoding="utf-8")
        classes=tmp/"classes"
        classes.mkdir()
        args=[javac,"--release",str(target["java"]),"-encoding","UTF-8","-d",
              str(classes),str(stub),str(entry)]
        subprocess.run(args,check=True)
        with zipfile.ZipFile(dest,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as out:
            out.writestr("META-INF/MANIFEST.MF",
                b"Manifest-Version: 1.0\r\nImplementation-Title: Farmer's Delight Localization\r\n\r\n")
            for file in classes.rglob("*.class"):
                if file.name=="Mod.class":continue
                out.write(file,file.relative_to(classes).as_posix())
            path,payload=metadata(target)
            out.writestr(path,payload)
            out.writestr("pack.mcmeta",json.dumps({"pack":{"pack_format":target["pack"],
                "description":"Farmer's Delight Localization: only missing translation keys"}},
                ensure_ascii=False,indent=2)+"\n")
            for file in langfiles:
                out.write(file,"assets/farmersdelight/lang/"+file.name)
            out.write(ROOT/"LICENSE","LICENSE")
            out.write(ROOT/"licenses/FarmersDelight-LICENSE.txt",
                "META-INF/licenses/FarmersDelight-LICENSE.txt")
            out.write(ROOT/"docs/ATTRIBUTIONS.md","META-INF/ATTRIBUTIONS.md")
    print("JAR",mc,target["loader"],len(langfiles),"locales",dest.stat().st_size,"bytes",flush=True)
    return dest
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--target",default=None,choices=list(INDEX))
    p.add_argument("--all",action="store_true")
    p.add_argument("--skip-java25",action="store_true")
    args=p.parse_args()
    jobs=[INDEX[args.target]] if args.target else TARGETS if args.all else [INDEX["1.16.1"]]
    for target in jobs:
        if args.skip_java25 and target["java"]==25:continue
        build(target)
if __name__=="__main__":main()
