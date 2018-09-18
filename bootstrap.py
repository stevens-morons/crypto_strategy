import pandas as pd
import numpy as np
import strat_volburst
import strat_donchian

# ===== Generate different samples of returns with replacement =====
def generate_samples(data,n_samples):
    returns = np.log(data['Close'].shift(1)/data['Close'])
    returns_sample = returns.sample(n=n_samples, replace=True)
    return returns_sample

# ===== Generate price series with an arbitrary starting point =====
def generate_price_series(data, sample):
    data.set_index('Date')
    starting_point = data.lookup([100], ['Close'])

    test_list = []
    for ret in range(len(sample)):
        price_series = starting_point * (1+sample[ret])
        test_list.append(price_series)
        starting_point = test_list[-1]
    # print test_list[0:5]
    test_list = pd.DataFrame(test_list, columns=['Close'])

    return test_list


# These test periods are the optimised periods we found from various strategies
# Include lists of periods of all Timeframes we optimised
test_volburst_1hr = [5, 6, 10, 12, 13]
test_donchian_1hr = [5, 6, 10, 12, 13]
test_rsi_1hr = [5, 6, 10, 12, 13]

# ===== Example of Volburst 1 Hr ==========
data = pd.read_csv("gemini_BTCUSD_1hr.csv")
samples_volburst_1hr = [generate_samples(data=data,
                                         n_samples=100000) for _ in range(10)]
price_series = [generate_price_series(data=data,
                                      sample=samples_volburst_1hr) for _ in range(10)]
cum_ret_list = [strat_volburst.strategy(data=price_series,
                                        list_periods=test_volburst_1hr) for _ in range(10)][1][-1:]
boot_volburst_1hr = np.mean(cum_ret_list)
print 'Bootstrap returns for Volburst_1hr: {}%'.format(boot_volburst_1hr)


