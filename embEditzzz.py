import tkinter as tk
from tkinter import Listbox, Text, Button, Frame
import openai
import chromadb
from chromadb.config import Settings
from embOpenAIService import MyEmbedding

my_embedding = openai.Embedding()


client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                  persist_directory="./dbChroma",
                                  ))

all_collections = [collection.name for collection in client.list_collections()]


    
def load_collection():
    selected_collection = collections_listbox.get(collections_listbox.curselection())
    collection = client.get_collection(name=selected_collection,
                                   embedding_function=my_embedding
                                   )
    ids = collection.get()['ids']
    for id in ids:
        listbox.insert(tk.END, id)
    documents = collection.get()['documents']


def show_document():
    pass
    # Obtiene el índice del elemento seleccionado
    # index = listbox.curselection()[0]
    # # Obtiene el documento correspondiente al ID seleccionado
    # document = documents[index]
    # print(document)
    # text_widget.config(state='normal') 
    # # Limpia el contenido actual del widget de texto y muestra el nuevo documento
    # text_widget.delete('1.0', tk.END)
    # # text_widget.insert(tk.END, document)
    # text_widget.config(state='disabled')
    
def delete_item():
    pass
    # # Obtiene el índice del elemento seleccionado
    # index = listbox.curselection()[0]
    # # Elimina el elemento seleccionado de la base de datos y de las listas
    
    # # collection.delete(ids[index])
    # # ids.pop(index)
    # # documents.pop(index)

    # # Actualiza la Listbox
    # listbox.delete(index)

def add_item():
    pass
    # # Define el nuevo ID y el documento
    # new_document = lower_text_widget.get('1.0', 'end-1c')
    # new_id = new_document[:20]
    
    # embedding, p_token, t_token = my_embedding.get_embedding(text=new_document)

    # collection.add(ids=[new_id], documents=[new_document], embeddings=[embedding])
    # print(embedding)
    # print('-----------')
    # print(p_token)
    # print('-----------')
    # print(t_token)
    # print('-----------')
    # ids.append(new_id)
    # documents.append(new_document)

    # # Actualiza la Listbox
    # listbox.insert(tk.END, new_id)
    # lower_text_widget.delete('1.0', 'end')

# Creación de la ventana de Tkinter
ventana_edit = tk.Tk()
ventana_edit.title("Edit Embeddings")
ventana_edit.geometry("800x600")
ventana_edit.iconbitmap("logoIP40.ico")

# ==== COLECCIONES
collections_frame = Frame(ventana_edit)
collections_frame.pack(side=tk.LEFT, padx=10, pady=10)

collections_listbox = Listbox(collections_frame)
collections_listbox.pack(fill=tk.BOTH, expand=True)

for collection_name in all_collections:
    collections_listbox.insert(tk.END, collection_name)

update_button = Button(collections_frame, text="Actualizar", command=load_collection)
update_button.pack(pady=10)
# ==== FIN COLECCIONES



content_frame = Frame(ventana_edit)
content_frame.pack(padx=10, pady=10)  

# Creación de un widget Listbox
listbox = Listbox(content_frame)
listbox.grid(row=0, column=0, sticky='nsew', padx=(0,15))

delete_button = Button(content_frame, text="Eliminar", command=delete_item)
delete_button.grid(row=1, column=0, sticky='w', padx=5, pady=5) 

lower_text_widget = Text(ventana_edit, height=5)
lower_text_widget.pack(fill='both', expand=True, padx=15)

# Creación de un widget Text
text_widget = Text(content_frame)
text_widget.grid(row=0, column=1, sticky='nsew')
text_widget.config(state='disabled')

add_button = Button(ventana_edit, text="Agregar", command=add_item)
add_button.pack(side=tk.LEFT, padx=5, pady=5)  
    
# Vincula el evento de clic del mouse al manejador de eventos
listbox.bind('<<ListboxSelect>>', show_document)

# Comenzar el bucle principal de la ventana
ventana_edit.mainloop()
