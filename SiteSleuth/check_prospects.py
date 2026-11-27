import csv, ipaddress, json, socket, urllib.request, urllib.error
from urllib.parse import urlparse, urljoin
CSV='C:/Users/DELL/Hermes-Output/Local-Business-Prospects/prospects.csv'
HEADERS=['strict-transport-security','content-security-policy','x-content-type-options','x-frame-options','referrer-policy','permissions-policy']

def public_url(url):
 p=urlparse(url)
 if p.scheme not in ('http','https') or not p.hostname: raise ValueError('invalid HTTP URL')
 for row in socket.getaddrinfo(p.hostname,p.port or (443 if p.scheme=='https' else 80),type=socket.SOCK_STREAM):
  if not ipaddress.ip_address(row[4][0]).is_global: raise ValueError('redirect/host resolves to non-public IP')

class Redirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  dest=urljoin(req.full_url,newurl); public_url(dest)
  return super().redirect_request(req,fp,code,msg,headers,dest)

rows=list(csv.DictReader(open(CSV,encoding='utf-8')))
seen=set(); out=[]
opener=urllib.request.build_opener(Redirect())
for row in rows:
 url=row['Website / listing'].strip()
 if url in seen: continue
 seen.add(url)
 entry={'business':row['Business'],'area':row['Area'],'url':url,'type': 'business website' if 'website' in row['Website status'].lower() and 'listing' not in row['Website status'].lower() else 'website or third-party listing'}
 try:
  public_url(url)
  req=urllib.request.Request(url,headers={'User-Agent':'SiteSleuth/0.1 passive homepage header review'})
  res=opener.open(req,timeout=15)
  h={k.lower():v for k,v in res.headers.items()}
  entry.update(status=res.status,final_url=res.geturl(),present=[k for k in HEADERS if h.get(k)],missing=[k for k in HEADERS if not h.get(k)],csp_unsafe=('unsafe-inline' in h.get('content-security-policy','') or 'unsafe-eval' in h.get('content-security-policy','')),server=h.get('server'))
  res.close()
 except urllib.error.HTTPError as e:
  entry.update(status=e.code,error='Access returned HTTP '+str(e.code))
 except Exception as e: entry.update(error=str(e))
 out.append(entry)
print(json.dumps({'unique_urls':len(out),'results':out},ensure_ascii=False,indent=2))
