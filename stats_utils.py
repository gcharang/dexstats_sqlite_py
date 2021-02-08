import requests
import json
from decimal import Decimal
from datetime import datetime, timedelta


# getting list of pairs with amount of swaps > 0 from db (list of tuples)
# sql_coursor -> list (of base, rel tuples)
def get_availiable_pairs(sql_coursor):
    sql_coursor.execute("SELECT DISTINCT maker_coin, taker_coin FROM stats_swaps;")
    available_pairs = (sql_coursor.fetchall())
    return available_pairs

# tuple, integer -> list (with swap status dicts)
# select from DB swap statuses for desired pair with timestamps > than providedß
def get_swaps_since_timestamp_for_pair(sql_coursor, pair, timestamp):
    sql_coursor.execute("SELECT * FROM stats_swaps WHERE started_at > {} AND maker_coin='{}' AND taker_coin='{}';".format(timestamp,pair[0],pair[1]))
    swap_statuses = (sql_coursor.fetchall())
    return swap_statuses

# TODO: implement
# list (with swaps statuses) -> dict 
# iterating over the list of swaps and counting data for CMC summary call
# last_price, base_volume, quote_volume, highest_price_24h, lowest_price_24h, price_change_percent_24h
def count_volumes_and_prices(swap_statuses):
    return {}

# tuple, string, string -> list
# returning orderbook for given trading pair
def get_mm2_orderbook_for_pair(pair, mm2_rpc_password):
    mm2_host = "http://127.0.0.1:7783"
    params = {
              'userpass': mm2_rpc_password,
              'method': 'orderbook',
              'base': pair[0],
              'rel': pair[1]
             }
    r = requests.post(mm2_host, json=params)
    return json.loads(r.text)


# list -> string
# returning lowest ask from provided orderbook

def find_lowest_ask(orderbook):
    lowest_ask = {"price" : "0"}
    for ask in orderbook["asks"]:
        if lowest_ask["price"] == "0":
            lowest_ask = ask
        elif Decimal(ask["price"]) < Decimal(lowest_ask["price"]):
            lowest_ask = ask
    return lowest_ask["price"]


# list -> string
# returning highest bid from provided orderbook
def find_highest_bid(orderbook):
    highest_bid = {"price" : "0"}
    for bid in orderbook["bids"]:
        if Decimal(bid["price"]) > Decimal(highest_bid["price"]):
            highest_bid = bid
    return highest_bid["price"]

# SUMMARY Endpoint
# tuple, string -> dictionary
# Receiving tuple with base and rel as an argument and producing CMC summary endpoint data, requires mm2 rpc password and sql db connection
def summary_for_pair(pair, mm2_rpc_password, sql_coursor):
    # TODO: calculate data
    pair_summary = {"traiding_pair": "", "last_price": 0, "lowest_ask": 0, "highest_bid": 0,
                    "base_volume": 0, "quote_volume": 0, "price_change_percent_24h": 0, "highest_price_24h": 0,
                    "lowest_price_24h": 0}

    pair_summary["trading_pair"] = pair[0] + "_" + pair[1]
    orderbook = get_mm2_orderbook_for_pair(pair, mm2_rpc_password)
    pair_summary["lowest_ask"] = find_lowest_ask(orderbook)
    pair_summary["highest_bid"] = find_highest_bid(orderbook)

    # TODO: functions stubbed atm!!!
    timestamp_24h_ago = int((datetime.now() - timedelta(1)).strftime("%s"))
    swaps_for_pair_24h = get_swaps_since_timestamp_for_pair(sql_coursor, pair, timestamp_24h_ago)
    pair_24h_volumes_and_prices = count_volumes_and_prices(swaps_for_pair_24h)

    pair_summary["last_price"] = pair_24h_volumes_and_prices["last_price"]
    pair_summary["base_volume"] = pair_24h_volumes_and_prices["base_volume"]
    pair_summary["quote_volume"] = pair_24h_volumes_and_prices["quote_volume"]
    pair_summary["price_change_percent_24h"] = pair_24h_volumes_and_prices["price_change_percent_24h"]
    pair_summary["highest_price_24h"] = pair_24h_volumes_and_prices["highest_price_24h"]
    pair_summary["lowest_price_24h"] = pair_24h_volumes_and_prices["lowest_price_24h"]

    return pair_summary