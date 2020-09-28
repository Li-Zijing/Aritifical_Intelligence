"""
Created on 2020/9/26
@author: lizijing
"""


class Node(object):   # 搜索树的结点
    
    def __init__(self, state, depth, parent_node = None, parent_rule = None):   
        self.state = state   
        # state: (c1, c2, c3, p1, p2, p3, p4) 8两杯1水量，8两杯2水量，3两杯水量；人1喝水量， 人2喝水量，人3喝水量，人4喝水量
        self.depth = depth
        self.parent = parent_node
        self.parent_rule = parent_rule
        
    def term(self):    # 判断是否完成
        return self.state == (0,0,0,4,4,4,4)
    
    def gen_rules(self):  # 从一个状态产生所有可行的规则
        apprules = []
        c1, c2, c3, p1, p2, p3, p4 = self.state
        # 倒水
        if c1 > 0 and 0 < c2 < 8:
            apprules.append(12)
        if c1 > 0 and c3 < 3:
            apprules.append(13)
        #if c2 > 0 and 0 < c1 < 8:   # 1倒2和2倒1是等价的
            #apprules.append(21)
        if c2 > 0 and c3 < 3:
            apprules.append(23)
        if c3 > 0 and c1 < 8:
            apprules.append(31)
        if c3 > 0 and c2 < 8:
            apprules.append(32)
        # 由于两个8两杯是一模一样的，有时候可以剪掉一些rule
        if c1 == c2:       
            if 13 in apprules and 23 in apprules:
                apprules.remove(23)
            if 31 in apprules and 32 in apprules:
                apprules.remove(32)
        # 喝水
        if p1 < 4:
            if c1 <= 4-p1 and c1 > 0:
                apprules.append(101)
            if c2 <= 4-p1 and c2 > 0:
                apprules.append(102)
            if c3 <= 4-p1 and c3 > 0:
                apprules.append(103)
        if p2 < 4 and p2 != p1:         
        # 当第一个人和第二个人剩余要喝的水量相同时，谁喝都一样，就不再考虑第二个人。下同
            if c1 <= 4-p2 and c1 > 0:
                apprules.append(201)
            if c2 <= 4-p2 and c2 > 0:
                apprules.append(202)
            if c3 <= 4-p2 and c3 > 0:
                apprules.append(203)
        if p3 < 4 and p3 != p1 and p3 != p2:   
            if c1 <= 4-p3 and c1 > 0:
                apprules.append(301)
            if c2 <= 4-p3 and c2 > 0:
                apprules.append(302)
            if c3 <= 4-p3 and c3 > 0:
                apprules.append(303)
        if p4 < 4 and p4 != p1 and p4 != p3 and p4 != p2:
            if c1 <= 4-p4 and c1 > 0:
                apprules.append(401)
            if c2 <= 4-p4 and c2 > 0:
                apprules.append(402)
            if c3 <= 4-p4 and c3 > 0:
                apprules.append(403)  
                
        return apprules
    
    
    def gen_child(self, rule):   # 根据规则从当前状态产生子节点
        c1, c2, c3, p1, p2, p3, p4 = self.state
        if rule == 12:
            water = min(c1, 8-c2)
            c1, c2 = c1 - water, c2 + water
        elif rule == 13:
            water = min(c1, 3-c3)
            c1, c3 = c1 - water, c3 + water
        elif rule == 21:
            water = min(c2, 8-c1)
            c2, c1 = c2 - water, c1 + water
        elif rule == 23:
            water = min(c2, 3-c3)
            c2, c3 = c2 - water, c3 + water
        elif rule == 31:
            water = min(c3, 8-c1)
            c3, c1 = c3 - water, c1 + water
        elif rule == 32:
            water = min(c3, 8-c2)
            c3, c2 = c3 - water, c2 + water
        elif rule == 101:
            c1, p1 = 0, p1 + c1
        elif rule == 102:
            c2, p1 = 0, p1 + c2
        elif rule == 103:
            c3, p1 = 0, p1 + c3
        elif rule == 201:
            c1, p2 = 0, p2 + c1
        elif rule == 202:
            c2, p2 = 0, p2 + c2
        elif rule == 203:
            c3, p2 = 0, p2 + c3
        elif rule == 301:
            c1, p3 = 0, p3 + c1
        elif rule == 302:
            c2, p3 = 0, p3 + c2
        elif rule == 303:
            c3, p3 = 0, p3 + c3
        elif rule == 401:
            c1, p4 = 0, p4 + c1
        elif rule == 402:
            c2, p4 = 0, p4 + c2
        elif rule == 403:
            c3, p4 = 0, p4 + c3
        
        return (c1, c2, c3, p1, p2, p3, p4)       
        
        
        
if __name__ == "__main__":

    import collections
    import time
    start = time.perf_counter()
    rule_map = {12: '8两杯1倒入8两杯2', 13: '8两杯1倒入3两杯', 21: '8两杯2倒入8两杯1', 
                23: '8两杯2倒入3两杯', 31: '3两杯倒入8两杯1', 32: '3两杯倒入8两杯2', 
                101:'人1喝8两杯1的水', 102:'人1喝8两杯2的水', 103:'人1喝3两杯的水',
                201:'人2喝8两杯1的水', 202:'人2喝8两杯2的水', 203:'人2喝3两杯的水',
                301:'人3喝8两杯1的水', 302:'人3喝8两杯2的水', 303:'人3喝3两杯的水',
                401:'人4喝8两杯1的水', 402:'人4喝8两杯2的水', 403:'人4喝3两杯的水'}
    
    s = Node((8,8,0,0,0,0,0), 0)   # 初始状态

    opened = collections.deque([s])
    closed = []
    while opened:
        n = opened.popleft()
        closed.append(n)
        if n.term():
            break
        rules = n.gen_rules()
        for rule in rules:
            child_state = n.gen_child(rule)
            child_depth = n.depth + 1
            flag = True                   # 表示这是一个新的状态，之前未出现过
            for node in opened:
                if node.state == child_state: 
                    flag = False
                    if node.depth > child_depth:    # 如果n产生的子节点深度更浅，修改其父节点为n，更新深度
                        node.depth = child_depth
                        node.parent = n
                        node.parent_rule = rule
                    break
            # if flag:
            #     for node in closed:
            #         if node.state == child_state:
            #             flag = False
            #             if node.depth > child_depth:  
            #                 node.depth = child_depth
            #                 node.parent = n
            #                 node.parent_rule = rule
            if flag:
                child = Node(child_state, child_depth, n, rule)
                opened.append(child)  
                
    while n:   # 从下往上倒着看
        print(n.state, end = ' ')
        if n.parent_rule:
            print(rule_map[n.parent_rule])
        n = n.parent
        
    end = time.perf_counter()
    print('用时：', end-start, 's')