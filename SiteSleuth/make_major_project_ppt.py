from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path

OUT=Path(r'C:\Users\DELL\Hermes-Output\SiteSleuth\SiteSleuth-Major-Project.pptx')
prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
BG=RGBColor(11,17,32); PANEL=RGBColor(18,28,45); LINE=RGBColor(35,51,74); WHITE=RGBColor(232,239,248); MUTED=RGBColor(154,171,192); MINT=RGBColor(105,224,177); BLUE=RGBColor(125,185,255); AMBER=RGBColor(255,202,106); RED=RGBColor(255,122,134)
FONT='Times New Roman'
def shape(s,x,y,w,h,fill=PANEL,line=LINE,kind=MSO_SHAPE.ROUNDED_RECTANGLE):
 q=s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h)); q.fill.solid(); q.fill.fore_color.rgb=fill; q.line.color.rgb=line; q.line.width=Pt(1); return q
def text(s,x,y,w,h,t,size=17,color=WHITE,bold=False,align=None):
 q=s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); f=q.text_frame; f.clear(); f.word_wrap=True; f.margin_left=Inches(.06); f.margin_right=Inches(.06); f.margin_top=Inches(.03); f.margin_bottom=Inches(.03); p=f.paragraphs[0]; p.text=t; p.font.name=FONT; p.font.size=Pt(size); p.font.bold=bold; p.font.color.rgb=color
 if align is not None:p.alignment=align
 return q
def base(title,kicker):
 s=prs.slides.add_slide(prs.slide_layouts[6]); s.background.fill.solid(); s.background.fill.fore_color.rgb=BG; shape(s,0,0,.12,7.5,MINT,MINT,MSO_SHAPE.RECTANGLE); text(s,.55,.25,12,.25,'SITESLEUTH  |  MAJOR PROJECT',11,MINT,True); text(s,.55,.65,12,.25,kicker.upper(),10,BLUE,True); text(s,.55,.95,12,.6,title,28,WHITE,True); text(s,.55,7.16,12,.18,'ACADEMIC PROTOTYPE • PASSIVE REVIEW ONLY • FICTIONAL DEMO DATA',9,MUTED); return s
def bullets(s,x,y,w,items,size=16,gap=.58):
 for i,item in enumerate(items):
  yy=y+i*gap; shape(s,x,yy+.1,.12,.12,MINT,MINT,MSO_SHAPE.OVAL); text(s,x+.22,yy,w-.22,gap-.02,item,size,WHITE)
# 1 cover
s=prs.slides.add_slide(prs.slide_layouts[6]); s.background.fill.solid(); s.background.fill.fore_color.rgb=BG; shape(s,0,0,.15,7.5,MINT,MINT,MSO_SHAPE.RECTANGLE)
text(s,.85,.65,10,.32,'MAJOR PROJECT PRESENTATION  |  2025–2026',13,MINT,True); text(s,.85,1.45,8.2,1.2,'SiteSleuth',46,WHITE,True); text(s,.9,2.85,8.6,1.1,'A read-only helper for an initial, authorized website security review',24,MUTED); shape(s,.9,4.65,7.6,.8); text(s,1.15,4.86,7.05,.35,'Presented by: [Student name(s)]  |  [Roll no(s)]',15,WHITE,True); text(s,.9,5.7,8,.35,'Guide: [Guide name]  |  Department: Computer Science and Engineering',14,MUTED); text(s,.9,6.65,8,.25,'[College / University name]',12,BLUE,True)
# 2
s=base('Project overview & motivation','01 / introduction'); bullets(s,.8,1.85,7.2,['Small websites may lack clear visibility into basic browser-security configuration.','Manual first-pass checks can be inconsistent and difficult for beginners to interpret.','SiteSleuth turns a small set of observable signals into evidence-linked review leads.','The prototype is deliberately passive; it is not a penetration-testing or exploit tool.'],16,.75); shape(s,8.6,2.1,3.8,3.35,RGBColor(15,35,42),RGBColor(39,85,74)); text(s,8.95,2.45,3.2,.4,'PROJECT AIM',13,MINT,True); text(s,8.95,3.0,3.05,1.45,'Make a bounded first review understandable, reproducible and safer.',22,WHITE,True)
#3
s=base('Problem statement, objectives & scope','02 / problem definition'); shape(s,.8,1.85,11.7,1.25); text(s,1.05,2.05,11.2,.85,'Problem: Users need a simple way to surface selected website-header and source-code review signals, but lightweight checks can be mistaken for proof of security or exploitability.',17,WHITE,True); bullets(s,1,3.45,11,['Objective: inspect six selected response headers from one supplied public homepage.','Objective: scan one local source text file for selected secret-like and risky-code patterns.','Objective: present finding ID, severity label, evidence and a suggested remediation.','Scope exclusions: no crawling, form submission, payloads, credential guessing, authentication tests or bypass attempts.'],15,.67)
#4
s=base('Prerequisites, assumptions & ethical use','03 / prerequisites'); bullets(s,.85,1.85,7.2,['Python 3.10 or later; prototype uses Python standard library (no third-party packages required).','For local dashboard: a browser and the project folder containing index.html and demo_data.json.','For URL mode: internet connectivity and a user-supplied public HTTP(S) homepage.','For source mode: permission to read the local file and UTF-8-compatible text input.','Written authorization and agreed scope are prerequisites for assessing any real asset.'],15,.7); shape(s,8.55,2.1,3.85,3.65,RGBColor(39,27,34),RGBColor(87,48,58)); text(s,8.85,2.45,3.2,.35,'SAFETY GUARDRAILS',13,RED,True); text(s,8.85,3.0,3.1,1.8,'Blocks non-public resolved IPs in URL mode. Demo dashboard uses fictional data and makes no target request.',19,WHITE,True)
#5
s=base('System design & data flow','04 / design');
for i,(a,b) in enumerate([('INPUT','One public URL OR one local source file'),('VALIDATE','URL scheme, hostname and resolved IP scope'),('ANALYZE','Response-header rules OR local text heuristics'),('REPORT','JSON findings: ID, label, evidence, remediation')]):
 x=.7+i*3.15; shape(s,x,2.15,2.75,2.5); text(s,x+.2,2.42,2.3,.3,a,13,MINT,True); text(s,x+.2,2.95,2.28,1.25,b,16,WHITE,True)
 if i<3:text(s,x+2.78,3.15,.3,.35,'→',19,BLUE,True,PP_ALIGN.CENTER)
text(s,.9,5.2,11.3,.62,'Architecture: command-line Python checker + static local HTML dashboard reading a JSON demo report. The dashboard is not wired to live scanning.',16,AMBER,True)
#6
s=base('Methodology & algorithms','05 / method'); bullets(s,.85,1.85,11.2,['URL validation: accept http/https, reject embedded credentials, resolve host and block any non-global address.','Homepage mode: issue one ordinary request (12-second timeout); inspect response status and selected headers only.','Header rules: report absent headers as low hardening recommendations; CSP unsafe allowances as informational review items.','Source mode: apply regular-expression heuristics line by line; report line numbers while redacting matched secret values.','Serialize results as JSON with scope, findings and notes; human reviewer validates context and data flow.'],15,.72)
#7
s=base('Tools, technologies & prerequisites used','06 / technology');
for i,(a,b) in enumerate([('LANGUAGE','Python 3'),('LIBRARIES','Standard library: urllib, socket, ipaddress, re, json'),('INTERFACE','HTML, CSS, JavaScript dashboard'),('DATA','JSON fictional demonstration report'),('TESTING','Python unittest; sample source fixture')]):
 y=1.9+i*.86; shape(s,.9,y,11.45,.65); text(s,1.15,y+.13,2.2,.32,a,13,MINT,True); text(s,3.55,y+.11,8.4,.37,b,16,WHITE)
#8
s=base('Implementation: modules & operation','07 / implementation'); bullets(s,.85,1.85,11.1,['sitesleuth.py: validate_public_url(), analyze_headers(), scan_text(), CLI argument handling and JSON output.','index.html: local dashboard interface; demo_data.json: explicitly fictional report content.','URL CLI: python sitesleuth.py https://your-authorized-site.example','Source CLI: python sitesleuth.py --source path/to/authorized-file.js','Dashboard: python -m http.server 8765 --bind 127.0.0.1 then open http://127.0.0.1:8765/','Tests: python -m unittest discover -s tests -v'],15,.69)
#9
s=base('Results & sample observations','08 / results'); text(s,.85,1.78,11,.35,'Prototype demo summary (fictional training data; no real website scanned)',15,AMBER,True)
for i,(n,l) in enumerate([('4','items'),('0','high'),('1','medium'),('2','low'),('1','info')]):
 x=.8+i*2.45; shape(s,x,2.35,2.12,1.12); text(s,x+.18,2.48,1.72,.43,n,26,WHITE,True); text(s,x+.18,2.94,1.72,.27,l.upper(),10,MUTED,True)
shape(s,.85,3.95,11.55,1.65); text(s,1.12,4.2,10.9,1.12,'Illustrative findings: CSP unsafe-inline (Info); absent HSTS and Referrer-Policy (Low); potential innerHTML sink in sample source (Medium). These are review leads, not confirmed vulnerabilities.',16,WHITE); text(s,.9,5.95,11.4,.45,'Observed prototype behavior: local dashboard serves fictional JSON; CLI produces structured findings. No performance/security guarantee is claimed.',14,MINT,True)
#10
s=base('Testing, limitations & risk management','09 / evaluation'); bullets(s,.85,1.8,6.1,['Unit tests cover core check behavior and sample input.','Manual checks should verify JSON structure, redaction and URL scope blocking.','False positives and false negatives are expected; heuristics do not establish exploitability.'],15,.83); shape(s,7.25,2.0,5.0,3.7,RGBColor(39,27,34),RGBColor(87,48,58)); text(s,7.6,2.35,4.1,.35,'NOT COVERED',13,RED,True); text(s,7.6,2.9,4.0,2.25,'Access control, authentication, injection, CSRF, uploads, API authorization, dependencies, cloud configuration, business logic and AI safety.',18,WHITE,True); text(s,.9,5.85,11.2,.48,'“No findings” does not mean “secure.” Deeper testing requires explicit written scope and owner-approved safeguards.',15,AMBER,True)
#11
s=base('Team roles, future scope & conclusion','10 / conclusion'); bullets(s,.85,1.8,6.3,['Member 1 – [Name]: requirements, interface and documentation.','Member 2 – [Name]: URL validation and header-analysis module.','Member 3 – [Name]: source heuristics, tests and integration.','Adjust names and responsibilities to match actual contributions.'],14,.65); shape(s,7.45,1.95,4.85,3.85); text(s,7.8,2.25,4.0,.35,'NEXT STEPS',13,MINT,True); text(s,7.8,2.8,4.0,2.35,'Safer local repository review; improved report metadata/confidence; exportable reports; passive HTML configuration review with explicit authorization.',17,WHITE,True); text(s,.9,5.0,6.2,.8,'Conclusion: SiteSleuth demonstrates a small, bounded workflow that surfaces selected signals and communicates limitations.',16,WHITE,True)
#12
s=base('References & questions','11 / references'); bullets(s,.9,1.9,11,['SiteSleuth project source: sitesleuth.py, README.md, index.html, demo_data.json and tests/ (project prototype).','MDN Web Docs, HTTP response headers — https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers','OWASP, Secure Headers Project — https://owasp.org/www-project-secure-headers/','Python 3 documentation — https://docs.python.org/3/','Template: “PPT Format for Major Project” supplied by the student.'],15,.72); shape(s,.9,5.95,11.3,.7); text(s,1.2,6.13,10.7,.3,'THANK YOU  |  Questions?',18,MINT,True,PP_ALIGN.CENTER)
prs.core_properties.title='SiteSleuth Major Project Presentation'; prs.core_properties.subject='SiteSleuth prototype: authorized passive website review'; prs.core_properties.author='[Student name(s)]'; OUT.parent.mkdir(parents=True,exist_ok=True); prs.save(OUT); print(f'CREATED {OUT} | slides={len(prs.slides)} | bytes={OUT.stat().st_size}')