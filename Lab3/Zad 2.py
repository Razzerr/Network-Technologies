import random

class ethernet:
    def __init__(self, length):
        self.length = length
        self.stats = [0, 0, 0]
        self.lInject = []
        self.rInject = []
        self.probOfSending = 0.99

        self.cableSim = []
        for i in range(0, self.length):
            self.cableSim += [[0, 0]]

    def lgen(self, cycles):
        for i in range(0, int(cycles/2)):
            if random.random() > self.probOfSending:
                for j in range(0, random.randint(2, 16)):
                    self.lInject += [1]
            else: 
                self.lInject += [0]


    def rgen(self, cycles):
        for i in range(0, int(cycles/2)):
            if random.random() > self.probOfSending:
                for j in range(0, random.randint(2, 16)):
                    self.rInject += [1]
            else: 
                self.rInject += [0]

    def cycle(self):
        self.stats[0] += 1

        for i in range(self.length-1, -1, -1):
            if self.cableSim[i][1] == 1:
                if i<self.length-1:
                    if self.cableSim[i+1][1] == 0:
                        self.cableSim[i+1][0] = 1
                        self.cableSim[i+1][1] = 1
                        self.cableSim[i] = [0, 0]
                    else:
                        self.cableSim[i] = [0, 0]
                        self.cableSim[i+1] = [0, 0]
                        self.stats[1] += 1
                else:
                    self.cableSim[i] = [0, 0]
                    self.stats[2] += 1
        for i in range(0, self.length):
            if self.cableSim[i][1] == -1:
                if i>0:
                    if self.cableSim[i-1][1] == 0:
                        self.cableSim[i-1][0] = 1
                        self.cableSim[i-1][1] = -1
                        self.cableSim[i] = [0, 0]
                    else:
                        self.cableSim[i] = [0, 0]
                        self.cableSim[i-1] = [0, 0]
                        self.stats[1] += 1
                else:
                    self.cableSim[i] = [0, 0]
                    self.stats[2] += 1
        
        if len(self.rInject) > 0 and self.rInject[0] == 1 and self.cableSim[self.length-1][1]==0:
            self.cableSim[self.length-1][0] = self.rInject[0]
            self.cableSim[self.length-1][1] = -1
            self.rInject = self.rInject[1:]
        elif len(self.rInject) > 0 and self.rInject[0] == 0:
            self.rInject = self.rInject[1:]
        
        if len(self.lInject) > 0 and self.lInject[0] == 1 and self.cableSim[0][1]==0:
            self.cableSim[0][0] = self.lInject[0]
            self.cableSim[0][1] = 1
            self.lInject = self.lInject[1:]
        elif len(self.lInject) > 0 and self.lInject[0] == 0:
            self.lInject = self.lInject[1:]
                
def main():
    #checking different p for n = 1000, l = 100
    #results: prob, crashed, delivered
    cycles = 1000
    p_results = []
    for k in range(0, 10):
        p_results += [[0.99-k/100, 0, 0]]
        for j in range(0, 100):
            eth = ethernet(100)
            eth.probOfSending = 0.99-k/100
            eth.rgen(cycles)
            eth.lgen(cycles)
            for i in range(0, cycles):
                eth.cycle()
            p_results[k][1] += eth.stats[1]/100
            p_results[k][2] += eth.stats[2]/100
    with open('p_results', 'w') as f:
        for i in p_results:
            f.write(str(i[0])+','+str(i[1])+','+str(i[2])+'\n')

    #checking different l for p = 0.99, n = 1000
    #results: l, crashed, delivered
    p = 0.99
    cycles = 10000
    l_results = []
    for k in range(0, 10):
        l_results += [[2**k, 0, 0]]
        for j in range(0, 100):
            eth = ethernet(2**k)
            eth.probOfSending = p
            eth.rgen(cycles)
            eth.lgen(cycles)
            for i in range(0, cycles):
                eth.cycle()
            l_results[k][1] += eth.stats[1]/100
            l_results[k][2] += eth.stats[2]/100
    with open('l_results', 'w') as f:
        for i in l_results:
            f.write(str(i[0])+','+str(i[1])+','+str(i[2])+'\n')

main()

