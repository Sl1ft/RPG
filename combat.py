from random import randint
def fight(hero: 'Hero', MonsterClass: type('Monster') ) -> None:
    monster = MonsterClass()
    print(f'\n⚔️Начался бой, {hero.name} дерется с {monster.name}')
    while hero.is_alive > 0 and monster.is_alive > 0:
        print('\nВаш ход')
        while True:
            for i,decision in enumerate(('Атаковать','Использовать предмет','Попытаться сбежать'),start=1):
                print(f'{i}: {decision}')
            try:
                play: int = int(input())
                if play-1 == 0:
                    hero.attack(monster)
                    break
                elif play-1 == 1:
                    hero.use()
                elif play-1 == 2:
                    if randint(1,4) == 4:
                        print('Вы успешно сбежали из боя')
                        return

                    else:
                        print('Попытка неудалась')
                        break
            except (ValueError, IndexError, TypeError):
                print('Выберите действие из приведенных выше')

        if not monster.is_alive:
            print(f'Вы победили {monster.name}')
            if monster.loot:
                print(f'🔎Вы нашли предмет ({monster.loot().name} добавлено в инвентарь)')
                hero.take_item(monster.loot)
            hero.gain_exp(monster.exp_reward)

            break
        monster.attack(hero)
