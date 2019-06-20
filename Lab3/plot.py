def plotdata():
    import matplotlib.pyplot as plt
    import numpy as np

    x_p = []
    x_l = []
    y_p = []
    y_l = []

    with open('p_results', 'r') as f:
        for line in f.readlines():
            linetab = line.split(',')
            linetab[2] = linetab[2].replace("\n", '')
            x_p += [1-float(linetab[0])]
            y_p += [float(linetab[1])/float(linetab[2])]

    with open('l_results', 'r') as f:
        for line in f.readlines():
            linetab = line.split(',')
            linetab[2] = linetab[2].replace("\n", '')
            x_l += [float(linetab[0])]
            y_l += [float(linetab[1])/float(linetab[2])]

    fig1 = plt.figure()
    ax1_1 = fig1.add_subplot(111)
    ax1_1.plot(x_p, y_p, c='b', marker="s")

    plt.ylabel('Kolizje/Dostarczone')
    plt.xlabel('Prawdopodobienstwo wyslania serii pakietow')

    fig2 = plt.figure()
    ax1_2 = fig2.add_subplot(111)
    ax1_2.plot(x_l, y_l, c='b', marker="s")

    plt.ylabel('Kolizje/Dostarczone')
    plt.xlabel('Dlugosc kabla')

    plt.show()

plotdata()