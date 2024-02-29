from web3 import Web3
from web3.middleware import geth_poa_middleware

networks = {}

polygon = Web3(Web3.HTTPProvider('https://polygon-rpc.com/'))
polygon.middleware_onion.inject(geth_poa_middleware, layer=0)
networks["polygon"] = polygon
print("Connected to Polygon network")

bsc = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
bsc.middleware_onion.inject(geth_poa_middleware, layer=0)
networks["bsc"] = bsc
print("Connected to Binance Smart Chain network")