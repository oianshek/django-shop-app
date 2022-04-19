from shop.models import Item
from decimal import Decimal

class Cart():
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('skey')
        
        if 'skey' not in request.session:
            cart = self.session['skey'] = {}
        
        self.cart = cart

    def add(self, item, item_qty):
        """
        Adding and updating the users cart session data
        """
        item_id = str(item.id)

        if item_id in self.cart:
            self.cart[item_id]['item_qty'] = item_qty
        else:
            self.cart[item_id] = {'price': str(item.price), 'item_qty': item_qty}

        self.save()

    def delete(self, item):
        """
        Delete item from cart session data
        """
        item_id = str(item)

        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def update(self, item, item_qty):
        """
        Update values in cart session data
        """
        item_id = str(item)

        if item_id in self.cart:
            self.cart[item_id]['item_qty'] = item_qty

        self.save()

    def __len__(self):
        """
        Get the cart data and count the qty of items
        """
        return sum(item_obj['item_qty'] for item_obj in self.cart.values())

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        item_ids = self.cart.keys() 
        items = Item.items.filter(id__in=item_ids)
        cart = self.cart.copy()

        for item in items:
            cart[str(item.id)]['item'] = item

        for item_obj in cart.values():
            item_obj['price'] = Decimal(item_obj['price'])
            item_obj['total_price'] = item_obj['price'] * item_obj['item_qty']
            yield item_obj

    def get_total_price(self):
        return sum(Decimal(item_obj['price']) * item_obj['item_qty'] for item_obj in self.cart.values())

    def save(self):
        self.session.modified = True
