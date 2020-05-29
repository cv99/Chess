#version 09

def pwnMove(p, a, b, board, whiteMove):
    dx=a-p.x
    dy=b-p.y
    if dx==0:
        if whiteMove:
            return  (dy==-1 or (dy==-2 and p.y==6)) and not (isPiece(board, a, b, True) or isPiece(board, a, b, False))
        else:
            return (dy==1 or (dy==2 and p.y==1)) and not (isPiece(board, a, b, True) or isPiece(board, a, b, False))
    else:
        if whiteMove:
            return (dy==-1 and isPiece(board, a, b, False) and dx in [1, -1])
        else:
            return (dy==1 and isPiece(board, a, b, True) and dx in [1, -1])

def rkMove(p, a, b, board, whiteMove):
    if (a==p.x or b==p.y) and not (a==p.x and b==p.y):
        return (not ( True in [isPiece(board, t[0], t[1], True) for t in sLineExcl(p.x, p.y, a, b)]
               or True in [isPiece(board, t[0], t[1], False) for t in sLineExcl(p.x, p.y, a, b)])) and not isPiece(board, a, b, whiteMove)
    else:
        return False
    
    return True

def kntMove(p, a, b, board, whiteMove):
    dx=a-p.x
    dy=b-p.y
    
    return (((dx==1 and dy==2) or (dx==-1 and dy==2) or (dx==1 and dy==-2) or (dx==-1 and dy==-2)
        or (dx==2 and dy==1) or (dx==-2 and dy==1) or (dx==2 and dy==-1) or (dx==-2 and dy==-1))
                        and not isPiece(board, a, b, whiteMove) )

def bhpMove(p, a, b, board, whiteMove):
    dx=a-p.x
    dy=b-p.y

    if abs(dx)==abs(dy):
        return (not (True in [isPiece(board, t[0], t[1], True) for t in dLineExcl(p.x, p.y, a, b)]
            or True in [isPiece(board, t[0], t[1], False) for t in dLineExcl(p.x, p.y, a, b)])) and not isPiece(board, a, b, whiteMove) 
    else:
        return False

def qnMove(p, a, b, board, whiteMove):
    dx=a-p.x
    dy=b-p.y

    if abs(dx)==abs(dy):
        return (not (True in [isPiece(board, t[0], t[1], True) for t in dLineExcl(p.x, p.y, a, b)]
            or True in [isPiece(board, t[0], t[1], False) for t in dLineExcl(p.x, p.y, a, b)])) and not isPiece(board, a, b, whiteMove)
    elif (a==p.x or b==p.y) and not (a==p.x and b==p.y):
        return (not ( True in [isPiece(board, t[0], t[1], True) for t in sLineExcl(p.x, p.y, a, b)]
               or True in [isPiece(board, t[0], t[1], False) for t in sLineExcl(p.x, p.y, a, b)])) and not isPiece(board, a, b, whiteMove)
    else:
        return False

def kngMove(p, a, b, board, whiteMove):
    dx=a-p.x
    dy=b-p.y

    if abs(dx) in [0, 1] or abs(dy) in [0, 1]:
        return not isPiece(board, a, b, whiteMove)
    else:
        rks=[]
        for pp in board:
            if pp.typ=='RK' and not pp.hasMoved:
                rks.append(pp)
        if dx==2:
            for r in rks:
                if r.x<p.x:
                    rks.remove(r)
            if not len(rks)==0:
                r=rks[0]
                if not p.hasMoved:
                    nothing=None
                    print('CASTLING not implemented')
            else:
                return False
        elif dx==-2:
            for r in rks:
                if r.x>p.x:
                    rks.remove(r)
            if not len(rks)==0:
                r=rks[0]
                if not p.hasMoved:
                    nothing=None
                    print('CASTLING not implemented')
            else:
                return False
        else:
            return False

def isPiece(board, x, y, lookingForWhite):
    n=False
    for p in board:
        if p.x==x and p.y==y and p.isWhite==lookingForWhite:
            n=True
    return n

def takePieces(board, x, y):
    register=[]
    for p in board:
        if p.x==x and p.y==y and not p.typ=='KNG':
            board.remove(p)
            register.append(p)
    return register

def putBackPieces(board, register):
    for p in register:
        board.append(p)
    return board

def dLineExcl(sx, sy, ex, ey):
    dx=ex-sx
    dy=ey-sy

    x=sx
    y=sy
    output=[]
    if dx>0 and dy>0:
        while x<ex and y<ey:
            output.append([x, y])
            x+=1
            y+=1
    if dx<0 and dy>0:
        while x>ex and y<ey:
            output.append([x, y])
            x-=1
            y+=1
    if dx>0 and dy<0:
        while x<ex and y>ey:
            output.append([x, y])
            x+=1
            y-=1
    if dx<0 and dy<0:
        while x>ex and y>ey:
            output.append([x, y])
            x-=1
            y-=1
    return output[1:]

def sLineExcl(sx, sy, ex, ey):
    output=[]
    x=sx
    y=sy
    if sx==ex:
        if ey-sy>0:
            while y<ey:
                output.append([x, y])
                y+=1
        else:
            while y>ey:
                output.append([x, y])
                y-=1
    elif sy==ey:
        if ex-sx>0:
            while x<ex:
                output.append([x, y])
                x+=1
        else:
            while x>ex:
                output.append([x, y])
                x-=1
    else:
        print('Error line not straight')
    return output[1:]
