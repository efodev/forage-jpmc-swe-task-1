import unittest
from client3 import getDataPoint, getRatio

class ClientTest(unittest.TestCase):
  def test_getDataPoint_calculatePrice(self):
    quotes = [
      {'top_ask': {'price': 121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
      {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'},
      {'top_ask': {'price':'DEF', 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
    ]
    """ Unit tests  """
    # testing for correct output for price
    quote_1 = quotes[0]
    expected_price = (quote_1['top_bid']['price'] + quote_1['top_ask']['price']) / 2
    _, _, _, calc_price  = getDataPoint(quote_1)
    self.assertEqual(calc_price, expected_price)
    
    # test for incorrect calculation of price
    quote_2 = quotes[1]
    expected_price = (quote_2['top_bid']['price'] + quote_2['top_ask']['price'])
    _, _, _, calc_price = getDataPoint(quote_2)

    self.assertNotEqual(calc_price, expected_price)
    
    # Not necessary - catching incorrect input for either top or bid prices
    with self.assertRaises((ValueError, TypeError)):
        quote_3 = quotes[2]
        stock = quote_3['stock']
        bid_price = quote_3['top_bid']['price'] 
        ask_price = quote_3['top_ask']['price'] # top_ask has incorrect value for price
        price = (bid_price + ask_price) / 2 # resulting in an error here
        self.assertEqual(getDataPoint(quote_1), (stock, bid_price, ask_price, price))


  def test_getDataPoint_calculatePriceBidGreaterThanAsk(self):
    quotes = [
      {'top_ask': {'price': 119.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
      {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
    ]
    # test for calculated price less than ask 
    quote_1 = quotes[0]
    _, _, _, calc_price  = getDataPoint(quote_1)
    ask_price = quote_1['top_ask']['price']
    self.assertTrue(calc_price > ask_price)

    # test for calculated price greater than ask
    quote_2 = quotes[1]
    ask_price = quote_2['top_ask']['price']
    _, _, _, calc_price = getDataPoint(quote_2)
    self.assertFalse(calc_price > ask_price)


  def test_getRatio(self):
    # test case for price_b is 0
    self.assertEqual(getRatio(120.00, 0), None)

    # test for any other price value
    self.assertEqual(getRatio(120.48, 119.2), 120.48/119.2)

    # test for incorrect output
    self.assertNotAlmostEqual(getRatio(120.48, 119.2), 119.2/120.48)

  

if __name__ == '__main__':
    unittest.main()
