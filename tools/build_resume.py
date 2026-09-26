"""Generate the public résumé from the same verified career source as the website."""
from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
r=Path(__file__).resolve().parents[1];c=json.loads((r/'content/career.json').read_text())
ink=HexColor('#1d3029');muted=HexColor('#53605a');line=HexColor('#bdc9c0')
def txt(s):return escape(s.replace('–','-').replace('—','-').replace('’',"'").replace('·','|'))
styles={
 'name':ParagraphStyle('name',fontName='Helvetica-Bold',fontSize=25,leading=29,textColor=ink),
 'headline':ParagraphStyle('headline',fontName='Helvetica',fontSize=11,leading=15,textColor=muted),
 'contact':ParagraphStyle('contact',fontName='Helvetica',fontSize=9,leading=13,textColor=muted),
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=9.6,leading=13.3,textColor=ink),
 'section':ParagraphStyle('section',fontName='Helvetica-Bold',fontSize=9,leading=13,textColor=ink,spaceBefore=12,spaceAfter=7),
 'company':ParagraphStyle('company',fontName='Helvetica-Bold',fontSize=11,leading=15,textColor=ink),
 'date':ParagraphStyle('date',fontName='Helvetica',fontSize=9,leading=15,textColor=muted,alignment=2),
 'role':ParagraphStyle('role',fontName='Helvetica-Bold',fontSize=9.5,leading=13,textColor=muted,spaceBefore=2,spaceAfter=3),
 'bullet':ParagraphStyle('bullet',fontName='Helvetica',fontSize=9.4,leading=13.0,textColor=ink,leftIndent=10,firstLineIndent=-8,spaceAfter=3),
}
def p(s,style='body'):return Paragraph(txt(s),styles[style])
def heading(left,right):
 t=Table([[p(left,'company'),p(right,'date')]],colWidths=[345,183]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]));return t
story=[p(c['name'].upper(),'name'),p(c['headline'],'headline'),Spacer(1,7),Paragraph('baylor@manifoldengineering.ai  |  <link href="https://baylor-harrison.com">baylor-harrison.com</link><br/><link href="https://www.linkedin.com/in/baylor-harrison/">linkedin.com/in/baylor-harrison</link>  |  <link href="https://github.com/BaylorH">github.com/BaylorH</link>',styles['contact']),Spacer(1,10),p(c['summary']),p('EXPERIENCE','section')]
for x in c['experience']:
 roles=x.get('roles',[x]);story.append(KeepTogether([heading(x['company'],x['period']),p(roles[0]['role']+(' | '+roles[0]['period'] if 'roles' in x else ''),'role'),p('- '+roles[0]['bullets'][0],'bullet')]))
 for v in roles:
  if v!=roles[0]:story.append(p(v['role']+' | '+v['period'],'role'))
  for item in (v['bullets'][1:] if v==roles[0] else v['bullets']):story.append(p('- '+item,'bullet'))
 story.append(Spacer(1,7))
story+=[p('EDUCATION','section'),heading('Arizona State University','2021 - 2025'),p('Bachelor of Science in Computer Science | Graduated May 2025'),p('Dean\'s List | Merit scholarship recipient','contact'),p('TECHNICAL FOCUS','section')]
for title,detail in c['skills']:story.append(Paragraph('<b>'+txt(title)+':</b> '+txt(detail),styles['body']))
def footer(canvas,doc):
 canvas.setStrokeColor(line);canvas.line(42,32,570,32);canvas.setFillColor(muted);canvas.setFont('Helvetica',8);canvas.drawString(42,20,'Baylor Harrison | '+c['updated']);canvas.drawRightString(570,20,str(doc.page))
doc=SimpleDocTemplate(str(r/'files/Baylor-Harrison-Resume.pdf'),pagesize=(612,792),leftMargin=42,rightMargin=42,topMargin=36,bottomMargin=42,title='Baylor Harrison - AI & Software Engineer',author='Baylor Harrison',subject='Professional resume - September 2026')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('Updated public résumé')
