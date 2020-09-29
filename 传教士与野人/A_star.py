"""
Created on 2020/9/29
@author: lizijing
"""

class Node:
    def __init__(self, state, depth, f, parent = None, parent_rule = None):
        self.state = state
        self.depth = depth
        self.f = f
        self.parent = parent
        self.parent_rule = parent_rule
    
    def term(self):
        return self.state == (0,0,0)
    
    
    def gen_child(self, rule):
        m = int(rule[:rule.find('m')])
        c = int(rule[rule.find('m')+1: rule.find('c')])
        lm, lc, lb = self.state
        if lb == 1:
            return (lm-m, lc-c, 0)
        else:
            return (lm+m, lc+c, 1)


def all_rules(m, c, k):   # 产生所有可能的规则
    rule_map = {}
    for i in range(m):
        for j in range(c):
            if i + j > k:
                break
            if i + j == 0:
                continue
            rule_map[str(i) + 'm' + str(j) + 'c_1'] = '{}个传教士和{}个野人从左岸渡河到右岸'.format(i, j)
            rule_map[str(i) + 'm' + str(j) + 'c_0'] = '{}个传教士和{}个野人从右岸渡河到左岸'.format(i, j)
    return rule_map


def is_valid(state, params):
    lm, lc, lb = state
    m, c, k = params
    rm, rc = m-lm, c-lc
    if lm < 0 or lc < 0 or rm < 0 or rc < 0:
        return False
    if lm < lc and lm != 0:
        return False
    if rm < rc and rm != 0:
        return False
    return True


def h(state, k):
    lm, lc, lb = state
    if lb == 1:
        return ((lm + lc - k) // (k-1) + 1) * 2 + 1
    else:
        return ((lm + lc + 1 - k) // (k-1) + 1) * 2 + 2




def A_star(M, C, K):
    
    s_h = h((M, C, 1), K)
    s = Node((M, C, 1), 0, s_h)
    rule_map = all_rules(M, C, K)

    opened = [s]
    closed = []
    while opened:
        n = opened.pop(0)
        if n.term():
            return n
        closed.append(n)
        cand_rules = [k for k in rule_map.keys() if int(k[-1]) == n.state[-1]]
        for rule in cand_rules:
            child_state = n.gen_child(rule)
            if not is_valid(child_state, (M, C, K)):
                continue
            child_depth = n.depth + 1
            child_f = child_depth + h(child_state, K)
            child = Node(child_state, child_depth, child_f, n, rule)

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

    M = 5  # 传教士
    C = 5  # 野人
    K = 3  # 每船乘坐人数
    import time

    start = time.perf_counter()
    rule_map = all_rules(M, C, K)
    rules = []
    process = []
    n = A_star(M, C, K)
    while n:
        process.append(n.state)
        if n.parent_rule:
            rules.append(rule_map[n.parent_rule])
        n = n.parent
    print('起始状态：{}个传教士和{}个野人在左岸'.format(M, C), process[-1])
    for i in range(len(rules)-1, -1, -1):
        print(rules[i], process[i])

    end = time.perf_counter()
    print('\n用时', end-start, 's\n')