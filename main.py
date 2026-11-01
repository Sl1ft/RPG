from Items import Sword,Hammer,Bow,HealPotion
from Character import Hero,Goblin,Skeleton,Orc
from combat import fight
from random import choice
from Rooms import room
from Saves import save, load_saves, load_hero, delete_save, MAX_SAVES

monsters = [Goblin,Skeleton,Orc]
items = [Sword,HealPotion,Hammer,Bow]
def create_hero():
    hero = Hero(input('Добро пожаловать в игру путник, как тебя зовут? \n'))
    hero.input_item(Hammer)
    hero.input_item(Sword)
    hero.input_item(Bow)
    hero.input_item(HealPotion)

    return hero
def save_choose(hero: Hero) -> None:
    saves_name = input('Введите название сохранения:')
    saves = load_saves()
    if saves_name not in saves and len(saves) >= MAX_SAVES:
        print('У вас максимум сохранений')
        slot = ask_slot_to_rewrite(saves)
        if slot is not None:
            delete_save(slot)
            save(hero,saves_name)
        else:
            print('Сохранение отменено')
    else:
        save(hero, saves_name)

def ask_slot_to_rewrite(saves: dict) -> str | None:
    while True:
        user_answer = input('Хотите перезаписать:  да/нет\n').lower()
        if user_answer in ['да', 'д', 'yes', 'y']:
            print('Какой из файлов вы хотите переписать?:')
            while True:
                for number, key in enumerate(saves.keys(), start=1):
                    print(f'{number}: {key}')
                try:
                    slot = int(input())
                except ValueError:
                    print('Введите ЧИСЛО')
                    continue
                if 1 <= slot <= len(saves):
                    return list(saves)[slot - 1]
                else:
                    print('Введите число из списка')
        elif user_answer in ['нет','н','no','n']:
            return None
        else:
            print('Выберите да или нет')

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
                print('Загрузка произошла успешно')
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
            save_choose(user1)
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