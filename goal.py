from typing import List
from artifact import Artifact

from scipy.optimize import minimize, LinearConstraint


def goal(artifacts: List[Artifact]) -> float:
    assert len(artifacts) == 5

    cr = 0
    cd = 0
    atkp = 0

    for A in artifacts:
        for a in A.minor_affixes:
            if a.key == 'cr':
                cr += a.value
            elif a.key == 'cd':
                cd += a.value
            elif a.key == 'atkp':
                atkp += a.value

    return (1 + cr*cd) * (1 + atkp)


def score(artifact: Artifact) -> float:
    cra = 0
    cda = 0
    atkpa = 0

    for a in artifact.minor_affixes:
        if a.key == 'cr':
            cra += a.value
        elif a.key == 'cd':
            cda += a.value
        elif a.key == 'atkp':
            atkpa += a.value

    return (1+cra*cda)*(atkpa+1.97)


def score_(artifact: Artifact) -> float:
    cra = 0
    cda = 0
    atkpa = 0

    print(artifact)

    for a in artifact.minor_affixes:
        if a.key == 'cr':
            cra += a.value
        elif a.key == 'cd':
            cda += a.value
        elif a.key == 'atkp':
            atkpa += a.value

    def fun(x):
        return -(1+(x[0]+cra)*(x[1]+cda))*(1+x[2]+atkpa)

    def jac(x):
        return [
            -(x[1]+cda)*(1+x[2]+atkpa),
            -(x[0]+cra)*(1+x[2]+atkpa),
            -(1+(x[0]+cra)*(x[1]+cda))
        ]

    constr = LinearConstraint(
        [1/0.0389, 1/0.0777, 1/0.0583], 0, 32)

    inf = 1e5
    bounds = [(0, inf) for _ in range(3)]

    x0 = [0.389, 0.777, 0.583]

    res = minimize(fun, x0, jac=jac, bounds=bounds, constraints=constr)
    print(res.x)

    return -fun(res.x)
