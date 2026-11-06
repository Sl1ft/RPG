from abc import ABC, abstractmethod

SELL_RATIO = 0.7

class Item(ABC):
    def __repr__(self) -> str:
        return f'{self.name}'
    @abstractmethod
    def use(self,character: 'Character') -> None:
        pass
    @property
    @abstractmethod
    def price(self) -> int:
        pass
    @property
    @abstractmethod
    def json_name(self) -> str:
        pass
    @property
    def sell_price(self) -> int:
        return round(self.price * SELL_RATIO)

class Weapon(Item):
    def __init__(self,damage: int) -> None:
        self.damage: int = damage

    def __repr__(self) -> str:
        return f'{super().__repr__()},({self.damage} урона)'

    def use(self,character: 'Hero') -> None:
        if character.is_equipped:
            character.inventory.append(character.is_equipped)
        character.inventory.remove(self)
        character.is_equipped = self

        character.damage = character.level * 2 + self.damage
        print(f'Вы экипировали {self.name}, ваш урон: {character.damage}')


class Potion(Item):
    def __init__(self,effect: int) -> None:
        self.effect: int = effect
    def __repr__(self) -> str:
        return f'{super().__repr__()}(восстанавливает {self.effect} здоровья)'
    def use(self,character: 'Hero') -> None:
        character.hp += self.effect
        print(f'Вы выпили зелье, ваше здоровье: {character.hp}')
        character.inventory.remove(self)


class HealPotion(Potion):
    name = "Малое зелье лечения"
    json_name = 'heal_potion'
    weight = 40
    price = 300
    def __init__(self) -> None:
        super().__init__(20)

class Sword(Weapon):
    name = 'Меч'
    json_name = 'sword'
    weight = 20
    price = 250
    def __init__(self) -> None:
        super().__init__(20)

class Bow(Weapon):
    name = 'Лук'
    json_name = 'bow'
    weight = 15
    price = 500
    def __init__(self) -> None:
        super().__init__(45)

class Hammer(Weapon):
    name = 'Молот'
    json_name = 'hammer'
    weight = 5
    price = 1500
    def __init__(self) -> None:
        super().__init__(100)