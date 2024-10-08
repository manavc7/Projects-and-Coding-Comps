import numpy as np

#Initiate parameters
S0 = 100        # initial stock prie
K = 120         # strike price
T = 1           # time to maturity
r = 0.06        # annual risk-free rate
N = 3           # number of time steps
u = 1.1         # up-factor in binomial model
d = 1/u         # ensure recombining tree
opttype = 'P'  # Option Type 'C' or 'P'

def binomial_tree_slow(S0,K,T,r,N,u,d,opttype):
    # precompute constants
    dt = T/N
    q = (np.exp(r*dt)-d)/(u-d)
    disc = np.exp(-r*dt)

    # initialise asset prices at maturity
    S = np.zeros(N+1) 
    S[0] = S0*d**N
    for j in range(1,N+1):
        S[j] = S[j-1]*u/d

    # initialise option values at maturity
    C = np.zeros(N+1)
    for j in range(0,N+1):
        if opttype == 'C':
            C[j] = max(0,S[j]-K)
        elif opttype == 'P':
            C[j] = max(0, K - S[j])

    # step backwards through tree
    for i in np.arange(N,0,-1):
        for j in range(0,i):
            if opttype == 'C':
                C[j] = disc* ( q*C[j+1] + (1-q)*C[j] )
            elif opttype == 'P':
                C[j] = disc* ( (1-q)*C[j+1] + q*C[j] )
 
    return C[0]

print(binomial_tree_slow(S0,K,T,r,N,u,d,opttype))

