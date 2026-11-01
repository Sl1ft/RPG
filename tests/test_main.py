import pytest
from Character import Hero,INVENTORY_LIMIT,InventoryFullError
from Items import Hammer, Sword, HealPotion
from Saves import save,load_hero


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
@pytest.fixture
def hero_full(hero):
    for _ in range(INVENTORY_LIMIT):
        hero.input_item(Sword)
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

    def test_make_dct_items_load(self,hero_items,tmp_path):
        file = tmp_path / "TEST.json"
        save(hero_items,"test",file)
        hero2 = load_hero("test",file)

        assert hero_items.make_dct() == hero2.make_dct()
        assert hero2 is not hero_items

    def test_full_inventory(self,hero_full):
        with pytest.raises(InventoryFullError):
            hero_full.input_item(Sword)
        assert len(hero_full.inventory) == INVENTORY_LIMIT

    def test_drop_item(self,hero_items):
        item = hero_items.inventory[0]
        dropped_item = hero_items.drop_item(0)
        inventory = [i.json_name for i in hero_items.inventory]

        assert inventory == ['heal_potion']
        assert item == dropped_item
        assert item not in hero_items.inventory

    def test_drop_item_bad_index(self,hero_items):
        with pytest.raises(IndexError):
            hero_items.drop_item(99)