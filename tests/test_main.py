from contextlib import nullcontext
from pickle import FALSE

import pytest
from Character import Hero, INVENTORY_LIMIT, InventoryFullError, NotEnoughGold, ItemNotFoundError
from Items import Hammer, Sword, HealPotion, Bow
from Rooms import buy_item
from Saves import save,load_hero
from Shop import OutOfStockError, Shop


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
    hero.input_item(Hammer)
    for _ in range(INVENTORY_LIMIT - 1):
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
         "is_equipped": None,
         "gold": 0
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
            "is_equipped": "hammer",
            "gold": 0
        }

    def test_make_dct_items_load(self,hero_items,tmp_path):
        file = tmp_path / "TEST.json"
        save(hero_items,"test",file)
        hero2 = load_hero("test",file)

        assert hero_items.make_dct() == hero2.make_dct()
        assert hero2 is not hero_items

class TestInventory:

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

    def test_drop_menu(self,monkeypatch,hero_full):
        found = Bow()
        monkeypatch.setattr('builtins.input', lambda prompt='': '1' )
        hero_full.drop_menu(found)
        inventory = [i.json_name for i in hero_full.inventory]

        assert len(hero_full.inventory) == INVENTORY_LIMIT
        assert inventory[-1] == 'bow'
        assert inventory[0] != 'hammer'
class TestGold:
    @pytest.mark.parametrize(
        "gold,cost,expectation,result",[
            (100,100,nullcontext(),0),
            (100,101,pytest.raises(NotEnoughGold),100)
        ]
    )
    def test_spend_gold(self,hero,gold,cost,expectation,result):
        hero.gold = gold
        with expectation:
            hero.spend_gold(cost)
        assert hero.gold == result

class TestShop:
    @pytest.mark.parametrize(
        "inventory_flag,gold,item,item_count,gold_after,expectation,item_count_after,inventory_size",[
            (False,500,Sword,1,250,nullcontext(),0,1),
            (False,500,Sword,0,500,pytest.raises(OutOfStockError),0,0),
            (False,100,Sword,1,100,pytest.raises(NotEnoughGold),1,0),
            (True,500,Sword,1,500,pytest.raises(InventoryFullError),1,INVENTORY_LIMIT)
        ],
        ids=["Success_buy","OutOfStock","NotEnoughGold","FullInventory"]
    )
    def test_buy_item(self,hero,inventory_flag,gold,item,item_count,gold_after,expectation,item_count_after,inventory_size):
        shop = Shop({item: item_count})
        if inventory_flag:
            for _ in range(INVENTORY_LIMIT):
                hero.input_item(Sword)
        hero.gold = gold
        with expectation:
            buy_item(hero,shop,item)
        assert hero.gold == gold_after
        assert shop.shop_dict[item] == item_count_after
        assert len(hero.inventory) == inventory_size


    @pytest.mark.parametrize(
        "have_item_flag,item,gold_after,expectation",[
            (True,Sword,175,nullcontext()),
            (False,Sword,0,pytest.raises(ItemNotFoundError))
        ],
        ids=["success","item not found"]
    )
    def test_sell_item(self,hero,have_item_flag,item,gold_after,expectation):
        item = item()
        if have_item_flag:
            hero.inventory.append(item)
        with expectation:
            hero.sell_item(item)
        assert hero.gold == gold_after
        assert item not in hero.inventory
