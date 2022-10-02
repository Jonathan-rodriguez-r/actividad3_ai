# Actividad 3 - Búsqueda y sistemas basados en 
# Jonathan Rodriguez
# Autor : AaronHe7
# Azul oscuro para punto de partida y destino
# Negro para obstaculos o puntos de bloqueo
# Azul Claro para el mejor camino
# Blanco para lugar vacio

import pygame, math, sys
from a_star import *

pygame.init()
pygame.font.init()

HEIGHT = 600
WIDTH = 600

display = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 250)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

font = pygame.font.SysFont('Arial', 10)
text1 = font.render('Punto de Partida/Destino (Click Derecho)', False, BLACK)
text2 = font.render('Obstaculos (Click Izquierdo)', False, BLACK)
text3 = font.render('Iniciar', False, WHITE)
text4 = font.render('Atras', False, WHITE)
text5 = font.render('Limpiar', False, WHITE)
text6 = font.render('Jonathan Rodriguez', False, BLACK)


icon = pygame.image.load('./img/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Jonathan Rodriguez Pathfinder')

def update_display():
  display.fill(WHITE)

  pygame.draw.rect(display, BLUE, (10, 5, 10, 10))
  pygame.draw.rect(display, BLACK, (200, 5, 10, 10))
  display.blit(text1, (25, 5))
  display.blit(text2, (215, 5))

  # Botones
  pygame.draw.rect(display, BLACK, (355, 7, 40, 10))
  pygame.draw.rect(display, BLACK, (435, 7, 40, 10))
  pygame.draw.rect(display, BLACK, (515, 7, 40, 10))

  display.blit(text3, (362, 6))
  display.blit(text4, (445, 6))
  display.blit(text5, (524, 6))

# Grilla
rows = 40
cols = 40
grid = []
undo_log = []
start = None
end = None

def reset_grid():
  global grid, start, end, undo_log
  grid, undo_log, start, end = [], [], None, None

  for i in range(rows):
    row_nodes = []
    for j in range(cols):
      node = Node(grid, j, i)
      row_nodes.append(node)
    grid.append(row_nodes)
  update_grid(display, grid)

def update_grid(display, grid):
  update_display()
  rect_width = (WIDTH - 1)/cols
  rect_height = (HEIGHT - 21)/cols

  for i in range(rows):
    for j in range(cols):
      color = None
      node = grid[i][j]
      if node.type == 'wall':
        color = BLACK
      elif node == start or node == end:
        color = BLUE
      elif node.type == 'path':
        color = LIGHT_BLUE

      if color:
        pygame.draw.rect(display, color, (j * rect_width + 1, i * rect_height + 21, rect_width, rect_height))
              
  for i in range(len(grid) + 1):
    pygame.draw.rect(display, GRAY, (i * rect_width, 20, 1, HEIGHT))
    pygame.draw.rect(display, GRAY, (0, i * rect_height + 20, WIDTH, 1))

  pygame.display.update()
reset_grid()
update_grid(display, grid)

def draw_tile(x, y, tile_type):
  global start, end, undo_log
  clear_path_nodes()
  
  row = ((y - 20) * rows)//(HEIGHT - 20)
  col = (x * cols)//WIDTH
  node = grid[row][col]

  if row < 0 or col < 0 or row >= rows or col >= cols or node.type == 'wall' or node == start or node == end:
    return
  elif tile_type == 'endpoint' and start and end:
    return

  if tile_type == 'wall':
    grid[row][col].type = 'wall'
  elif tile_type == 'endpoint':
    if not start:
      start = node
    elif not end:
      end = node

  undo_log.append(node)
  update_grid(display, grid)

def pathfind():
  if not start or not end:
    print('Por favor marca ambos puntos')
    return
  path = a_star(grid, start, end)
  if not path:
    print('No hay cominos posibles')
    return
  else:
    distance = round(path[-1].f_score, 2)
    if distance % 1 == 0:
      distance = int(distance)
    print('Costo del camino ' + str(distance) + '.')
  for node in path:
    if node != start and node != end:
      node.type = 'path'
  update_grid(display, grid)

def clear_path_nodes():
  for i in range(rows):
    for j in range(cols):
      node = grid[i][j]
      if node.type == 'path':
        node.type = 'road'
            

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

    # Test for click on start and clear button
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = pygame.mouse.get_pos()
      x = mouse_pos[0]
      y = mouse_pos[1]
      
      # Botón de inicio
      if x >= 355 and x <= 395 and y >= 7 and y <= 17:
        pathfind()
      # Botón atras
      elif x >= 435 and x <= 475 and y >= 7 and y <= 17:
        if len(undo_log) > 0:
          node = undo_log[-1]
          node.type = 'road'
          if node == start or node == end:
            if end:
              end = None
            elif start:
              start = None 
          update_grid(display, grid)
          undo_log.pop(-1)

      # Botón Limpiar
      elif x >= 515 and x <= 555 and y >= 7 and y <= 17:
        reset_grid()

    # Click derecho
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
      mouse_pos = pygame.mouse.get_pos()
      x = mouse_pos[0]
      y = mouse_pos[1]
      draw_tile(x, y, 'endpoint')

    # Click Izquierdo
    if pygame.mouse.get_pressed()[0]:
      mouse_pos = pygame.mouse.get_pos()
      x = mouse_pos[0]
      y = mouse_pos[1]
      draw_tile(x, y, 'wall')
