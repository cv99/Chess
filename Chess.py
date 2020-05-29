import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 30)

# version 09

import pygame
from chess2 import piece, backDrop, board, screenFreeze, checkCheck

displayDims = (800, 800)
pygame.init()
screen = pygame.display.set_mode(displayDims)
pygame.display.set_caption(u'Chess - \u25A1\u25A0 move')
icon = pygame.Surface((30, 30))
icon.fill((255, 255, 255))
pygame.display.set_icon(icon)

print('Icons from https://www.flaticon.com/packs/chess. Licensed by Creative Commons BY 3.0')

print()
print('Game details:')
running = True
dragging = False
dragList = []
offSet = [0, 0]
whiteMove = True
check = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
            startPos = event.pos
            dragList = []
            offSet = [0, 0]
            for p in board:
                if p.inBox(event.pos):
                    dragList.append(p)
        if event.type == pygame.MOUSEMOTION and dragging:
            try:
                offSet = [startPos[0] - event.pos[0], startPos[1] - event.pos[1]]
            except NameError:
                nothing = None
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
            check = checkCheck(check, board)
            for p in dragList:
                whiteMove = p.endDrag(offSet, board, whiteMove, check)
                if p.selectType:
                    m = screenFreeze(screen, p)
                    p.typ = m
            dragList = []
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print('Board: (len Board:', str(len(board)) + ')')
                print(board)
                print()

    screen.blit(backDrop, (0, 0))

    if whiteMove:
        pygame.display.set_caption(u'Chess - \u25A1 move')
        icon.fill((255, 255, 255))
        # pygame.draw.lines(icon, (0, 0, 0), True, [(0, 0), (0, 30), (30, 30), (30, 0), (0, 0)])
        pygame.display.set_icon(icon)
    else:
        pygame.display.set_caption(u'Chess - \u25A0 move')
        icon.fill((0, 0, 0))
        pygame.display.set_icon(icon)

    for p in board:
        p.render(screen, dragList, offSet)

    pygame.display.flip()
pygame.quit()
