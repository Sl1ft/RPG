from random import choices, randint

from Items import Item,Hammer,Sword,Bow,HealPotion,Potion
ITEMS_LIST = [Hammer,Sword,Bow,HealPotion]
MAX_ITEMS = 3

class OutOfStockError(Exception):
    pass

class Shop:
    def __init__(self,shop_dict: dict = None) -> None:
        if shop_dict != None:
            self.shop_dict: dict = shop_dict
        else:
            self.shop_dict = self._generate()

    def _generate(self) -> dict:
        shop_dct = {}
        copy: list = list(ITEMS_LIST)

        for _ in range(MAX_ITEMS):
            item = choices(copy, weights=[i.weight for i in copy], k=1)[0]
            if issubclass(item,Potion):
                shop_dct[item] = randint(1,5)
            else:
                shop_dct[item] = 1
            copy.remove(item)
        return shop_dct
    def item_sell(self,item: type[Item]) -> None:
        if self.shop_dict[item] > 0:
            self.shop_dict[item] -= 1
        else:
            raise OutOfStockError("Данный предмет закончился")

a = Shop()
print(a.shop_dict)
dct = {Hammer: 1, Sword: 1, Bow: 1}
b = Shop(dct)
print(b.shop_dict)
b.item_sell(Hammer)
print(b.shop_dict)

