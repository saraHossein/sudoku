import pygame

WIDTH = 550
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)

grid = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def escape():
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            return


def DrawGrid(grid):
    win = pygame.display.set_mode((WIDTH, WIDTH))
    win.fill(background_color)
    my_font = pygame.font.SysFont('Comic Sans MS', 35)

    for i in range(0, 9):
        for j in range(0, 9):
            if grid[i][j] != 0:
                value = my_font.render(str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))

    pygame.display.update()

    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(win, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 6)
            pygame.draw.line(win, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 6)

        pygame.draw.line(win, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
        pygame.draw.line(win, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)
    pygame.display.update()

def define_domain(grid):
    domains = [[None for i in range(9)]for j in range(9)]
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                domains[i][j] = [1,2,3,4,5,6,7,8,9]
            else:
                domains[i][j] = [grid[i][j]]
    return domains

def limits(domains):
    for i in range(9):
        x =[]
        for j in range(9):
            if len(domains[i][j]) == 1:
                x.append(domains[i][j][0])
        if len(x) > 0:
            for k in x:
                for j in range(len(domains[i])):
                    if k in domains[i][j]:
                            if len(domains[i][j]) != 1:
                                domains[i][j].remove(k)
    for i in range(9):
        y = []
        for j in range(9):
            if len(domains[j][i]) == 1:
                y.append(domains[j][i][0])
        
        if len(y) > 0:
            for k in y:
                for j in range(len(domains[j])):
                    if k in domains[j][i]:
                            if len(domains[j][i]) != 1:
                                domains[j][i].remove(k)

    for a in range(3):
        for b in range(3):
            k = []
            for c in range(3):
                for d in range(3):
                    if len(domains[3*a+c][3*b+d]) == 1:
                        k.append(domains[3*a+c][3*b+d][0]) 

            if len(k) > 0:
                for e in k:
                    for c in range(3):
                        for d in range(3):
                            if e in domains[3*a+c][3*b+d]:
                                if len(domains[3*a+c][3*b+d]) != 1:
                                    domains[3*a+c][3*b+d].remove(e)
            
    return domains


def mrv(domains):
    m = (10,(-1,-1))
    for i in range(9):
        for j in range(9):
            num = len(domains[i][j])
            if num < m[0] and num > 1:
                m = (num,(i,j))
    if m[0] == 10:
        return False
    
    i = m[1][0]
    j = m[1][1]

    c = {}
    for elem in domains[i][j]:
        count = 0
        for k in range(9):
            if elem in domains[i][k]:
                count += 1
            if elem in domains[k][j]:
                count += 1
        if i//3 == 0:
            if j//3 == 0:
                for a in range(3):
                    for b in range(3):
                        if elem in domains[a][b]:
                            count +=1
            elif j//3 == 1:
                for a in range(3):
                    for b in range(3,6):
                        if elem in domains[a][b]:
                            count +=1
            else:
                for a in range(3):
                    for b in range(6,9):
                        if elem in domains[a][b]:
                            count +=1
        elif i//3 == 1:
            if j//3 == 0:
                for a in range(3,6):
                    for b in range(3):
                        if elem in domains[a][b]:
                            count +=1
            elif j//3 == 1:
                for a in range(3,6):
                    for b in range(3,6):
                        if elem in domains[a][b]:
                            count +=1
            else:
                for a in range(3,6):
                    for b in range(6,9):
                        if elem in domains[a][b]:
                            count +=1
        else:
            if j//3 == 0:
                for a in range(6,9):
                    for b in range(3):
                        if elem in domains[a][b]:
                            count +=1
            elif j//3 == 1:
                for a in range(6,9):
                    for b in range(3,6):
                        if elem in domains[a][b]:
                            count +=1
            else:
                for a in range(6,9):
                    for b in range(6,9):
                        if elem in domains[a][b]:
                            count +=1
        c[elem] = count
    dom = min(c, key = lambda e: c[e])
    domains[i][j] = [dom]
    c = {}
    return domains


def solver(grid):
    domains = define_domain(grid)
    domains = limits(domains)
    temp = mrv(domains)
    while temp:
        domains = temp
        domains = limits(domains)
        temp = mrv(domains)
    for i in range(9):
        for j in range(9):
            domains[i][j] = domains[i][j][0]
    res = domains
    return res



def main():
    pygame.font.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("CH02")
    win.fill(background_color)
    res = solver(grid)
    DrawGrid(res)
    while True:
        escape()
    


main()
