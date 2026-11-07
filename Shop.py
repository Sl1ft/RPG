from random import choices, randint

from Items import Item,Hammer,Sword,Bow,HealPotion,Potion
ITEMS_LIST = [Hammer,Sword,Bow,HealPotion]
MAX_ITEMS = 3

class OutOfStockError(Exception):
    pass

class Shop:
    def __init__(self,shop_dict: dict = None) -> None:
        if shop_dict is not None:
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

    def buy_menu(self) -> None:

        for number,(item,count) in enumerate(self.shop_dict.items(), start= 1):
            if count > 0:
                print(f'{number}. {item.name} | ({count}шт) | {item.price}🪙')
            else:
                print(f'{number}. {item.name} | Продано')



    def choose_buy(self,number:int) -> type[Item]:
        lst = enumerate(self.shop_dict.keys(),start=1)
        for i,v in lst:
            if i == number:
                return v
