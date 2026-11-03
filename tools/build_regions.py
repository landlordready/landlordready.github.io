#!/usr/bin/env python3
"""Generate one SEO page per English region for the PRS Database deadline.
Edit REGIONS below and re-run: python3 tools/build_regions.py"""
import json, os, datetime, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://landlordready.github.io"
REGIONS = [
 ("west-midlands","West Midlands","2026-12-15","2027-03-14",["Birmingham","Coventry","Wolverhampton","Dudley","Walsall","Sandwell","Solihull","Stoke-on-Trent","Telford","Worcester","Hereford","Shrewsbury","Stafford","Warwick","Nuneaton"]),
 ("east-of-england","East of England","2027-01-15","2027-04-14",["Norwich","Cambridge","Peterborough","Ipswich","Colchester","Chelmsford","Southend-on-Sea","Luton","Bedford","Watford","St Albans","Stevenage","Basildon","King's Lynn"]),
 ("east-midlands","East Midlands","2027-02-15","2027-05-14",["Nottingham","Leicester","Derby","Northampton","Lincoln","Chesterfield","Mansfield","Loughborough","Kettering","Corby","Boston","Grantham"]),
 ("south-east","South East","2027-03-15","2027-06-14",["Brighton and Hove","Southampton","Portsmouth","Reading","Oxford","Milton Keynes","Slough","Canterbury","Maidstone","Guildford","Crawley","Basingstoke","High Wycombe","Medway"]),
 ("yorkshire-and-the-humber","Yorkshire and The Humber","2027-04-15","2027-07-14",["Leeds","Sheffield","Bradford","Hull","York","Wakefield","Doncaster","Rotherham","Barnsley","Huddersfield","Halifax","Harrogate","Scarborough","Grimsby"]),
 ("north-west","North West","2027-05-15","2027-08-14",["Manchester","Liverpool","Salford","Bolton","Stockport","Wigan","Preston","Blackpool","Blackburn","Warrington","Oldham","Rochdale","Chester","Lancaster","Carlisle"]),
 ("north-east","North East","2027-06-15","2027-09-14",["Newcastle upon Tyne","Sunderland","Gateshead","Middlesbrough","Durham","Darlington","Hartlepool","Stockton-on-Tees","South Shields","Northumberland"]),
 ("london","London","2027-07-15","2027-10-14",["the City of London","Tower Hamlets","Newham","Southwark","Lambeth","Camden","Hackney","Croydon","Barnet","Ealing","Brent"]),
 ("south-west","South West","2027-08-15","2027-11-14",["Bristol","Plymouth","Exeter","Bath","Bournemouth","Poole","Swindon","Gloucester","Cheltenham","Torquay","Taunton","Truro","Salisbury"]),
]
def fmt(d): return datetime.date.fromisoformat(d).strftime("%-d %B %Y")
def short(d): return datetime.date.fromisoformat(d).strftime("%-d %B")

CSS = open(os.path.join(ROOT,"tools","region.css")).read()

def page(slug,name,opens,deadline,cities,idx):
    prev_r = REGIONS[idx-1] if idx>0 else None
    next_r = REGIONS[idx+1] if idx<len(REGIONS)-1 else None
    title = f"Landlord register deadline {name}: register by {fmt(deadline)}"
    desc = (f"PRS Database for landlords in {name}: registration opens {fmt(opens)} and must be done by {fmt(deadline)}. "
            f"£65 per property, penalties up to £7,000. Free checklist.")
    city_txt = ", ".join(cities)
    faq = [
      (f"When must landlords in {name} register on the PRS Database?",
       f"The regulations start in {name} on {fmt(opens)}. You then have three months, so the deadline is {fmt(deadline)}. You can register early."),
      ("How much does it cost?","Published local-authority guidance says £65 per property per year. The fee is per property, not per landlord, and is paid again on each annual renewal."),
      ("What happens if I don't register?","Councils can issue a civil penalty of up to £7,000 for letting or advertising without an active entry, and up to £40,000 for repeated breaches or false information. Unregistered landlords are also limited in the possession grounds they can use."),
      ("What do I need before I start?","Your contact details, the property address and type, number of bedrooms and occupants, rent and included bills, any HMO or selective licence number, your gas safety record date (if there is gas), your EICR expiry date and your EPC details."),
      ("Does it depend on where I live?",f"No. It depends on where the rented property is. A landlord living elsewhere with a home in {name} follows the {name} dates."),
    ]
    ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    faq_html = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q,a in faq)
    nav = []
    if prev_r: nav.append(f'<a href="../{prev_r[0]}/">← {prev_r[1]}</a>')
    nav.append('<a href="../">All regions</a>')
    if next_r: nav.append(f'<a href="../{next_r[0]}/">{next_r[1]} →</a>')
    return f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{BASE}/register/{slug}/">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{BASE}/register/{slug}/"><meta property="og:type" content="article">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld)}</script>
</head><body><div class="wrap">
<header><a class="brand" href="../../">LandlordReady</a> <span class="muted small">· independent guide for landlords in England</span></header>
<p class="crumbs small"><a href="../../">Home</a> › <a href="../">Landlord register by region</a> › {html.escape(name)}</p>
<h1>Landlord register deadline in {html.escape(name)}</h1>
<p class="lead">If you rent out a home in {html.escape(name)}, you must add it to the new PRS Database (the national landlord register) by <b>{fmt(deadline)}</b>.</p>
<div class="dates">
<div><span>Register opens</span><b>{fmt(opens)}</b></div>
<div><span>Deadline</span><b>{fmt(deadline)}</b></div>
<div><span>Fee</span><b>£65 / property / year</b></div>
</div>
<p><a class="btn" href="../../?region={slug}">Check my property and get a document checklist</a></p>
<h2>Who this applies to</h2>
<p>Private landlords with rented homes anywhere in {html.escape(name)}, including {html.escape(city_txt)}. The date follows the property's location, not where you live.</p>
<h2>What to do and when</h2>
<ol>
<li><b>Now:</b> find your gas safety record, EICR (electrical report) and EPC. Note their dates. Book any that have expired.</li>
<li><b>Before {short(opens)}:</b> gather tenancy details: occupants, rent, bills included, any licence numbers.</li>
<li><b>From {short(opens)}:</b> register each property on the official GOV.UK service and pay £65 per property.</li>
<li><b>By {short(deadline)}:</b> every let property in {html.escape(name)} should have an active entry. After this councils can enforce.</li>
</ol>
<h2>Questions landlords in {html.escape(name)} ask</h2>
{faq_html}
<p class="nav">{" · ".join(nav)}</p>
<footer><p>Dates and fee are taken from published local-authority guidance (November 2026) and may change. LandlordReady is an independent tool, not affiliated with the UK Government, and does not give legal advice. Always check GOV.UK before acting.</p></footer>
</div></body></html>"""

def index_page():
    rows = "".join(f'<tr><td><a href="{s}/">{n}</a></td><td>{fmt(o)}</td><td>{fmt(d)}</td></tr>' for s,n,o,d,_ in REGIONS)
    title = "Landlord register deadlines by region (England) – PRS Database dates"
    desc = "When must you register on the PRS Database? Opening dates and deadlines for all 9 English regions, from West Midlands (Dec 2026) to South West (Nov 2027)."
    return f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}/register/"><style>{CSS}</style></head><body><div class="wrap">
<header><a class="brand" href="../">LandlordReady</a> <span class="muted small">· independent guide for landlords in England</span></header>
<h1>Landlord register deadlines by region</h1>
<p class="lead">The PRS Database opens region by region. Each region gets three months to register. Pick the region where your rented property is.</p>
<table><thead><tr><th>Region</th><th>Opens</th><th>Deadline</th></tr></thead><tbody>{rows}</tbody></table>
<p><a class="btn" href="../">Not sure of your region? Check by postcode</a></p>
<footer><p>Dates from published local-authority guidance (November 2026); they may change. Independent tool, not affiliated with the UK Government. Check GOV.UK before acting.</p></footer>
</div></body></html>"""

os.makedirs(os.path.join(ROOT,"register"),exist_ok=True)
open(os.path.join(ROOT,"register","index.html"),"w").write(index_page())
for i,r in enumerate(REGIONS):
    d=os.path.join(ROOT,"register",r[0]); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,"index.html"),"w").write(page(*r,i))
today=datetime.date.today().isoformat()
urls=[f"{BASE}/",f"{BASE}/register/"]+[f"{BASE}/register/{r[0]}/" for r in REGIONS]
open(os.path.join(ROOT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)+"</urlset>\n")
print("built",len(urls),"urls")
