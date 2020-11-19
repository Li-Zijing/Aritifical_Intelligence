import random
import numpy as np

def read_tsp(filename = 'TSP10.txt'):
    with open(filename, 'r') as f:
        tsp = f.readlines()
    tsp = [tsp[i].split() for i in range(1, len(tsp))]
    n = len(tsp)
    pos = np.array([[float(x), float(y)] for name, x, y in tsp])
    city = list(city[0] for city in tsp)
    dists = {}
    for i in range(n):
        x1, y1 = pos[i]
        for j in range(i+1, n):
            x2, y2 = pos[j]
            distance = np.sqrt((x1-x2)**2 + (y1-y2)**2)
            dists[(city[i], city[j])] = dists[(city[j], city[i])] = distance
    
    return city, dists
    

if __name__ == '__main__':
    n = 20
    city, dists = read_tsp('TSP20.txt')
    random.shuffle(city)
    fi = 0
    for i in range(1, n):
        fi += dists[(city[i-1], city[i])]
    print(city, fi)
    
    
    epoch = 1
    t = 280
    lk = 100*n
    alpha = 0.92
    fs = [float('inf'), fi]

    while epoch < 1000:
        num_accept = 0
        for _ in range(lk):
            u = random.randint(0, n-3)
            v = random.randint(u+3, n)
            delta = dists[(city[u], city[v-1])] - dists[(city[u], city[u+1])]
            if v < n:
                delta += dists[(city[u+1], city[v])] - dists[(city[v-1], city[v])]
                
            if delta < 0: 
                p_accept = 1
            else:
                p_accept = np.exp(-delta/t)
            rn = random.random()
            if p_accept > rn:   # accept
                fi = fi + delta
                city[u+1:v] = city[v-1:u:-1]
                num_accept += 1
                
        t = alpha * t
        print('round %d: distance %.6f, accept rate %.6f'%(epoch, fi, num_accept / lk))
        epoch += 1
        if fs[-1] == fs[-2] == fi:
            print(city, fi)
            break
        fs.append(fi)