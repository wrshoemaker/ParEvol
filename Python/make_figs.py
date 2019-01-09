from __future__ import division
import math, os, re
import numpy as np
import pandas as pd
import parevol_tools as pt
import matplotlib.pyplot as plt
from matplotlib import cm, rc_context
import matplotlib.patches as mpatches
from scipy.special import comb
from scipy import stats

from sklearn.decomposition import PCA


def intro_fig():
    #https://github.com/miloharper/visualise-neural-network
    fig = plt.figure()

    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=1)
    f1=7
    omega_font=8

    #plt.gca().add_patch(circle)
    ax1.set_xlim([0,1])
    ax1.set_ylim([0,1])

    ax1_points = [ [0.5, 0, '0000'],
                    [0.125, 0.25, '0001'],
                    [0.375, 0.25, '0010'],
                    [0.625, 0.25, '0100'],
                    [0.875, 0.25, '1000'],
                    [0.0835, 0.5, '0011'],
                    [0.0835 + 0.167, 0.5, '0101'],
                    [0.0835 + (0.167*2), 0.5, '1001'],
                    [0.0835 + (0.167*3), 0.5, '0110'],
                    [0.0835 + (0.167*4), 0.5, '1010'],
                    [0.0835 + (0.167*4), 0.5, '1010'],
                    [0.9165, 0.5, '1100'],
                    [0.125, 0.75, '0111'],
                    [0.375, 0.75, '1011'],
                    [0.625, 0.75, '1101'],
                    [0.875, 0.75, '1110'],
                    [0.5, 1, '1111']]

    for ax1_point in ax1_points:
        ax1.text(ax1_point[0], ax1_point[1], ax1_point[2],
                      ha="center",
                      size=f1,
                      transform=ax1.transAxes,
                      bbox=dict(boxstyle='round', fc="w", ec="k"))


    ax1.plot([0.5,0.125], [0, 0.25], 'k-')
    ax1.plot([0.5,0.375], [0, 0.25], 'k-')
    ax1.plot([0.5,0.625], [0, 0.25], 'k-')
    ax1.plot([0.5,0.875], [0, 0.25], 'k-')

    ax1.plot([0.125,0.0835], [0.25, 0.5], 'k-')
    ax1.plot([0.125,0.0835 + 0.167], [0.25, 0.5], 'k-')
    ax1.plot([0.125,0.0835 + (0.167*2)], [0.25, 0.5], 'k-')

    ax1.plot([0.375,0.0835], [0.25, 0.5], 'k-')
    ax1.plot([0.375,0.0835 + (0.167*3)], [0.25, 0.5], 'k-')
    ax1.plot([0.375,0.0835 + (0.167*4)], [0.25, 0.5], 'k-')

    ax1.plot([0.625,0.0835 + 0.167], [0.25, 0.5], 'k-')
    ax1.plot([0.625,0.0835 + (0.167*3)], [0.25, 0.5], 'k-')
    ax1.plot([0.625,0.9165], [0.25, 0.5], 'k-')

    ax1.plot([0.875,0.0835 + (0.167*2)], [0.25, 0.5], 'k-')
    ax1.plot([0.875,0.0835 + (0.167*4)], [0.25, 0.5], 'k-')
    ax1.plot([0.875,0.9165], [0.25, 0.5], 'k-')

    ax1.plot([0.0835,0.125], [0.5,0.75], 'k-')
    ax1.plot([0.0835,0.375], [0.5,0.75], 'k-')
    ax1.plot([0.0835 + 0.167, 0.125], [0.5,0.75], 'k-')
    ax1.plot([0.0835 + 0.167, 0.625], [0.5,0.75], 'k-')
    ax1.plot([0.0835 + (0.167*2), 0.375], [0.5,0.75], 'k-')
    ax1.plot([0.0835 + (0.167*2), 0.625], [0.5,0.75], 'k-')
    ax1.plot([0.0835 + (0.167*3), 0.125], [0.5,0.75], 'k-')
    ax1.plot([0.0835 + (0.167*3), 0.875], [0.5,0.75], 'k-')
    ax1.plot([0.0835 + (0.167*4), 0.375], [0.5,0.75], 'k-')
    ax1.plot([0.0835 + (0.167*4), 0.875], [0.5,0.75], 'k-')
    ax1.plot([0.9165, 0.625], [0.5,0.75], 'k-')
    ax1.plot([0.9165, 0.875], [0.5,0.75], 'k-')

    ax1.plot([0.125,0.5], [0.75, 1], 'k-')
    ax1.plot([0.375,0.5], [0.75, 1], 'k-')
    ax1.plot([0.625,0.5], [0.75, 1], 'k-')
    ax1.plot([0.875,0.5], [0.75, 1], 'k-')

    ax1.text(-0.24, -0.01, r'$\Omega_{0}\left ( 0 \right )=1$', fontsize = omega_font)
    ax1.text(-0.24, 0.24, r'$\Omega_{0}\left ( 1 \right )=4$', fontsize = omega_font)
    ax1.text(-0.24, 0.49, r'$\Omega_{0}\left ( 2 \right )=6$', fontsize = omega_font)
    ax1.text(-0.24, 0.74, r'$\Omega_{0}\left ( 3 \right )=4$', fontsize = omega_font)
    ax1.text(-0.24, 0.99, r'$\Omega_{0}\left ( 4 \right )=1$', fontsize = omega_font)

    ax1.axis('off')

    ax2 = plt.subplot2grid((2, 2), (0, 1), colspan=1)
    ax2.set_xlim([0,1])
    ax2.set_ylim([0,1])
    y_offset = 0.004
    ax2.text(0.5, 0-y_offset, '       ',
                  ha="center",
                  size=f1+2,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.47, 0, '0',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.53, 0, '0',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))


    ax2.text(0.25, 0.25 -y_offset, ' '*6,
                  ha="center",
                  size=f1+2,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.22, 0.25, '0',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.28, 0.25, '1',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))


    ax2.text(0.75, 0.25 -y_offset, ' '*6,
                  ha="center",
                  size=f1+2,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.72, 0.25, '1',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.78, 0.25, '0',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))


    ax2.text(0.165, 0.5 -y_offset, ' '*6,
                  ha="center",
                  size=f1+2,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.135, 0.5, '0',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.195, 0.5, '2',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))

    ax2.text(0.5, 0.5 -y_offset, ' '*6,
                  ha="center",
                  size=f1+2,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.47, 0.5, '1',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.53, 0.5, '1',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))


    ax2.text(0.835, 0.5 -y_offset, ' '*6,
                  ha="center",
                  size=f1+2,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.805, 0.5, '2',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.865, 0.5, '0',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))



    ax2.text(0.25, 0.75 -y_offset, ' '*6,
                  ha="center",
                  size=f1+2,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.22, 0.75, '1',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.28, 0.75, '2',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))


    ax2.text(0.75, 0.75 -y_offset, ' '*6,
                  ha="center",
                  size=f1+2,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.72, 0.75, '2',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.78, 0.75, '1',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))


    ax2.text(0.5, 1-y_offset, '       ',
                  ha="center",
                  size=f1+2,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.47, 1, '0',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))
    ax2.text(0.53, 1, '0',
                  ha="center",
                  size=f1,
                  transform=ax2.transAxes,
                  bbox=dict(boxstyle='round', fc="w", ec="k"))

    ax2.plot([0.5,0.25], [0, 0.25], 'k-')
    ax2.plot([0.5,0.75], [0, 0.25], 'k-')
    ax2.plot([0.25,0.165], [0.25, 0.5], 'k-')
    ax2.plot([0.25,0.5], [0.25, 0.5], 'k-')
    ax2.plot([0.75,0.5], [0.25, 0.5], 'k-')
    ax2.plot([0.75,0.835], [0.25, 0.5], 'k-')

    ax2.plot([0.165,0.25], [0.5, 0.75], 'k-')
    ax2.plot([0.5,0.25], [0.5, 0.75], 'k-')
    ax2.plot([0.5,0.75], [0.5, 0.75], 'k-')
    ax2.plot([0.835,0.75], [0.5, 0.75], 'k-')
    ax2.plot([0.25,0.5], [0.75, 1], 'k-')
    ax2.plot([0.75,0.5], [0.75, 1], 'k-')

    ax2.text(-0.16, -0.01, r'$\Omega_{1}\left ( 0 \right )=1$', fontsize = omega_font)
    ax2.text(-0.16, 0.24, r'$\Omega_{1}\left ( 1 \right )=2$', fontsize = omega_font)
    ax2.text(-0.16, 0.49, r'$\Omega_{1}\left ( 2 \right )=3$', fontsize = omega_font)
    ax2.text(-0.16, 0.74, r'$\Omega_{1}\left ( 3 \right )=2$', fontsize = omega_font)
    ax2.text(-0.16, 0.99, r'$\Omega_{1}\left ( 4 \right )=1$', fontsize = omega_font)

    ax2.axis('off')

    ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=1)#, aspect='equal')

    L=20
    c1 = [5,5,5,5]
    c2 = [11,5,3,1]
    c3 = [17,1,1,1]
    omega_0 = []
    omega_1_1 = []
    omega_1_2 = []
    omega_1_3 = []
    ks = list(range(L+1))
    for k in ks:
        omega_0.append(int(comb(L, k)))
        omega_1_1.append(pt.comb_n_muts_k_genes(k, c1 ))
        omega_1_2.append(pt.comb_n_muts_k_genes(k, c2 ))
        omega_1_3.append(pt.comb_n_muts_k_genes(k, c3 ))

    plt.plot(ks, np.asarray(omega_1_1)/ np.asarray(omega_0), linestyle='--', lw =2.2, color='#87CEEB', alpha = 0.7, label = r'$\mathcal{L} =  \left \{  5,5,5,5 \right \}$')
    plt.plot(ks, np.asarray(omega_1_2)/ np.asarray(omega_0), linestyle='--', lw =2.2, color='#FFA500', alpha = 0.7, label = r'$\mathcal{L} =  \left \{  11,5,3,1 \right \}$')
    plt.plot(ks, np.asarray(omega_1_3)/ np.asarray(omega_0), linestyle='--', lw =2.2, color='#FF6347', alpha = 0.7, label = r'$\mathcal{L} =  \left \{  17,1,1,1 \right \}$')


    ax3.set_xlabel('Substitutions, ' + r'$k$', fontsize = 16)
    ax3.set_ylabel(r'$\mathrm{log}_{10}   \left (    \Omega_{1} / \Omega_{0} \right )$', fontsize = 15)
    ax3.legend(loc='upper center', fontsize=7)
    ax3.set_yscale("log")


    ax4 = plt.subplot2grid((2, 2), (1, 1), colspan=1)
    c0_ax4 = [20]
    c1_ax4 = [10,10]
    c2_ax4 = [5,5,5,5]
    c3_ax4 = [2,2,2,2,2,2,2,2,2,2]
    omega_0 = []
    omega_1_1_ax4 = []
    omega_1_2_ax4 = []
    omega_1_3_ax4 = []
    omega_1_0_ax4 = []
    ks = list(range(L+1))
    for k in ks:
        omega_0.append(int(comb(L, k)))
        omega_1_1_ax4.append(pt.comb_n_muts_k_genes(k, c1_ax4 ))
        omega_1_2_ax4.append(pt.comb_n_muts_k_genes(k, c2_ax4 ))
        omega_1_3_ax4.append(pt.comb_n_muts_k_genes(k, c3_ax4 ))

        omega_1_0_ax4.append(pt.comb_n_muts_k_genes(k, c0_ax4 ))

    print(omega_1_0_ax4)
    print(omega_1_1_ax4)

    plt.plot(ks, np.asarray(omega_1_1_ax4)/ np.asarray(omega_0), linestyle='--', lw =2.2, color='#FF6347', alpha = 0.7, label=r'$G=2$')
    plt.plot(ks, np.asarray(omega_1_2_ax4)/ np.asarray(omega_0), linestyle='--', lw =2.2, color='#FFA500', alpha = 0.7, label=r'$G=4$')
    plt.plot(ks, np.asarray(omega_1_3_ax4)/ np.asarray(omega_0), linestyle='--', lw =2.2, color='#87CEEB', alpha = 0.7, label=r'$G=10$')

    ax4.set_xlabel('Substitutions, ' + r'$k$', fontsize = 14)
    ax4.set_ylabel(r'$ \mathrm{log}_{10}   \left (    \Omega_{1} / \Omega_{0} \right )$', fontsize = 15)
    ax4.legend(loc='lower left', fontsize=7)
    ax4.set_yscale("log")

    plt.tight_layout()
    fig_name = pt.get_path() + '/figs/test_network.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()





def hist_tenaillon(k = 3):
    df_path = pt.get_path() + '/data/Tenaillon_et_al/gene_by_pop.txt'
    df = pd.read_csv(df_path, sep = '\t', header = 'infer', index_col = 0)
    df_delta = pt.likelihood_matrix(df, 'Tenaillon_et_al').get_likelihood_matrix()
    X = pt.hellinger_transform(df_delta)
    pca = PCA()
    df_out = pca.fit_transform(X)

    df_null_path = pt.get_path() + '/data/Tenaillon_et_al/permute_PCA.txt'
    df_null = pd.read_csv(df_null_path, sep = '\t', header = 'infer', index_col = 0)

    mean_angle = pt.get_mean_angle(df_out, k = k)
    mcd = pt.get_mean_centroid_distance(df_out, k=k)
    #mean_length = pt.get_euclidean_distance(df_out, k=k)
    mean_dist = pt.get_mean_pairwise_euc_distance(df_out, k=k)
    x_stat = pt.get_x_stat(pca.explained_variance_[:-1])

    fig = plt.figure()

    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=1)
    ax1.axhline(y=0, color='k', linestyle=':', alpha = 0.8, zorder=1)
    ax1.axvline(x=0, color='k', linestyle=':', alpha = 0.8, zorder=2)
    ax1.scatter(0, 0, marker = "o", edgecolors='none', c = 'darkgray', s = 120, zorder=3)
    ax1.scatter(df_out[:,0], df_out[:,1], marker = "o", edgecolors='#244162', c = '#175ac6', alpha = 0.4, s = 60, zorder=4)

    ax1.set_xlim([-0.75,0.75])
    ax1.set_ylim([-0.75,0.75])
    ax1.set_xlabel('PCA 1 (' + str(round(pca.explained_variance_ratio_[0],3)*100) + '%)' , fontsize = 14)
    ax1.set_ylabel('PCA 2 (' + str(round(pca.explained_variance_ratio_[1],3)*100) + '%)' , fontsize = 14)


    ax2 = plt.subplot2grid((2, 2), (0, 1), colspan=1)
    mcd_list = df_null.MCD.tolist()
    #ax2.hist(mcd_list, bins=30, histtype='stepfilled', normed=True, alpha=0.6, color='b')
    ax2.hist(mcd_list,bins=30, weights=np.zeros_like(mcd_list) + 1. / len(mcd_list), alpha=0.8, color = '#175ac6')
    ax2.axvline(mcd, color = 'red', lw = 3)
    ax2.set_xlabel("Mean centroid distance, " + r'$ \left \langle \delta_{c}  \right \rangle$', fontsize = 14)
    ax2.set_ylabel("Frequency", fontsize = 16)

    mcd_list.append(mcd)
    relative_position_mcd = sorted(mcd_list).index(mcd) / (len(mcd_list) -1)
    if relative_position_mcd > 0.5:
        p_score_mcd = 1 - relative_position_mcd
    else:
        p_score_mcd = relative_position_mcd
    print('mean centroid distance p-score = ' + str(round(p_score_mcd, 3)))
    ax2.text(0.366, 0.088, r'$p < 0.05$', fontsize = 10)

    ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=1)
    delta_L_list = df_null.mean_dist.tolist()
    #ax3.hist(delta_L_list, bins=30, histtype='stepfilled', normed=True, alpha=0.6, color='b')
    ax3.hist(delta_L_list,bins=30, weights=np.zeros_like(delta_L_list) + 1. / len(delta_L_list), alpha=0.8, color = '#175ac6')
    ax3.axvline(mean_dist, color = 'red', lw = 3)
    ax3.set_xlabel("Mean pair-wise \n Euclidean distance, " + r'$   \left \langle   d \right  \rangle$', fontsize = 14)
    ax3.set_ylabel("Frequency", fontsize = 16)

    delta_L_list.append(mean_dist)
    relative_position_delta_L = sorted(delta_L_list).index(mean_dist) / (len(delta_L_list) -1)
    if relative_position_delta_L > 0.5:
        p_score_delta_L = 1 - relative_position_delta_L
    else:
        p_score_delta_L = relative_position_delta_L
    print('mean difference in distances p-score = ' + str(round(p_score_delta_L, 3)))
    ax3.text(0.50, 0.09, r'$p < 0.05$', fontsize = 10)




    ax4 = plt.subplot2grid((2, 2), (1, 1), colspan=1)
    ax4_values = df_null.x_stat.values
    ax4_values = ax4_values[np.logical_not(np.isnan(ax4_values))]
    #ax4.hist(ax4_values, bins=30, histtype='stepfilled', normed=True, alpha=0.6, color='b')
    ax4.hist(ax4_values, bins=30, weights=np.zeros_like(ax4_values) + 1. / len(ax4_values), alpha=0.8, color = '#175ac6')
    print(np.mean(ax4_values))
    print(stats.mode(ax4_values))

    ax4.axvline(x_stat, color = 'red', lw = 3)
    ax4.set_xlabel(r'$F_{1}$', fontsize = 14)
    ax4.set_ylabel("Frequency", fontsize = 16)

    mean_angle_list = ax4_values.tolist()
    mean_angle_list.append(mean_angle)
    relative_position_angle = sorted(mean_angle_list).index(mean_angle) / (len(mean_angle_list) -1)
    print(x_stat)
    print( len([x for x in mean_angle_list if x > x_stat])/  sum(mean_angle_list)  )
    if relative_position_angle > 0.5:
        p_score_angle = 1 - relative_position_angle
    else:
        p_score_angle = relative_position_angle
    print('F_{1} statistic p-score = ' + str(round(p_score_angle, 3)))
    ax4.text(19.1, 0.09, r'$p \nless  0.05$', fontsize = 10)

    plt.tight_layout()
    fig_name = pt.get_path() + '/figs/fig1.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()


def fig2(alpha = 0.05, k = 3):
    df_path = pt.get_path() + '/data/Tenaillon_et_al/gene_by_pop.txt'
    df = pd.read_csv(df_path, sep = '\t', header = 'infer', index_col = 0)
    df_delta = pt.likelihood_matrix(df, 'Tenaillon_et_al').get_likelihood_matrix()
    X = pt.hellinger_transform(df_delta)
    pca = PCA()
    df_out = pca.fit_transform(X)
    mcd = pt.get_mean_centroid_distance(df_out, k = k)
    mean_angle = pt.get_mean_angle(df_out, k = k)
    mean_length = pt.get_euclidean_distance(df_out, k=k)

    df_sample_path = pt.get_path() + '/data/Tenaillon_et_al/sample_size_permute_PCA.txt'
    df_sample = pd.read_csv(df_sample_path, sep = '\t', header = 'infer')#, index_col = 0)
    sample_sizes = sorted(list(set(df_sample.Sample_size.tolist())))

    fig = plt.figure()
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=2)
    ax2 = plt.subplot2grid((6, 1), (2, 0), rowspan=2)
    ax3 = plt.subplot2grid((6, 1), (4, 0), rowspan=2)
    ax1.axhline(mcd, color = 'darkgray', lw = 3, ls = '--', zorder = 1)
    ax2.axhline(mean_angle, color = 'darkgray', lw = 3, ls = '--', zorder = 1)
    ax3.axhline(mean_length, color = 'darkgray', lw = 3, ls = '--', zorder = 1)
    for sample_size in sample_sizes:
        df_sample_size = df_sample.loc[df_sample['Sample_size'] == sample_size]
        x_sample_size = df_sample_size.Sample_size.values
        y_sample_size_mcd = np.sort(df_sample_size.MCD.values)
        y_sample_size_mean_angle = np.sort(df_sample_size.mean_angle.values)
        y_sample_size_delta_L = np.sort(df_sample_size.delta_L.values)

        lower_ci_mcd = np.mean(y_sample_size_mcd) -    y_sample_size_mcd[int(len(y_sample_size_mcd) * alpha)]
        upper_ci_mcd = abs(np.mean(y_sample_size_mcd) -    y_sample_size_mcd[int(len(y_sample_size_mcd) * (1 - alpha) )])

        lower_ci_angle = np.mean(y_sample_size_mean_angle) -    y_sample_size_mean_angle[int(len(y_sample_size_mean_angle) * alpha)]
        upper_ci_angle = abs(np.mean(y_sample_size_mean_angle) -    y_sample_size_mean_angle[int(len(y_sample_size_mean_angle) * (1 - alpha) )])

        lower_ci_delta_L = np.mean(y_sample_size_delta_L) -    y_sample_size_delta_L[int(len(y_sample_size_delta_L) * alpha)]
        upper_ci_delta_L = abs(np.mean(y_sample_size_delta_L) -    y_sample_size_delta_L[int(len(y_sample_size_delta_L) * (1 - alpha) )])
        with rc_context(rc={'errorbar.capsize': 3}):
            ax1.errorbar(sample_size, np.mean(y_sample_size_mcd), yerr = [np.asarray([lower_ci_mcd]), np.asarray([upper_ci_mcd])], c = 'k', fmt='-o') #, xerr=0.2, yerr=0.4)
            ax2.errorbar(sample_size, np.mean(y_sample_size_mean_angle), yerr = [np.asarray([lower_ci_angle]), np.asarray([upper_ci_angle])], c = 'k', fmt='-o')
            ax3.errorbar(sample_size, np.mean(y_sample_size_delta_L), yerr = [np.asarray([lower_ci_delta_L]), np.asarray([upper_ci_delta_L])], c = 'k', fmt='-o')

    ax3.set_xlabel("Number of replicate populations", fontsize = 16)
    ax1.set_ylabel(r'$\left \langle \delta_{c}  \right \rangle$', fontsize = 14)
    ax2.set_ylabel(r'$\left \langle \theta \right \rangle$', fontsize = 14)
    ax3.set_ylabel(r'$\left \langle  \left | \Delta L \right |\right \rangle$', fontsize = 14)
    fig.tight_layout()
    fig.savefig(pt.get_path() + '/figs/fig2.png', bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()



def fig3(alpha = 0.05, k = 5):
    df_path = pt.get_path() + '/data/Good_et_al/gene_by_pop.txt'
    df = pd.read_csv(df_path, sep = '\t', header = 'infer', index_col = 0)
    to_exclude = pt.complete_nonmutator_lines()
    to_exclude.append('p5')
    df_nonmut = df[df.index.str.contains('|'.join( to_exclude))]
    # remove columns with all zeros
    df_nonmut = df_nonmut.loc[:, (df_nonmut != 0).any(axis=0)]
    df_delta = pt.likelihood_matrix(df_nonmut, 'Good_et_al').get_likelihood_matrix()
    X = pt.hellinger_transform(df_delta)
    pca = PCA()
    df_out = pca.fit_transform(X)

    time_points = [ int(x.split('_')[1]) for x in df_nonmut.index.values]
    time_points_set = sorted(list(set([ int(x.split('_')[1]) for x in df_nonmut.index.values])))

    df_rndm_delta_out = pd.DataFrame(data=df_out, index=df_delta.index)
    mcds = []
    angles = []
    Ls = []
    for tp in time_points_set:
        df_rndm_delta_out_tp = df_rndm_delta_out[df_rndm_delta_out.index.str.contains('_' + str(tp))]
        mcds.append(pt.get_mean_centroid_distance(df_rndm_delta_out_tp.as_matrix(), k=k))
        angles.append(pt.get_mean_angle(df_rndm_delta_out_tp.as_matrix(), k=k))
        Ls.append(pt.get_euclidean_distance(df_rndm_delta_out_tp.as_matrix(), k=k))

    perm_path = pt.get_path() + '/data/Good_et_al/permute_PCA.txt'
    perm = pd.read_csv(perm_path, sep = '\t', header = 'infer', index_col = 0)
    perm_gens = np.sort(list(set(perm.Generation.tolist())))
    lower_ci_mcd = []
    upper_ci_mcd = []
    lower_ci_angle = []
    upper_ci_angle = []
    lower_ci_L = []
    upper_ci_L = []
    mean_mcd = []
    mean_angle = []
    mean_L = []
    for x in perm_gens:
        perm_x = perm.loc[perm['Generation'] == x]
        mcd_perm_x = np.sort(perm_x.MCD.tolist())
        angle_perm_x = np.sort(perm_x.mean_angle.tolist())
        L_perm_x = np.sort(perm_x.delta_L.tolist())

        mean_mcd_perm_x = np.mean(mcd_perm_x)
        mean_mcd.append(mean_mcd_perm_x)
        mean_angle_perm_x = np.mean(angle_perm_x)
        mean_angle.append(mean_angle_perm_x)
        mean_L_perm_x = np.mean(L_perm_x)
        mean_L.append(mean_L_perm_x)

        lower_ci_mcd.append(mean_mcd_perm_x - mcd_perm_x[int(len(mcd_perm_x) * alpha)])
        upper_ci_mcd.append(abs(mean_mcd_perm_x - mcd_perm_x[int(len(mcd_perm_x) * (1 - alpha))]))

        lower_ci_angle.append(mean_angle_perm_x - angle_perm_x[int(len(angle_perm_x) * alpha)])
        upper_ci_angle.append(abs(mean_angle_perm_x - angle_perm_x[int(len(angle_perm_x) * (1 - alpha))]))

        lower_ci_L.append(mean_L_perm_x - L_perm_x[int(len(L_perm_x) * alpha)])
        upper_ci_L.append(abs(mean_L_perm_x - L_perm_x[int(len(L_perm_x) * (1 - alpha))]))

    fig = plt.figure()

    plt.figure(1)
    plt.subplot(311)
    plt.errorbar(perm_gens, mean_mcd, yerr = [lower_ci_mcd, upper_ci_mcd], fmt = 'o', alpha = 0.5, \
        barsabove = True, marker = '.', mfc = 'k', mec = 'k', c = 'k', zorder=1)
    plt.scatter(time_points_set, mcds, c='#175ac6', marker = 'o', s = 70, \
        edgecolors='#244162', linewidth = 0.6, alpha = 0.5, zorder=2)#, edgecolors='none')

    #plt.ylabel("Mean \n centroid distance", fontsize = 10)
    plt.ylabel(r'$\left \langle \delta_{c}  \right \rangle$', fontsize = 12)

    plt.figure(1)
    plt.subplot(312)
    plt.errorbar(perm_gens, mean_angle, yerr = [lower_ci_angle, upper_ci_angle], fmt = 'o', alpha = 0.5, \
        barsabove = True, marker = '.', mfc = 'k', mec = 'k', c = 'k', zorder=1)
    plt.scatter(time_points_set, angles, c='#175ac6', marker = 'o', s = 70, \
        edgecolors='#244162', linewidth = 0.6, alpha = 0.5, zorder=2)#, edgecolors='none')

    #plt.ylabel("Standardized mean \n centroid distance", fontsize = 14)
    plt.ylabel(r'$\left \langle \theta \right \rangle$', fontsize = 12)

    plt.figure(1)
    plt.subplot(313)
    plt.errorbar(perm_gens, mean_L, yerr = [lower_ci_L, upper_ci_L], fmt = 'o', alpha = 0.5, \
        barsabove = True, marker = '.', mfc = 'k', mec = 'k', c = 'k', zorder=1)
    plt.scatter(time_points_set, Ls, c='#175ac6', marker = 'o', s = 70, \
        edgecolors='#244162', linewidth = 0.6, alpha = 0.5, zorder=2)#, edgecolors='none')

    plt.xlabel("Time (generations)", fontsize = 16)
    #plt.ylabel("Standardized mean \n centroid distance", fontsize = 14)
    plt.ylabel(r'$\left \langle  \left | \Delta L \right |\right \rangle$', fontsize = 12)

    fig.tight_layout()
    fig.savefig(pt.get_path() + '/figs/fig3.png', bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()




def plot_permutation(dataset, analysis = 'PCA', alpha = 0.05):
    if dataset == 'tenaillon':
        df_path = pt.get_path() + '/data/Tenaillon_et_al/gene_by_pop.txt'
        df = pd.read_csv(df_path, sep = '\t', header = 'infer', index_col = 0)
        df_delta = pt.likelihood_matrix(df, 'Tenaillon_et_al').get_likelihood_matrix()
        if analysis == 'PCA':
            X = pt.hellinger_transform(df_delta)
            pca = PCA()
            df_out = pca.fit_transform(X)
        elif analysis == 'cMDS':
            df_delta_bc = np.sqrt(pt.get_scipy_bray_curtis(df_delta.as_matrix()))
            df_out = pt.cmdscale(df_delta_bc)[0]

        mcd = pt.get_mean_centroid_distance(df_out, k = 3)

        mcd_perm_path = pt.get_path() + '/data/Tenaillon_et_al/permute_' + analysis + '.txt'
        mcd_perm = pd.read_csv(mcd_perm_path, sep = '\t', header = 'infer', index_col = 0)
        mcd_perm_list = mcd_perm.MCD.tolist()
        iterations = len(mcd_perm_list)
        mcd_perm_list.append(mcd)
        relative_position = sorted(mcd_perm_list).index(mcd) / iterations
        if relative_position > 0.5:
            p_score = 1 - (sorted(mcd_perm_list).index(mcd) / iterations)
        else:
            p_score = (sorted(mcd_perm_list).index(mcd) / iterations)
        print(p_score)

        fig = plt.figure()
        plt.hist(mcd_perm_list, bins=30, histtype='stepfilled', normed=True, alpha=0.6, color='b')
        plt.axvline(mcd, color = 'red', lw = 3)
        plt.xlabel("Mean centroid distance", fontsize = 18)
        plt.ylabel("Frequency", fontsize = 18)
        fig.tight_layout()
        plot_out = pt.get_path() + '/figs/permutation_hist_tenaillon_' + analysis + '.png'
        fig.savefig(plot_out, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
        plt.close()

    elif dataset == 'good':
        df_path = pt.get_path() + '/data/Good_et_al/gene_by_pop.txt'
        df = pd.read_csv(df_path, sep = '\t', header = 'infer', index_col = 0)
        to_exclude = pt.complete_nonmutator_lines()
        to_exclude.append('p5')
        df_nonmut = df[df.index.str.contains('|'.join( to_exclude))]
        # remove columns with all zeros
        df_nonmut = df_nonmut.loc[:, (df_nonmut != 0).any(axis=0)]
        df_delta = pt.likelihood_matrix(df_nonmut, 'Good_et_al').get_likelihood_matrix()
        if analysis == 'PCA':
            X = pt.hellinger_transform(df_delta)
            pca = PCA()
            df_out = pca.fit_transform(X)
        elif analysis == 'cMDS':
            df_delta_bc = np.sqrt(pt.get_scipy_bray_curtis(df_delta.as_matrix()))
            df_out = pt.cmdscale(df_delta_bc)[0]

        time_points = [ int(x.split('_')[1]) for x in df_nonmut.index.values]
        time_points_set = sorted(list(set([ int(x.split('_')[1]) for x in df_nonmut.index.values])))

        df_rndm_delta_out = pd.DataFrame(data=df_out, index=df_delta.index)
        mcds = []
        for tp in time_points_set:
            df_rndm_delta_out_tp = df_rndm_delta_out[df_rndm_delta_out.index.str.contains('_' + str(tp))]
            mcds.append(pt.get_mean_pairwise_euc_distance(df_rndm_delta_out_tp.as_matrix(), k=3))

        mcd_perm_path = pt.get_path() + '/data/Good_et_al/permute_' + analysis + '.txt'
        mcd_perm = pd.read_csv(mcd_perm_path, sep = '\t', header = 'infer', index_col = 0)
        mcd_perm_x = np.sort(list(set(mcd_perm.Generation.tolist())))
        lower_ci = []
        upper_ci = []
        mean_mcds = []
        std_mcds = []
        lower_z_ci = []
        upper_z_ci = []
        for x in mcd_perm_x:
            mcd_perm_y = mcd_perm.loc[mcd_perm['Generation'] == x]
            mcd_perm_y_sort = np.sort(mcd_perm_y.mean_dist.tolist())
            mean_mcd_perm_y = np.mean(mcd_perm_y_sort)
            std_mcd_perm_y = np.std(mcd_perm_y_sort)
            mean_mcds.append(mean_mcd_perm_y)
            std_mcds.append(std_mcd_perm_y)
            lower_ci.append(mean_mcd_perm_y - mcd_perm_y_sort[int(len(mcd_perm_y_sort) * alpha)])
            upper_ci.append(abs(mean_mcd_perm_y - mcd_perm_y_sort[int(len(mcd_perm_y_sort) * (1 - alpha))]))
            # z-scores
            mcd_perm_y_sort_z = [ ((i - mean_mcd_perm_y) /  std_mcd_perm_y) for i in mcd_perm_y_sort]
            lower_z_ci.append(abs(mcd_perm_y_sort_z[int(len(mcd_perm_y_sort_z) * alpha)]))
            upper_z_ci.append(abs(mcd_perm_y_sort_z[int(len(mcd_perm_y_sort_z) * (1 - alpha))]))

        fig = plt.figure()

        plt.figure(1)
        plt.subplot(211)
        plt.errorbar(mcd_perm_x, mean_mcds, yerr = [lower_ci, upper_ci], fmt = 'o', alpha = 0.5, \
            barsabove = True, marker = '.', mfc = 'k', mec = 'k', c = 'k', zorder=1)
        plt.scatter(time_points_set, mcds, c='#175ac6', marker = 'o', s = 70, \
            edgecolors='#244162', linewidth = 0.6, alpha = 0.5, zorder=2)#, edgecolors='none')

        #plt.xlabel("Time (generations)", fontsize = 16)
        #plt.ylabel("Mean \n Euclidean distance", fontsize = 14)
        plt.ylabel("Mean pair-wise \n Euclidean \n distance, " + r'$   \left \langle   d \right  \rangle$', fontsize = 14)


        plt.figure(1)
        plt.subplot(212)
        plt.errorbar(mcd_perm_x, [0] * len(mcd_perm_x), yerr = [lower_z_ci, upper_z_ci], fmt = 'o', alpha = 0.5, \
            barsabove = True, marker = '.', mfc = 'k', mec = 'k', c = 'k', zorder=1)
        # zip mean, std, and measured values to make z-scores
        zip_list = list(zip(mean_mcds, std_mcds, mcds))
        z_scores = [((i[2] - i[0]) / i[1]) for i in zip_list ]
        plt.scatter(time_points_set, z_scores, c='#175ac6', marker = 'o', s = 70, \
            edgecolors='#244162', linewidth = 0.6, alpha = 0.5, zorder=2)#, edgecolors='none')
        plt.ylim(-2.2, 2.2)
        #plt.axhline(0, color = 'k', lw = 2, ls = '-')
        #plt.axhline(-1, color = 'dimgrey', lw = 2, ls = '--')
        #plt.axhline(-2, color = 'dimgrey', lw = 2, ls = ':')
        plt.xlabel("Time (generations)", fontsize = 16)

        plt.ylabel("Standardized mean \n pair-wise Euclidean \n distance, " + r'$   z_{\left \langle   d \right  \rangle}$', fontsize = 14)
        #plt.ylabel("Standardized mean \n Euclidean distance", fontsize = 14)

        fig.tight_layout()
        fig.savefig(pt.get_path() + '/figs/permutation_scatter_good.png', bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
        plt.close()

    else:
        print('Dataset argument not accepted')


#def mean_euc_dist_fig():
#plot_permutation(dataset='good')

#fig1()
hist_tenaillon()
