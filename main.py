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
acoes = []
itens_redimensionaveis = {}
borda_redimensionamento = None
item_redimensionando = None
movendo_borda = False

def iniciar_borda(event):
    global movendo_borda
    movendo_borda = True

def parar_borda(event):
    global movendo_borda
    movendo_borda = False

def movimento_borda(event):
    global movendo_borda
    if movendo_borda:
        redimensionar_item(event)
    else:
        mover_item(event)


def limpar_selecao():
    global borda_redimensionamento, item_redimensionando
    if borda_redimensionamento:
        canvas.delete(borda_redimensionamento)
        borda_redimensionamento = None
        item_redimensionando = None

def exibir_alca(item_id):
    global borda_redimensionamento, item_redimensionando

    if borda_redimensionamento:
        canvas.delete(borda_redimensionamento)

    bbox = canvas.bbox(item_id)
    if bbox:
        x1, y1, x2, y2 = bbox
        borda_redimensionamento = canvas.create_rectangle(
            x2 - 10, y2 - 10, x2, y2,
            fill="blue", tags="alca"
        )
        item_redimensionando = item_id
        
def redimensionar_item(event):
    global item_redimensionando, itens_redimensionaveis

    if not item_redimensionando:
        return

    obj = itens_redimensionaveis[item_redimensionando]
    bbox = canvas.bbox(item_redimensionando)
    if not bbox:
        return

    x1, y1, _, _ = bbox
    nova_largura = max(20, event.x - x1)
    nova_altura = max(20, event.y - y1)

    if obj["tipo"] == "imagem":
        imagem = Image.open(obj["caminho"])
        imagem = imagem.resize((nova_largura, nova_altura))
        imagem_tk = ImageTk.PhotoImage(imagem)

        canvas.itemconfig(item_redimensionando, image=imagem_tk)
        itens_redimensionaveis[item_redimensionando]["imagem"] = imagem_tk
        itens_redimensionaveis[item_redimensionando]["largura"] = nova_largura
        itens_redimensionaveis[item_redimensionando]["altura"] = nova_altura

    elif obj["tipo"] == "texto":
        novo_tamanho = max(6, int(nova_altura / 1.5))
        canvas.itemconfig(item_redimensionando, font=("Arial", novo_tamanho))
        itens_redimensionaveis[item_redimensionando]["tamanho_fonte"] = novo_tamanho

    exibir_alca(item_redimensionando)

def alternar_desenho ():
    global desenho
    desenho = not desenho
    cursor = "pencil" if desenho else "arrow"
    canvas.config(cursor=cursor)
    
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
        acoes.append(("desenho", linha))

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
     itens_redimensionaveis[item]={
         "tipo": "texto",
         "tamanho_fonte": 14
     }
     acoes.append(("criar", item))
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
        acoes.append(("criar_grupo", [caixa, texto]))

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
    itens_redimensionaveis[item] = {
    "tipo": "imagem",
    "imagem": imagem_tk,
    "caminho": caminho,
    "largura": 100,
    "altura": 100
}
    acoes.append(("criar", item))
    imagens_carregadas[item] = imagem_tk  
    return item

def iniciar_movimento(evento):
     global item_atual, linha
     if desenho:
        linha = canvas.create_line(evento.x, evento.y, evento.x, evento.y, fill="red", width=2, capstyle="round", smooth=True, tags="desenho")
        item_atual = None
     else:
        itens = canvas.find_closest(evento.x, evento.y)
        if itens:
            id_item = itens[0]
            pos_antiga = canvas.coords(id_item)
            acoes.append(("mover", id_item, pos_antiga))
            if id_item in itens_redimensionaveis:
                item_atual = id_item
                exibir_alca(id_item)
                return
            acoes.append(("mover", id_item, pos_antiga))  
            for tarefa in tarefas:
                if tarefa["caixa"] == id_item or tarefa["texto"] == id_item:
                    item_atual = tarefa["tag"]
                    return
            item_atual = id_item

def mover_item(evento):
     global linha
     if desenho:
        if linha:
            coords = canvas.coords(linha)
            coords.extend([evento.x, evento.y])
            canvas.coords(linha, *coords)
            
     elif item_atual:
        if isinstance(item_atual, str):
            itens = canvas.find_withtag(item_atual)
            if itens:
                caixa = canvas.bbox(itens[0])
                if caixa:
                    x_antigo, y_antigo = caixa[0], caixa[1]
                    dx = evento.x - x_antigo
                    dy = evento.y - y_antigo
                    for item in itens:
                        canvas.move(item, dx, dy)
        else:
            canvas.coords(item_atual, evento.x, evento.y)
            if item_atual in itens_redimensionaveis:
             exibir_alca(item_atual)
            
def desfazer_acao(event=None):
    if not acoes:
        return

    acao = acoes.pop()
    tipo= acao[0]

    if tipo == "criar":
        item_id = acao[1]
        canvas.delete(item_id)
        if item_id in imagens_carregadas:
            del imagens_carregadas[item_id]

    elif tipo == "criar_grupo":
        for item_id in acao[1]:
            canvas.delete(item_id)

    elif tipo == "mover":
        item_id = acao[1]
        pos_antiga = acao[2]
        canvas.coords(item_id, *pos_antiga)
        
    elif tipo == 'desenho':
        linha = acao[1]
        canvas.delete(linha)


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
    canvas.bind("<ButtonRelease-1>", lambda e: None if not desenho else finalizar_linha(e))
    tela.bind("<Control-z>", desfazer_acao)
    canvas.bind("<B1-Motion>", movimento_borda)
    canvas.tag_bind("alca", "<Button-1>", iniciar_borda)
    canvas.tag_bind("alca", "<ButtonRelease-1>", parar_borda)
    canvas.tag_bind("alca", "<Enter>", lambda e: canvas.config(cursor="bottom_right_corner"))
    canvas.tag_bind("alca", "<Leave>", lambda e: canvas.config(cursor="arrow"))



    tela.mainloop()


if aleatorio == "a":
    criar_interface()
