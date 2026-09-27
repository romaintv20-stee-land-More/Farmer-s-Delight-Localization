from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Ordered by upstream Minecraft release; Forge is required before NeoForge.
TARGETS=[
 {'mc':'1.15.2','branch':'1.15.2','loader':'forge','java':8,'pack':5,'loader_range':'[31,)','platform_range':'[31.2.12,)'},
 {'mc':'1.16.1','branch':'1.16.1','loader':'forge','java':8,'pack':5,'loader_range':'[32,)','platform_range':'[32,)'},
 {'mc':'1.16.3','branch':'1.16.3','loader':'forge','java':8,'pack':6,'loader_range':'[34,)','platform_range':'[34,)'},
 {'mc':'1.16.5','branch':'1.16.5','loader':'forge','java':8,'pack':6,'loader_range':'[36,)','platform_range':'[36,)'},
 {'mc':'1.17.1','branch':'1.17.1','loader':'forge','java':16,'pack':7,'loader_range':'[37,)','platform_range':'[37,)'},
 {'mc':'1.18.1','branch':'1.18.1','loader':'forge','java':17,'pack':8,'loader_range':'[37,)','platform_range':'[39.0.45,)'},
 {'mc':'1.18.2','branch':'1.18.2','loader':'forge','java':17,'pack':8,'loader_range':'[40,)','platform_range':'[40.1.46,)'},
 {'mc':'1.19.2','branch':'1.19','loader':'forge','java':17,'pack':9,'loader_range':'[41,)','platform_range':'[41.1.0,)'},
 {'mc':'1.20.1','branch':'1.20','loader':'forge','java':17,'pack':15,'loader_range':'[46,)','platform_range':'[47.1.0,)'},
 {'mc':'1.20.4','branch':'1.20.4','loader':'neoforge','java':17,'pack':22,'loader_range':'[1,)','platform_range':'[1,)'},
 {'mc':'1.21.1','branch':'1.21','loader':'neoforge','java':21,'pack':34,'loader_range':'[4,)','platform_range':'[21.1.219,)'},
 {'mc':'26.1.2','branch':'26.1','loader':'neoforge','java':25,'pack':84,'loader_range':'[1,)','platform_range':'[26.1.2.30-beta,)'},
]
INDEX={t['mc']:t for t in TARGETS}
def source(t):return ROOT/'sources/farmersdelight'/t['mc']
def native_locales(t):
    import json
    return json.loads((ROOT/'sources/minecraft'/(t['mc']+'_languages.json')).read_text(encoding='utf-8'))['languages']
def fallback_folder(t):
    return ROOT/'src/forge_1152/resources/assets/farmersdelight/lang' if t['mc']=='1.15.2' else ROOT/'src/versions'/t['mc']/'assets/farmersdelight/lang'
