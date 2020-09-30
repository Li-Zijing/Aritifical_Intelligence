"""
Created on 2020/9/30
@author: lizijing
"""

class Node:
    def __init__(self, state, g, f, parent = None, prev_move = None, move_number = None):
        self.state = state
        self.g = g
        self.f = f
        self.parent = parent
        self.prev_move = prev_move
        self.move_number = move_number
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:   # 空格的位置
                    self.pos = (i,j)
                    break
        
    def term(self):
        return self.state == [[1,2,3],[8,0,4],[7,6,5]]
    
    def gen_rules(self):
        # up, down, left, right分别表示把空格上方、下方、左侧、右侧的数字移动到空格处
        r, c = self.pos
        rules = []
        if r == 0:
            rules.append('down')
        elif r == 1:
            rules.extend(['down', 'up'])
        else:
            rules.append('up')
        if c == 0:
            rules.append('right')
        elif c == 1:
            rules.extend(['left', 'right'])
        else:
            rules.append('left')
        
        opp_direction = {'up':'down', 'down':'up', 'left':'right', 'right':'left'}
        if self.prev_move:
            rules.remove(opp_direction[self.prev_move])
        return rules
        
    def gen_child(self, rule):
        r, c = self.pos
        r_new, c_new = r, c
        if rule == 'up':
            r_new -= 1
        elif rule == 'down':
            r_new += 1
        elif rule == 'right':
            c_new += 1
        else:
            c_new -= 1
        child_state = [[j for j in self.state[i]] for i in range(3)]
        moved_num = child_state[r_new][c_new]
        child_state[r][c] = moved_num
        child_state[r_new][c_new] = 0
        return child_state, moved_num





def h(state):
    h_ = 0
    final_state = [[1,2,3],[8,0,4],[7,6,5]]
    state_dic = {}
    for i in range(3):
        for j in range(3):
            state_dic[state[i][j]] = (i,j)
    for i in range(3):
        for j in range(3):
            num = final_state[i][j]
            if state_dic[num] != (i,j):
                r, c = state_dic[num]
                h_ += num*(abs(i-r) + abs(j-c))
    return h_





def num8_Astar(start_state):

    h_s = h(start_state)
    s = Node(start_state, 0, h_s)
    opened = [s]
    closed = []
    while opened:
        n = opened.pop(0)
        if n.term():
            return n
        closed.append(n)
        rules = n.gen_rules()
        for rule in rules:
            child_state, move_num = n.gen_child(rule)

            child_g = n.g + move_num
            child_f = child_g + h(child_state)
            child = Node(child_state, child_g, child_f, n, rule, move_num)

            continue_flag = False                  
            for node in opened:
                if node.state == child_state: 
                    continue_flag = True
                    if node.f > child_f:
                        opened.remove(node)
                        opened.append(child)
                        opened.sort(key = lambda x: x.f)
                    break
            if continue_flag:
                continue

            for node in closed:
                if node.state == child_state:
                    continue_flag = True
                    if node.f > child_f:  
                        closed.remove(n)
                        opened.append(child)
                        opened.sort(key = lambda x: x.f)
                    break
            if continue_flag:
                continue
            opened.append(child)  
            opened.sort(key = lambda x: x.f)





if __name__ == '__main__':

    import time
    start = time.perf_counter()
#     start_state = [[2,8,3],[1,6,4],[7,0,5]]   
    start_state = [[1,2,3],[4,7,6],[5,0,8]]   # 测试用例
    n = num8_Astar(start_state)
    total_cost = n.f
    rules = []
    process = []
    while n:
        process.append(n.state)
        if n.prev_move:
            rules.append((n.prev_move, n.move_number))
        n = n.parent
    print('起始状态：')
    for row in process[-1]:
        print(row)
    for i in range(len(rules)-1, -1, -1):
        print('移动', rules[i][1])
        for row in process[i]:
            print(row)
    end = time.perf_counter()
    print('总耗散值：', total_cost)
    print('用时', end-start, 's')