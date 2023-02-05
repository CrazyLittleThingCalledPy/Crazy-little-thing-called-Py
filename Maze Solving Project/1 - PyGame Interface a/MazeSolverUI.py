import numpy as np
import pygame

active = True

window_size = (500, 600)
pygame.init()
pygame.display.set_caption('Maze solver')
window = pygame.display.set_mode(window_size)
text_creator = pygame.font.SysFont('Arial', 20)

rows, cols, dim = 20, 20, 25

board = np.zeros((rows, cols), dtype='int')

def handle_events():
    global active
    global board
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            row = event.pos[1]//dim
            col = event.pos[0]//dim
            if row<rows and col<cols:
                
                if event.button == 1:
                    board[row][col] = (board[row][col]+1)%2
                if event.button == 2:
                    board[row][col] = 2
                if event.button == 3:
                    board[row][col] = 3
                
                draw()
                draw_text(f'Clicked cell {row},{col} - value set {board[row][col]}')

def draw_text(text):
    text_surface = text_creator.render(text, True, (50,0,0))
    window.blit(text_surface, (25,525))
    pygame.display.update()

def draw():
    global board
    window.fill((255,255,255)) #r,g,b   red,green,blue  0 min  255 max
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:
                pygame.draw.rect(window, (200,200,200), pygame.Rect(col*dim,row*dim,dim,dim), width=1)
            if board[row][col] == 1:
                pygame.draw.rect(window, (50,50,50), pygame.Rect(col*dim,row*dim,dim,dim), width=0)
            if board[row][col] == 2:
                pygame.draw.rect(window, (50,200,50), pygame.Rect(col*dim,row*dim,dim,dim), width=0)
            if board[row][col] == 3:
                pygame.draw.rect(window, (200,50,50), pygame.Rect(col*dim,row*dim,dim,dim), width=0)
                
    pygame.display.update()

def main():
    draw()    
    while active:
        handle_events()
   
if __name__ == '__main__':   
    main()