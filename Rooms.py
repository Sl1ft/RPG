from random import randint,choice,choices
from combat import fight
from enum import Enum

class Events(Enum):
    MONSTER = "Монстр"
    TREASURE = "Сокровище"
    UNKNOWN = "Неизвестность"
    TRAP = "Ловушка"

def chance(some_list):
    return choices(some_list, weights=[i.weight for i in some_list], k=1)[0]

ROOM_EVENTS = [i for i in Events if i != Events.TRAP]

def room(hero: 'Hero', monsters_list: list,items_list:list):
    a = randint(1,3)
    if a == 1:
        print(f'Перед вами {a} комната')
    else:
        print(f'Перед вами {a} комнаты')

    directions = ['Прямо', 'Слева', 'Справа']
    choose = []
    current_events ={}
    for i in range(1,a+1):

        direction = choice(directions)
        choose.append(direction)
        current_events.setdefault(direction, choice(ROOM_EVENTS))
        directions.remove(direction)
        print(f'{direction} от вас находится {current_events[direction].value}')
    print('\nКуда вы собираетесь пойти?')
    while True:
        for i,j in enumerate(choose,start= 1):
            print(f'{i}: {j}')

        try:
            user_input = int(input())
            if user_input in range(1,a+1):
                if current_events[choose[user_input-1]] == Events.MONSTER:
                    chosen_monstr = chance(monsters_list)
                    fight(hero,chosen_monstr)
                    break
                elif current_events[choose[user_input-1]] == Events.TREASURE:
                    chosen_item = chance(items_list)
                    hero.take_item(chosen_item)
                    break
                elif current_events[choose[user_input-1]] == Events.UNKNOWN:
                    chosen_event = choices([e for e in Events if e != Events.UNKNOWN], weights=[60,50,30], k=1)[0]
                    print(f'В комнате за слоем тумана, оказывается {chosen_event.value}')
                    if chosen_event == Events.MONSTER:
                        fight(hero,chance(monsters_list))
                        break
                    elif chosen_event == Events.TREASURE:
                        hero.take_item(chance(items_list))
                        break
                    elif chosen_event == Events.TRAP:
                        trap_damage = randint(10,50)
                        print(f'Вы попались в ловушку и вам нанесло {trap_damage} урона')
                        hero.hp -= trap_damage
                        break
            else:
                print('Введите вариант из списка')
        except(ValueError,IndexError):
            print('\nВведити вариант из выше перечисленных!\n')

