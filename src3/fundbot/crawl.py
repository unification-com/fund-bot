from python_graphql_client import GraphqlClient

XFUND_MARKET = '0xab2d2f5bc36620a57ec4bb60d6a7df2a847deab5'


def uniswap_data():
    client = GraphqlClient(
        endpoint="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2")
    query = """
     query CurrentTokenData($pairId: ID){
          pair(id: $pairId)  {
            token0 {id symbol name}
            token1 {id symbol name}
            reserve0
            reserve1
          }
      }
    """
    variables = {"pairId": XFUND_MARKET}
    data = client.execute(query=query, variables=variables)
    pooled_xfund = data['data']['pair']['reserve0']
    pooled_eth = data['data']['pair']['reserve1']
    return float(pooled_eth), float(pooled_xfund)


if __name__ == "__main__":
    uniswap_data()
