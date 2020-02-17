'''
The CurrencySymbols class defines the mapping between
currency symbols and their names (abbreviated)
'''

class CurrencySymbols:
    currency_symbols = {
        "$": "USD",  # US Dollar
        "€": "EUR",  # Euro
        "₡": "CRC",  # Costa Rican Colón
        "£": "GBP",  # British Pound Sterling
        "₪": "ILS",  # Israeli New Sheqel
        "₹": "INR",  # Indian Rupee
        "¥": "JPY",  # Japanese Yen
        "₩": "KRW",  # South Korean Won
        "₦": "NGN",  # Nigerian Naira
#        "₱": "PHP",  # Philippine Peso
#        "zł": "PLN", # Polish Zloty
        "₲": "PYG",  # Paraguayan Guarani
        "฿": "THB",  # Thai Baht
        "₴": "UAH",  # Ukrainian Hryvnia
        "₫": "VND",  # Vietnamese Dong
    }

    @classmethod
    def get_symbol(self, csymbol):
        if csymbol in self.currency_symbols:
            return self.currency_symbols[csymbol]
        return None