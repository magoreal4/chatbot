import tkinter as tk
from tkinter import Listbox, Text, Button, Frame, messagebox  
import chromadb
from chromadb.config import Settings
from chromaDBService import MyChromaDB
from embOpenAIService import MyEmbedding

class EmbeddingEditor:
    def __init__(self, root):
        self.root = root
        self.my_embedding = MyEmbedding()
        self.chroma_db = MyChromaDB()
        self.client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./dbChroma"))
        self.all_collections = [collection.name for collection in self.client.list_collections()]
        self.documents = []
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Edit Embeddings")
        self.root.geometry("800x600")
        self.root.iconbitmap("logoIP40.ico")

        # Collections
        self.setup_collections_ui()

        # Content
        self.setup_content_ui()

        # Lower Text Widget
        self.lower_text_widget = Text(self.root, height=5)
        self.lower_text_widget.pack(fill='both', expand=True, padx=15)

        # Add Button
        add_button = Button(self.root, text="Agregar", command=self.add_item)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)
            
    def setup_collections_ui(self):
        collections_frame = Frame(self.root)
        collections_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.collections_listbox = Listbox(collections_frame)
        self.collections_listbox.pack(fill=tk.BOTH, expand=True)

        for collection_name in self.all_collections:
            self.collections_listbox.insert(tk.END, collection_name)

        update_button = Button(collections_frame, text="Actualizar", command=self.load_collection)
        update_button.pack(pady=10)

        # Botón para borrar colección
        delete_collection_button = Button(collections_frame, text="Borrar Colección", command=self.delete_collection)
        delete_collection_button.pack(pady=10)

    def delete_collection(self):
        selected_collection = self.collections_listbox.get(self.collections_listbox.curselection())
        # Muestra un cuadro de confirmación
        confirm = messagebox.askyesno("Confirmación", f"¿Estás seguro de que deseas eliminar la colección '{selected_collection}'?")
        
        if confirm:
            self.client.delete_collection(selected_collection)
            
            # Actualizar la lista de colecciones y borra contenidos
            self.update_collections_list()
            self.listbox.delete(0, tk.END)
            self.text_widget.config(state='normal')
            self.text_widget.delete(1.0, tk.END)
        
    def update_collections_list(self):
        self.all_collections = [collection.name for collection in self.client.list_collections()]
        self.collections_listbox.delete(0, tk.END)
        for collection_name in self.all_collections:
            self.collections_listbox.insert(tk.END, collection_name)

    def setup_content_ui(self):
        content_frame = Frame(self.root)
        content_frame.pack(padx=10, pady=10)

        self.listbox = Listbox(content_frame)
        self.listbox.grid(row=0, column=0, sticky='nsew', padx=(0,15))
        self.listbox.bind('<<ListboxSelect>>', self.show_document)

        delete_button = Button(content_frame, text="Eliminar", command=self.delete_item)
        delete_button.grid(row=1, column=0, sticky='w', padx=5, pady=5)

        self.text_widget = Text(content_frame)
        self.text_widget.grid(row=0, column=1, sticky='nsew')
        self.text_widget.config(state='disabled')

    def load_collection(self):
        self.listbox.delete(0, tk.END)
        selected_collection = self.collections_listbox.get(self.collections_listbox.curselection())
        self.collection = self.client.get_collection(name=selected_collection, embedding_function=self.my_embedding)
        self.ids = self.collection.get()['ids']
        for id in self.ids:
            self.listbox.insert(tk.END, id)
        
        self.documents = self.collection.get()['documents']

    def show_document(self, event=None):
        # Obtener el índice del elemento seleccionado
        index = self.listbox.curselection()[0]
        
        # Obtener el documento correspondiente al índice seleccionado
        self.document = self.documents[index]
        
        # Limpiar el widget de texto y mostrar el documento seleccionado
        self.text_widget.config(state='normal')  # Habilitar la edición del widget de texto
        self.text_widget.delete(1.0, tk.END)  # Limpiar el widget de texto
        self.text_widget.insert(tk.END, self.document)  # Insertar el documento en el widget de texto
        self.text_widget.config(state='disabled')  # Deshabilitar la edición del widget de texto
    

    def delete_item(self):
        # Obtiene el índice del elemento seleccionado
        index = self.listbox.curselection()[0]

        # Elimina el elemento seleccionado de la base de datos y de las listas  
        self.collection.delete(self.ids[index])
        self.ids.pop(index)
        self.documents.pop(index)

        # Actualiza la Listbox
        self.listbox.delete(index)
        self.text_widget.config(state='normal')
        self.text_widget.delete(1.0, tk.END)

    def add_item(self):
        # Define el nuevo ID y el documento
        new_document = self.lower_text_widget.get('1.0', 'end-1c')
        new_id = self.chroma_db.get_id(new_document)
        
        embedding, t_token = self.my_embedding.get_embedding(text=new_document)

        self.collection.add(ids=[new_id], documents=[new_document], embeddings=[embedding])
        print(embedding)
        print('-----------')
        print(t_token)
        print('-----------')
        self.ids.append(new_id)
        self.documents.append(new_document)

        # Actualiza la Listbox
        self.listbox.insert(tk.END, new_id)
        self.lower_text_widget.delete('1.0', 'end')

if __name__ == "__main__":
    root = tk.Tk()
    app = EmbeddingEditor(root)
    root.mainloop()
