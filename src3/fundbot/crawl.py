import requests

TOKEN_ADDRESS = '0xab2D2F5bc36620A57Ec4bB60D6A7Df2a847dEab5'


def uniswap_data():
    payload = '{"query":"query CurrentTokenData($pairId: ID\u0021, $yesterday: Int\u0021) {\\n  pair(id: $pairId) {\\n    token0 {id symbol name}\\n    token1 {id symbol name}\\n    reserve0\\n    reserve1\\n    txCount\\n  }\\n  pairHourDatas(where: {hourStartUnix_gt: $yesterday, pair: $pairId}) {\\n    hourlyVolumeToken0\\n    hourlyVolumeToken1\\n    hourlyVolumeUSD\\n  }\\n  swaps(first: 1000, where: {pair: $pairId}, orderBy: timestamp, orderDirection: desc) {\\n    id\\n    pair {\\n      token0 {symbol}\\n      token1 {symbol}\\n    }\\n    transaction {id}\\n    timestamp\\n    sender\\n    amount0In\\n    amount1In\\n    amount0Out\\n    amount1Out\\n    amountUSD\\n    to\\n  }\\n}","variables":{"pairId":"0xab2d2f5bc36620a57ec4bb60d6a7df2a847deab5","yesterday":1602077532}}'
    url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
    r = requests.post(url, data=payload)
    data = r.json()
    pooled_xfund = data['data']['pair']['reserve0']
    pooled_eth = data['data']['pair']['reserve1']
    return float(pooled_eth), float(pooled_xfund)


if __name__ == "__main__":
    uniswap_data()
