# import redis


class Calculator:
    def __init__(self, metrics: [], count_frames=0):
        self.potato = {}
        self.metrics = metrics
        self.count_frames = count_frames
        # self.redis = redis.Redis()
        # self.redis.set('potato_strong', 0)
        # self.min_size = min_size
        # self.max_size = max_size

    def add(self, id_entity: str, size: float):
        # self.redis.zadd('potato', {id: size})
        if id_entity in self.potato:
            self.potato[id_entity]['count'] += 1
            self.potato[id_entity]['size'] = size
        else:
            self.potato[id_entity] = {'count': 1, 'size': size}

    def count(self) -> {}:
        """

        :return: {'big': 2, 'medium': 0, 'small': 0}
        :rtype:
        """
        # if self.min_size < size < self.max_size:
        #     self.redis.incr('potato_strong')
        # self.redis.zcount('potato', min_size, max_size)
        sorted_potato = {}
        # count = 0

        for key in self.potato.keys():
            if self.potato[key]['count'] > self.count_frames:
                for metrics in self.metrics:
                    name = metrics[0]
                    min_size = metrics[1]
                    max_size = metrics[2]
                    if min_size <= self.potato[key] < max_size:
                        if name in sorted_potato:
                            sorted_potato[name] += 1
                        else:
                            sorted_potato[name] = 1
        return sorted_potato


if __name__ == '__main__':
    c = Calculator()
    c.add('1', 0.3)
    c.add('1', 0.1)
    c.add('2', 0.4)
    c.add('3', 0.5)
    count = c.count(0.2, 0.5)
    print(count)
