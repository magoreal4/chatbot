from embOpenAIService import MyEmbedding

my_embedding = MyEmbedding("s_collection")

texto = "Hola como estas, si estas bien di si"
texto2 = "Hola como estas, si estas mal di no"
texto3 = "Hola como estas"
texto4 = "Hola"

textos = [texto, texto2, texto3, texto4]

a = my_embedding.create_db(textos=textos)