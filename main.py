from Items import Sword,Hammer,Bow,HealPotion
from Character import Hero,Goblin,Skeleton,Orc
from combat import fight
from random import choice
from Rooms import room
from Saves import save,load_saves,load_hero

monsters = [Goblin,Skeleton,Orc]
items = [Sword,HealPotion,Hammer,Bow]
def create_hero():
    hero = Hero(input('Добро пожаловать в игру путник, как тебя зовут? \n'))
    hero.input_item(Hammer)
    hero.input_item(Sword)
    hero.input_item(Bow)
    hero.input_item(HealPotion)

    return hero

def game():
    while True:
        print('Вы хотите создать нового героя или загрузить старого?')
        print('1 - создать нового/ 2 - загрузить старого')
        while True:
            try:
                user_choose = int(input())
                break
            except ValueError:
                print('Введите число')
        if user_choose == 1:
            user1 = create_hero()
            break
        elif user_choose == 2:
            print('Введите название сохранения: ')
            saves_name = input()
            try:
                user1 = load_hero(saves_name)
                break
            except KeyError:
                print('❌Ошибка, не удалось загрузить сохранение❌\n')
                continue
        else:
            print('Выберите из двух чисел')

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
        elif a == 'save':
            file_name = input('Введите имя файла:')
            save(user1,file_name)
        elif a == 'help':
            print('--- 📜 Доступные команды 📜 ---'.center(50))
            print('stats - показывает статистику'.center(50))
            print('use - использовать предмет из инвенторя'.center(50))
            print('explore - ты начинаешь исследовать комнаты подземелья')
            print('hunt - подбирает случайного врага для битвы'.center(50))
            print('inventory - позволяет заглянуть в ваш рюкзак'.center(50))
            print('save - позволяет сохранить вашу игру'.center(50))
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