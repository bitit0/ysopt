from artifact import rand_artifact
from goal import score, goal
from rich.progress import track
import matplotlib.pyplot as plt


N = 200

arts = {
    'flower': [],
    'feather': [],
    'sands': [],
    'goblet': [],
    'circlet': []
}

cnt_arts = {
    'flower': 0,
    'feather': 0,
    'sands': 0,
    'goblet': 0,
    'circlet': 0
}

cnt_ns = []
cnt_bps = []
goals = []


def update_cnt_ns(type):
    cnt_arts[type] += 1
    n = 1
    for key in arts:
        if key != type:
            n *= cnt_arts[key]
    if len(cnt_ns) == 0:
        cnt_ns.append(n)
    else:
        cnt_ns.append(n+cnt_ns[-1])


def update_cnt_bps(n):
    if len(cnt_bps) == 0:
        cnt_bps.append(n)
    else:
        cnt_bps.append(n+cnt_bps[-1])


goal_max = 0

for i in track(range(N)):
    A = rand_artifact()
    update_cnt_ns(A.type)
    # add A, decide whether or not accept it
    A.score = score(A)
    if A.score <= goal_max:
        goals.append(goal_max)
        update_cnt_bps(0)
        continue
    # search for maximum
    tmp = arts[A.type]
    arts[A.type] = [A]
    cnt = 0
    for a1 in arts['flower']:
        for a2 in arts['feather']:
            for a3 in arts['sands']:
                for a4 in arts['goblet']:
                    for a5 in arts['circlet']:
                        cnt += 1
                        g = goal([a1, a2, a3, a4, a5])
                        goal_max = max(goal_max, g)
    arts[A.type] = tmp
    arts[A.type].append(A)
    update_cnt_bps(cnt)
    goals.append(goal_max)
    # filter
    for key in arts:
        filter(lambda a: a.score > goal_max, arts[key])

plt.subplot(3, 1, 1)
plt.plot(cnt_ns, label="NS")
plt.plot(cnt_bps, label="BPS")
plt.legend()
plt.ylabel('No. enum')

plt.subplot(3, 1, 2)
plt.plot(cnt_ns, label="NS")
plt.plot(cnt_bps, label="BPS")
plt.legend()
plt.ylabel('log no. enum')
plt.yscale('log')

plt.subplot(3, 1, 3)
plt.plot(goals)
plt.ylabel('Opt')
plt.xlabel('No. artifacts')

plt.savefig('compage.png')
