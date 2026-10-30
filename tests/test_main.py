import pytest
from Character import Hero
from Items import Hammer, Sword, HealPotion


@pytest.fixture
def hero():
    return Hero('Test')
@pytest.fixture
def hero_items(hero):
    a = hero.input_item(Hammer)
    hero.input_item(Sword)
    hero.input_item(HealPotion)
    hero.use_item(a)
    return hero
class TestHp:
    @pytest.mark.parametrize(
        "x,expectation",[
        (1,True),
        (0, False),
        (-10, False),
        (100, True)
    ])
    def test_hp(self,hero,x,expectation):
        hero.hp = x
        assert hero.is_alive == expectation

class TestSaves:
    def test_make_dct(self,hero):
        assert hero.make_dct() == {
         "name": "Test",
         "max_hp": 100,
         "hp": 100,
         "level": 1,
         "exp": 0,
         "exp_to_next_lvl": 100,
         "damage": 3,
         "inventory": [],
         "is_equipped": None
      }
    def test_make_dct_items(self,hero_items):
        assert hero_items.make_dct() == {
            "name": "Test",
            "max_hp": 100,
            "hp": 100,
            "level": 1,
            "exp": 0,
            "exp_to_next_lvl": 100,
            "damage": 102,
            "inventory": ["sword","heal_potion"],
            "is_equipped": "hammer"
        }