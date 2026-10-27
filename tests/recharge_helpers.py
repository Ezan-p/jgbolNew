"""Test-only funded gold-card orders; never used by the game runtime."""
from network_redirect import summon


LEGACY_PRODUCTS = {1: 101, 2: 102, 3: 103, 4: 105, 5: 106}
PRICES = {101: 10, 102: 50, 103: 100, 104: 200, 105: 500, 106: 1000,
          201: 50, 202: 45}


def funded_order(backend, product, order):
    role = backend.profile()
    if not role.get('_test_gold_cards_seeded'):
        summon.add_item(role, 1152, 1000)
        summon.add_item(role, 1156, 1000)
        role['_test_gold_cards_seeded'] = True
        backend.save(role)
    product = LEGACY_PRODUCTS.get(product, product)
    price = PRICES[product]
    return summon.lua(dict(item_id=product, order_id=order,
                          large_count=price // 50, small_count=price % 50 // 5))
