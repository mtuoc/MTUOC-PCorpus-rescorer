#    MTUOC-MonoCorpus-selector
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

parser = argparse.ArgumentParser(description='MTUOC-PCorpus-selector: a script to select parallel segments from a rescorer text file created with MTUOC_PCorpus-rescorer-txt. ')
parser.add_argument("-i","--input", type=str, help="The text file resulting from MTUOC-PCorpus-rescorer.py.", required=True)
parser.add_argument("-l", help="The language code.", required=True)
parser.add_argument("--ldc", type=float, help="The minimum source language detection confidence.", required=True)

parser.add_argument("-o","--outfile", type=str, help="The output file containing the parallel corpus.", required=True)

args = parser.parse_args()
inputfile=args.input
print(inputfile)
l=args.l
ldc=float(args.ldc)
outfile=args.outfile

sortida=codecs.open(outfile,"w",encoding="utf-8")

entrada=codecs.open(inputfile,"r",encoding="utf-8")

for linia in entrada:
    try:
        linia=linia.rstrip()
        camps=linia.split("\t")
        segment=camps[0]    
        sinfolangs=camps[1]  
        
        slang=sinfolangs.split(":")[0]
        sconf=float(sinfolangs.split(":")[1])
        
        if slang==l and sconf>=ldc:
            cadena=segment
            #print(cadena)
            sortida.write(cadena+"\n")
    except:
        pass
