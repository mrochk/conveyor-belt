CONVBELT_WIDTH = 100
SQUARES_PER_ROW = 4
SQUARE_LEN = CONVBELT_WIDTH // SQUARES_PER_ROW

class Rect: 
    def __init__(self, w, h, letter="x"):
        self.w, self.h = (w, h) if max(w, h) == w else (h, w)
        self.l = letter

    def __str__(self):
        return f"({self.w}, {self.h})"

class Item(Rect):
    def __init__(self, w, h, name="item"):
        self.w, self.h = (w, h) if max(w, h) == w else (h, w)
        self.name = name

class Assembly:
    def __init__(self, h, valid_shapes, how):
        self.height = h
        self.shapes = valid_shapes
        self.how    = how

def divisors(n):
    from math import sqrt, ceil
    result, limit = (), ceil(sqrt(n)) + 1

    if n % 2 != 0:
        for i in range(1, limit, 2):
            if n % i == 0: result += (i,)
        return result

    for i in range(1, limit):
        if n % i == 0: result += (i,)
    return result

def fits(item: Item, shape: Rect):
    A = (shape.w * SQUARE_LEN) >= item.w
    B = (shape.h * SQUARE_LEN) >= item.h
    return A and B

def gen_shapes(k, l):
    s, result = set(), []
    for n in divisors(k):
        if not set([n]).issubset(s): result.append(Rect(k // n, n, l))
        s = s.union(set([n, k//n]))
    return result

def item_to_shape(item: Item):
    """
    Returns a pair (width, height) representing the minimum-sized 
    rectangle (made of squares of size SQUARE_LEN), in which the item fits.
    """
    k,  shapes = 1, (Rect(1, 1, item.name[0]),)
    if fits(item, shapes[0]): return shapes[0]

    while True:
        shapes, k = gen_shapes(k+1, item.name[0]), k+1
        for i in range(len(shapes)):
            if fits(item, shapes[i]): return shapes[i]

def items_to_shapes(items: list[Item]):
    return [item_to_shape(item) for item in items]

def make_convbelt(length):
    result = []
    for _ in range(0, length, SQUARE_LEN):
        result.append([' ' for _ in range(0, SQUARES_PER_ROW)])
    return result

def print_convbelt(c): return [print(row) for row in c]

HORIZONTALLY = 0
VERTICALLY   = 1
BOTH         = 2
CANT_PLACE   = 3

def can_place_shape(shape: Rect, x, y, conv):
    if conv[y][x] != ' ': return CANT_PLACE

    for req_width in range(1, SQUARES_PER_ROW - x+1):
        if conv[y][x+req_width-1] != ' ': req_width -= 1; break

    horizontally = shape.w <= req_width
    vertically   = shape.h <= req_width

    if horizontally and vertically: return BOTH
    if horizontally               : return HORIZONTALLY
    if vertically                 : return VERTICALLY
    else                          : return CANT_PLACE

def place_shape(conv, shape: Rect, how, x, y):
    for i in range(shape.w):
        for j in range(shape.h):
            if how == VERTICALLY: conv[y+i][x+j] = shape.l
            else: conv[y+j][x+i] = shape.l

def empty_row(row):
    for i in row:
        if i != ' ': return False
    return True

def convbelt_len(c):
    res = 0
    for r in c:
        if empty_row(r): return res
        res += 1
    return -1

def min_convbelt_len(convbelts):
    result = int(10e9)
    for c in convbelts: result = min(result, convbelt_len(c))
    return result

def rect_equals(rA, rB):
    a = rA.w == rB.w and rA.h == rB.h
    b = rA.h == rB.w and rA.w == rB.h
    return a or b

def is_square(shape): return shape.w == shape.h

def get_squares(shapes):
    result = []
    for i in range(len(shapes)): 
        result.append(True if is_square(shapes[i]) else False)
    return result

def assemble(shapes: list[Rect], squares):
    from itertools import product

    length = len(shapes)
    prod   = list(product({True, False}, repeat=length))

    if squares:
        for i in range(len(prod)):
            j = 0
            while j < length and j < len(squares):
                prod[i] = list(prod[i])
                if squares[j]: prod[i][j] = True
                prod[i] = tuple(prod[i])
                j += 1

    prod = list(set(prod))
    for p in prod:
        widths, heights = [], []

        for i in range(len(p)):
            if p[i]:
                widths.append(shapes[i].w)
                heights.append(shapes[i].h)
            else:
                widths.append(shapes[i].h)
                heights.append(shapes[i].w)

        same_height, height = True, heights[0]
        for h in heights:
            if h != height: same_height = False; break
        if not same_height: continue

        sum_widths = 0
        for w in widths:
            sum_widths += w
            if sum_widths > SQUARES_PER_ROW: break
        if sum_widths != SQUARES_PER_ROW: continue

        validshapes, how = [], []
        for i in range(len(widths)):
            validshapes.append(shapes[i])
            how.append(p[i])

        return Assembly(height, validshapes, how)
    return None


def assemble_shapes(shapes: list[Rect], memo):
    from itertools import combinations

    squares = get_squares(shapes)
    for i in range(1, SQUARES_PER_ROW+1, +1):
        if set({i}).issubset(memo): continue

        allcombinations = list(combinations(shapes, i))
        for combination in allcombinations:
            assembly = assemble(combination, squares)
            if assembly:
                for shape in assembly.shapes: shapes.remove(shape)
                return assembly
        memo.add(i)
    return None

def inc_x(x, i): return (x + i) % SQUARES_PER_ROW

def place_assembly_of_shapes(convbelt, shapes):
    print(f"Placing {len(shapes)} items:\n")
    memo, y = set(), 0
    while True:
        validsh = assemble_shapes(shapes, memo)
        if not validsh: break
        x = 0
        for shape, horizontally in zip(validsh.shapes, validsh.how):
            if horizontally: how = HORIZONTALLY; inc = shape.w
            else: how = VERTICALLY; inc = shape.h
            print(f"Placing \"{shape.l}\" : {shape}, {'horizontally' if horizontally else 'vertically'} in {(x, y)}.")
            place_shape(convbelt, shape, how, x, y)
            x = inc_x(x, inc)
        y += validsh.height

    print(f"\nNumber of shapes left to place: {len(shapes)}.")
    for sh in shapes: print(f"{sh.l}: ({sh.w}, {sh.h})\n")

    return y

sett = set()

def place_rest(convbelt, shapes, y):
    x = 0
    while shapes:
        for shape in shapes:
            how = can_place_shape(shape, x, y, convbelt)

            if how in {HORIZONTALLY, BOTH}:
                print(f"Placing \"{shape.l}\" : {shape}, horizontally in {(x, y)}.")
                place_shape(convbelt, shape, HORIZONTALLY, x, y)
                inc = shape.w-1
            elif how == VERTICALLY:
                print(f"Placing \"{shape.l}\" : {shape}, vertically in {(x, y)}.")
                place_shape(convbelt, shape, how, x, y)
                inc = shape.h-1

            if how != CANT_PLACE:
                shapes.remove(shape)
                x = inc_x(x, inc)
                break

        x = inc_x(x, 1)
        if x == 0: y += 1

    return convbelt_len(convbelt)

def solve(items, length=500):
    shapes = items_to_shapes(items)
    conveyor_belt = make_convbelt(length)
    y = place_assembly_of_shapes(conveyor_belt, shapes)
    conveyor_belt_len = place_rest(conveyor_belt, shapes, y)
    print()
    print_convbelt(conveyor_belt)
    return conveyor_belt_len * SQUARE_LEN


if __name__ == '__main__':
    from random import random
    randint = lambda ub, lb: random() * (ub - lb) + lb
    alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    items = []
    for i in range(125):
        w = randint(0, 100)
        h = randint(0, 100)
        items.append(Item(w, h, alph[i%10]))

    result = solve(items, length=7000)
    print(f"\nResult: {result}cm.")
