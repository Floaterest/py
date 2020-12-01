'''
https://i.redd.it/rgfmlyqruiq41.png
'''
from os import system
from codecs import open
from json import dumps, loads, JSONEncoder
from dataclasses import dataclass

kohl = '合成コール'
manganese = 'マンガン'
grindstone = '砥石'
rma = 'RMA'
orirock = '源岩'
device = '装置'
polyester = 'エステル'
sugar = '糖原'
oriron = '異鉄'
aketon = 'アケトン'


@dataclass
class Item:
    name: str
    count: float


@dataclass
class Material:
    quantities: list
    stage: str


cost = {
    kohl: 48.46,
    manganese: 60.02,
    grindstone: 60.33,
    rma: 69.97,
    orirock: 24.1,
    device: 69.19,
    polyester: 45.53,
    sugar: 45.96,
    oriron: 57.2,
    aketon: 57.61,
}

syn = {
    kohl: [[Item(kohl, 1), Item(rma, 1), Item(sugar, 1)], [Item(kohl, 1)]],
    manganese: [[Item(kohl, 1), Item(manganese, 2), Item(polyester, 1)], [Item(manganese, 1)]],
    grindstone: [[Item(grindstone, 1), Item(device, 1), Item(oriron, 1)], [Item(grindstone, 1)]],
    rma: [[Item(rma, 1), Item(orirock, 2), Item(aketon, 1)], [Item(rma, 1)]],
    orirock: [[Item(orirock, 4)], [Item(orirock, 1)], [Item(orirock, 0.2)]],
    device: [[Item(grindstone, 1), Item(orirock, 2), Item(device, 1)], [Item(device, 1)], [Item(device, 0.25)]],
    polyester: [[Item(kohl, 1), Item(polyester, 2), Item(aketon, 1)], [Item(polyester, 1)], [Item(polyester, 0.25)]],
    sugar: [[Item(manganese, 1), Item(sugar, 2), Item(manganese, 1)], [Item(sugar, 1)], [Item(sugar, 0.25)]],
    oriron: [[Item(device, 1), Item(polyester, 1), Item(oriron, 2)], [Item(oriron, 1)], [Item(oriron, 0.25)]],
    aketon: [[Item(manganese, 1), Item(sugar, 1), Item(aketon, 2)], [Item(aketon, 1)], [Item(aketon, 0.25)]],
}


@dataclass
class Material:
    quantities: list[int]
    stage: str = ''


class Encoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Material):
            return o.__dict__
        return super(Encoder, self).default(o)


class Planner:
    def __init__(self, data: list):
        self.data = {d['name']: Material(d['quantities'], d['stage']) for d in data}

    @property
    def total(self):
        total = {
            kohl: 0,
            manganese: 0,
            grindstone: 0,
            rma: 0,
            orirock: 0,
            device: 0,
            polyester: 0,
            sugar: 0,
            oriron: 0,
            aketon: 0,
        }
        # get item amount
        for k, v in syn.items():
            for i, f in enumerate(v):
                for item in f:
                    total[item.name] += item.count * self.data[k].quantities[i]
        # get total sanity
        for k, v in cost.items():
            total[k] = round(total[k] * v, 2)
        # add all the data
        json = [{
            'name': k,
            'quantities': v.quantities,
            'stage': v.stage,
            'total': total[k]
        } for k, v in self.data.items()]

        return sorted(json, key=lambda j: j['total'])


def main():
    file='ak.json'
    with open(file, 'r', 'utf8') as f:
        p = Planner(loads(f.read()))
    with open(file, 'w', 'utf8') as f:
        f.write(dumps(p.total, ensure_ascii=False, indent=4))
    system(file)


if __name__ == '__main__':
    main()
