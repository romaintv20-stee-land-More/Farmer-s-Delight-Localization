#!/usr/bin/env python3
"""Create a Forge 1.15.2-compatible JAR with actual @Mod metadata and fallback JSON."""
from pathlib import Path
import shutil,subprocess,tempfile,zipfile
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"src/forge_1152"
DIST=ROOT/"dist/farmersdelight-localization-0.1.0+1.15.2.jar"
STUB="""package net.minecraftforge.fml.common;
import java.lang.annotation.*;
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Mod { String value(); }
"""
def main():
    preferred=Path("C:/Program Files/Java/jdk-21/bin/javac.exe")
    compiler=str(preferred) if preferred.exists() else shutil.which("javac")
    if not compiler:raise RuntimeError("javac required (JDK 21 compiler targeting Java 8)")
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        stub=tmp/"net/minecraftforge/fml/common/Mod.java"
        stub.parent.mkdir(parents=True,exist_ok=True)
        stub.write_text(STUB,encoding="utf-8")
        classes=tmp/"classes"
        classes.mkdir()
        source=SRC/"java/fr/rtv20/farmersdelightlocalization/FarmersDelightLocalization.java"
        subprocess.run([compiler,"--release","8","-encoding","UTF-8",
           "-d",str(classes),str(stub),str(source)],check=True)
        manifest=b"Manifest-Version: 1.0\r\nImplementation-Title: Farmer's Delight Localization\r\n\r\n"
        resources=SRC/"resources"
        DIST.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(DIST,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zipout:
            zipout.writestr("META-INF/MANIFEST.MF",manifest)
            for root in (classes,resources):
                for item in sorted(root.rglob("*")):
                    if item.is_file():
                        if item.name=="Mod.class":continue
                        zipout.write(item,item.relative_to(root).as_posix())
            zipout.write(ROOT/"LICENSE","LICENSE")
            zipout.write(ROOT/"licenses/FarmersDelight-LICENSE.txt",
                "META-INF/licenses/FarmersDelight-LICENSE.txt")
            zipout.write(ROOT/"docs/ATTRIBUTIONS.md","META-INF/ATTRIBUTIONS.md")
    print(f"Built {DIST} ({DIST.stat().st_size} bytes)")
if __name__=="__main__":main()
