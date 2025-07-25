#    MTUOC-PCorpus-rescorer
#    Copyright (C) 2024 Antoni Oliver
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
from sentence_transformers import SentenceTransformer, util


def process(sources, targets, scores, sortida):
    data = []
    embeddings1 = model.encode(sources, convert_to_tensor=False)
    embeddings2 = model.encode(targets, convert_to_tensor=False)
    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    for i in range(len(sources)):
        try:
            source = sources[i]
            target = targets[i]
            score = float(scores[i]) if scores[i] != 0 else 0.0
            cosine_score = cosine_scores[i][i].item()
            
            # Language detection predictions
            DL1 = modelFT.predict(source, k=5)
            DL2 = modelFT.predict(target, k=5)
            
            # Validate DL1 and DL2 have enough predictions
            if len(DL1[0]) < 1 or len(DL2[0]) < 1:
                print(f"WARNING: Insufficient labels for line {i}")
                continue
            
            predL1 = []
            for j in range(len(DL1)-1):
                L1 = DL1[0][j].replace("__label__", "")
                confL1 = float(DL1[1][j])
                predL1.append(f"{L1}:{confL1}")
            predL1 = ";".join(predL1)

            predL2 = []
            for j in range(len(DL2)-1):
                L2 = DL2[0][j].replace("__label__", "")
                confL2 = float(DL2[1][j])
                predL2.append(f"{L2}:{confL2}")
            predL2 = ";".join(predL2)

            # Write the output line
            cadena = f"{source}\t{target}\t{predL1}\t{predL2}\t{cosine_score}"
            sortida.write(cadena + "\n")

        except Exception as e:
            print(f"ERROR processing line {i}: {e}")




    

parser = argparse.ArgumentParser(description='MTUOC-PCorpus-rescorer: a script to score parallel corpora. The parallel corpus file should be a TSV file with source segment, target segment and, optionally, a score. It creates a text file that should be used with the companion program MTUOC-PCorpus-selector-txt.')
parser.add_argument("-i","--input", type=str, help="The input parallel corpus file.", required=True)
parser.add_argument("-o","--output", type=str, help="The output file with the data.", required=True)
parser.add_argument("-SEmodel",type=str, help="The SentenceTransformer model. Default model: LaBSE", required=False, default="LaBSE")
parser.add_argument("-LDmodel",type=str, help="The fasttext language detection model. Default model: lid.176.bin", required=False, default="lid.176.bin")
maxlines=10000
args = parser.parse_args()

fentrada=args.input
fsortida=args.output
SEmodel=args.SEmodel
LDmodel=args.LDmodel

#Available languages lid.176.bin fasttext model: af als am an ar arz as ast av az azb ba bar bcl be bg bh bn bo bpy br bs bxr ca cbk ce ceb ckb co cs cv cy da de diq dsb dty dv el eml en eo es et eu fa fi fr frr fy ga gd gl gn gom gu gv he hi hif hr hsb ht hu hy ia id ie ilo io is it ja jbo jv ka kk km kn ko krc ku kv kw ky la lb lez li lmo lo lrc lt lv mai mg mhr min mk ml mn mr mrj ms mt mwl my myv mzn nah nap nds ne new nl nn no oc or os pa pam pfl pl pms pnb ps pt qu rm ro ru rue sa sah sc scn sco sd sh si sk sl so sq sr su sv sw ta te tg th tk tl tr tt tyv ug uk ur uz vec vep vi vls vo wa war wuu xal xmf yi yo yue zh


modelFT = fasttext.load_model(LDmodel)
model = SentenceTransformer(SEmodel, device="cpu")




entrada=codecs.open(fentrada,"r",encoding="utf-8")
sortida=codecs.open(fsortida,"w",encoding="utf-8")


cont=0
sources=[]
targets=[]
scores=[]


cont=0
cont2=1



for linia in entrada:
    linia=linia.rstrip()
    camps=linia.split("\t")
    try:
        sources.append(camps[0])
        targets.append(camps[1])
        if len(camps)>=3:
            scores.append(camps[2])
        else:
            scores.append(0)
    except:
        pass
    cont+=1
    if cont%maxlines==0:
        print("CONT: ",cont2*maxlines)
        cont2+=1
    if cont==maxlines:
        process(sources,targets,scores,sortida)
        cont=0
        sources=[]
        targets=[]
        scores=[]
process(sources,targets,scores,sortida)
    

    

        


