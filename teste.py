import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

imagens_carregadas = {}

tela = None
canvas = None
item_atual = None
aleatorio = 'a'

def adicionar_tarefa():
    item = canvas.create_text(100, 100, text='Tarefa', font=("Arial", 14), anchor="nw", tags="tarefa") 
    return item

def adicionar_imagem():
    caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
    if not caminho:
        return

    imagem = Image.open(caminho)
    imagem = imagem.resize((100, 100))
    imagem_tk = ImageTk.PhotoImage(imagem)

    item = canvas.create_image(200, 200, image=imagem_tk, anchor="nw", tags="imagem")
    imagens_carregadas[item] = imagem_tk  
    return item

def iniciar_movimento(evento):
    global item_atual
    itens = canvas.find_closest(evento.x, evento.y)
    if itens:
        item_atual = itens[0]

def mover_item(evento):
    if item_atual:
        canvas.coords(item_atual, evento.x, evento.y)

def criar_interface():
    global tela, canvas

    tela = tk.Tk()
    tela.title("Organizador Visual de Tarefas")

    canvas = tk.Canvas(tela, width=800, height=600, bg="white")
    canvas.pack(fill="both", expand=True)

    
    btn_tarefa = tk.Button(tela, text="Adicionar Tarefa", command=adicionar_tarefa)
    btn_tarefa.pack(side="left")

    btn_imagem = tk.Button(tela, text="Adicionar Imagem", command=adicionar_imagem)
    btn_imagem.pack(side="left")

   
    canvas.bind("<Button-1>", iniciar_movimento)
    canvas.bind("<B1-Motion>", mover_item)

    tela.mainloop()


if aleatorio == "a":
    criar_interface()