import pickle
from settings import Y, V

A = {'graphe_1' : (Y, V)}

with open('../data/graph', 'wb') as d :
    pickle.dump(A, d)