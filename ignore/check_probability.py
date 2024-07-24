# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/12 19:37
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : check_probability.py
# ----------------------
import random
from collections import Counter
from pprint import pprint


def random_choice_amount(amount_list, limit_list, receive_list):
    n = len(amount_list)
    # 生成可领取的红包列表
    l = []
    remain_list = []
    for i in range(n):
        remain = limit_list[i] - receive_list[i]
        if remain < 0:
            remain = 0
        remain_list.append(remain)
        l = l + [amount_list[i]] * remain
    if len(l) == 0:
        return None, None
    # 抽取红包
    random.shuffle(l)
    amount = random.choice(l)
    # 查找领了哪个红包，以便用于后续更新数量
    index = None
    for i in range(n):
        if amount_list[i] == amount and remain_list[i] > 0:
            index = i
            break
    if index is None:
        return None, None
    return index, amount


def get_avg_probs(red_packet_list):
    n = len(red_packet_list)
    total_probs = Counter()
    for i in range(n):
        freq = Counter(red_packet_list[:i+1])
        probs = {key: val / (i+1) for key, val in freq.items()}
        total_probs.update(probs)
    avg_probs = {key: val / n for key, val in total_probs.items()}
    return avg_probs


def main():
    # 红包金额列表
    amount_list = [1, 2, 3, 4]
    # 红包个数次数
    limit_list = [70000, 10000, 10000, 10000]
    # 领取次数
    receive_count = 10000
    # 已领取红包数量列表
    receive_list = [0, 0, 0, 0]
    # 领取的红包金额列表
    receive_amount_list = []
    #
    for i in range(receive_count):
        # index 是抽取的红包索引，amount 是红包金额
        index, amount = random_choice_amount(amount_list, limit_list, receive_list)
        if amount is None:
            print('领取失败！奖励已被人抢光了', i)
            continue
        receive_list[index] += 1
        receive_amount_list.append(amount)
    print('领取的红包', receive_amount_list)

    avg_prob = get_avg_probs(receive_amount_list)
    print('金额概率')
    pprint(avg_prob)


if __name__ == '__main__':
    main()
