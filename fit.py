from sklearn.linear_model import LinearRegression
from copy import deepcopy
import numpy as np
from rich.progress import track

from artifact import rand_artifact, MINOR_AFFIX_STAT

eula_base = {
    'atk': 342+565,
    'atkp': 0.18,
    'cr': 0.05,
    'cd': 0.884,
}
eula_stat = {
    'atk': eula_base['atk']+311,
    'atkp': eula_base['atkp']+0.466,
    'cr': eula_base['cr']+0.311,
    'cd': eula_base['cd'],
}

def rand_equip_stat():
    equip_stat = deepcopy(eula_stat)
    for _ in range(5):
        A = rand_artifact()
        for a in A.minor_affixes:
            if a.key in equip_stat:
                equip_stat[a.key] += a.value
    return equip_stat

def target_function(equip_stat):
    s = equip_stat
    return (1+s['cr']*s['cd'])*(s['atk']+eula_base['atk']*s['atkp'])

def stat_to_input(stat):
    x = []
    for key in eula_stat:
        x.append((stat[key]-eula_stat[key])/MINOR_AFFIX_STAT[key]['v'])
    return x

def rand_train_set(N):
    X = []
    y = []
    for _ in track(range(N), 'Generating'):
        s = rand_equip_stat()
        X.append(stat_to_input(s))
        y.append(target_function(s))
    return np.array(X), np.array(y)

def test_model(model, N):
    n_ok = 0
    for _ in track(range(N), 'Testing'):
        s = [rand_equip_stat() for i in range(2)]
        t = [target_function(st) for st in s]
        X = [stat_to_input(st) for st in s]
        y = model.predict(X)
        if (y[0]-y[1])*(t[0]-t[1]) > 0:
            n_ok += 1
    return n_ok/N

n_train = 10000
n_test  = 10000

X, y = rand_train_set(n_train)

model = LinearRegression()
print('Fitting')
model.fit(X, y)
print(model.coef_)

rate = test_model(model, n_test)
print(rate)