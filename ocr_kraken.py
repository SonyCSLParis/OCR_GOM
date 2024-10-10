import subprocess
import glob
import os
import time
from alto import parse_file
import xml.etree.ElementTree as ET
import re
import sys
import io
import codecs



def ocr_page(f, xml_folder, txt_folder):
   out_alto  = xml_folder + f.split('/')[-1].strip('.jpg') 
   out_txt  = txt_folder + f.split('/')[-1].strip('.jpg') 
   subprocess.run(["kraken","-a","-d", "cuda:1", "-i", f, out_alto, "segment", "-bl", "ocr", "-m", "catmus-print-fondue-large.mlmodel"])
   subprocess.run(["kraken","-d", "cuda:1", "-i", f, out_txt, "segment", "-bl", "ocr", "-m", "catmus-print-fondue-large.mlmodel"])

def ocr_book(folder, xml_folder, txt_folder):
    fs = glob.glob(folder+"/*")
    fs.sort()
    print(fs[0])
    for f in fs:
       ocr_page(f, xml_folder, txt_folder)

def ocr_books():       
   t0 = time.time()    
    
   IMG_PATH = "/mnt/diskSustainability/david/GOM_corpus/corpus_img/"
   XML_PATH = "/mnt/diskSustainability/david/GOM_corpus/corpus_xml/"
   TXT_PATH = "/mnt/diskSustainability/david/GOM_corpus/corpus_txt/"

   folders = glob.glob(IMG_PATH+"*")

   for folder in folders:
      bname = folder.split('/')[-1]
      xml_folder = XML_PATH + bname
      txt_folder = TXT_PATH + bname
      #os.mkdir(xml_folder)
      #os.mkdir(txt_folder)
      ocr_book(folder, xml_folder, txt_folder)

   print("It took ", time.time()-t0)

def make_text_file(folder):
   fps=glob.glob(folder)
   fps.sort()

   res = ""

   for fp in fps:
      with open(fp) as f:
         res+="\n\r\n"+f.read()

   res=res.replace("\n", " ")
   res=res.replace("¬ ", "")
   print(res)

def get_linewidth(xml, xmlns):
   ws = []
   for l in xml.iterfind(".//{%s}TextLine" % xmlns):
      ws.append(int(l.attrib.get('WIDTH')))
   if len(ws): return max(ws)
   else: return 0

   
def alto_text(xml, xmlns, lw = 10):
    """Extract text content from ALTO xml file"""
    # Ensure use of UTF-8
    if isinstance(sys.stdout, io.TextIOWrapper) and sys.stdout.encoding != "UTF-8":
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    page=""
    for i,lines in enumerate(xml.iterfind(".//{%s}TextLine" % xmlns)):
        if ((i>1) or (int(lines.attrib.get('WIDTH'))>.9*lw)):
           text = ""
           for line in lines.findall("{%s}String" % xmlns):
               if "SUBS_CONTENT" not in line.attrib and "SUBS_TYPE" not in line.attrib:
                  text += line.attrib.get("CONTENT") + " "
               else:
                   if "HypPart1" in line.attrib.get("SUBS_TYPE"):
                      text += line.attrib.get("CONTENT")
                   if "HypPart2" in line.attrib.get("SUBS_TYPE"):
                        text += line.attrib.get("CONTENT") + " "            
           page+=text
           if int(lines.attrib.get('WIDTH'))<.98*lw: page+="\n"
    return page
   
def process_page(alto):
   with open(alto, "rb") as f:
      m = re.search('encoding="(.*?)"', f.read(45).decode("utf-8"))
      xml_encoding = m.group(1)
   
   xmlp = ET.XMLParser(encoding=xml_encoding)
   xml = ET.parse(alto, parser=xmlp)
   xmlns = xml.getroot().tag.split("}")[0].strip("{")

   lw = get_linewidth(xml, xmlns)
   return alto_text(xml, xmlns, lw).replace("¬ ", "")

def process_book():
   fs = glob.glob('/mnt/diskSustainability/david/GOM_corpus/corpus_xml/L_école_du_jardin_potager*')
   fs.sort()

   text = ""
   for f in fs[1:]:
      print(f)
      text += process_page(f)

   text = text.replace("\n", " ")
   text = text.replace("  ", " ")

   with open("../L_école_du_jardin_potager.txt","w", encoding="ISO-8859-1") as f:
      f.write(text)

#ocr_books()
#process_book()
