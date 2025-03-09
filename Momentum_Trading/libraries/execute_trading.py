# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 19:43:33 2024

@author: ritwi
"""

'Executing Trade'
def execute_trading(self):
    
    'Execute hold action'
    if (self.action==0):
        
        print('\nHold Action\n')
        
        'The money_reserve remains the same'
        self.money = self.money
        
        'The stock_holdings remains the same'
        self.stock = self.stock
        
        'No fee for holding'
        total_fee = 0
  
        
    'Execute buy operation'
    if (self.action > 0):
        
        print('\nBuy Action\n')
        
        'Target position. position_per_action_value have range 0-1'
        target_position_in_money = (self.money - self.max_fee) * (self.action * self.position_per_action_value)
        print('\nTarget position to buy in money:', target_position_in_money)
        
        'Calculate the stock quantity that can be bought'      
        stock_buy_in_quantity = target_position_in_money//self.execution_price        
        print('\nActual stock quantity bought:', stock_buy_in_quantity)
        
        'Update the stock holdings'        
        self.stock += stock_buy_in_quantity
        
        'Actual money spent to buy the stocks'
        actual_money_spent = stock_buy_in_quantity * self.execution_price        
        print('\nThe actual money spent to purchase stock:', actual_money_spent)
        
        'Trading Fee calculation'
        total_fee = actual_money_spent * (self.fee_percentage/100)
        total_fee = min(total_fee, self.max_fee)       
        print('\nThe total fee to be paid', total_fee)
        
        'Update the money_reserve after the sell'
        self.money = self.money - actual_money_spent - total_fee

        
    'Execute sell operation'
    if (self.action < 0):
        
        print('\nSell Action\n')
        
        'Calculate the stock quantity that can be sold'
        stock_sell_in_quantity = int(self.stock * (-self.action * self.position_per_action_value))
        
        'Sell all stocks if stock_sell_in_quantity==0, but self.stock>0'
        if (stock_sell_in_quantity==0 and self.stock>0):
            stock_sell_in_quantity = self.stock
            print('\nSelling all stocks as stock reserve is too low to get percentage')
            
        print('\nStock Reserve', self.stock)
        print('\nActual stock quantity to be sold', stock_sell_in_quantity)
        
        'Update the stock holdings'        
        self.stock -= stock_sell_in_quantity
        
        'Calculate the money earned by the sell'       
        money_earn = stock_sell_in_quantity * self.execution_price   
        print('\nActual money earned in the stock selling:', money_earn)
        
        'Fee calculation'
        total_fee = money_earn * (self.fee_percentage/100)
        total_fee = min(total_fee, self.max_fee)
        print('\nThe total fee to be paid', total_fee)
        
        'Update the money_reserve after the sell'
        self.money = self.money + money_earn - total_fee