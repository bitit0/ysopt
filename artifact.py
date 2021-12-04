from numpy.random import choice

MINOR_AFFIX_STAT = {
    'hp':   { 'p': 6, 'v': 298.75 },
    'atk':  { 'p': 6, 'v': 19.45 },
    'def':  { 'p': 6, 'v': 23.15 },
    'hpp':  { 'p': 4, 'v': 0.0583 },
    'atkp': { 'p': 4, 'v': 0.0583 },
    'defp': { 'p': 4, 'v': 0.0729 },
    'er':   { 'p': 4, 'v': 23.31 },
    'em':   { 'p': 4, 'v': 0.0648 },
    'cr':   { 'p': 3, 'v': 0.0389 },
    'cd':   { 'p': 3, 'v': 0.0777 },
}

MINOR_AFFIXES = ['hp', 'atk', 'def', 'hpp', 'atkp', 'defp', 'er', 'em', 'cr', 'cd']
AFFIX_DISTRIB = [6/44,  6/44,  6/44,  4/44,   4/44,   4/44, 4/44, 4/44, 3/44, 3/44]

ARTIFACT_TYPE = ['flower', 'feather', 'sands', 'goblet', 'circlet']


class Affix:
    def __init__(self, key, value=None):
        assert key in MINOR_AFFIX_STAT
        self.key = key
        if not value:
            self.value = 0
            self.enhance()
        else:
            self.value = value
    
    def enhance(self):
        l = choice(4, 1)[0] * 0.1 + 0.7
        m = MINOR_AFFIX_STAT[self.key]['v']
        self.value += m * l

class Artifact:
    def __init__(self, type=None):
        if type:
            self.type = type
        else:
            self.type = choice(ARTIFACT_TYPE, 1)[0]
        self.minor_affixes = []
    
    def __str__(self):
        ret = f'Type: {self.type}\n'
        ret += 'Minor Affixes:\n'
        for a in self.minor_affixes:
            ret += f'  {a.key}: {a.value}\n'
        return ret

def rand_artifact():
    A = Artifact()
    draw = choice(MINOR_AFFIXES, 4, replace=False, p=AFFIX_DISTRIB)
    for key in draw:
        a = Affix(key)
        A.minor_affixes.append(a)
    for _ in range(5):
        i = choice(4, 1)[0]
        A.minor_affixes[i].enhance()
    return A
