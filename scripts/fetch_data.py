import json, subprocess, concurrent.futures, pathlib, datetime
ROOT=pathlib.Path(__file__).resolve().parents[1]
CODES={'population':'SP.POP.TOTL','birthRate':'SP.DYN.CBRT.IN','sexRatio':'SP.POP.BRTH.MF','urban':'SP.URB.TOTL.IN.ZS','infant':'SP.DYN.IMRT.IN','under5':'SH.DYN.MORT','water':'SH.H2O.BASW.ZS','electricity':'EG.ELC.ACCS.ZS','school':'SE.PRM.NENR','gdp':'NY.GDP.PCAP.CD','life':'SP.DYN.LE00.IN','q1':'SI.DST.FRST.20','q2':'SI.DST.02ND.20','q3':'SI.DST.03RD.20','q4':'SI.DST.04TH.20','q5':'SI.DST.05TH.20'}
def fetch(url):
    raw=subprocess.check_output(['curl','-fLsS','--retry','2','--max-time','90',url]); return json.loads(raw)
def indicator(item):
    key,code=item
    url=f'https://api.worldbank.org/v2/country/all/indicator/{code}?date=2000:2010&format=json&per_page=20000'
    result=fetch(url)
    if not isinstance(result,list) or len(result)<2: raise ValueError((code,result))
    (ROOT/'data'/f'{key}.json').write_text(json.dumps(result,ensure_ascii=False))
    print(key, len(result[1]),flush=True)
    return key,result[1]
countries=fetch('https://api.worldbank.org/v2/country?format=json&per_page=400')[1]
metrics=dict(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(indicator,CODES.items()))
output=[]
for c in countries:
    if c['region']['id']=='NA':continue
    row={'id':c['id'],'iso2':c['iso2Code'],'name':c['name'],'region':c['region']['value'],'lat':c['latitude'],'lon':c['longitude']}
    for key, values in metrics.items():
        matches=[v for v in values if v['countryiso3code']==c['id'] and v['value'] is not None and (int(v['date'])==2005 if key in ['population','birthRate'] else True)]
        if matches:
            v=min(matches,key=lambda x:(abs(int(x['date'])-2005),int(x['date'])))
            row[key]={'value':v['value'],'year':int(v['date'])}
        else:row[key]=None
    if row['population'] and row['birthRate']:
        row['births']=row['population']['value']*row['birthRate']['value']/1000
        output.append(row)
world={key:next((v['value'] for v in vals if v['countryiso3code']=='WLD' and v['date']=='2005'),None) for key,vals in metrics.items()}
bundle={'year':2005,'retrieved':datetime.date.today().isoformat(),'indicators':CODES,'countries':output,'world':world,'totalBirths':sum(c['births'] for c in output)}
(ROOT/'data.json').write_text(json.dumps(bundle,ensure_ascii=False,separators=(',',':')))
print('Countries',len(output),'births',bundle['totalBirths'],'world',world['population']*world['birthRate']/1000)
