import os
import codecs
import fasttext
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
from sentence_transformers import SentenceTransformer, util

def process(sources, targets, scores, sortida, model, modelFT):
    embeddings1 = model.encode(sources, convert_to_tensor=False)
    embeddings2 = model.encode(targets, convert_to_tensor=False)
    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    for i in range(len(sources)):
        try:
            source = sources[i]
            target = targets[i]
            score = float(scores[i]) if scores[i] != 0 else 0.0
            cosine_score = cosine_scores[i][i].item()

            DL1 = modelFT.predict(source, k=5)
            DL2 = modelFT.predict(target, k=5)

            predL1 = [f"{DL1[0][j].replace('__label__', '')}:{float(DL1[1][j])}" for j in range(len(DL1[0]))]
            predL2 = [f"{DL2[0][j].replace('__label__', '')}:{float(DL2[1][j])}" for j in range(len(DL2[0]))]

            predL1 = ";".join(predL1)
            predL2 = ";".join(predL2)

            cadena = f"{source}\t{target}\t{predL1}\t{predL2}\t{cosine_score}"
            print(cadena)
            sortida.write(cadena + "\n")
        except Exception as e:
            print(f"ERROR processing line {i}: {e}")


def start_processing(input_file, output_file, se_model, ld_model):
    if not os.path.isfile(input_file):
        raise FileNotFoundError("El fitxer d'entrada no existeix.")

    model = SentenceTransformer(se_model)
    modelFT = fasttext.load_model(ld_model)

    maxlines = 1000
    sources, targets, scores = [], [], []

    with codecs.open(input_file, "r", encoding="utf-8") as entrada, \
         codecs.open(output_file, "w", encoding="utf-8") as sortida:

        cont = 0
        for linia in entrada:
            linia = linia.rstrip()
            camps = linia.split("\t")
            try:
                sources.append(camps[0])
                targets.append(camps[1])
                scores.append(camps[2] if len(camps) >= 3 else 0)
            except:
                pass

            cont += 1
            if cont % maxlines == 0:
                process(sources, targets, scores, sortida, model, modelFT)
                sources, targets, scores = [], [], []

        process(sources, targets, scores, sortida, model, modelFT)

# GUI amb Tkinter
def main():
    def select_input_file():
        filename = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        input_file_entry.delete(0, "end")
        input_file_entry.insert(0, filename)

    def select_output_file():
        filename = filedialog.asksaveasfilename(filetypes=[("All files", "*.*")], defaultextension=".tsv")
        output_file_entry.delete(0, "end")
        output_file_entry.insert(0, filename)

    def start():
        input_file = input_file_entry.get()
        output_file = output_file_entry.get()
        se_model = se_model_entry.get()
        ld_model = ld_model_entry.get()

        try:
            start_processing(input_file, output_file, se_model, ld_model)
            messagebox.showinfo("Completat", "Processament finalitzat amb èxit!")
        except Exception as e:
            messagebox.showerror("Error", f"S'ha produït un error: {e}")

    root = Tk()
    root.title("MTUOC-PCorpus-rescorer GUI")

    Label(root, text="Input file:").grid(row=0, column=0, sticky="w")
    input_file_entry = Entry(root, width=50)
    input_file_entry.grid(row=0, column=1)
    Button(root, text="Select file", command=select_input_file).grid(row=0, column=2)

    Label(root, text="Output file:").grid(row=1, column=0, sticky="w")
    output_file_entry = Entry(root, width=50)
    output_file_entry.grid(row=1, column=1)
    Button(root, text="Select file", command=select_output_file).grid(row=1, column=2)

    Label(root, text="SentenceTransformer model:").grid(row=2, column=0, sticky="w")
    se_model_entry = Entry(root, width=50)
    se_model_entry.insert(0, "LaBSE")
    se_model_entry.grid(row=2, column=1)

    Label(root, text="FastText model:").grid(row=3, column=0, sticky="w")
    ld_model_entry = Entry(root, width=50)
    ld_model_entry.insert(0, "lid.176.bin")
    ld_model_entry.grid(row=3, column=1)

    Button(root, text="Go!", command=start).grid(row=4, column=1)

    root.mainloop()

if __name__ == "__main__":
    main()