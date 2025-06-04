import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

imagens_carregadas = {}

tela = None
canvas = None
item_atual = None
aleatorio = 'a'
entrada = None
tarefas = []
desenho = False
linha = None

def alternar_desenho ():
    global desenho
    desenho = not desenho
    
def iniciar_linha (evento):
    global linha
    if desenho:
        linha = canvas.create_line(evento.x, evento.y, evento.x, evento.y, fill="red", width=2, capstyle="round", smooth=True, tags="desenho")

def desenhar_linha (evento):
    global linha
    if desenho and linha :
        coords = canvas.coords(linha)
        coords.extend([evento.x, evento.y])
        canvas.coords(linha, *coords)
        
def finalizar_linha(evento):
    global linha_atual
    if desenho:
        linha_atual = None

        

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
     
def texto_checkbox():
    global entrada
    entrada = tk.Entry(tela, font=("Arial", 14))
    entrada.pack(pady=10)
    entrada.focus_set()
    entrada.bind("<Return>", adicionar_tarefa_com_checkbox)
     
def adicionar_tarefa_com_checkbox(evento=None):
    global entrada
    nome = entrada.get()
    if nome:
        x, y = 100, 100 

        tag_tarefa = f"tarefa_{len(tarefas)}" 

        caixa = canvas.create_rectangle(x, y, x + 20, y + 20, outline="black", fill="white", tags=(tag_tarefa, "checkbox"))
        texto = canvas.create_text(x + 30, y, text=nome, font=("Arial", 14), anchor="nw", tags=(tag_tarefa, "tarefa"))

        tarefas.append({
            "caixa": caixa,
            "texto": texto,
            "marcado": False,
            "tag": tag_tarefa
        })

        canvas.tag_bind(caixa, "<Button-1>", lambda e, c=caixa: alternar_checkbox(c))
        canvas.tag_bind(texto, "<Button-1>", lambda e, tag=tag_tarefa: selecionar_conjunto(tag))

        entrada.destroy()
        entrada = None

def selecionar_conjunto(tag):
    global item_atual
    item_atual = tag
    
def alternar_checkbox(caixa_id):
    for tarefa in tarefas:
        if tarefa["caixa"] == caixa_id:
            tarefa["marcado"] = not tarefa["marcado"]
            cor = "green" if tarefa["marcado"] else "white"
            canvas.itemconfig(caixa_id, fill=cor)
            

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
        id_item = itens[0]
        for tarefa in tarefas:
            if tarefa["caixa"] == id_item or tarefa["texto"] == id_item:
                item_atual = tarefa["tag"]
                return
        item_atual = id_item

def mover_item(evento):
    if item_atual:
        if isinstance(item_atual, str):
             itens = canvas.find_withtag(item_atual)
             caixa = canvas.bbox(itens[0]) 
             if caixa:
                x_antigo, y_antigo = caixa[0], caixa[1]
                dx = evento.x - x_antigo
                dy = evento.y - y_antigo
                for item in itens:
                    canvas.move(item, dx, dy)
        else:
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
    
    btn_imagem = tk.Button(tela, text="Checkbox", command=texto_checkbox)
    btn_imagem.pack(side="left")
    
    btn_caneta = tk.Button(tela, text="Modo Caneta", command=alternar_desenho)
    btn_caneta.pack(side="left")

   
    canvas.bind("<Button-1>", iniciar_movimento)
    canvas.bind("<B1-Motion>", mover_item)
    canvas.bind("<ButtonPress-1>", iniciar_linha)
    canvas.bind("<B1-Motion>", desenhar_linha)
    canvas.bind("<ButtonRelease-1>", finalizar_linha)

    tela.mainloop()


if aleatorio == "a":
    criar_interface()