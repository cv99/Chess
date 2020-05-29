import pygame
import math
import copy

from chess3 import pwnMove, rkMove, kntMove, bhpMove, qnMove, kngMove, isPiece, takePieces, putBackPieces

# version 09

pygame.font.init()
myfont = pygame.font.SysFont('Avenir', 56)

firstTime = True

types = {
    "PWN": "Pawn",
    "RK": "Rook",
    "KNT": "Knight",
    "BHP": "Bishop",
    "QN": "Queen",
    "KNG": "King"
}

side = {
    True: "white",
    False: "black"
}


def positions(t):
    return ["A", "B", "C", "D", "E", "F", "G", "H"][t[0]] + str(8 - t[1])


class piece:
    def __init__(self, x, y, isWhite, icon, typ='PWN'):
        self.x = x
        self.y = y
        self.isWhite = isWhite
        self.typ = typ
        self.icon = icon
        self.selectType = False
        if self.typ in ['RK', 'KNG']:
            self.hasMoved = False

    def render(self, screen, dragList, offSet):
        a = 0
        b = 0
        if self in dragList:
            a = offSet[0]
            b = offSet[1]

        if self.icon == None:
            if self.isWhite:
                col = (255, 255, 255)
            else:
                col = (0, 0, 0)
            pygame.draw.rect(screen, col, pygame.Rect(self.x * 100 - a + 10, self.y * 100 - b + 10, 80, 80))
            plq = myfont.render(self.typ, True, (0, 200, 0))
            screen.blit(plq, (self.x * 100 - a + 10, self.y * 100 - b + 10))
        else:
            screen.blit(self.icon, (self.x * 100 - a + 5, self.y * 100 - b + 5))

    def inBox(self, tup):
        x = tup[0]
        y = tup[1]
        a = x - 100 < self.x * 100 < x
        b = y - 100 < self.y * 100 < y
        return a and b

    def endDrag(self, offSet, board, whiteMove, check):
        c = check
        store = [self.x, self.y]

        a = self.x - math.floor((offSet[0] + 50) / 100)
        b = self.y - math.floor((offSet[1] + 50) / 100)
        if self.legalMove(a, b, board, whiteMove):
            register = takePieces(board, a, b)
            self.x = a
            self.y = b

            print(types[self.typ], 'to', positions((self.x, self.y)), '(' + side[self.isWhite] + ')')

            if self.typ == 'PWN' and ((self.isWhite and self.y == 0) or ((not self.isWhite) and self.y == 7)):
                self.selectType = True
            else:
                whiteMove = not whiteMove
            check = checkCheck(check, board)
            if check in [1, 2] and c in [1, 2]:
                board = putBackPieces(board, register)
                self.x = store[0]
                self.y = store[1]
                whiteMove = not whiteMove
                print('Upward action undone due to check.')
            if c == 0 and check == 1 and not whiteMove:
                board = putBackPieces(board, register)
                self.x = store[0]
                self.y = store[1]
                whiteMove = not whiteMove
                print('Upward action undone due to white putting white in check.')
            if c == 0 and check == 2 and whiteMove:
                board = putBackPieces(board, register)
                self.x = store[0]
                self.y = store[1]
                whiteMove = not whiteMove
                print('Upward action undone due to black putting black in check.')
            try:
                self.hasMoved = True
            except:
                nothing = None
        return whiteMove

    def legalMove(self, a, b, board, whiteMove):
        if self.isWhite == whiteMove and not (self.x == a and self.y == b):
            if self.typ == 'PWN':
                return pwnMove(self, a, b, board, whiteMove)
            elif self.typ == 'RK':
                return rkMove(self, a, b, board, whiteMove)
            elif self.typ == 'KNT':
                return kntMove(self, a, b, board, whiteMove)
            elif self.typ == 'BHP':
                return bhpMove(self, a, b, board, whiteMove)
            elif self.typ == 'QN':
                return qnMove(self, a, b, board, whiteMove)
            elif self.typ == 'KNG':
                return kngMove(self, a, b, board, whiteMove)
            else:
                print('Error unknown piece type')
        else:
            return False

    def __repr__(self):
        return self.typ + ' [' + str(self.x) + ', ' + str(self.y) + ']'


backDrop = pygame.Surface((800, 800))
backDrop.fill((226, 203, 180))
for r in range(8):
    for c in range(8):
        if (r + c) % 2 == 0:
            pygame.draw.rect(backDrop, (150, 70, 25), pygame.Rect(c * 100, r * 100, 100, 100))

blackRkIcon = pygame.transform.scale(pygame.image.load('icons/black/rook.png'), (90, 90))
blackKntIcon = pygame.transform.scale(pygame.image.load('icons/black/knight.png'), (90, 90))
blackBhpIcon = pygame.transform.scale(pygame.image.load('icons/black/bishop.png'), (90, 90))
blackQnIcon = pygame.transform.scale(pygame.image.load('icons/black/queen.png'), (90, 90))
blackKngIcon = pygame.transform.scale(pygame.image.load('icons/black/king.png'), (90, 90))
blackPwnIcon = pygame.transform.scale(pygame.image.load('icons/black/pawn.png'), (90, 90))
blackIcons = [blackRkIcon, blackKntIcon, blackBhpIcon, blackQnIcon, blackKngIcon, blackPwnIcon]

whiteRkIcon = pygame.transform.scale(pygame.image.load('icons/white/rook.png'), (90, 90))
whiteKntIcon = pygame.transform.scale(pygame.image.load('icons/white/knight.png'), (90, 90))
whiteBhpIcon = pygame.transform.scale(pygame.image.load('icons/white/bishop.png'), (90, 90))
whiteQnIcon = pygame.transform.scale(pygame.image.load('icons/white/queen.png'), (90, 90))
whiteKngIcon = pygame.transform.scale(pygame.image.load('icons/white/king.png'), (90, 90))
whitePwnIcon = pygame.transform.scale(pygame.image.load('icons/white/pawn.png'), (90, 90))
whiteIcons = [whiteRkIcon, whiteKntIcon, whiteBhpIcon, whiteQnIcon, whiteKngIcon, whitePwnIcon]

board = [
    piece(0, 0, False, blackIcons[0], 'RK'),
    piece(1, 0, False, blackIcons[1], 'KNT'),
    piece(2, 0, False, blackIcons[2], 'BHP'),
    piece(3, 0, False, blackIcons[3], 'QN'),
    piece(4, 0, False, blackIcons[4], 'KNG'),
    piece(5, 0, False, blackIcons[2], 'BHP'),
    piece(6, 0, False, blackIcons[1], 'KNT'),
    piece(7, 0, False, blackIcons[0], 'RK'),
    piece(0, 1, False, blackIcons[5]),
    piece(1, 1, False, blackIcons[5]),
    piece(2, 1, False, blackIcons[5]),
    piece(3, 1, False, blackIcons[5]),
    piece(4, 1, False, blackIcons[5]),
    piece(5, 1, False, blackIcons[5]),
    piece(6, 1, False, blackIcons[5]),
    piece(7, 1, False, blackIcons[5]),

    piece(0, 7, True, whiteIcons[0], 'RK'),
    piece(1, 7, True, whiteIcons[1], 'KNT'),
    piece(2, 7, True, whiteIcons[2], 'BHP'),
    piece(3, 7, True, whiteIcons[3], 'QN'),
    piece(4, 7, True, whiteIcons[4], 'KNG'),
    piece(5, 7, True, whiteIcons[2], 'BHP'),
    piece(6, 7, True, whiteIcons[1], 'KNT'),
    piece(7, 7, True, whiteIcons[0], 'RK'),
    piece(0, 6, True, whiteIcons[5]),
    piece(1, 6, True, whiteIcons[5]),
    piece(2, 6, True, whiteIcons[5]),
    piece(3, 6, True, whiteIcons[5]),
    piece(4, 6, True, whiteIcons[5]),
    piece(5, 6, True, whiteIcons[5]),
    piece(6, 6, True, whiteIcons[5]),
    piece(7, 6, True, whiteIcons[5])]


def xor(a, b):
    return (a and not b) or (b and not a)


def screenFreeze(screen, p):
    subSurface = pygame.Surface((430, 130))
    rning = True
    while rning:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if 0 <= t[0] < 100 and 0 < t[1] < 100:
                    p.type = 'RK'
                    rning = False
                elif 100 <= t[0] < 200 and 0 < t[1] < 100:
                    p.type = 'KNT'
                    rning = False
                elif 200 <= t[0] < 300 and 0 < t[1] < 100:
                    p.type = 'BHP'
                    rning = False
                elif 300 <= t[0] < 400 and 0 < t[1] < 100:
                    p.type = 'QN'
                    rning = False

        subSurface.fill((150, 70, 25))
        pygame.draw.rect(subSurface, (0, 0, 0), pygame.Rect(0, 0, 430, 15))
        pygame.draw.rect(subSurface, (0, 0, 0), pygame.Rect(0, 115, 430, 15))
        pygame.draw.rect(subSurface, (0, 0, 0), pygame.Rect(0, 0, 15, 130))
        pygame.draw.rect(subSurface, (0, 0, 0), pygame.Rect(415, 0, 15, 130))

        t = list(pygame.mouse.get_pos())
        t[0] -= 200
        t[1] -= 300

        if 0 <= t[0] < 100 and 0 < t[1] < 100:
            pygame.draw.rect(subSurface, (37, 122, 253), pygame.Rect(15, 15, 100, 100))
        elif 100 <= t[0] < 200 and 0 < t[1] < 100:
            pygame.draw.rect(subSurface, (37, 122, 253), pygame.Rect(115, 15, 100, 100))
        elif 200 <= t[0] < 300 and 0 < t[1] < 100:
            pygame.draw.rect(subSurface, (37, 122, 253), pygame.Rect(215, 15, 100, 100))
        elif 300 <= t[0] < 400 and 0 < t[1] < 100:
            pygame.draw.rect(subSurface, (37, 122, 253), pygame.Rect(315, 15, 100, 100))

        if p.isWhite:
            subSurface.blit(whiteIcons[0], (15, 20))
            subSurface.blit(whiteIcons[1], (115, 20))
            subSurface.blit(whiteIcons[2], (215, 20))
            subSurface.blit(whiteIcons[3], (315, 20))
        else:
            subSurface.blit(blackIcons[0], (15, 20))
            subSurface.blit(blackIcons[1], (115, 20))
            subSurface.blit(blackIcons[2], (215, 20))
            subSurface.blit(blackIcons[3], (315, 20))

        screen.blit(subSurface, (185, 285))

        pygame.display.flip()

    if p.type == 'RK':
        if p.isWhite:
            p.icon = whiteIcons[0]
            p.selectType = False
        else:
            p.icon = blackIcons[0]
            p.selectType = False
        return 'RK'
    if p.type == 'KNT':
        if p.isWhite:
            p.icon = whiteIcons[1]
            p.selectType = False
        else:
            p.icon = blackIcons[1]
            p.selectType = False
        return 'KNT'
    if p.type == 'BHP':
        if p.isWhite:
            p.icon = whiteIcons[2]
            p.selectType = False
        else:
            p.icon = blackIcons[2]
            p.selectType = False
        return 'BHP'
    if p.type == 'QN':
        if p.isWhite:
            p.icon = whiteIcons[3]
            p.selectType = False
        else:
            p.icon = blackIcons[3]
            p.selectType = False
        return 'QN'


def checkCheck(check, board):
    global firstTime
    check = 0
    for p in board:
        if p.typ == 'KNG' and p.isWhite:
            whiteKing = p
        if p.typ == 'KNG' and not p.isWhite:
            blackKing = p
    for p in board:
        if p.isWhite:
            if p.legalMove(blackKing.x, blackKing.y, board, True) and not p.typ == 'KNG':
                if firstTime:
                    print('Black in check, due to', p, 'blocking black king', blackKing, '.')
                    firstTime = False
                check = 2
        else:
            if p.legalMove(whiteKing.x, whiteKing.y, board, False) and not p.typ == 'KNG':
                if firstTime:
                    print('White in check, due to', p, 'blocking white king', whiteKing, '.')
                    firstTime = False
                check = 1
    return check
