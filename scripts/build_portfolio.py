"""Render the editable Markdown portfolio into a paginated consultancy PDF."""
from pathlib import Path
import re,html,csv,json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
BASE=Path(__file__).resolve().parents[1]
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY
FONT_DIR=Path('/System/Library/Fonts/Supplemental')
for face,suffix in [('TNR',''),('TNR-Bold',' Bold'),('TNR-Italic',' Italic'),('TNR-BoldItalic',' Bold Italic')]:
    pdfmetrics.registerFont(TTFont(face,str(FONT_DIR/f'Times New Roman{suffix}.ttf')))
pdfmetrics.registerFontFamily('TNR',normal='TNR',bold='TNR-Bold',italic='TNR-Italic',boldItalic='TNR-BoldItalic')
pdfmetrics.registerFont(TTFont('Calibri','/Applications/Microsoft Word.app/Contents/Resources/DFonts/Calibri.ttf'))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body',fontName='TNR',fontSize=12,leading=20.7,spaceAfter=8,textColor=HexColor('#000000'),alignment=TA_JUSTIFY))
styles.add(ParagraphStyle(name='SmallCell',fontName='TNR',fontSize=12,leading=20.7,textColor=HexColor('#171717')))
styles.add(ParagraphStyle(name='HeadCell',parent=styles['SmallCell'],textColor=HexColor('#101828')))
for name in ['Heading1','Heading2']:
    styles[name].fontName='TNR-BoldItalic';styles[name].fontSize=12;styles[name].leading=20.7;styles[name].textColor=HexColor('#000000');styles[name].spaceAfter=8;styles[name].spaceBefore=8;styles[name].keepWithNext=True

def markup(text):
    text=html.escape(text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',text)
    text=re.sub(r'`(.+?)`',r'<font name="TNR">\1</font>',text)
    return text

def footer(c,doc):
    c.saveState();w,h=A4
    c.setFont('Calibri',11.04);c.setFillColor(HexColor('#000000'))
    c.drawCentredString(w/2,51,str(doc.page+1));c.restoreState()

out=BASE/'output/pdf/kabooki-micheal-portfolio.pdf';out.parent.mkdir(parents=True,exist_ok=True)
width=A4[0]-144
story=[];page_index=[]
for index,page in enumerate((BASE/'docs/portfolio.md').read_text().split('[PAGE]')):
    if index==0:continue
    if story and (page.lstrip().startswith('# Appendix A') or page.lstrip().startswith('# A1 | Board memo')):story.append(PageBreak())
    lines=page.strip().splitlines();i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                vals=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[-: ]+',v or '-') for v in vals):rows.append(vals)
                i+=1
            cols=len(rows[0]);weights=[max(8,sum(len(r[j]) for r in rows)/len(rows)) for j in range(cols)]
            # Avoid tiny key columns and overly wide descriptions.
            weights=[max(16,min(v,65)) for v in weights]; widths=[width*v/sum(weights) for v in weights]
            data=[[Paragraph(markup(v),styles['HeadCell' if n==0 else 'SmallCell']) for v in row] for n,row in enumerate(rows)]
            t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5.4),('RIGHTPADDING',(0,0),(-1,-1),5.4),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),('GRID',(0,0),(-1,-1),.5,HexColor('#000000'))]))
            story.extend([t,Spacer(1,10)]);continue
        if line.startswith('!['):
            path=re.search(r'\((.*?)\)',line).group(1);im=Image(str(BASE/path));scale=min(width/im.imageWidth,(280 if "etl.png" in path else 430)/im.imageHeight)
            im.drawWidth=im.imageWidth*scale;im.drawHeight=im.imageHeight*scale;story.extend([im,Spacer(1,12)]);i+=1;continue
        if line.startswith('# '):
            if 'CFO memo' in line or 'Memo to the CFO' in line or line.startswith('# B1 | Architecture'):story.append(PageBreak())
            story.append(Paragraph(markup(line[2:]),styles['Heading1']));i+=1;continue
        if line.startswith('## '):story.append(Paragraph(markup(line[3:]),styles['Heading2']));i+=1;continue
        if line.startswith('- '):story.append(Paragraph(markup(line[2:]),styles['Body'],bulletText='-'));i+=1;continue
        block=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','![','- ')):
            block.append(lines[i].strip());i+=1
        story.append(Paragraph(markup(' '.join(block)),styles['Body']))
SimpleDocTemplate(str(out),pagesize=A4,rightMargin=72,leftMargin=72,topMargin=72,bottomMargin=72,title='Savanna Retail Group - Kabooki Micheal',author='KABOOKI MICHEAL',allowSplitting=1).build(story,onFirstPage=footer,onLaterPages=footer)
from pypdf import PdfReader,PdfWriter
writer=PdfWriter();writer.append(str(BASE/'docs/cover/cover.pdf'));writer.append(str(out))
with out.open('wb') as f:writer.write(f)
print(out)
