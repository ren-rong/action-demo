import pytest
from order_service import (
    create_order,
    validate_inventory,
    calculate_subtotal,
    apply_discount,
    calculate_order_total,
    confirm_order,
    OutOfStockError,
    InvalidDiscountError,
)


def sample_items():
    return [
        {"sku": "A001", "name": "手机", "price": 2999.00, "qty": 1},
        {"sku": "A002", "name": "耳机", "price": 199.00, "qty": 2},
    ]


def test_create_order():
    items = sample_items()
    order = create_order(items, customer_id="C10086")
    assert order["customer_id"] == "C10086"
    assert order["status"] == "created"
    assert len(order["items"]) == 2


def test_create_order_empty_items():
    with pytest.raises(ValueError):
        create_order([], customer_id="C10086")


def test_validate_inventory_ok():
    items = sample_items()
    inventory = {"A001": 10, "A002": 5}
    assert validate_inventory(items, inventory) is True


def test_validate_inventory_out_of_stock():
    items = sample_items()
    inventory = {"A001": 0, "A002": 5}
    with pytest.raises(OutOfStockError):
        validate_inventory(items, inventory)


def test_calculate_subtotal():
    items = sample_items()
    assert calculate_subtotal(items) == 2999.00 + 199.00 * 2


def test_apply_discount_none():
    assert apply_discount(100, None) == 100


def test_apply_discount_save10():
    assert apply_discount(100, "SAVE10") == 90.0


def test_apply_discount_invalid():
    with pytest.raises(InvalidDiscountError):
        apply_discount(100, "FAKECODE")


def test_calculate_order_total_with_tax():
    items = sample_items()
    order = create_order(items, "C10086")
    total = calculate_order_total(order, discount_code="SAVE10", tax_rate=0.06)
    # 2999 + 199*2 = 3397；3397 * 0.9 = 3057.3；税费 3057.3 * 0.06 = 183.438；合计 3240.738 -> 3240.74
    assert total == 3240.74


def test_confirm_order_success():
    items = sample_items()
    order = create_order(items, "C10086")
    inventory = {"A001": 10, "A002": 5}
    confirmed = confirm_order(order, inventory, discount_code="SAVE20", tax_rate=0.06)
    assert confirmed["status"] == "confirmed"
    assert "total" in confirmed
    # 3397 * 0.8 = 2717.6；税费 163.056；合计 2880.656 -> 2880.66
    assert confirmed["total"] == 2880.66


def test_confirm_order_out_of_stock():
    items = sample_items()
    order = create_order(items, "C10086")
    inventory = {"A001": 10, "A002": 1}
    with pytest.raises(OutOfStockError):
        confirm_order(order, inventory)
