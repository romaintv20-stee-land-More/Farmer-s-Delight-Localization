from pathlib import Path
import urllib.request,urllib.error,json,time,subprocess,concurrent.futures
ROOT=Path(__file__).resolve().parents[1]
VERSIONS=[('1.16.1','1.16.1'),('1.16.3','1.16.3'),('1.16.5','1.16.5'),('1.17.1','1.17.1'),('1.18.1','1.18.1'),('1.18.2','1.18.2'),('1.19','1.19'),('1.20','1.20'),('1.20.4','1.20.4'),('1.21','1.21.1'),('26.1','26.1.2')]
def download(url):
    for retry in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'FDLocalization/0.1','Accept':'application/vnd.github+json'}),timeout=50) as r:return r.read()
        except Exception as error:
            if retry==4:raise
            time.sleep(retry+1)
def put(path,document):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(document,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def snapshot(branch,version,sha):
    source=ROOT/'sources/farmersdelight'/version
    if (source/'source_manifest.json').is_file():
        saved=json.loads((source/'source_manifest.json').read_text(encoding='utf-8'))
        if saved['commit']==sha:
            print('CACHED',branch,version,flush=True)
            return saved
    languages=set(json.loads((ROOT/'sources/minecraft'/(version+'_languages.json')).read_text(encoding='utf-8'))['languages'])
    path='src/main/resources/assets/farmersdelight/lang'
    url='https://api.github.com/repos/vectorwing/FarmersDelight/contents/'+path+'?ref='+sha
    directory=json.loads(download(url))
    links={Path(item['name']).stem:item['download_url'] for item in directory if item['name'].endswith('.json')}
    english=json.loads(download(links['en_us']))
    if len(english)<100:raise RuntimeError('Unexpectedly few keys '+branch)
    tasks={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for locale in (languages & links.keys())-{'en_us'}:tasks[pool.submit(download,links[locale])]=locale
        for task in concurrent.futures.as_completed(tasks):
            locale=tasks[task]
            try:data=json.loads(task.result())
            except json.JSONDecodeError as exc:
                print('INVALID OFFICIAL JSON',branch,locale,repr(exc),flush=True)
                continue
            put(source/'upstream'/(locale+'.json'),data)
    put(source/'en_us.json',english)
    manifest={'branch':branch,'minecraft':version,'commit':sha,'english_keys':len(english),'minecraft_languages':len(languages),'official_translations':len(tasks),'excluded_non_minecraft':sorted(links.keys()-languages)}
    put(source/'source_manifest.json',manifest)
    print('SNAPSHOT',branch,version,len(english),'keys',len(tasks),'upstream locales',flush=True)
    return manifest
def main():
    remote=subprocess.check_output(['git','-C',str(ROOT.parent/'upstream'),'ls-remote','--heads','origin'],text=True,timeout=90)
    commits={line.split('refs/heads/')[1].strip():line.split()[0] for line in remote.splitlines()}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        tasks=[pool.submit(snapshot,b,v,commits[b]) for b,v in VERSIONS]
        results=[task.result() for task in concurrent.futures.as_completed(tasks)]
    put(ROOT/'sources/upstream_versions.json',sorted(results,key=lambda item:[v[0] for v in VERSIONS].index(item['branch'])))
    print('ALL BRANCHES FETCHED',len(results),flush=True)
if __name__=='__main__':main()
