#encoding=utf-8

import itertools
import copy

class Water_cup:
    '''
    水杯，可以向水杯注满水、注入指定量的水，或者从另一个杯子向杯子倒水
    '''

    def __init__(self, size = 0):
        '''
        初始化
        size: 水杯容量
        '''
        self._size = size
        self._water = 0

    def __str__(self):
        return "<class {}> {}".format(self.__class__, self._water)

    def get_size(self):
        '''
        获取水杯容量

        return:
            size
        '''

        return self._size

    def is_empty(self):
        '''
        水杯是否空

        return：
            boolean
        '''
        return self._water == 0

    def is_full(self):
        '''
        水杯是否满

        return:
            boolean
        '''
        return self._water >= self._size

    def fill(self, n):
        '''
        向 cup 灌水
        n: 灌水的数量，或者是一个杯子，会一直灌到当前杯子满或者水源杯子空为止
        '''
        if isinstance(n, Water_cup):
            from_cup = n
            while from_cup.is_empty() == False and self.is_full() == False:
                n_water = from_cup.get_n_water(1)
                self.fill(n_water)
            return

        self._water += n

    def fillup(self):
        '''
        向水杯注满水
        '''
        self._water = self._size
            

    def get_water(self):
        '''
        获取水杯中水量

        return:
            int 水量
        '''
        return self._water

    def get_n_water(self, n = 1):
        '''
        从杯子里取出水
        n: 取出水的数量

        return:
            int 取出的水量，<= n
        '''
        if self._water >= n:
            self._water -=n 
            return n

        water = self._water
        self._water = 0
        return water


cup_index_list  = [0, 1, 2]

# 杯子顺序所有可能的组合
cup_map = list(itertools.permutations(cup_index_list, 2))


cup_size_list = [8, 5, 3]

cups = [Water_cup(size) for size in cup_size_list]

cups[0].fillup()

result_set = set([(8,0,0)])

print("cup size:")
for cup in cups:
    print(cup.get_size())

def add_result(cups):
    result = tuple([cup.get_water() for cup in cups])
    if result not in result_set:
        result_set.add(result)
        return True, result

    return False, None


class End_point:
    def __init__(self, cups, record):
        self._cups = cups
        self._record = record

    def get_cups(self):
        return self._cups

    def get_record(self):
        return self._record

    def __str__(self):
        return "cups:{}, record:{}".format(str(self._cups), str(self._record))


level = [End_point(cups, [(8,0,0)])]


def search_level(level):

    if len(level) == 0:
        return

    next_level = []

    for point in level:
        cups = point.get_cups()
        record = point.get_record()

        for index in cup_map:
            cups_copy = copy.deepcopy(cups)

            from_cup_index = index[0]
            to_cup_index = index[1]

            # make copy, or original data will be lost.
            from_cup = cups_copy[from_cup_index]
            to_cup = cups_copy[to_cup_index]

            to_cup.fill(from_cup)

            is_new, result = add_result(cups_copy)
            if is_new:
                record_copy = copy.copy(record)
                record_copy.append(result)
                if 4 in result:
                    print("ok path:", record_copy)
                else:
                    next_level.append(End_point(cups_copy, record_copy))
                
    search_level(next_level)


search_level(level)

