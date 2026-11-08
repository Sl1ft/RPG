from typing import Optional,List
from abc import ABC
from random import randint,choice
from Items import Item,HealPotion,Bow,Sword,Hammer
INVENTORY_LIMIT = 10

class ItemNotFoundError(Exception):
    pass
class NotEnoughGold(Exception):
    pass
class InventoryFullError(Exception):
    pass

class Character(ABC):
    def __init__(self,name: str, hp: int = 100, damage: int = 2) -> None:
        self.name: str = name
        self.max_hp: int = hp
        self.__hp: int = hp
        self.level: int = 1
        self.exp: int = 0
        self.damage: int = damage + self.level
        self.is_equipped: Optional['Weapon'] = None

    @property
    def hp(self) -> int:
        return self.__hp
    @hp.setter
    def hp(self,value: int) -> None:
        if value > self.max_hp:
            self.__hp = self.max_hp
        elif value <= 0:
            self.__hp = 0
        else:
            self.__hp = value

    @property
    def is_alive(self) -> bool:
        return self.hp > 0
    def attack(self,target: 'Character') -> None:
        min_dmg = int(self.damage * 0.8)
        max_dmg = int(self.damage * 1.2)
        current_damage = randint(min_dmg,max_dmg)

        is_crit = randint(1,10) == 10
        if is_crit:
            current_damage *= 2
            print(f'💥{self.name} наносит критический урон в {current_damage}')
        else:
            print(f'{self.name} атакует {target.name} удар, нанося {current_damage} урона')
        target.hp -= current_damage



class Hero(Character):
    def __init__(self,name: str, exp_to_next_lvl:int = 100) -> None:
        super().__init__(name)
        self.inventory: List['Item'] = []
        self.exp_to_next_lvl:int = self.level * exp_to_next_lvl
        self.gold = 0

    def gain_exp(self,exp:int) -> None:
        self.exp += exp
        print(f'Вы получили {exp} опыта')
        while self.exp >= self.exp_to_next_lvl:
            self.level += 1
            print(f'\nВы повысили свой уровень!({self.level} уровень)')
            print(f'Следущие характеристики улучшились:')
            print(f'Максимальное здоровье +20 ')
            self.max_hp += 20
            print(f'Урон +2 ')
            self.damage +=2
            print(f'Здоровье восстановлено полностью \n')
            self.hp = self.max_hp
            self.exp -= self.exp_to_next_lvl
            self.exp_to_next_lvl = self.level * 100
    def gain_gold(self,gold:int):
        self.gold += gold
        print(f'+{gold} 🪙')

    def spend_gold(self,cost:int) -> None:
        if self.gold >= cost:
            self.gold -= cost
        else:
            raise NotEnoughGold('У вас недостаточно золота')

    def statistic(self) -> None:
        print(f'Вы {self.name}, Ваше текущее здоровье: {self.hp} из {self.max_hp}')
        print(f'Ваш текущий уровень: {self.level} (Опыта до следущего уровня: {self.exp_to_next_lvl- self.exp})')
        print(f'Ваш урон: {self.damage}')
        print(f'Баланс: {self.gold} 🪙')
        if self.is_equipped:
            print(f'Вы держите в руках {self.is_equipped.name}')
        else:
            print('В руках у вас ничего нет')

    def check_inventory(self) -> None:
        if len(self.inventory) == 0:
            print("Инвентарь пуст(")
        else:
            print('\n🎒Ваш инвентарь:')
            for i in self.inventory:
                print(i)
            print('')

    def input_item(self,item: type[Item]) -> Item:
        if len(self.inventory) < INVENTORY_LIMIT:
            new_item = item()
            self.inventory.append(new_item)
            return new_item
        else:
            raise InventoryFullError("Инвентарь переполнен")

    def take_item(self,item: type[Item]) -> None:
        try:
            new_item = self.input_item(item)
        except InventoryFullError:
            print('\nИнвентарь переполнен\n')
            found = item()
            self.drop_menu(found)
        else:
            print(f'Герой {self.name} подобрал {new_item.name}')

    def drop_menu(self, found: Item) -> None:
        while True:
            print(f'Найден: {found}. Что выбросить?\n')
            for num, value in enumerate(self.inventory, start=1):
                print(f'{num}: {value}')
            print('0: Выбросить найденный предмет\n')
            try:
                b = int(input())
            except ValueError:
                print('\n❌Введите номер предмета из приведенного выше списка\n')
            else:
                if 0 <= b <= len(self.inventory):
                    if b == 0:
                        print(f'Вы выбросили {found}')
                    else:
                        dropped = self.drop_item(b - 1)
                        print(f'Вы выбросили {dropped}. И взяли {found}')
                        self.input_item(type(found))
                    break
                else:
                    print('\n❌Введите номер предмета из списка\n')


    def use_item(self,item: 'Item') -> None:
        if item in self.inventory:
            item.use(self)

        else:
            print(f'Данного предмета нет в вашем инвентаре')

    def sell_menu(self) -> Item | None:
        if self.inventory:
            while True:
                print('Что вы хотите продать?')
                for num,value in enumerate(self.inventory,start= 1):
                    print(f'{num}: {value} | {value.sell_price} 🪙')
                print('0: Выйти')

                try:
                    b = int(input())
                except ValueError:
                    print('❌Введите число\n')
                    continue
                if 0 <= b <= len(self.inventory):
                    if b == 0:
                        return None
                    return self.inventory[b - 1]
                else:
                    print('❌Введите номер предмета из списка')
        else:
            print('Ваш инвентарь пуст')

    def sell_item(self,item: Item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.gain_gold(item.sell_price)
        else:
            raise ItemNotFoundError('Данного предмета нету в инвентаре')

    def use(self):
        if self.inventory:
            while True:
                print('Что вы хотите использовать?')
                for num, value in enumerate(self.inventory, start=1):
                    print(f'{num}: {value}')
                print('0: Выйти')

                try:
                    b = int(input())
                    if b in range(0,len(self.inventory)+1):
                        if b == 0:
                            print('Вы закрыли рюкзак')
                        else:
                            self.use_item(self.inventory[b - 1])
                        break
                    else:
                        print('❌Введите номер предмета из списка')
                except ValueError:
                    print('❌Введите номер предмета из приведенного выше списка\n')
        else:
            print(f'Ваш инвентарь пуст')
    def drop_item(self,index: int) -> Item:
        item = self.inventory.pop(index)
        return item

    def make_dct(self) -> dict:
        return {'name': self.name,
                'max_hp': self.max_hp,
                'hp': self.hp,
                'level': self.level,
                'exp': self.exp,
                'exp_to_next_lvl': self.exp_to_next_lvl,
                'damage': self.damage,
                'inventory': [i.json_name for i in self.inventory],
                'is_equipped': self.is_equipped.json_name if self.is_equipped  else None,
                'gold': self.gold}

class Monster(Character):
    def __init__(self,name:str,hp:int,damage:int,exp_reward:int = 100, gold_reward: int = 100,loot: type[Item] = None) -> None:
        super().__init__(name,hp,damage)
        self.exp_reward:int = exp_reward
        self.loot: type[Item] = loot
        self.gold_reward: int = gold_reward

    def __repr__(self) -> str:
        return f'{self.name} ({self.hp}HP,{self.damage} урона)'

class Goblin(Monster):
    weight = 100
    def __init__(self) -> None:
        super().__init__('Гоблин',100,10,100,randint(80,120),choice([HealPotion,Sword]))

class Skeleton(Monster):
    weight = 70
    def __init__(self) -> None:
        super().__init__('Скелет',200,20,200,randint(250,400),choice([HealPotion,Bow]))

class Orc(Monster):
    weight = 30
    def __init__(self) -> None:
        super().__init__('Орк',300,50,300,randint(700,1000),Hammer)

