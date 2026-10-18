from Items import Weapon,Potion
from Character import Hero,Monster,Goblin,Skeleton,Orc
from combat import fight
from random import choice
from Rooms import room

def create_hero():
    hero = Hero(input('Введите имя своего героя: \n'))
    hero.take_item(Weapon('Фрост Морн', 100, 5))
    hero.take_item(sword)
    hero.take_item(sword)
    hero.take_item(bor)
    hero.take_item(bottle_of_heal)

    return hero

def game():
    user1 = create_hero()

    while True:
        if not user1.is_alive:
            print('Game over💀')
            break
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
            print('explore - ты начинаешь исследовать комнаты подземелья')
            print('hunt - подбирает случайного врага для битвы'.center(50))
            print('inventory - позволяет заглянуть в ваш рюкзак'.center(50))
            print('exit - завершает игру'.center(50))

monstr = Monster('Гоблин',50,5)
bow = Weapon('Лук',25,15)
bottle_of_heal = Potion("Зелье лечение",40)
sword = Weapon('Меч',12)
bor = Weapon('Булова',20,10)
Monsters = [Goblin,Skeleton,Orc]
Items = [sword,bor,bow,bottle_of_heal, Weapon('Фрост Морн', 100, 5)]

game()