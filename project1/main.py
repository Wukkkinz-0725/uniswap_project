# +
import pandas as pd
from pycoingecko import CoinGeckoAPI
from datetime import datetime
from dateutil import tz

class CoinGeckoWrapper:
    def __init__(self):
        self.cg = CoinGeckoAPI()
        
    def get_trend_coins_df(self):
        trend_coins_data = self.cg.get_search_trending()
        trend_coins_data = [coin['item'] for coin in trend_coins_data['coins']]
        trend_coins_df = pd.DataFrame(trend_coins_data)[['id', 'name', 'symbol']]
        return trend_coins_df

    def get_all_coins_df(self):
        def local_update_time(t):
            last_updated_utc = datetime.fromisoformat(t.replace("Z", "+00:00"))
            local_timezone = tz.tzlocal()
            last_updated_local = last_updated_utc.astimezone(local_timezone)
            return last_updated_local.strftime("%Y-%m-%d %H:%M:%S")
        df = pd.DataFrame(self.cg.get_coins_markets(vs_currency='usd'))[['id', 'symbol', 'name', 'current_price', 'last_updated']]
        df['last_updated'] = df['last_updated'].apply(local_update_time)
        df['current_price'] = df['current_price'].apply(lambda x: round(x, 4))
        return df


# -

cgw = CoinGeckoWrapper()

cgw.get_all_coins_df()

cgw.get_trend_coins_df()


