from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from pypdf import PdfReader
p=next(Path('output/reports').glob('*.docx'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(p) as z:
 root=E.fromstring(z.read('word/document.xml'))
 for r in root.xpath('//w:body/w:p/w:r[w:t]',namespaces=ns):
  fonts=r.find('w:rPr/w:rFonts',ns);size=r.find('w:rPr/w:sz',ns)
  assert fonts.get('{'+ns['w']+'}eastAsia')=='宋体'
  assert fonts.get('{'+ns['w']+'}ascii')=='Times New Roman'
  assert size.get('{'+ns['w']+'}val')=='24'
 styles=E.fromstring(z.read('word/styles.xml'))
 assert not styles.xpath('//w:pBdr',namespaces=ns)
 for sty in ['Normal','Title','Heading1']:
  st=styles.xpath('//w:style[@w:styleId="'+sty+'"]',namespaces=ns)[0]
  spacing=st.find('w:pPr/w:spacing',ns)
  assert spacing.get('{'+ns['w']+'}line')=='288'
 pdf=PdfReader(p.with_suffix('.pdf'))
 assert len(pdf.pages)==4
 for page in pdf.pages:
  assert abs(float(page.mediabox.width)-595.28)<1
  assert abs(float(page.mediabox.height)-841.89)<1
 print('PASS: 4 A4 pages, SimSun/Times New Roman, 12pt, 1.2 spacing, no decorative borders')
 print('PDF sizes:',[(round(float(x.mediabox.width),2),round(float(x.mediabox.height),2)) for x in pdf.pages])
