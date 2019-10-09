import math
import json
import statistics


def get_quantile_avgs(scores, num_quantiles=4):
    def _avg(scores: list, group: int):
        # print("group %d: %s" % (group, ' '.join(scores)))
        sum = 0
        count = 0
        for s in scores:
            if not s.endswith('*'):
                count += 1
            else:
                s = s.replace('*', '')
                count += 1
            sum += int(s)
        return sum / count

    sorted_arr = sorted(scores, key=lambda x: int(x.replace('*', '')))
    q = len(scores) / num_quantiles
    quantile_avgs = [_avg(sorted_arr[math.ceil(i*q):math.ceil((i+1)*q)], i+1) for i in range(num_quantiles)]
    return quantile_avgs


def get_median(scores):
    int_scores = [int(s.replace('*', '')) for s in scores]
    return statistics.median(int_scores)


if __name__ == '__main__':
    with open('test_innings.json') as test_innings_f:
        j = json.load(test_innings_f)
        for player in j:
            avgs = get_quantile_avgs(player['test_innings'], 4)
            med = get_median(player['test_innings'])
            print(player['name'] + ": " + str(med))
            print(player['name'] + ": " + '\t'.join(map(lambda x: '{0:.2f}'.format(x), avgs)))

