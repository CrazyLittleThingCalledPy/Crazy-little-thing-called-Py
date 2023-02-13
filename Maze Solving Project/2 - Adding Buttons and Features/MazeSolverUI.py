import numpy as np
import pygame

active = True

window_size = (640, 600)
pygame.init()
pygame.display.set_caption('Maze solver')
window = pygame.display.set_mode(window_size)
text_creator = pygame.font.SysFont('Arial', 20)

rows, cols, dim = 20, 20, 25

board = np.zeros((rows, cols), dtype='int')
start_pos = (-1,-1)
target_pos = (-1,-1)


# ----------------------- Buttons -------------------------

buttons = []

explored_state = False

def add_button(image_filename, position, function_name):
    buttons.append({'image': pygame.image.load(image_filename),
                    'pos': position,
                    'func': function_name})


def draw_buttons():
    pygame.draw.rect(window, (255,255,255), pygame.Rect(500,0,140,600), width=0)
    for button in buttons:
        window.blit(button['image'], button['pos'])
    pygame.display.update()
    
def button_pressed(mouse_pos):
    x, y = mouse_pos
    for button in buttons:
        b_x, b_y, b_w, b_h = button['pos']
        if b_x <= x <= b_x+b_w and b_y <= y <= b_y+b_h:
            return button
    return False

# ---------------------------------------------------------



def handle_events():
    global active, board, start_pos, target_pos
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            #test if one of the buttons was pressed, if so call its function
            button = button_pressed(event.pos)
            if button:
                button['func'](button)
            
            row = event.pos[1]//dim
            col = event.pos[0]//dim
            if row<rows and col<cols:
                if event.button == 1:
                    board[row][col] = (board[row][col]+1)%2
                if event.button == 2:
                    if start_pos != (-1,-1):
                        board[start_pos[0], start_pos[1]] = 0
                    start_pos = (row, col)
                    board[row][col] = 2
                if event.button == 3:
                    if target_pos != (-1,-1):
                        board[target_pos[0], target_pos[1]] = 0
                    target_pos = (row, col)
                    board[row][col] = 3
                
                draw_board()
                draw_text(f'Clicked cell {row},{col} - value set {board[row][col]}')

def draw_text(text):
    pygame.draw.rect(window, (255,255,255), pygame.Rect(0,500,cols*dim,100), width=0)
    text_surface = text_creator.render(text, True, (50,0,0))
    window.blit(text_surface, (25,525))
    pygame.display.update()

def draw_board():
    global board
    # window.fill((255,255,255)) #r,g,b   red,green,blue  0 min  255 max
    pygame.draw.rect(window, (255,255,255), pygame.Rect(0,0,cols*dim,rows*dim), width=0)
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

def clear_button_func(button):
    global board
    board = np.zeros((rows, cols), dtype='int')
    start_pos = (-1,-1)
    target_pos = (-1,-1)
    draw_board()
    draw_text('The screen was cleared')   
    
def save_button_func(button):
    np.savetxt('Maze.txt', board, fmt='%d')
    draw_text('The file was saved...')
    
def load_button_func(button):
    global board, start_pos, target_pos
    board = np.loadtxt('Maze.txt', dtype='int')
    draw_board() 
    
    search_results = np.argwhere(board == 2)
    if len(search_results) > 0:
        start_pos = tuple(search_results[0])
    else:
        start_pos = (-1, -1)
    
    search_results = np.argwhere(board == 3)
    if len(search_results) > 0:
        target_pos = tuple(search_results[0])
    else:
        target_pos = (-1, -1)
        
    draw_text('The board was loaded from file...')
    
def explored_button_func(button):
    global explored_state
    if explored_state:
        button['image'] = pygame.image.load('buttons\\ExploredOffButton.png')
        explored_state = False
        draw_text('Explored state off')
    else:
        button['image'] = pygame.image.load('buttons\\ExploredOnButton.png')
        explored_state = True
        draw_text('Explored state on')
    draw_buttons()
    
   
def draw_path(path):
    for i in range(1, len(path)):
        start_x = (path[i-1][1]+0.5) * dim
        start_y = (path[i-1][0]+0.5) * dim
        end_x = (path[i][1]+0.5) * dim
        end_y = (path[i][0]+0.5) * dim
        pygame.draw.line(window, (255,0,0), (start_x,start_y), (end_x, end_y), width=3)
    pygame.display.update()
   
    
def path_button_func(button):
    example_path = [(0,0),(0,1),(0,2),(0,3),(1,3),(2,3),(2,4),(2,5)]
    draw_path(example_path)
    

def main():
    add_button('Buttons\\ClearButton.png', pygame.Rect(520, 20, 100, 30), clear_button_func)
    add_button('Buttons\\SaveButton.png', pygame.Rect(520, 70, 100, 30), save_button_func)
    add_button('Buttons\\LoadButton.png', pygame.Rect(520, 120, 100, 30), load_button_func)
    add_button('Buttons\\ExploredOffButton.png', pygame.Rect(520, 170, 100, 30), explored_button_func)
    add_button('Buttons\\PathButton.png', pygame.Rect(520, 220, 100, 30), path_button_func)
    draw_board()  
    draw_text('Hello')
    draw_buttons()
    while active:
        handle_events()
   
if __name__ == '__main__':   
    main()