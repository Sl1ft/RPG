from typing import Optional,List
from abc import ABC
from random import randint,choice
from Items import Item,HealPotion,Bow,Sword,Hammer


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

    def statistic(self) -> None:
        print(f'Вы {self.name}, Ваше текущее здоровье: {self.hp} из {self.max_hp}')
        print(f'Ваш текущий уровень: {self.level} (Опыта до следущего уровня: {self.exp_to_next_lvl- self.exp})')
        print(f'Ваш урон: {self.damage}')

    def check_inventory(self) -> None:
        if len(self.inventory) == 0:
            print("Инвентарь пуст(")
        else:
            print('\n🎒Ваш инвентарь:')
            for i in self.inventory:
                print(i)
            print('')

    def take_item(self,item: 'Item') -> None:
        if issubclass(item,Item ):
            print(f'Герой {self.name} подобрал {item().name}')
            self.inventory.append(item())
        else:
            print('Вы не можете это подобрать!')

    def use_item(self,item: 'Item') -> None:
        if item in self.inventory:
            item.use(self)

        else:
            print(f'Данного предмета нет в вашем инвентаре')

    def use(self):
        if self.inventory:
            while True:
                print('Что вы хотите использовать?')
                for num, item in enumerate(self.inventory, start=1):
                    print(f'{num}: {item}')
                print('0: Выйти')

                try:
                    b = int(input())
                    if b in range(0,len(self.inventory)+1):
                        if b == 0:
                            break
                        else:
                            self.use_item(self.inventory[b - 1])
                            break
                    else:
                        print('❌Введите номер предмета из списка')
                except (ValueError, IndexError):
                    print('❌Введите номер предмета из приведенного выше списка\n')
        else:
            print(f'Ваш инвентарь пуст')

class Monster(Character):
    def __init__(self,name:str,hp:int,damage:int,exp_reward:int = 100,loot: Optional['Item'] = None) -> None:
        super().__init__(name,hp,damage)
        self.exp_reward:int = exp_reward
        self.loot: Optional['Item'] = loot

    def __repr__(self) -> str:
        return f'{self.name} ({self.hp}HP,{self.damage} урона)'

class Goblin(Monster):
    weight = 100
    def __init__(self) -> None:
        super().__init__('Гоблин',100,10,100,choice([HealPotion,Sword]))

class Skeleton(Monster):
    weight = 70
    def __init__(self) -> None:
        super().__init__('Скелет',200,20,200,choice([HealPotion,Bow]))

class Orc(Monster):
    weight = 30
    def __init__(self) -> None:
        super().__init__('Орк',300,50,300,Hammer)

