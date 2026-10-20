from Items import Sword,Hammer,Bow,HealPotion
from Character import Hero,Goblin,Skeleton,Orc
from combat import fight
from random import choice
from Rooms import room

monsters = [Goblin,Skeleton,Orc]
items = [Sword,HealPotion,Hammer,Bow]
def create_hero():
    hero = Hero(input('Добро пожаловать в игру путник, как тебя зовут? \n'))
    hero.take_item(Hammer)
    hero.take_item(Sword)
    hero.take_item(Bow)
    hero.take_item(HealPotion)

    return hero

def game():
    user1 = create_hero()
    print(f'\nПриветствую {user1.name},игра началась ')
    print('Если хочешь узнать активные команды напиши help')

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
        elif a == 'test':
            print(user1.inventory[0] == user1.is_equipped)
        elif a == 'hunt':
            fight(user1,choice(monsters))
        elif a == 'explore':
            room(user1,monsters,items)

        elif a == 'help':
            print('--- 📜 Доступные команды 📜 ---'.center(50))
            print('stats - показывает статистику'.center(50))
            print('use - использовать предмет из инвенторя'.center(50))
            print('explore - ты начинаешь исследовать комнаты подземелья')
            print('hunt - подбирает случайного врага для битвы'.center(50))
            print('inventory - позволяет заглянуть в ваш рюкзак'.center(50))
            print('exit - завершает игру'.center(50))
        else:
            print('Введите действующую команду (help)')



flag = True
while flag:
    game()
    while True:
        answer = input('\nВы хотите начать заново? \n').lower()
        if answer in ('да','д','y','yes'):
            break
        elif answer in ('нет','н','no','n'):
            print('bye')
            flag = False
            break
        else:
            print('введите да или нет!')