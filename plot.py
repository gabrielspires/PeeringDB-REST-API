from statsmodels.distributions.empirical_distribution import ECDF
from matplotlib import pyplot as plt
import pandas as pd
# import numpy as np


def main():
    df = pd.read_csv('analise1.csv', sep='\t', names=['id', 'name', 'ass'])
    plotECDF(df['ass'], filename='plot1.png')


def plotECDF(data, scale_x="linear", scale_y="linear", filename=None):
    ecdf = ECDF(data)
    x, y = ecdf.x, ecdf.y


    for a in x:
        for b in y:
            #if a > 0:
            print(b,a, end="\r\n")


    fig = plt.figure()
    plt.plot(x, y, 'o-')
    plt.ylabel("Pr(X $\leq$ x)")
    plt.xlabel("x")
    plt.xscale(scale_x)
    plt.yscale(scale_y)
    # plt.show()
    if filename:
        fig.savefig(filename, dpi=150)


if __name__ == '__main__':
    main()
