
import matplotlib.pyplot as plt
import numpy as np


def draw_CRs_over_Rep(replacement_rate,Algo_mean_list,Algo_std_list,Algo_Names,fname,x_label='Perturbing Probability',y_label = 'Competitive Ratio', position = None):
    plt.cla()

    color_list = ['k','g','r', 'm',  'b','y',  'c','#D2691E','#CEFFCE']#['k','r','b', 'm', 'y', 'g',  ]
    marker_list = ['o', 'v', '^', '<', '>', 's','3','8','|','x'] #['o', 'v', '^', '<', '>', 's']
    plt.xlabel(x_label,fontsize=18)
    plt.ylabel(y_label,fontsize=18)

    for i in range(len(Algo_Names)):
        plt.errorbar(replacement_rate, Algo_mean_list[i], yerr=np.array([x*0.1 for x in Algo_std_list[i]]),ecolor=color_list[i],fmt='none')

        plt.plot(replacement_rate, Algo_mean_list[i], color=color_list[i],linestyle='-', linewidth=1,label = Algo_Names[i]) # marker=marker_list[i]


    if len(Algo_Names) > 1:
        if position == None:
            plt.legend(loc='lower right') #bbox_to_anchor=(0.2, 0.95))
        else:
            plt.legend(loc=position)
    plt.tight_layout()
    plt.savefig(fname, dpi=200)





