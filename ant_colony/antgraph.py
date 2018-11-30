from threading import Lock

class AntGraph:
    def __init__(self, num_nodes, delta_mat, tau_mat=None):
        # print len(delta_mat)
        # El tamano de la matriz de distancias debe ser igual al numero de nodos
        if len(delta_mat) != num_nodes:
            raise Exception("len(delta) != num_nodes")

        self.num_nodes = num_nodes
        self.delta_mat = delta_mat # matriz de deltas de distancias a nodos
        self.lock = Lock()

        # La matriz Tau contiene la cantidad de feromona en el nodo x,y
        if tau_mat is None:
            self.tau_mat = []
            for i in range(0, num_nodes):
                self.tau_mat.append([0]*num_nodes)
        else:
            self.tau_mat = tau_mat

    def delta(self, r, s):
        return self.delta_mat[r][s]

    def tau(self, r, s):
        return self.tau_mat[r][s]

    # 1 / delta = eta or etha
    def etha(self, r, s):
        return 1.0 / self.delta(r, s)

    # inner locks most likely not necessary
    def update_tau(self, r, s, val):
        lock = Lock()
        lock.acquire()
        self.tau_mat[r][s] = val
        lock.release()

    def reset_tau(self):
        lock = Lock()
        lock.acquire()
        avg = self.average_delta()

        # initial tau
        self.tau0 = 1.0 / (self.num_nodes * 0.5 * avg)

        #print "Average = %s" % (avg,)
        #print "Tau0 = %s" % (self.tau0)

        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                self.tau_mat[r][s] = self.tau0
        lock.release()
        
    def reset_tau_mod(self, tau_mat):
        lock = Lock()
        lock.acquire()
        self.tau_mat = tau_mat
        avg = self.average_delta()
        self.tau0 = 1.0 / (self.num_nodes * 0.5 * avg)
        lock.release()

    # average delta in delta matrix
    def average_delta(self):
        return self.average(self.delta_mat)

    # average tau in tau matrix
    def average_tau(self):
        return self.average(self.tau_mat)

    # average val of a matrix
    def average(self, matrix):
        sum = 0
        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                sum += matrix[r][s]

        avg = sum / (self.num_nodes * self.num_nodes)
        return avg
