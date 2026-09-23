class OutOfStockError(Exception):
    """库存不足时抛出"""
    pass


class InvalidDiscountError(Exception):
    """优惠码无效时抛出"""
    pass


# 企业级业务规则：折扣配置
DISCOUNT_CONFIG = {
    "SAVE10": 0.10,
    "SAVE20": 0.20,
    "VIP50": 0.50,
}


def create_order(items, customer_id):
    """
    创建订单
    items: 商品列表，例如 [{"sku": "A001", "name": "手机", "price": 2999.00, "qty": 2}]
    """
    if not items:
        raise ValueError("订单商品不能为空")

    order = {
        "customer_id": customer_id,
        "items": items,
        "status": "created",
    }
    return order


def validate_inventory(items, inventory):
    """
    校验库存是否足够
    inventory: 库存字典，例如 {"A001": 100, "A002": 0}
    """
    for item in items:
        sku = item["sku"]
        qty = item["qty"]
        available = inventory.get(sku, 0)
        if available < qty:
            raise OutOfStockError(f"商品 {sku} 库存不足，需要 {qty}，实际 {available}")
    return True


def calculate_subtotal(items):
    """计算商品小计"""
    return sum(item["price"] * item["qty"] for item in items)


def apply_discount(total, discount_code):
    """根据优惠码计算折扣后金额"""
    if discount_code is None or discount_code == "":
        return total

    if discount_code not in DISCOUNT_CONFIG:
        raise InvalidDiscountError(f"无效优惠码: {discount_code}")

    rate = DISCOUNT_CONFIG[discount_code]
    return round(total * (1 - rate), 2)


def calculate_order_total(order, discount_code=None, tax_rate=0.0):
    """
    计算订单最终总价
    步骤：小计 -> 折扣 -> 税费
    """
    subtotal = calculate_subtotal(order["items"])
    after_discount = apply_discount(subtotal, discount_code)
    tax = round(after_discount * tax_rate, 2)
    return round(after_discount + tax, 2)


def confirm_order(order, inventory, discount_code=None, tax_rate=0.0):
    """完整下单流程：校验库存 -> 计算总价 -> 确认订单"""
    validate_inventory(order["items"], inventory)
    total = calculate_order_total(order, discount_code, tax_rate)
    order["total"] = total
    order["status"] = "confirmed"
    return order
