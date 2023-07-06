import tkinter as tk
from tkinter import filedialog, messagebox
import csv
from embOpenAI import MyEmbedding

my_embedding = MyEmbedding("serprolim_collection")

def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if archivo:
        try:
            with open(archivo, 'r') as csv_file:
                lector_csv = csv.reader(csv_file)
                datos = list(lector_csv)
                lista.delete(0, tk.END)
                for fila in datos:
                    fila_formateada = [str(elemento) for elemento in fila]
                    lista.insert(tk.END, " ".join(fila_formateada))
        except IOError as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

def mostrar_contenido(event):
    seleccionado = lista.curselection()
    if seleccionado:
        contenido = lista.get(seleccionado)
        marco_texto_seleccionado.delete('1.0', tk.END)
        contenido_sin_llaves = f"{contenido}".replace('[', '').replace(']', '')
        marco_texto_seleccionado.insert(tk.END, contenido_sin_llaves)

def actualizar_elemento():
    seleccionado = lista.curselection()
    if seleccionado:
        nuevo_contenido = marco_texto_seleccionado.get('1.0', tk.END).strip()
        lista.delete(seleccionado)
        lista.insert(seleccionado, nuevo_contenido)

def agregar_elemento():
    nuevo_elemento = entrada_nuevo_elemento.get("1.0", tk.END).strip()
    if nuevo_elemento:  # verifica que la entrada no esté vacía
        lista.insert(tk.END, nuevo_elemento)
        entrada_nuevo_elemento.delete("1.0", tk.END) # limpia  para el próximo uso

def borrar_elemento():
    seleccionado = lista.curselection()
    if seleccionado:
        index = seleccionado[0]
        lista.delete(index)

def funcion_embedding():
    seleccionados = lista.get(0, tk.END)
    my_embedding.create_db(seleccionados)
    messagebox.showinfo("Información", "Embedding finalizado con éxito")


def guardar_archivo():
    archivo = filedialog.asksaveasfilename(defaultextension=".csv", 
                                           filetypes=[("Archivos CSV", "*.csv")])
    if archivo:
        try:
            with open(archivo, 'w', newline='') as csv_file:
                escritor_csv = csv.writer(csv_file)
                for elemento in lista.get(0, tk.END):
                    escritor_csv.writerow(elemento.split())
        except IOError as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

def create_menu():
    menubar = tk.Menu(ventana)
    ventana.config(menu=menubar)

    archivo_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Archivo", menu=archivo_menu)
    archivo_menu.add_command(label="Cargar archivo", command=cargar_archivo)
    archivo_menu.add_command(label="Guardar archivo", command=guardar_archivo)

def create_left_frame():
    marco_izq = tk.Frame(ventana)
    marco_izq.pack(pady=10, padx=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

    label_lista = tk.Label(marco_izq, width=30, text="Lista de textos")
    label_lista.pack()

    lista = tk.Listbox(marco_izq)
    lista.pack(fill=tk.BOTH, expand=True)

    btn_borrar = tk.Button(marco_izq, text="Borrar elemento", command=borrar_elemento)
    btn_borrar.pack(pady=10)

    return lista

def create_right_frame():
    marco_der = tk.Frame(ventana)
    marco_der.pack(pady=10, padx=10, side=tk.RIGHT, fill=tk.X, expand=True)

    label_titulo = tk.Label(marco_der, text="Texto seleccionado")
    label_titulo.pack()

    marco_texto_seleccionado = tk.Text(marco_der, 
                                       height=10, 
                                       relief=tk.SOLID, 
                                       borderwidth=1)
    marco_texto_seleccionado.pack()

    btn_actualizar = tk.Button(marco_der, 
                               text="Actualizar texto", 
                               command=actualizar_elemento)
    btn_actualizar.pack(pady=10, anchor=tk.E)

    label_titulo = tk.Label(marco_der, text="Texto nuevo")
    label_titulo.pack()

    entrada_nuevo_elemento = tk.Text(marco_der, 
                                     height=10, 
                                     relief=tk.SOLID, 
                                     borderwidth=1)
    entrada_nuevo_elemento.pack()

    btn_agregar = tk.Button(marco_der, 
                            text="Agregar texto", 
                            command=agregar_elemento)
    btn_agregar.pack(pady=10, anchor=tk.E)

    btn_embedding = tk.Button(marco_der, 
                              text="Realizar Embedding", 
                              command=funcion_embedding, 
                              width=20, 
                              height=2)
    btn_embedding.pack(pady=30, side=tk.BOTTOM)

    return marco_texto_seleccionado, entrada_nuevo_elemento

ventana = tk.Tk()
ventana.title("Embeddings CSV")
ventana.geometry("600x600")
ventana.iconbitmap("logoIP40.ico")



create_menu()
lista = create_left_frame()

marco_texto_seleccionado, entrada_nuevo_elemento = create_right_frame()

lista.bind('<<ListboxSelect>>', mostrar_contenido)

ventana.mainloop()



