#    MTUOC-PCorpus-selector
#    Copyright (C) 2024  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import codecs
import sys
import argparse

parser = argparse.ArgumentParser(description='MTUOC-PCorpus-selector: a script to select parallel segments from a rescorer database created with MTUOC_PCorpus-rescorer. ')
parser.add_argument("-i","--input", type=str, help="The text file resulting from MTUOC-PCorpus-rescorer.py.", required=True)
parser.add_argument("--sl", help="The source language code.", required=True)
parser.add_argument("--sldc", type=float, help="The minimum source language detection confidence.", required=True)
parser.add_argument("--tl", help="The target language code.", required=True)
parser.add_argument("--tldc", type=float, help="The minimum target language detection confidence.", required=True)
parser.add_argument("-m","--minSBERT", type=float, help="The minimum value for SBERT score.", required=False)
parser.add_argument("-o","--outfile", type=str, help="The output file containing the parallel corpus.", required=True)

args = parser.parse_args()
inputfile=args.input
print(inputfile)
sl=args.sl
tl=args.tl
sldc=float(args.sldc)
tldc=float(args.tldc)
minSBERT=args.minSBERT
if minSBERT==None:
    minSBERT=-1000000
else:
    minSBERT=float(minSBERT)
outfile=args.outfile

sortida=codecs.open(outfile,"w",encoding="utf-8")

entrada=codecs.open(inputfile,"r",encoding="utf-8")

for linia in entrada:
    linia=linia.rstrip()
    camps=linia.split("\t")
    slsegment=camps[0]
    tlsegment=camps[1]
    slinfolangs=camps[2]
    slinfolang1=slinfolangs.split(";")[0]
    sllang=slinfolang1.split(":")[0]
    slconf=float(slinfolang1.split(":")[1])
    
    tlinfolangs=camps[3]
    tlinfolang1=tlinfolangs.split(";")[0]
    tllang=tlinfolang1.split(":")[0]
    tlconf=float(tlinfolang1.split(":")[1])
    
    sbert=float(camps[4])
    
    if sllang==sl and slconf>=sldc and tllang==tl and tlconf>=tldc and sbert>=minSBERT:
        cadena=slsegment+"\t"+tlsegment
        #print(cadena)
        sortida.write(cadena+"\n")
