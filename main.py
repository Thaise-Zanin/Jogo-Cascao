import pygame
import random
import os
from tkinter import simpledialog

pygame.init()

relogio = pygame.time.Clock()
icone  = pygame.image.load("recursos/icone.png")
cascao = pygame.image.load("recursos/cascao.png")
fundo = pygame.image.load("recursos/fundoprincipal.png")
fundoStart = pygame.image.load("recursos/fundoinicio.png")
fundoDead = pygame.image.load("recursos/fundofinal.png")

gotadechuva = pygame.image.load("recursos/gotachuva.png")
raio = pygame.image.load("recursos/raio.png")
nuvem = pygame.image.load("recursos/nuvem.webp")
tamanho = (800,600)
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Jogo do Cascão")
pygame.display.set_icon(icone)

fonte = pygame.font.SysFont("Cooper Black",28)
fonteStart = pygame.font.SysFont("Cooper Black",55)
fonterestart = pygame.font.SysFont("Cooper Black",40)
fonteMorte = pygame.font.SysFont("Cooper Black",120)

pygame.mixer.music.load("recursos\correndoMolhado.mp3")
finalSound = pygame.mixer.Sound("recursos\somTriste.mp3")
chuvaSound = pygame.mixer.Sound("recursos\somChuva.mp3")
trovaoSound = pygame.mixer.Sound("recursos\somTrovao.mp3")

chuvaSound.set_volume(0.1) 
trovaoSound.set_volume(0.1) 
finalSound.set_volume(0.1)
pygame.mixer.music.set_volume(0.1)

branco = (255,255,255)
azul = (56, 108, 215)
amarelo = (237, 235, 153)


def jogar(nome):
    pygame.mixer.Sound.play(chuvaSound)
    pygame.mixer.music.play(-180)
    posicaoXPersona = 300
    posicaoYPersona = 350
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXgotadechuva = 400
    posicaoYgotadechuva = -240
    posicaoXraio = 100
    posicaoYraio = -350
    velocidadegotadechuva = 1
    velocidaderaio = 1
    pontos = 0
    larguraPersona = 190
    alturaPersona = 100
    larguragotadechuva  = 200
    alturagotadechuva  = 204
    larguraraio = 200
    alturaraio = 204
    dificuldade  = 20
    posicaoXnuvem = 440
    posicaoYnuvem = 25

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0

                
        posicaoXPersona = posicaoXPersona + movimentoXPersona            
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        
        if posicaoXPersona < 0 :
            posicaoXPersona = 10
        elif posicaoXPersona >550:
            posicaoXPersona = 540
            
        if posicaoYPersona < 0 :
            posicaoYPersona = 10
        elif posicaoYPersona > 473:
            posicaoYPersona = 463
        
            
        tela.fill(branco)
        tela.blit(fundo, (0,0) )
        #pygame.draw.circle(tela, azul, (posicaoXPersona,posicaoYPersona), 40, 0 )
        tela.blit( cascao, (posicaoXPersona, posicaoYPersona) )
        tela.blit( nuvem, (posicaoXnuvem, posicaoYnuvem) )
        
        posicaoYgotadechuva = posicaoYgotadechuva + velocidadegotadechuva
        posicaoYraio = posicaoYraio + velocidaderaio
        if posicaoYgotadechuva > 600:
            posicaoYgotadechuva = -240
            pontos = pontos + 1
            velocidadegotadechuva = velocidadegotadechuva + 1
            posicaoXgotadechuva = random.randint(0,800)
            pygame.mixer.Sound.play(chuvaSound)
        elif posicaoYraio > 600:
            posicaoYraio = -240
            pontos = pontos + 1
            velocidaderaio = velocidaderaio + 1
            posicaoXraio = random.randint(0,800)
            pygame.mixer.Sound.play(trovaoSound)

            
        tela.blit( gotadechuva, (posicaoXgotadechuva, posicaoYgotadechuva) )
        tela.blit( raio, (posicaoXraio, posicaoYraio) )
        
        texto = fonte.render(nome+"- Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (10,10))
        
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelsgotadechuvaX = list(range(posicaoXgotadechuva, posicaoXgotadechuva + larguragotadechuva))
        pixelsgotadechuvaY = list(range(posicaoYgotadechuva, posicaoYgotadechuva + alturagotadechuva))
        pixelsraioX = list(range(posicaoXraio, posicaoXraio + larguraraio))
        pixelsraioY = list(range(posicaoYraio, posicaoYraio + alturaraio))
        
        #print( len( list( set(pixelsgotadechuvaX).intersection(set(pixelsPersonaX))   ) )   )
        if  len( list( set(pixelsgotadechuvaY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsgotadechuvaX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                chuvaSound.stop()
                dead(nome, pontos)
        
        elif len(set(pixelsraioY).intersection(set(pixelsPersonaY))) > dificuldade:
            if len(set(pixelsraioX).intersection(set(pixelsPersonaX))) > dificuldade:
                chuvaSound.stop()
                dead(nome, pontos)
        
    
        
        pygame.display.update()
        relogio.tick(60)


def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(finalSound)
    
    jogadas  = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt","w",encoding="utf-8")
        arquivo.close()
 
    jogadas[nome] = pontos   
    arquivo = open("historico.txt","w",encoding="utf-8") 
    arquivo.write(str(jogadas))
    arquivo.close()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                finalSound.stop()
                jogar(nome)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    finalSound.stop()
                    jogar(nome)
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        buttonStart = pygame.draw.rect(tela, amarelo, (35,482,750,100),0)
        textoStart = fonterestart.render("RESTART", True, branco)
        tela.blit(textoStart, (500,505))
        textoEnter = fonte.render("Press enter to continue...", True, branco)
        tela.blit(textoEnter, (60,515))
        pygame.display.update()
        relogio.tick(60)


def ranking():
    estrelas = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8" )
        estrelas = eval(arquivo.read())
        arquivo.close()
    except:
        pass
    
    nomes = sorted(estrelas, key=estrelas.get,reverse=True)
    print(estrelas)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    finalSound.stop()
                    start()

        tela.fill(amarelo)
        buttonStart = pygame.draw.rect(tela, amarelo, (35,482,750,100),0)
        textoStart = fonteStart.render("BACK TO START", True, branco)
        tela.blit(textoStart, (170,500))
        
        
        posicaoY = 50
        for key,nome in enumerate(nomes):
            if key == 13:
                break
            textoJogador = fonte.render(nome + " - "+str(estrelas[nome]), True, branco)
            tela.blit(textoJogador, (300,posicaoY))
            posicaoY = posicaoY + 30

            
        
        pygame.display.update()
        relogio.tick(60)


def start():
    nome = simpledialog.askstring("Cascão","Nome Completo:")
    
    
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
                elif buttonRanking.collidepoint(evento.pos):
                    ranking()

        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        buttonStart = pygame.draw.rect(tela, azul, (35,482,750,100),0)
        buttonRanking = pygame.draw.rect(tela, azul, (35,50,200,50),0,30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (72,58))
        textoStart = fonteStart.render("START", True, branco)
        tela.blit(textoStart, (308,500))

        
        
        pygame.display.update()
        relogio.tick(60)

start()