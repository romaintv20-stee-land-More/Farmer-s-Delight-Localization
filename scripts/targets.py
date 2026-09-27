from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Ordered by upstream Minecraft release; Forge is required before NeoForge.
TARGETS=[
 {'mc':'1.15.2','branch':'1.15.2','loader':'forge','java':8,'pack':5,'loader_min':'31'},
 {'mc':'1.16.1','branch':'1.16.1','loader':'forge','java':8,'pack':5,'loader_min':'32'},
 {'mc':'1.16.3','branch':'1.16.3','loader':'forge','java':8,'pack':6,'loader_min':'34'},
 {'mc':'1.16.5','branch':'1.16.5','loader':'forge','java':8,'pack':6,'loader_min':'36'},
 {'mc':'1.17.1','branch':'1.17.1','loader':'forge','java':16,'pack':7,'loader_min':'37'},
 {'mc':'1.18.1','branch':'1.18.1','loader':'forge','java':17,'pack':8,'loader_min':'39'},
 {'mc':'1.18.2','branch':'1.18.2','loader':'forge','java':17,'pack':8,'loader_min':'40'},
 {'mc':'1.19.2','branch':'1.19','loader':'forge','java':17,'pack':9,'loader_min':'43'},
 {'mc':'1.20.1','branch':'1.20','loader':'forge','java':17,'pack':15,'loader_min':'47'},
 {'mc':'1.20.4','branch':'1.20.4','loader':'neoforge','java':17,'pack':22,'loader_min':'1'},
 {'mc':'1.21.1','branch':'1.21','loader':'neoforge','java':21,'pack':34,'loader_min':'4'},
 {'mc':'26.1.2','branch':'26.1','loader':'neoforge','java':25,'pack':84,'loader_min':'1'},
]
INDEX={t['mc']:t for t in TARGETS}
def source(t):return ROOT/'sources/farmersdelight'/t['mc']
def native_locales(t):
    import json
    return json.loads((ROOT/'sources/minecraft'/(t['mc']+'_languages.json')).read_text(encoding='utf-8'))['languages']
def fallback_folder(t):
    return ROOT/'src/forge_1152/resources/assets/farmersdelight/lang' if t['mc']=='1.15.2' else ROOT/'src/versions'/t['mc']/'assets/farmersdelight/lang'
