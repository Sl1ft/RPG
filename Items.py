from abc import ABC, abstractmethod

class Item(ABC):
    def __init__(self,name:str,weight) -> None:
        self.name: str = name
        self.weight: int = weight
    def __repr__(self) -> str:
        return f'{self.name}'
    @abstractmethod
    def use(self,character: 'Character') -> None:
        pass

class Weapon(Item):
    def __init__(self,name: str,damage: int,weight: int = 20) -> None:
        super().__init__(name,weight)
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
    def __init__(self,name: str,effect: int,weight: int = 40) -> None:
        super().__init__(name,weight)
        self.effect: int = effect
    def __repr__(self) -> str:
        return f'{super().__repr__()}(восстанавливает {self.effect} здоровья)'
    def use(self,character: 'Hero') -> None:
        character.hp += self.effect
        print(f'Вы выпили зелье, ваше здоровье: {character.hp}')
        character.inventory.remove(self)