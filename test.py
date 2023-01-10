
import math
import pdla_algorithms as PDLA_A
import pdla_functions as PDLA_F
import numpy as np
import algorithms as ALA_A


nb_experiments = 5
d = 100
mean = 1
shape = 2
length = 1000

def function(x):
    return x/(1-math.exp(-x))

lambdas = [0.6,0.2]
ala_lams = [function(x)-1 for x in lambdas]
print('ala_lam = {}'.format(ala_lams))
replacement_rate =[0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]

iterations_poisson= 1
key = "Poisson"

print('--------------------Poisson---------------------')
print('{0}_iter{1}_mean{2}_Possion'.format(key,iterations_poisson,mean))
Doubling_CR = [ [] for _ in replacement_rate]
ALA_CR = [ [] for _ in replacement_rate]
Blindly_Follow_CR = [ [] for _ in replacement_rate ]
PDLA_CR = [ [] for _ in replacement_rate ]

for p_index, p in enumerate(replacement_rate):
    for i in range(0, nb_experiments):
        np.random.seed(i)
        instance = PDLA_F.instance_generator(mean, length, iterations_poisson, shape, key)
        OPT,sol,OPT_Matrix = ALA_A.TCP_OPT(PDLA_F.agreggate_instance(instance),1.0/d)
        print("===== true instance ======")
        instance_with_noise = PDLA_F.noisy_instance(instance,mean,iterations_poisson, shape, key,p)
        (sol_noisy,OPT_noisy) = PDLA_A.TCP_OFFLINE(instance_with_noise,d)
        print("===== noisy instance ======")
        print("Replacement rate = ", p)
        print("=================")

        cost,double_sol = ALA_A.TCP_2_Competitive(PDLA_F.agreggate_instance(instance),1.0/d)
        print('Greedy CR = {}'.format(1.0*cost/OPT))
        Doubling_CR[p_index].append(1.0*cost/OPT)

        cost,Turn_Points = ALA_A.TCP_Blind_Follow(PDLA_F.agreggate_instance(instance),1.0/d,sol_noisy,predicted_opt_value=OPT_noisy,opt_matrix=OPT_Matrix,lam_list=ala_lams)
        print('Blindly_Follow CR = {}'.format(1.0*cost/OPT))
        Blindly_Follow_CR[p_index].append(1.0*cost/OPT)


        for lam_index, l in enumerate(lambdas):
            LAPD = PDLA_A.ONLINE_LA(instance,d,l,sol_noisy)
            print(" Lambda = ", l, " PDLA CR = ", LAPD/OPT)
            PDLA_CR[p_index].append(1.0*LAPD/OPT)
            ala_lam = ala_lams[lam_index]
            cost,ala_sol,_ = ALA_A.TCP_ALA(PDLA_F.agreggate_instance(instance),1.0/d,PDLA_F.agreggate_instance(instance_with_noise),opt_matrix=OPT_Matrix,turn_point=Turn_Points[lam_index], lam=ala_lam)

            print(' Lambda = {0}, TCP_ALA CR = {1}'.format(ala_lam,1.0*cost/OPT))

            ALA_CR[p_index].append(1.0*cost/OPT)



CR_list = [ Doubling_CR, Blindly_Follow_CR, ALA_CR, PDLA_CR ]
CR_Name_list = [ 'Doubling_CR', 'Blindly_Follow_CR', 'ALA_CR', 'PDLA_CR' ]

with open('{0}_iter{1}_mean{2}_CR.txt'.format(key,iterations_poisson,mean),"w") as file:

    for index in range(len(CR_Name_list)):
        file.write('{0} = {1}\n'.format(CR_Name_list[index], CR_list[index]))



key = "Pareto"
print('--------------------Pareto---------------------')

Doubling_CR = [ [] for _ in replacement_rate]
ALA_CR = [ [] for _ in replacement_rate]
Blindly_Follow_CR = [ [] for _ in replacement_rate ]
PDLA_CR = [ [] for _ in replacement_rate ]

for p_index, p in enumerate(replacement_rate):
    for i in range(0, nb_experiments):
        np.random.seed(i)
        instance = PDLA_F.instance_generator(mean, length, iterations_poisson, shape, key)
        OPT,sol,OPT_Matrix = ALA_A.TCP_OPT(PDLA_F.agreggate_instance(instance),1.0/d)
        print("===== true instance ======")
        instance_with_noise = PDLA_F.noisy_instance(instance,mean,iterations_poisson, shape, key,p)
        (sol_noisy,OPT_noisy) = PDLA_A.TCP_OFFLINE(instance_with_noise,d)
        print("===== noisy instance ======")
        print("Replacement rate = ", p)
        print("=================")

        cost,double_sol = ALA_A.TCP_2_Competitive(PDLA_F.agreggate_instance(instance),1.0/d)
        print('Greedy CR = {}'.format(1.0*cost/OPT))
        Doubling_CR[p_index].append(1.0*cost/OPT)

        cost,Turn_Points = ALA_A.TCP_Blind_Follow(PDLA_F.agreggate_instance(instance),1.0/d,sol_noisy,predicted_opt_value=OPT_noisy,opt_matrix=OPT_Matrix,lam_list=ala_lams)
        print('TCP_Blind_Follow CR = {}'.format(1.0*cost/OPT))
        Blindly_Follow_CR[p_index].append(1.0*cost/OPT)



        for lam_index, l in enumerate(lambdas):
            LAPD = PDLA_A.ONLINE_LA(instance,d,l,sol_noisy)
            print(" Lambda = ", l, " PDLA CR = ", LAPD/OPT)
            PDLA_CR[p_index].append(1.0*LAPD/OPT)
            ala_lam = ala_lams[lam_index]
            cost,ala_sol,_ = ALA_A.TCP_ALA(PDLA_F.agreggate_instance(instance),1.0/d,PDLA_F.agreggate_instance(instance_with_noise),opt_matrix=OPT_Matrix,turn_point=Turn_Points[lam_index], lam=ala_lam)

            print(' Lambda = {0}, TCP_ALA CR = {1}'.format(ala_lam,1.0*cost/OPT))

            ALA_CR[p_index].append(1.0*cost/OPT)


CR_list = [ Doubling_CR, Blindly_Follow_CR, ALA_CR, PDLA_CR ]
CR_Name_list = [ 'Doubling_CR', 'Blindly_Follow_CR', 'ALA_CR', 'PDLA_CR' ]

with open('{}_CR.txt'.format(key),"w") as file:

    for index in range(len(CR_Name_list)):
        file.write('{0} = {1}\n'.format(CR_Name_list[index], CR_list[index]))



iterations_poisson= 10
key = "Poisson"
print('--------------------Iterated Poisson---------------------')
print('{0}_iter{1}_mean{2}_Possion'.format(key,iterations_poisson,mean))
Doubling_CR = [ [] for _ in replacement_rate]
ALA_CR = [ [] for _ in replacement_rate]
Blindly_Follow_CR = [ [] for _ in replacement_rate ]
PDLA_CR = [ [] for _ in replacement_rate ]

for p_index, p in enumerate(replacement_rate):
    for i in range(0, nb_experiments):
        np.random.seed(i)
        instance = PDLA_F.instance_generator(mean, length, iterations_poisson, shape, key)
        OPT,sol,OPT_Matrix = ALA_A.TCP_OPT(PDLA_F.agreggate_instance(instance),1.0/d)
        print("===== true instance ======")
        instance_with_noise = PDLA_F.noisy_instance(instance,mean,iterations_poisson, shape, key,p)
        (sol_noisy,OPT_noisy) = PDLA_A.TCP_OFFLINE(instance_with_noise,d)
        print("===== noisy instance ======")
        print("Replacement rate = ", p)
        print("=================")

        cost,double_sol = ALA_A.TCP_2_Competitive(PDLA_F.agreggate_instance(instance),1.0/d)
        print('TCP_2_Competitive CR = {}'.format(1.0*cost/OPT))
        Doubling_CR[p_index].append(1.0*cost/OPT)

        cost,Turn_Points = ALA_A.TCP_Blind_Follow(PDLA_F.agreggate_instance(instance),1.0/d,sol_noisy,predicted_opt_value=OPT_noisy,opt_matrix=OPT_Matrix,lam_list=ala_lams)
        print('TCP_Blind_Follow CR = {}'.format(1.0*cost/OPT))
        Blindly_Follow_CR[p_index].append(1.0*cost/OPT)




        for lam_index, l in enumerate(lambdas):
            LAPD = PDLA_A.ONLINE_LA(instance,d,l,sol_noisy)
            print(" Lambda = ", l, " PDLA CR = ", LAPD/OPT)
            PDLA_CR[p_index].append(1.0*LAPD/OPT)
            ala_lam = ala_lams[lam_index]
            cost,ala_sol,_ = ALA_A.TCP_ALA(PDLA_F.agreggate_instance(instance),1.0/d,PDLA_F.agreggate_instance(instance_with_noise),opt_matrix=OPT_Matrix,turn_point=Turn_Points[lam_index], lam=ala_lam)

            print(' Lambda = {0}, TCP_ALA CR = {1}'.format(ala_lam,1.0*cost/OPT))

            ALA_CR[p_index].append(1.0*cost/OPT)


CR_list = [ Doubling_CR, Blindly_Follow_CR, ALA_CR, PDLA_CR ]
CR_Name_list = [ 'Doubling_CR', 'Blindly_Follow_CR', 'ALA_CR', 'PDLA_CR']

with open('{0}_iter{1}_mean{2}_CR.txt'.format(key,iterations_poisson,mean),"w") as file:

    for index in range(len(CR_Name_list)):
        file.write('{0} = {1}\n'.format(CR_Name_list[index], CR_list[index]))
