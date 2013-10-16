import math
from numpy import *
from random import random, randint
from time import time
from copy import deepcopy

def length(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def greed(pts):
    solution = [0]
    while len(solution) != len(pts):
        i = solution[len(solution) - 1]
        best, next_v = float('inf'), None
        for j in range(len(pts)):
            if j not in solution and j != i:
                cost = length(pts[i], pts[j])
                if cost < best:
                    best = cost
                    next_v = j
        solution.append(next_v)
    return solution

def cost(solution, pts):
    obj = length(pts[solution[-1]], pts[solution[0]])
    for i in range(len(pts) - 1):
        obj += length(pts[solution[i]], pts[solution[i + 1]])
    return obj

def two_opt(solution, indexs): 
    indexs.sort()
    proxy = solution[0:indexs[0] + 1] + solution[indexs[1]:indexs[0]:-1]\
            + solution[indexs[1] + 1:]
    return proxy
    #proxy = hstack((solution[0:indexs[0] + 1], solution[indexs[1]:indexs[0]:-1]))
    #return hstack((proxy, solution[indexs[1] + 1:]))

def swap(solution, indexs):
    indexs.sort()
    proxy = deepcopy(solution)
    proxy[indexs[0]] = solution[indexs[1]]
    proxy[indexs[1]] = solution[indexs[0]]
    return proxy

def insert_sol(solution, indexs):
    indexs.sort()
    proxy = deepcopy(solution)
    temp = proxy.pop(indexs[0])
    proxy.insert(indexs[1], temp)
    return proxy


def sim_anneal_rand(solution, pts):
    start = time()
    obj = best_obj = cost(solution, pts)
    temp, cool, reheats = 30, .99, 3
    reheat_target = temp/len(solution)
    best_sol, tabu = solution, []
    while temp > .5:
        for iteration in range(169):
            i = j =  randint(0, len(solution) - 1)
            while j == i:
                j = randint(0, len(solution) - 1)
            mode = randint(1, 12)
            proxy = None
            if mode < 9:
                proxy = two_opt(solution, [i, j])
            elif mode < 11:
                proxy = insert_sol(solution, [i, j])
            else:
                proxy = swap(solution, [i, j])
            proxy_obj = cost(proxy, pts)
            if proxy_obj < obj or math.exp((obj-proxy_obj)/temp) > random():
                obj = proxy_obj
                solution = proxy
               # k = j
               # while k == j or k == i:
                #    k = randint(0, len(solution) - 1)
            #else:
                for k in range(len(solution)):
                    if k != i and k!= j:
                        three_opt_sol = two_opt(proxy, [i, k])
                        three_opt_cost = cost(three_opt_sol, pts)
                        if three_opt_cost < obj or \
                           math.exp((obj- three_opt_cost)/temp)>random():
                             obj = three_opt_cost
                             solution = three_opt_sol
        print obj, temp
        if obj < best_obj:
            best_obj = obj
            best_sol = solution
            reheat_target = temp
        elif temp < .8 and reheats > 0:
            temp = reheat_target* 1.33
            reheats -= 1
            print "reheating to " , reheat_target, " best_obj ", best_obj
        if obj > best_obj*1.11:
            temp *= .9
            solution = best_sol
            obj = best_obj
        temp *= cool
        if len(tabu) > len(pts)**1.33:
            tabu.pop(0)
    print 'Time taken ' , time() - start
    return best_sol

def sim_anneal_iter(solution, pts):
    start = time()
    obj = best_obj = cost(solution, pts)
    temp, cool, reheats = 30, .99, 3
    reheat_target = temp/len(solution)
    best_sol, tabu = solution, []
    while temp > .5:
        improved = True
        while improved:
            improved = False
            annealed = False
            for i in range(len(pts) - 1):
               for j in range(i + 1, len(pts)):
                    mode = randint(1, 12)
                    proxy = None
                    if mode < 9:
                        proxy = two_opt(solution, [i, j])
                    elif mode < 11:
                        proxy = insert_sol(solution, [i, j])
                    else:
                        proxy = swap(solution, [i, j])
                    proxy_obj = cost(proxy, pts)
                    if proxy_obj < obj:
                        obj = proxy_obj
                        solution = proxy
                        if not annealed:
                            improved = True
                    elif math.exp((obj-proxy_obj)/temp) > random():
                        obj = proxy_obj
                        solution = proxy
                        improved = False
                        annealed = True
        print obj, temp
        if obj < best_obj:
            best_obj = obj
            best_sol = solution
            reheat_target = temp
        elif temp < .8 and reheats > 0:
            temp = reheat_target* 1.33
            reheats -= 1
            print "reheating to " , reheat_target, " best_obj ", best_obj
        if obj > best_obj*1.11:
            temp *= .9
            solution = best_sol
            obj = best_obj
        temp *= cool
        if len(tabu) > len(pts)**1.33:
            tabu.pop(0)
    print 'Time taken ' , time() - start
    return best_sol

def solve(inputData):
    lines = inputData.split('\n')
    nodeCount = int(lines[0])
    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append((float(parts[0]), float(parts[1])))
    points = array(points)
    solution = greed(points)
    solution = sim_anneal_iter(solution, points)
    obj = cost(solution, points)
    outputData = str(obj) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, solution))

    return outputData


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solve(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'

