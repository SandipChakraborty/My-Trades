import util



def place_sl_m_robo_order():
    obj = util.get_session()
    order_id = "DUMMY"
    try:
        orderparams = {
            "variety": "ROBO",
            "tradingsymbol": "MARUTI26DEC24FUT",
            "symboltoken": "39298",
            "transactiontype": "BUY",
            "exchange": "NFO",
            "ordertype": "STOPLOSS_LIMIT",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "triggerprice": "862",
            "price": "863",
            "squareoff": "20",
            "stoploss": "10",
            "quantity": "50"
        }
        order_id = obj.placeOrder(orderparams)
        print("The order id is: {}".format(order_id))
    except Exception as e:
        print("Order placement failed: {}".format(e.message))
    finally:
        return order_id



