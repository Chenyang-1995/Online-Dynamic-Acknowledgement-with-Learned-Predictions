import random
import numpy as np
import math
from collections import defaultdict

def TCP_OPT(input_instance, d):

    total_length = len(input_instance)

    opt_value = [math.inf for _ in range(total_length)]

    opt_solution = [ [] for _ in range(total_length) ]

    for index in range(total_length):
        if index == 0:
            opt_value[index] = 1
            opt_solution[index] = [index]
        else:
            opt_value[index] = sum([input_instance[i]*d*(index-i)  for i in range(index)]) + 1
            opt_solution[index] = [index]

            for j in range(index):
                tmp_value = opt_value[j] + sum([input_instance[i]*d*(index-i)  for i in range(j+1,index)]) + 1
                if tmp_value < opt_value[index]:
                    opt_value[index] = tmp_value
                    opt_solution[index] = opt_solution[j] + [index]


    return  opt_value[total_length-1], opt_solution[total_length-1], opt_value

def TCP_2_Competitive(input_instance, d):

    total_length = len(input_instance)

    solution = []
    value = 0

    for index in range(total_length):
        if index == 0:
            current_delay_cost = 0
            current_num_packages = 0

        current_delay_cost += current_num_packages*d

        current_num_packages += input_instance[index]

        if index == total_length-1:
            value = value + current_delay_cost + 1
            solution.append(index)

        if current_delay_cost + current_num_packages*d > 1:
            value = value + current_delay_cost + 1
            solution.append(index)
            current_delay_cost = 0
            current_num_packages = 0


    return value, solution

def Relax_Solution(input_instance,d,solution,lam):
    relaxed_solution = solution.copy()
    interval_cost = []
    total_length = len(input_instance)

    current_delay_cost = 0
    current_num_packages = 0

    for time_index in range(total_length):
        current_delay_cost += current_num_packages*d
        if time_index in relaxed_solution:
            interval_cost.append(current_delay_cost+1)
            current_delay_cost = 0
            current_num_packages = 0
            continue
        current_num_packages += input_instance[time_index]
        next_ack = min([ack for ack in relaxed_solution if ack > time_index])
        remaining_delay_cost = current_num_packages*(next_ack-time_index)*d
        if remaining_delay_cost > 1-lam:
            relaxed_solution.append(time_index)
            interval_cost.append(current_delay_cost+1)
            current_delay_cost = 0
            current_num_packages = 0
    relaxed_solution.sort()

    return relaxed_solution, interval_cost

def Pre_Follow(input_instance, d,predicted_solution, opt_matrix, lam):
    total_length = len(input_instance)
    predicted_solution.sort()
    if predicted_solution[-1] != total_length - 1:
        predicted_solution.append(total_length-1)

    interval_cost = []
    solution  = []
    current_delay_cost = 0
    current_num_packages = 0
    for time_index in range(total_length):
        current_delay_cost += current_num_packages*d
        current_num_packages += input_instance[time_index]
        if time_index in predicted_solution:
            interval_cost.append(current_delay_cost + 1)
            solution.append(time_index)
            current_delay_cost = 0
            current_num_packages = 0
            if sum(interval_cost) > (1.0+lam)*opt_matrix[time_index]:
                break

    return solution


def ALA_One_Interval(input_instance,d, predicted_ack, predicted_budget, lam,is_last=False):
    total_length = len(input_instance)
    current_delay_cost = 0
    current_num_ack = 0
    current_num_packages = 0
    tmp_ddl = total_length
    predicted_budget = (1.0+lam)*predicted_budget
    time_index = 0
    solution = []
    used_up = 0
    flag_phase2 = 0

    while time_index < total_length:
        current_delay_cost += current_num_packages * d
        current_num_packages += input_instance[time_index]
        if used_up == 0:
            next_delay_cost = current_delay_cost + current_num_packages*d
            next_num_ack = current_num_ack + 1
            #if next_delay_cost + next_num_ack > predicted_budget or
            if (time_index >= predicted_ack and next_delay_cost + next_num_ack > predicted_budget ):
                solution.append(time_index)
                current_delay_cost = 0
                current_num_ack = 0
                current_num_packages = 0
                tmp_ddl = total_length
                #if is_last == False:
                #    break
                used_up = 1

            #'''
            else: #time_index <= predicted_ack:
                
                if current_num_packages > 0:
                    current_ddl = int(1.0/(current_num_packages*d) ) + time_index
                    tmp_ddl = min(current_ddl,tmp_ddl)
                if time_index >= tmp_ddl:
                    solution.append(time_index)
                    print(10000+time_index)
                    current_num_ack += 1
                    tmp_ddl = total_length
                    current_num_packages = 0
                    if next_delay_cost + next_num_ack > predicted_budget:
                        current_delay_cost = 0
                        current_num_ack = 0
                        current_num_packages = 0
                        tmp_ddl = total_length
                        #if is_last == False:
                        #    break
                        used_up = 1
            #'''

        else:

            if current_delay_cost <= 0 and time_index > predicted_ack and is_last == False:
                break


            '''
            
            '''
            flag_phase2 = 0
            next_delay_cost = current_delay_cost + current_num_packages*d
            if next_delay_cost > 1:
                print(time_index)
                solution.append(time_index)
                current_delay_cost = 0
                current_num_packages = 0





        time_index += 1

    if len(solution) == 0:
        solution.append(time_index-1)
    elif time_index-1 > solution[-1]:
        solution.append(time_index-1)

    return solution, flag_phase2


def TCP_ALA(input_instance,d,predicted_instance,opt_matrix, turn_point, lam):
    _,predicted_opt_solution,_ = TCP_OPT(predicted_instance,d)
    predicted_relaxed_opt_solution,predicted_relaxed_interval_cost = Relax_Solution(predicted_instance,d,predicted_opt_solution,lam=0)
    total_length = len(input_instance)
    if predicted_relaxed_opt_solution[-1] != total_length - 1:
        predicted_relaxed_opt_solution.append(total_length-1)
        predicted_relaxed_interval_cost.append(lam)
    time_index = 0
    solution = []
    #solution = Pre_Follow(input_instance,d,predicted_relaxed_opt_solution,opt_matrix,lam)
    #time_index = solution[-1] + 1

    while len(predicted_relaxed_opt_solution) > 1 and predicted_relaxed_opt_solution[0] < time_index:
        predicted_relaxed_opt_solution.pop(0)
        predicted_relaxed_interval_cost.pop(0)

    if time_index < total_length:



        predicted_ack = predicted_relaxed_opt_solution[0]
        predicted_budget = predicted_relaxed_interval_cost[0]
        if len(predicted_relaxed_opt_solution) == 1:
            is_last = True
        else:
            is_last = False




        while time_index < total_length:
            #print("time_index = {0}, current_budget = {1}".format(time_index,predicted_budget))
            tmp_solution, flag_phase2 = ALA_One_Interval(input_instance[time_index:],
                                                         d,
                                                         predicted_ack,
                                                         predicted_budget,
                                                         lam,
                                                         is_last)
            for ack in tmp_solution:
                solution.append(ack+time_index)



            time_index = solution[-1] + 1
            if time_index >= turn_point:
                print('time_index = {0}; turn_point = {1}'.format(time_index,turn_point))
                break




            if is_last == True:
                assert time_index == total_length, print('time_index = {0}, total_length = {1}'.format(time_index,total_length))
                break
            if flag_phase2 == 1:
                last_ack = predicted_relaxed_opt_solution.pop(0) + 1
                predicted_relaxed_interval_cost.pop(0)

            else:
                last_ack = predicted_relaxed_opt_solution.pop(0) + 1
                predicted_relaxed_interval_cost.pop(0)
                while len(predicted_relaxed_opt_solution) > 1 and predicted_relaxed_opt_solution[0] < time_index:
                    predicted_relaxed_opt_solution.pop(0)
                    predicted_relaxed_interval_cost.pop(0)
            predicted_ack = predicted_relaxed_opt_solution[0] - time_index
            predicted_len = len(predicted_instance)
            predicted_budget = 1+sum([ predicted_instance[t]*d*(predicted_relaxed_opt_solution[0]-t) for t in range(max(time_index,last_ack),min(predicted_relaxed_opt_solution[0],predicted_len-1)) ])#predicted_relaxed_interval_cost[0]

            if len(predicted_relaxed_opt_solution) == 1:
                is_last = True
            else:
                is_last = False


        if time_index < total_length:
            _,remaining_solution = TCP_2_Competitive(input_instance[time_index:],d)
            for ack in remaining_solution:
                if ack+time_index not in solution:
                    solution.append(ack+time_index)

    interval_cost = []
    current_delay_cost = 0
    current_num_packages = 0
    for time_index in range(total_length):
        current_delay_cost += current_num_packages*d
        current_num_packages += input_instance[time_index]
        if time_index in solution:
            interval_cost.append(current_delay_cost + 1)
            current_delay_cost = 0
            current_num_packages = 0


    return sum(interval_cost),solution, interval_cost



def TCP_Blind_Follow(input_instance,d,predicted_solution,predicted_opt_value,opt_matrix,lam_list):
    total_length = len(input_instance)
    predicted_solution.sort()
    if predicted_solution[-1] != total_length - 1:
        predicted_solution.append(total_length-1)

    interval_cost = []
    current_delay_cost = 0
    current_num_packages = 0
    turn_points = [total_length for _ in lam_list]
    for time_index in range(total_length):
        current_delay_cost += current_num_packages*d
        current_num_packages += input_instance[time_index]
        if time_index in predicted_solution:
            interval_cost.append(current_delay_cost + 1)

            for lam_index,lam in enumerate(lam_list):
                #print(sum(interval_cost) -opt_matrix[time_index])
                if sum(interval_cost) -opt_matrix[time_index] > lam*(1-lam)*predicted_opt_value:#(1.0+lam)*opt_matrix[time_index]: #or opt_matrix[time_index] > (1.0+lam)*sum(interval_cost):
                    turn_points[lam_index] = min(turn_points[lam_index],time_index)
            #print('interval_cost = {0}, interval_value = {1}, opt_matrix = {2}, turn_point = {3}'.format(interval_cost,sum(interval_cost),opt_matrix[time_index],turn_point))
            current_delay_cost = 0
            current_num_packages = 0
    print(turn_points)
    return sum(interval_cost), turn_points























def TCP_ALA_old(input_instance,d,predicted_instance,lam):
    _,predicted_opt_solution = TCP_OPT(predicted_instance,d)
    predicted_relaxed_opt_solution,predicted_relaxed_interval_cost = Relax_Solution(predicted_instance,d,predicted_opt_solution,lam)
    total_length = len(input_instance)

    predicted_ack = predicted_relaxed_opt_solution[0]
    predicted_budget = predicted_relaxed_interval_cost[0]
    if len(predicted_relaxed_opt_solution) == 1:
        is_last = True
    else:
        is_last = False
    time_index = 0
    solution = []

    while time_index < total_length:
        #print("time_index = {0}, current_budget = {1}".format(time_index,predicted_budget))
        tmp_solution, flag_phase2 = ALA_One_Interval(input_instance[time_index:],
                                                     d,
                                                     predicted_ack,
                                                     predicted_budget,
                                                     lam,
                                                     is_last)
        for ack in tmp_solution:
            solution.append(ack+time_index)
        time_index = solution[-1] + 1
        if is_last == True:
            assert time_index == total_length, print('time_index = {0}, total_length = {1}'.format(time_index,total_length))
            break
        if flag_phase2 == 1:
            predicted_relaxed_opt_solution.pop(0)
            predicted_relaxed_interval_cost.pop(0)

        else:
            predicted_relaxed_opt_solution.pop(0)
            predicted_relaxed_interval_cost.pop(0)
        predicted_ack = predicted_relaxed_opt_solution[0] - time_index
        predicted_budget = predicted_relaxed_interval_cost[0]
        if len(predicted_relaxed_opt_solution) == 1:
            is_last = True
        else:
            is_last = False

    interval_cost = []
    current_delay_cost = 0
    current_num_packages = 0
    for time_index in range(total_length):
        current_delay_cost += current_num_packages*d
        current_num_packages += input_instance[time_index]
        if time_index in solution:
            interval_cost.append(current_delay_cost + 1)
            current_delay_cost = 0
            current_num_packages = 0


    return sum(interval_cost),solution, interval_cost

















def ALA_One_Interval_original(input_instance,d, predicted_ack, predicted_budget, lam,is_last=False):
    total_length = len(input_instance)
    current_delay_cost = 0
    current_num_ack = 0
    current_num_packages = 0
    tmp_ddl = total_length
    predicted_budget = (1.0+lam)*predicted_budget
    time_index = 0
    solution = []
    used_up = 0
    flag_phase2 = 0
    while time_index < total_length:
        current_delay_cost += current_num_packages * d
        current_num_packages += input_instance[time_index]
        if used_up == 0:
            next_delay_cost = current_delay_cost + current_num_packages*d
            next_num_ack = current_num_ack + 1
            if next_delay_cost + next_num_ack > predicted_budget:
                solution.append(time_index)
                current_delay_cost = 0
                current_num_ack = 0
                current_num_packages = 0
                used_up = 1

            elif time_index <= predicted_ack:
                if current_num_packages > 0:
                    current_ddl = int(1.0/(current_num_packages*d) ) + time_index
                    tmp_ddl = min(current_ddl,tmp_ddl)
                if time_index >= tmp_ddl:
                    solution.append(time_index)
                    current_num_ack += 1
                    tmp_ddl = total_length
                    current_num_packages = 0
        else:
            if time_index > predicted_ack and is_last == False:
                break
            else:
                flag_phase2 = 1
                next_delay_cost = current_delay_cost + current_num_packages*d
                if next_delay_cost > 1:
                    solution.append(time_index)
                    current_delay_cost = 0
                    current_num_packages = 0


        time_index += 1

    if time_index-1 not in solution:
        solution.append(time_index-1)

    return solution, flag_phase2


def TCP_ALA_original(input_instance,d,predicted_instance,lam):
    _,predicted_opt_solution = TCP_OPT(predicted_instance,d)
    predicted_relaxed_opt_solution,predicted_relaxed_interval_cost = Relax_Solution(predicted_instance,d,predicted_opt_solution,lam)
    total_length = len(input_instance)

    predicted_ack = predicted_relaxed_opt_solution[0]
    predicted_budget = predicted_relaxed_interval_cost[0]
    if len(predicted_relaxed_opt_solution) == 1:
        is_last = True
    else:
        is_last = False
    time_index = 0
    solution = []

    while time_index < total_length:
        print("time_index = {0}, current_budget = {1}".format(time_index,predicted_budget))
        tmp_solution, flag_phase2 = ALA_One_Interval(input_instance[time_index:],
                                                     d,
                                                     predicted_ack,
                                                     predicted_budget,
                                                     lam,
                                                     is_last)
        for ack in tmp_solution:
            solution.append(ack+time_index)
        time_index = solution[-1] + 1
        if is_last == True:
            assert time_index == total_length, print('time_index = {0}, total_length = {1}'.format(time_index,total_length))
            break
        if flag_phase2 == 1:
            predicted_relaxed_opt_solution.pop(0)
            predicted_relaxed_interval_cost.pop(0)

        else:
            _,predicted_opt_solution = TCP_OPT(predicted_instance[time_index:],d)
            predicted_relaxed_opt_solution,predicted_relaxed_interval_cost = Relax_Solution(predicted_instance[time_index:],d,predicted_opt_solution,lam)
            predicted_relaxed_opt_solution = [x+time_index for x in predicted_relaxed_opt_solution]

        predicted_ack = predicted_relaxed_opt_solution[0] - time_index
        predicted_budget = predicted_relaxed_interval_cost[0]
        if len(predicted_relaxed_opt_solution) == 1:
            is_last = True
        else:
            is_last = False

    interval_cost = []
    current_delay_cost = 0
    current_num_packages = 0
    for time_index in range(total_length):
        current_delay_cost += current_num_packages*d
        current_num_packages += input_instance[time_index]
        if time_index in solution:
            interval_cost.append(current_delay_cost + 1)
            current_delay_cost = 0
            current_num_packages = 0


    return solution, interval_cost