from .models import Order


def get_orders_for_user(user, status):
    if user.is_customer:
        return user.customer_profile.orders.all()
    elif user.is_clerk:
        return Order.objects.filter(status=status)


def prepare_orders_for_json(user, status=None):
    orders = get_orders_for_user(user, status)
    results = []
    if orders:
        for order in orders:
            results.append({
                'author': order.owner.user.get_short_name(),
                'file_number': order.file_number or '',
                'case': order.case,
                'party_name': order.party_name,
                'name': order.name,
                'needed_date': order.needed_date,
                'detail': order.get_absolute_url()})
    return results
