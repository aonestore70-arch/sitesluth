from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path
OUT=Path(r'C:\Users\DELL\Hermes-Output\SiteSleuth\SiteSleuth-Prototype-Overview.pptx')
prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
BG=RGBColor(11,17,32); PANEL=RGBColor(18,28,45); LINE=RGBColor(35,51,74); WHITE=RGBColor(232,239,248); MUTED=RGBColor(154,171,192); MINT=RGBColor(105,224,177); AMBER=RGBColor(255,202,106); BLUE=RGBColor(125,185,255); RED=RGBColor(255,122,134)
def box(s,x,y,w,h,fill=PANEL,line=LINE,radius=True):
 q=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)); q.fill.solid(); q.fill.fore_color.rgb=fill; q.line.color.rgb=line; q.line.width=Pt(1); return q
def txt(s,x,y,w,h,t,size=18,color=WHITE,bold=False,font='Aptos',align=None,margin=.04):
 q=s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); f=q.text_frame; f.clear(); f.word_wrap=True; f.margin_left=Inches(margin); f.margin_right=Inches(margin); f.margin_top=Inches(margin); f.margin_bottom=Inches(margin); p=f.paragraphs[0]; p.text=t; p.font.name=font; p.font.size=Pt(size); p.font.bold=bold; p.font.color.rgb=color
 if align is not None:p.alignment=align
 return q
def base(title,kicker):
 s=prs.slides.add_slide(prs.slide_layouts[6]); s.background.fill.solid(); s.background.fill.fore_color.rgb=BG; box(s,0,0,.12,7.5,MINT,MINT,False); txt(s,.55,.28,11.8,.25,'SITESLEUTH / PROTOTYPE OVERVIEW',10,MINT,True); txt(s,.55,.75,12,.3,kicker.upper(),10,BLUE,True); txt(s,.55,1.05,12,.62,title,30,WHITE,True); txt(s,.55,7.15,12,.18,'LOCAL DEMO • FICTIONAL SAMPLE DATA • PASSIVE REVIEW ONLY',9,MUTED); return s
def bullets(s,x,y,w,items,size=17,gap=.7):
 for i,v in enumerate(items):
  yy=y+i*gap; z=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x),Inches(yy+.11),Inches(.12),Inches(.12)); z.fill.solid(); z.fill.fore_color.rgb=MINT; z.line.fill.background(); txt(s,x+.23,yy,w-.23,.58,v,size,WHITE)
# cover
s=prs.slides.add_slide(prs.slide_layouts[6]); s.background.fill.solid(); s.background.fill.fore_color.rgb=BG; box(s,0,0,.15,7.5,MINT,MINT,False)
for x,y,d,c in [(9.3,1.4,2.8,LINE),(10,2.1,1.7,MINT),(10.45,2.55,.8,BLUE)]:
 z=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x),Inches(y),Inches(d),Inches(d)); z.fill.background(); z.line.color.rgb=c; z.line.width=Pt(2)
txt(s,.8,.65,8,.35,'LOCAL SECURITY REVIEW • LEARNING PROTOTYPE',12,MINT,True); txt(s,.8,1.55,8.4,1.5,'SiteSleuth',48,WHITE,True); txt(s,.83,3,7.6,1.15,'A calm, read-only first look at common web security signals.',25,MUTED); box(s,.8,5.1,6.7,.76); txt(s,1.05,5.28,6.2,.32,'No crawling. No payloads. No real target in demo mode.',15,MINT,True); txt(s,.8,6.8,7,.25,'Based on the supplied SiteSleuth prototype and its local demo dashboard',11,MUTED)
# intent
s=base('The purpose: make a first review understandable','01 / intent'); txt(s,.65,1.95,5.4,.4,'A lightweight helper for authorized reviews',20,MINT,True); bullets(s,.7,2.55,5.6,['Check one supplied public homepage response for selected security headers.','Review one local source file for secret-like patterns and risky code sinks.','Show evidence and practical next steps without presenting heuristics as proof.'],17,.92); box(s,6.85,2.05,5.75,3.9,RGBColor(15,35,42),RGBColor(39,85,74)); txt(s,7.2,2.42,4.9,.36,'DESIGN BOUNDARY',12,MINT,True); txt(s,7.2,2.98,4.85,1.55,'Passive checks only. The tool is intentionally not an exploit scanner.',25,WHITE,True); txt(s,7.2,4.95,4.75,.62,'Use only on sites and code you own or have permission to assess.',16,MUTED)
# flow
s=base('How the prototype works','02 / workflow')
for i,(n,h,b) in enumerate([('01','Choose scope','One public homepage URL OR one local source file.'),('02','Run bounded check','Homepage: ordinary request + response headers. Source: local text scan.'),('03','Review report','Findings include an ID, severity label, evidence and suggested fix.'),('04','Validate manually','Treat each item as a lead; confirm context before acting.')]):
 x=.7+i*3.12; box(s,x,2.2,2.75,3.25); txt(s,x+.22,2.48,.7,.5,n,24,MINT,True); txt(s,x+.22,3.13,2.25,.5,h,19,WHITE,True); txt(s,x+.22,3.8,2.27,1.4,b,15,MUTED)
 if i<3:txt(s,x+2.78,3.4,.32,.4,'→',20,BLUE,True,align=PP_ALIGN.CENTER)
txt(s,.78,5.95,11.6,.44,'URL mode blocks non-public resolved addresses; it does not crawl or submit forms.',15,AMBER,True)
# checks
s=base('What it checks today','03 / implemented checks'); box(s,.7,2.05,5.9,4.35); box(s,6.8,2.05,5.85,4.35); txt(s,1.05,2.35,5,.4,'PUBLIC HOMEPAGE HEADERS',15,MINT,True); bullets(s,1.05,2.95,5,['HSTS','Content-Security-Policy','X-Content-Type-Options','X-Frame-Options','Referrer-Policy','Permissions-Policy'],15,.48); txt(s,7.15,2.35,4.9,.4,'LOCAL SOURCE TEXT',15,BLUE,True); bullets(s,7.15,2.95,4.95,['Secret-like patterns (values are not printed)','Potential innerHTML / document.write sinks','eval / new Function patterns','Line-number evidence with remediation hints'],15,.72); txt(s,1.05,6.55,11.5,.28,'A missing header is a hardening recommendation, not proof of an exploitable vulnerability.',13,AMBER,True)
# demo
s=base('The local dashboard uses fictional demo data','04 / demo mode'); txt(s,.7,1.95,7.1,.42,'Example report summary',18,MINT,True)
for i,(n,l) in enumerate([('4','review items'),('0','high'),('1','medium'),('2','low'),('1','info')]):
 x=.7+i*2.45; box(s,x,2.55,2.12,1.25); txt(s,x+.18,2.68,1.75,.47,n,28,WHITE,True); txt(s,x+.18,3.2,1.75,.3,l.upper(),10,MUTED,True)
box(s,.7,4.15,11.95,1.75,RGBColor(33,28,19),RGBColor(81,69,44)); txt(s,1,4.42,10.9,.4,'DEMO TARGET  https://demo.example.test',17,AMBER,True); txt(s,1,4.98,10.9,.55,'Sample items: CSP unsafe-inline (Info), absent HSTS and Referrer-Policy (Low), possible innerHTML sink in sample source (Medium).',15,WHITE); txt(s,.8,6.25,11.6,.42,'The dashboard reads demo_data.json. It does not contact or scan a real website.',16,MINT,True)
# detail
s=base('Example finding: a lead, not a verdict','05 / report detail'); box(s,.8,2.05,11.75,3.8); txt(s,1.15,2.4,1.25,.35,'MEDIUM',12,AMBER,True); txt(s,2.35,2.32,8.7,.48,'Potential unsafe DOM sink in sample source',21,WHITE,True); txt(s,1.15,3.1,10.7,.78,'Evidence: fictional sample uses innerHTML. This pattern alone does not prove exploitability.',17,MUTED); txt(s,1.15,4.12,1.4,.35,'NEXT STEP',11,MINT,True); txt(s,2.35,4.04,9.5,.72,'Prefer textContent for plain text; review whether untrusted input can reach the sink.',17,WHITE); txt(s,1.15,5.28,10.4,.3,'A reviewer must establish data flow, context and safeguards before calling this a vulnerability.',14,AMBER,True)
# limits
s=base('What SiteSleuth does not establish','06 / limitations'); box(s,.7,2,5.85,4.4,RGBColor(39,27,34),RGBColor(87,48,58)); box(s,6.8,2,5.85,4.4); txt(s,1.05,2.3,5,.4,'NOT TESTED BY THIS PROTOTYPE',14,RED,True); bullets(s,1.05,2.9,5,['Access control / IDOR','Authentication, sessions, CSRF','Injection or XSS exploitability','Uploads, APIs, dependencies, cloud setup','Rate limits, business logic, AI safety'],14,.57); txt(s,7.15,2.3,4.8,.4,'HOW TO READ THE RESULT',14,MINT,True); bullets(s,7.15,2.9,4.9,['No findings ≠ secure','Heuristics can miss issues or flag safe code','Header gaps are not confirmed vulnerabilities','Validate manually and document exact scope','Get written authorization for deeper testing'],14,.66)
# run
s=base('Run the demo locally','07 / getting started'); txt(s,.75,2,11.8,.42,'From the SiteSleuth project folder:',19,MINT,True); box(s,.8,2.65,11.7,1.02,RGBColor(7,12,22),LINE,False); txt(s,1.1,2.95,10.9,.42,'python -m http.server 8765 --bind 127.0.0.1',20,WHITE,True,'Cascadia Code'); txt(s,.85,4.05,11.5,.42,'Open  http://127.0.0.1:8765/  •  stop with Ctrl+C',18,BLUE,True); bullets(s,.9,4.85,11.2,['Loopback binding keeps the dashboard on this computer.','The browser loads index.html and fictional demo_data.json from the local folder.','CLI remains available: python sitesleuth.py --source tests/sample_source.js'],15,.6)
# roadmap
s=base('A sensible next iteration','08 / roadmap')
for i,(h,b) in enumerate([('Improve the report','Add timestamps, tested scope and confidence labels.'),('Add safe local checks','Expand source review with transparent rules and tests.'),('Make results easier to share','Export a small JSON/HTML report with evidence and limitations.'),('Keep scope explicit','Any live checks stay passive, authorized and narrowly bounded.')]):
 y=2.05+i*1.03; box(s,.85,y,11.6,.82); txt(s,1.12,y+.14,2.45,.35,h,17,MINT,True); txt(s,3.65,y+.14,8.25,.45,b,16,WHITE)
# close
s=prs.slides.add_slide(prs.slide_layouts[6]); s.background.fill.solid(); s.background.fill.fore_color.rgb=BG; box(s,0,0,.15,7.5,MINT,MINT,False); txt(s,.8,.65,8,.3,'SITESLEUTH / TAKEAWAY',11,MINT,True); txt(s,.8,1.45,10.9,1.15,'A safer first look,\nwith honest limits.',38,WHITE,True); txt(s,.85,4.15,10.2,.85,'SiteSleuth helps surface a few review signals. People still provide the authorization, context and judgment.',22,MUTED); box(s,.85,5.7,7.7,.75); txt(s,1.1,5.91,7.1,.34,'Prototype • local demo • fictional sample data • passive only',15,MINT,True); txt(s,.85,7.05,11,.2,'Prepared from the supplied SiteSleuth prototype files',10,MUTED)
prs.core_properties.title='SiteSleuth Prototype Overview'; prs.core_properties.subject='Local passive website security review prototype'; prs.core_properties.author='OpenAI'; OUT.parent.mkdir(parents=True,exist_ok=True); prs.save(OUT); print(f'created={OUT} slides={len(prs.slides)} bytes={OUT.stat().st_size}')
