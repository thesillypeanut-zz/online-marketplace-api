from src.helpers import validate_cart_item_quantity_is_not_more_than_product_inventory, handle_exception
from src.models import Order
from src.services import database_service, cart_service, product_service


def create(order_instance, current_user):
    _check_for_valid_field_keys(order_instance)

    cart_id = order_instance['cart_id']

    if cart_id not in [str(cart.id) for cart in current_user.carts if not cart.order]:
        raise handle_exception(
            'Unauthorized: You can only place an order on your cart (that has not already been ordered).', 401
        )

    cart = cart_service.get(cart_id, False)

    subtotal = _ensure_order_quantities_are_valid_and_get_subtotal(cart)
    order_instance.update({'subtotal': subtotal})
    order = database_service.post_entity_instance(Order, order_instance)

    for item in cart.cart_items:
        product_id = item.product_id
        product = product_service.get(product_id)

        product_service.update(
            item.product_id,
            {'inventory_count': product['inventory_count'] - item.quantity},
            item.id
        )

    return order


def get(order_id):
    return database_service.get_entity_instance_by_id(Order, order_id)


def list_all(cart_ids):
    try:
        orders = Order.query.filter(Order.cart_id.in_(cart_ids)).order_by(Order.date_ordered).all()
    except Exception:
        raise handle_exception(f'Exception encountered while querying orders.')

    return [order.serialize() for order in orders]


def _check_for_valid_field_keys(order_instance):
    if set(order_instance) != {'cart_id'}:
       raise handle_exception('Bad Request: Your POST request must include (only) the "cart_id" field.', 400)


def _ensure_order_quantities_are_valid_and_get_subtotal(cart):
    cart_id = cart.id

    if len(cart.cart_items) == 0:
        raise handle_exception(
            f'Bad Request: Cart with id "{cart_id}" does not contain any items to order.', 400
        )

    subtotal = 0
    for item in cart.cart_items:
        product_id = item.product_id
        product = product_service.get(product_id)
        product_inventory = product['inventory_count']
        order_quantity = item.quantity
        subtotal += item.quantity * product['price']
        validate_cart_item_quantity_is_not_more_than_product_inventory(product_inventory, order_quantity, product_id)

    return subtotal
