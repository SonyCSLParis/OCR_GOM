from pdf2image import convert_from_path
import os
import glob
import time

def convert_pdf(f, svg_folder=""):
      pages = convert_from_path(f)
      svg = f[:-3]   

      print(svg)  

      if not(os.path.exists(svg)): os.mkdir(svg)   

      i = 0
      for page in pages:
         image_name = svg+"/%04d.jpg"%i  
         page.save(image_name, "JPEG")
         i = i+1 
      print("Saved %s pages"%i)


def convert_folder(folder):
   files=glob.glob(folder+"/*")
   files.sort()   

   for f in files:
      convert_pdf(f)

#folder = "/home/kodda/Dropbox/p2pflab/data/guides_maraichage_19eme_siecle/corpus_pdf/from_bec_hellouin/"

t0 = time.time()
f = "data/Ma_Pratique_de_la_culture_[...]Curé_Jules_bpt6k9106288z.pdf"
convert_pdf(f, svg_folder="data/")
print(time.time() -t0)
