import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

imagens_carregadas = {}

tela = None
canvas = None
item_atual = None
aleatorio = 'a'
entrada = None

def apagar_item ():
    global item_atual
    if item_atual:
        canvas.delete(item_atual)
        if item_atual in imagens_carregadas:
            del imagens_carregadas[item_atual]
        item_atual = None

def caixa_de_texto():
    global entrada
    entrada = tk.Entry(tela, font=("Arial", 14))
    entrada.pack(pady=10)
    entrada.focus_set()
    entrada.bind("<Return>", adicionar_tarefa)
    
def adicionar_tarefa(evento=None):
    global entrada
    nome= entrada.get()
    if nome:
     item = canvas.create_text(100, 100, text=nome, font=("Arial", 14), anchor="nw", tags="tarefa") 
     entrada.destroy()
     entrada = None

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

    
    btn_tarefa = tk.Button(tela, text="Adicionar Tarefa", command=caixa_de_texto,)
    btn_tarefa.pack(side="left")

    btn_imagem = tk.Button(tela, text="Adicionar Imagem", command=adicionar_imagem)
    btn_imagem.pack(side="left")
    
    btn_remover = tk.Button(tela, text="Remover Item", command=apagar_item)
    btn_remover.pack(side="left")

   
    canvas.bind("<Button-1>", iniciar_movimento)
    canvas.bind("<B1-Motion>", mover_item)

    tela.mainloop()


if aleatorio == "a":
    criar_interface()