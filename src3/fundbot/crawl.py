import logging

from python_graphql_client import GraphqlClient

log = logging.getLogger(__name__)

XFUND_MARKET = '0xab2d2f5bc36620a57ec4bb60d6a7df2a847deab5'


def calculate_price(swap):
    amount0Out = float(swap['amount0Out'])
    amount1In = float(swap['amount1In'])
    amount0In = float(swap['amount0In'])
    amount1Out = float(swap['amount1Out'])

    if amount0Out != 0:
        price = amount1In / amount0Out
    else:
        price = amount1Out / amount0In

    return price


async def uniswap_data():
    log.info(f"Fetching Uniswap Data")
    client = GraphqlClient(
        endpoint="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2")
    query = """
     query CurrentTokenData($pairId: ID){
          pair(id: $pairId)  {
            token0 {id symbol name}
            token1 {id symbol name}
            reserve0
            reserve1
          },
          swaps(first:1000, where: {
            pair:$pairId
          },orderBy:timestamp
           ,orderDirection:desc) {
            pair {
              token0 {symbol}
              token1 {symbol}      
            }
            timestamp
            amount0In
            amount1In
            amount0Out
            amount1Out
            amountUSD
          }          
      }
    """
    variables = {"pairId": XFUND_MARKET}
    data = await client.execute_async(query=query, variables=variables)
    pooled_xfund = data['data']['pair']['reserve0']
    pooled_eth = data['data']['pair']['reserve1']
    swaps = data['data']['swaps']
    last_swap = swaps[0]
    last_price = calculate_price(last_swap)
    log.info(f"Last price {last_price} ETH ")
    log.info(f"Fetched Uniswap Data")
    return float(pooled_eth), float(pooled_xfund), last_price


if __name__ == "__main__":
    uniswap_data()
