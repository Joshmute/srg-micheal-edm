"""Generate editable draw.io files and SVG/PNG figures from the same graph."""
from pathlib import Path
import xml.etree.ElementTree as ET
import html,textwrap,math
import pymupdf
OUT=Path('diagrams');OUT.mkdir(exist_ok=True)

def graph(name,title,nodes,edges,w=1100,h=730,er=False):
    # node: id, label, x,y,width,height. edge: from,to,label,start,end.
    mx=ET.Element('mxfile',host='app.diagrams.net');d=ET.SubElement(mx,'diagram',name=title,id=name)
    model=ET.SubElement(d,'mxGraphModel',page='1',pageWidth=str(w),pageHeight=str(h));root=ET.SubElement(model,'root')
    ET.SubElement(root,'mxCell',id='0');ET.SubElement(root,'mxCell',id='1',parent='0')
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="#ffffff"/><text x="25" y="35" font-family="Times New Roman" font-size="24" font-weight="bold" fill="#000000">{html.escape(title)}</text>']
    lookup={n[0]:n for n in nodes}
    for k,(a,b,label,*markers) in enumerate(edges):
        start,end=(markers+['',''])[:2]
        na,nb=lookup[a],lookup[b]
        ax,ay=na[2]+na[4]/2,na[3]+na[5]/2;bx,by=nb[2]+nb[4]/2,nb[3]+nb[5]/2
        dx,dy=bx-ax,by-ay
        def boundary(n,cx,cy,vx,vy):
            ratios=[]
            if vx:ratios.append(n[4]/2/abs(vx))
            if vy:ratios.append(n[5]/2/abs(vy))
            t=min(ratios);return cx+vx*t,cy+vy*t
        x1,y1=boundary(na,ax,ay,dx,dy);x2,y2=boundary(nb,bx,by,-dx,-dy)
        route=None
        if False:
            x1,y1=na[2],ay;x2,y2=nb[2],by
            route=[(x1,y1),(na[2]-45,y1),(na[2]-45,y2),(x2,y2)]
        elif name=='etl' and (a,b)==('c','q'):
            x1,y1=na[2]+na[4],ay;x2,y2=nb[2]+nb[4],by
            route=[(x1,y1),(1090,y1),(1090,y2),(x2,y2)]
        path='M'+ ' L'.join(f'{x},{y}' for x,y in (route or [(x1,y1),(x2,y2)]))
        svg.append(f'<path d="{path}" stroke="#000000" stroke-width="2" fill="none"/>')
        def marker(x,y,tx,ty,kind):
            length=math.hypot(tx,ty);ux,uy=tx/length,ty/length;vx,vy=-uy,ux
            def line(a,b,c,d):svg.append(f'<path d="M{a},{b} L{c},{d}" stroke="#000000" stroke-width="2"/>')
            if 'many' in kind:
                for s in (-8,0,8):line(x+ux*16,y+uy*16,x+vx*s,y+vy*s)
            if 'one' in kind:
                for t in (7,13):line(x+ux*t+vx*7,y+uy*t+vy*7,x+ux*t-vx*7,y+uy*t-vy*7)
            if 'zero' in kind:
                svg.append(f'<circle cx="{x+ux*24}" cy="{y+uy*24}" r="5" fill="#ffffff" stroke="#000000" stroke-width="2"/>')
            if not kind:
                line(x,y,x+ux*12+vx*5,y+uy*12+vy*5);line(x,y,x+ux*12-vx*5,y+uy*12-vy*5)
        if er:
            if route: marker(x1,y1,route[1][0]-x1,route[1][1]-y1,start);marker(x2,y2,route[-2][0]-x2,route[-2][1]-y2,end)
            else: marker(x1,y1,dx,dy,start);marker(x2,y2,-dx,-dy,end)
        else:
            marker(x2,y2,-dx,-dy,'')
            if name=='mdm-flows': marker(x1,y1,dx,dy,'')
        if label:
            tx=(x1+x2)/2;ty=(y1+y2)/2-8
            svg.append(f'<rect x="{tx-len(label)*4.2}" y="{ty-14}" width="{len(label)*8.4}" height="20" fill="#ffffff"/><text x="{tx}" y="{ty}" text-anchor="middle" font-family="Times New Roman" font-size="14" fill="#000000">{html.escape(label)}</text>')
        def arrow(k):return {'one':'ERmandOne','zero_one':'ERzeroToOne','many':'ERmany','zero_many':'ERzeroToMany'}.get(k,'block')
        style=f'edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow={arrow(end) if er else "block"};startArrow={arrow(start) if er else ("block" if name=="mdm-flows" else "none")};fontSize=14;'
        c=ET.SubElement(root,'mxCell',id=f'e{k}',value=label,style=style,edge='1',parent='1',source=a,target=b);ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
    for id,label,x,y,nw,nh in nodes:
        svg.append(f'<rect x="{x}" y="{y}" width="{nw}" height="{nh}" rx="0" fill="white" stroke="#000000" stroke-width="2"/>')
        lines=[]
        for part in label.split('\n'):lines.extend(textwrap.wrap(part,width=max(10,int(nw/9.3))) or [''])
        for k,line in enumerate(lines):svg.append(f'<text x="{x+12}" y="{y+25+k*22}" font-family="Times New Roman" font-size="{17 if k else 18}" font-weight="{"bold" if k==0 else "normal"}" fill="#000000">{html.escape(line)}</text>')
        c=ET.SubElement(root,'mxCell',id=id,value=html.escape(label).replace('\n','&lt;br&gt;'),style='rounded=0;whiteSpace=wrap;html=0;fillColor=#ffffff;strokeColor=#000000;fontSize=17;',vertex='1',parent='1')
        c.set('value',label)
        ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(nw),height=str(nh),attrib={'as':'geometry'})
    svg.append('</svg>');data=''.join(svg).encode();(OUT/f'{name}.svg').write_bytes(data)
    ET.ElementTree(mx).write(OUT/f'{name}.drawio',encoding='utf-8',xml_declaration=True)
    doc=pymupdf.open(stream=data,filetype='svg');doc[0].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(OUT/f'{name}.png')

# The vertical decision path reflects the central reporting / registry design.
graph('lifecycle','Customer records and control gates',[
('a','Collect\nCashier / online form\nPurpose and provisional ID',50,85,390,135),('b','Retain securely\nIT device and backup controls\nRestricted landing',660,85,390,135),('c','Use with authority\nOwner approves purpose\nReview disputed identity',660,310,390,135),('d','Share minimum fields\nDPO + procurement\nTerms and destination',50,310,390,135),('e','Archive with expiry\nOwner sets schedule\nIT restricts recovery',50,535,390,135),('f','Delete and propagate\nSources + processors\nRestore applies tombstones',660,535,390,135)], [('a','b','capture'),('b','c','authorise'),('c','d','approve'),('d','e','schedule'),('e','f','expire')],h=720)
nodes=[('customer','Customer',55,95,250,90),('loyalty','LoyaltyAccount',55,360,250,90),('order','Order',425,95,250,90),('store','Store',790,95,250,90),('line','OrderLine',425,360,250,90),('payment','Payment',790,360,250,90),('product','Product',425,620,250,90),('supplier','Supplier',790,620,250,90)]
edges=[('customer','order','','zero_one','zero_many'),('customer','loyalty','','one','zero_one'),('order','line','','one','many'),('order','payment','','one','zero_many'),('store','order','','one','zero_many'),('product','line','','one','zero_many'),('product','supplier','','zero_many','zero_many')]
graph('conceptual-er','Retail entity relationships | circle optional, fork many',nodes,edges,h=770,er=True)
labels={'customer':'Customer\nPK customer_id\nname / phone / email','loyalty':'LoyaltyAccount\nPK account_id\nFK customer_id UNIQUE','order':'Order\nPK order_id\nFK store_id\nFK customer_id nullable','store':'Store\nPK store_id\ndistrict / name','line':'OrderLine\nPK/FK order_id\nPK line_no\nFK product_id\nqty / unit_price','payment':'Payment\nPK payment_id\nFK order_id\nprovider / reference','product':'Product\nPK product_id\ncategory / unit','supplier':'Supplier\nPK supplier_id\nname / contact'}
logical=[(i,labels[i],x,y,275,190 if i=='line' else 165) for i,l,x,y,w,h in nodes]
logical.append(('bridge','ProductSupplier\nPK/FK product_id\nPK/FK supplier_id\nsupplier_sku',790,890,275,155))
edges=[e for e in edges if e[:2]!=('product','supplier')]+[('product','bridge','','one','zero_many'),('supplier','bridge','','one','zero_many')]
graph('logical-er','Relational keys and optionality',logical,edges,h=1090,er=True)
graph('warehouse','Central reporting with separate fact grains',[
('a','Local sources\nPOS / web / loyalty\nCRM / Odoo',30,90,300,155),('b','Restricted intake\nManifest and immutable files\nContracts and quarantine',400,90,300,155),('c','Central dimensions\nDate / Customer\nProduct SCD2 / Store SCD2',770,90,300,155),('d','Sales fact\nSource order line\nSigned quantity and amount',770,390,300,155),('e','Inventory fact\nStore / product / snapshot\nComparable units',400,390,300,155),('f','Payment fact\nProvider event grain\nSettlement state',30,390,300,155)],[('a','b','batch'),('b','c','validate'),('c','d','keys'),('c','e','keys'),('b','f','provider feed')],h=590)
graph('etl','Batch certification and controlled replay',[
('a','Extract and record\nSource count / hash\nContract version',30,90,300,145),('b','Validate and minimise\nParse / standardise\nReject with reason',400,90,300,145),('c','Resolve dimensions\nRegistry mapping\nEvent-time version',770,90,300,145),('d','Review queue\nOwner and due date\nCorrect then replay',400,380,300,145),('e','Commit facts\nCompare existing payload\nUnique source/order/line',770,380,300,145),('f','Certify totals\nExpected-file checklist\nAdvance watermark',30,380,300,145)],[('a','b','intake'),('b','c','pass'),('b','d','fail'),('c','e','load'),('e','f','reconcile')],h=590)
graph('mdm-flows','Registry maps identities without taking over source creation',[
('p','POS\nOffline source ID\nVerified correction request',30,90,300,150),('w','E-commerce\nCheckout identity\nContact confirmation',770,90,300,150),('r','Enterprise registry\nSource crosswalk / evidence\nHuman review / version\nConsolidated read view',380,345,340,175),('l','Loyalty\nAccount claims\nAuditable points ledger',30,640,300,145),('c','CRM\nApproved permission view\nWithdrawal applied first',770,640,300,145)],[('p','r','IDs / acknowledgements'),('w','r','claims / mappings'),('r','l','reviewed links'),('r','c','approved view')],h=830)
graph('streaming','Event topics remain separate',[
('a','Store edge\nPersist and sequence\nFootfall without person IDs',30,90,300,150),('b','Broker\nAt-least-once delivery\nRetry and dead-letter',400,90,300,150),('c','Consumers\nDeduplication\nEvent-time windows',770,90,300,150),('d','Traffic\n5-minute counts\nLate-correction counter',30,400,300,150),('e','Stock movements\nSales / receipts / transfers\nFreshness and reconciliation',400,400,300,150),('f','Payment events\nProvider references\nHuman investigation',770,400,300,150)],[('a','b','durable send'),('b','c','consume'),('c','d','footfall topic'),('c','e','stock topic'),('c','f','payment topic')],h=610)
graph('lineage','Active member measure and its exclusions',[
('a','Source lines\nCustomer ID / event date\nSigned quantity',30,95,300,145),('b','Source contract\nKampala calendar date\nKeep refunds negative',400,95,300,145),('c','Registry crosswalk\nApproved member key\nUnresolved counted apart',770,95,300,145),('d','Certified fact\nReconcile source totals\nReject conflicting replays',770,390,300,145),('e','Monthly distinct count\nPositive purchase required\nAnonymous excluded',400,390,300,145),('f','Report context\nPeriod and channel\nNever add monthly distincts',30,390,300,145)],[('a','b','parse'),('b','c','link'),('c','d','load'),('d','e','aggregate'),('e','f','present')],h=590)
# Conventional fishbone with reordered branches and distinct hypotheses.
def fishbone():
 w,h=1100,530
 mx=ET.Element('mxfile',host='app.diagrams.net');d=ET.SubElement(mx,'diagram',name='Variance investigation',id='fishbone');root=ET.SubElement(ET.SubElement(d,'mxGraphModel'),'root');ET.SubElement(root,'mxCell',id='0');ET.SubElement(root,'mxCell',id='1',parent='0')
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="530"><rect width="100%" height="100%" fill="white"/><text x="25" y="35" font-family="Times New Roman" font-size="24">Stock variance investigation | S systemic, E entry</text>']
 def line(i,x1,y1,x2,y2):
  svg.append(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="black" stroke-width="2"/>');c=ET.SubElement(root,'mxCell',id=i,edge='1',parent='1',style='endArrow=none;');g=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'});ET.SubElement(g,'mxPoint',x=str(x1),y=str(y1),attrib={'as':'sourcePoint'});ET.SubElement(g,'mxPoint',x=str(x2),y=str(y2),attrib={'as':'targetPoint'})
 def label(i,x,y,ls):
  for j,t in enumerate(ls):svg.append(f'<text x="{x}" y="{y+j*24}" font-family="Times New Roman" font-size="18">{html.escape(t)}</text>')
  c=ET.SubElement(root,'mxCell',id=i,value='\n'.join(ls),vertex='1',parent='1',style='text;whiteSpace=wrap;');ET.SubElement(c,'mxGeometry',x=str(x),y=str(y-20),width='250',height='90',attrib={'as':'geometry'})
 line('spine',45,265,870,265)
 for j,ls in enumerate([['UNITS','S: pack conversion absent','E: carton entered as each'],['TIMING','S: unsynchronised cutoffs','E: backdated receipt'],['MOVEMENTS','S: unmatched transfer','E: wrong return code'],['COUNTING','S: no independent recount','E: skipped shelf'],['IDENTITY','S: duplicate SKU mapping','E: wrong product scan'],['APPROVALS','S: unreviewed adjustments','E: omitted damage entry']]):
  x=40+(j%3)*275;top=j<3;line('r'+str(j),x+70,165 if top else 380,x+165,265);label('t'+str(j),x,85 if top else 420,ls)
 label('effect',885,240,['8.4% reported','variance','Not explained yet'])
 svg.append('</svg>');data=''.join(svg).encode();(OUT/'fishbone.svg').write_bytes(data);ET.ElementTree(mx).write(OUT/'fishbone.drawio',encoding='utf-8',xml_declaration=True);pymupdf.open(stream=data,filetype='svg')[0].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(OUT/'fishbone.png')
fishbone()
print('Nine separate diagrams generated')
