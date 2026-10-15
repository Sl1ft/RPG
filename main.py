from Items import Weapon,Potion
from Character import Hero,Monster
from RPG.Character import Goblin, Skeleton, Orc
from combat import fight
from random import choice
from Rooms import room




#Персонажи

#Прописька
user1 = Hero('Sl1ft')
user1.statistic()
user1.max_hp = 100
user1.hp = 1
user1.check_inventory()
monstr = Monster('Гоблин',50,5)
bow = Weapon('Лук',25,15)
bottle_of_heal = Potion("Зелье лечение",40)
sword = Weapon('Меч',12)
bor = Weapon('Булова',20,10)
Monsters = [Goblin,Skeleton,Orc]
Items = [sword,bor,bow,bottle_of_heal, Weapon('Фрост Морн', 100, 5)]

user1.take_item(Weapon('Фрост Морн', 100, 5))
user1.take_item(sword)
user1.take_item(bor)
user1.take_item(bottle_of_heal)
user1.check_inventory()

user1.use_item(bottle_of_heal)

while True:
    a = input().lower()
    if a == 'exit':
        break
    elif a == 'stats':
        user1.statistic()
    elif a == 'inventory':
        user1.check_inventory()
    elif a == 'use':
        user1.use()

    elif a == 'hunt':
        fight(user1,choice(Monsters))
    elif a == 'explore':
        room(user1,Monsters,Items)

    elif a == 'help':
        print('--- 📜 Доступные команды 📜 ---'.center(50))
        print('stats - показывает статистику'.center(50))
        print('use - использовать предмет из инвенторя'.center(50))
        print('hunt - подбирает случайного врага для битвы'.center(50))
        print('inventory - позволяет заглянуть в ваш рюкзак'.center(50))
        print('exit - завершает игру'.center(50))