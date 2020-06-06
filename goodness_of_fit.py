from datetime import *
import pandas as pd
import numpy
import math
from scipy.stats import chi2
import ast


def get_deltas(df):
    deltas = []
    for i in range(len(df) - 1):
        if df.iloc[i].Day == df.iloc[i + 1].Day:
            delta = datetime.strptime(df.iloc[i + 1].Hour, '%H:%M:%S') - datetime.strptime(df.iloc[i].Hour, '%H:%M:%S')
            deltas.append(int(delta.total_seconds() / 60))
    return deltas


def get_check_time(df):
    times = []
    for i in range(len(df) - 1):
        times.extend(ast.literal_eval(df.iloc[i]['Checks_Lengths']))
    return times


def exp_func(t):
    return 1 - math.pow(math.e, -(1 / m) * t)


def uniform_func(t):
    return (t - a + 1) / (b - a + 1)


def fix_bins(df, min_quantity, func):
    problem = True
    while problem:
        df['Ei'] = df.apply(
            lambda row: df['Oi'].sum() * (func(row['max']) - func(row['min'])), axis=1)
        df = df.reset_index(drop=True)
        problem = False
        for i in range(len(df)):
            if df.iloc[i]['Ei'] < min_quantity:
                if i != len(df) - 1:
                    df.at[i, 'max'] = df.iloc[i + 1]['max']
                    df.at[i, 'Oi'] += df.iloc[i + 1]['Oi']
                    df = df.drop(df.index[i + 1])
                    problem = True
                    break
                else:
                    df.at[i, 'min'] = df.iloc[i - 1]['min']
                    df.at[i, 'Oi'] += df.iloc[i - 1]['Oi']
                    df = df.drop(df.index[i - 1])
                    problem = True
                    break
    df = df.reset_index(drop=True)
    return df


def split_to_bins(data, min_quantity, func):
    global m, b, a
    m = numpy.mean(data)
    b = max(data)
    a = min(data)
    data = sorted(data)
    min_num = min(data)
    max_num = max(data)
    bins = math.sqrt(len(data))
    jump = max(int((max_num - min_num) / bins), 2)
    max_bound = min_num + jump
    min_bound = min_num
    dict = {}
    ranges = []
    counts = []
    while True:
        count = 0
        for num in data:
            if min_bound <= num < max_bound:
                count += 1
        if max_bound == max_num:
            ranges.append((min_bound, max_bound + 1))
            counts.append(count + data.count(max_num))
            break
        else:
            ranges.append((min_bound, max_bound))
            counts.append(count)
        min_bound += jump
        max_bound = min(max_bound + jump, max_num)
    for i in range(len(ranges)):
        dict[ranges[i]] = counts[i]
    df = pd.DataFrame(columns=['min', 'max', 'Oi'])
    for key, val in dict.items():
        df = df.append({'min': key[0], 'max': key[1], 'Oi': val}, ignore_index=True)
    df = fix_bins(df, min_quantity, func)
    return df


def check_hypothesis(data, func):
    bins_df = split_to_bins(data, 5, func)
    bins_df['Oi-Ei'] = bins_df['Oi'] - bins_df['Ei']
    bins_df['(Oi-Ei)^2/Ei'] = bins_df['Oi-Ei'] ** 2 / bins_df['Ei']
    statistic = bins_df['(Oi-Ei)^2/Ei'].sum()
    chi2_critical = chi2.ppf(0.99, len(bins_df) - 2)
    print('Hypothesis', 'accepted' if statistic < chi2_critical else 'denied', 'because statistic(',
          round(statistic, 3), ') and critical(', round(chi2_critical, 3), ').')


for filename in ['east_data', 'west_data']:
    print("Filename:", filename)
    df = pd.read_csv(filename + '.csv')
    deltas = get_deltas(df)
    check_hypothesis(deltas, exp_func)
    print('m =', round(m, 4), '| lambda =', round(1 / m, 4))
    checks_time = get_check_time(df)
    check_hypothesis(checks_time, uniform_func)
    print('b =', b, '| a =', a)
