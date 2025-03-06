import codecs
import os
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox

def select_segments(inputfile, outfile, sl, sldc, tl, tldc, minSBERT):
    if not os.path.isfile(inputfile):
        raise FileNotFoundError(f"El fitxer {inputfile} no existeix.")

    with codecs.open(inputfile, "r", encoding="utf-8") as entrada, \
         codecs.open(outfile, "w", encoding="utf-8") as sortida:
        
        for linia in entrada:
            linia = linia.rstrip()
            camps = linia.split("\t")

            slsegment = camps[0]
            tlsegment = camps[1]

            slinfolangs = camps[2]
            slinfolang1 = slinfolangs.split(";")[0]
            sllang = slinfolang1.split(":")[0]
            slconf = float(slinfolang1.split(":")[1])

            tlinfolangs = camps[3]
            tlinfolang1 = tlinfolangs.split(";")[0]
            tllang = tlinfolang1.split(":")[0]
            tlconf = float(tlinfolang1.split(":")[1])

            sbert = float(camps[4])

            if sllang == sl and slconf >= sldc and tllang == tl and tlconf >= tldc and sbert >= minSBERT:
                cadena = slsegment + "\t" + tlsegment
                sortida.write(cadena + "\n")

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
        sl = sl_entry.get()
        tl = tl_entry.get()
        try:
            sldc = float(sldc_entry.get())
            tldc = float(tldc_entry.get())
            min_sbert = float(min_sbert_entry.get()) if min_sbert_entry.get() else -1000000
        except ValueError:
            messagebox.showerror("Error", "Els valors de confiança han de ser números.")
            return

        try:
            select_segments(input_file, output_file, sl, sldc, tl, tldc, min_sbert)
            messagebox.showinfo("Completat", "Processament finalitzat amb èxit!")
        except Exception as e:
            messagebox.showerror("Error", f"S'ha produït un error: {e}")

    root = Tk()
    root.title("MTUOC-PCorpus-selector-txt GUI")

    Label(root, text="Input file:").grid(row=0, column=0, sticky="w")
    input_file_entry = Entry(root, width=50)
    input_file_entry.grid(row=0, column=1)
    Button(root, text="Select file", command=select_input_file).grid(row=0, column=2)

    Label(root, text="Output file:").grid(row=1, column=0, sticky="w")
    output_file_entry = Entry(root, width=50)
    output_file_entry.grid(row=1, column=1)
    Button(root, text="Select file", command=select_output_file).grid(row=1, column=2)

    Label(root, text="SL code:").grid(row=2, column=0, sticky="w")
    sl_entry = Entry(root, width=50)
    sl_entry.grid(row=2, column=1)

    Label(root, text="SL min. confidence:").grid(row=3, column=0, sticky="w")
    sldc_entry = Entry(root, width=50)
    sldc_entry.grid(row=3, column=1)

    Label(root, text="TL code:").grid(row=4, column=0, sticky="w")
    tl_entry = Entry(root, width=50)
    tl_entry.grid(row=4, column=1)

    Label(root, text="TL min. confidence:").grid(row=5, column=0, sticky="w")
    tldc_entry = Entry(root, width=50)
    tldc_entry.grid(row=5, column=1)

    Label(root, text="SBERT min. confidence:").grid(row=6, column=0, sticky="w")
    min_sbert_entry = Entry(root, width=50)
    min_sbert_entry.grid(row=6, column=1)

    Button(root, text="Go!", command=start).grid(row=7, column=1)

    root.mainloop()

if __name__ == "__main__":
    main()
