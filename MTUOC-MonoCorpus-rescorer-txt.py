#    MTUOC-MonoCorpus-rescorer
#    Copyright (C) 2025 Antoni Oliver
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

import sys
import os
import codecs
import argparse
import fasttext


   

parser = argparse.ArgumentParser(description='MTUOC-PCorpus-rescorer: a script to score parallel corpora. The parallel corpus file should be a TSV file with source segment, target segment and, optionally, a score. It creates a text file that should be used with the companion program MTUOC-PCorpus-selector-txt.')
parser.add_argument("-i","--input", type=str, help="The input parallel corpus file.", required=True)
parser.add_argument("-o","--output", type=str, help="The output file with the data.", required=True)
parser.add_argument("-LDmodel",type=str, help="The fasttext language detection model. Default model: lid.176.bin", required=False, default="lid.176.bin")
maxlines=10000
args = parser.parse_args()

fentrada=args.input
fsortida=args.output
LDmodel=args.LDmodel

#Available languages lid.176.bin fasttext model: af als am an ar arz as ast av az azb ba bar bcl be bg bh bn bo bpy br bs bxr ca cbk ce ceb ckb co cs cv cy da de diq dsb dty dv el eml en eo es et eu fa fi fr frr fy ga gd gl gn gom gu gv he hi hif hr hsb ht hu hy ia id ie ilo io is it ja jbo jv ka kk km kn ko krc ku kv kw ky la lb lez li lmo lo lrc lt lv mai mg mhr min mk ml mn mr mrj ms mt mwl my myv mzn nah nap nds ne new nl nn no oc or os pa pam pfl pl pms pnb ps pt qu rm ro ru rue sa sah sc scn sco sd sh si sk sl so sq sr su sv sw ta te tg th tk tl tr tt tyv ug uk ur uz vec vep vi vls vo wa war wuu xal xmf yi yo yue zh


modelFT = fasttext.load_model(LDmodel)




entrada=codecs.open(fentrada,"r",encoding="utf-8")
sortida=codecs.open(fsortida,"w",encoding="utf-8")


cont=0
sources=[]
targets=[]
scores=[]


for linia in entrada:
    linia=linia.rstrip()
    DL = modelFT.predict(linia, k=5)
    predL = []
    for j in range(len(DL)-1):
        L = DL[0][j].replace("__label__", "")
        confL = float(DL[1][j])
        predL.append(f"{L}:{confL}")
    predL = ";".join(predL)
    cadena = f"{linia}\t{predL}"
    sortida.write(cadena + "\n")

    

        


