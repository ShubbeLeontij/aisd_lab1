import random
import time


class Element:
    def __init__(self, val=None, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

    def __eq__(self, other):  # Описание механизма сравнения двух элементов
        if other is None:
            return False
        if not isinstance(other, int | Element):
            raise TypeError
        return self.val == (other if isinstance(other, int) else other.val)

    def set(self, val):  # Установить значение
        self.val = val
        return self.val

    def get(self):  # Получить значение
        return self.val

    def copy(self):  # Копирование себя
        return Element(self.get())


class List2:
    def __init__(self, *elements):
        self.head = None
        self.tail = None
        self.cur = None
        self.empty = True
        for el in elements:
            self.add_bottom(el)

    def is_empty(self):  # Проверка на пустоту списка
        return self.empty

    def get_length(self):  # Получение размера списка
        counter = 0
        self.cur = self.head
        while self.cur is not None:
            counter += 1
            self.cur = self.cur.next
        return counter

    def add_first(self, el):  # Добавление первого элемента в пустой список
        if not isinstance(el, Element):
            el = Element(el)
        self.head = el
        self.tail = el
        self.empty = False

    def print(self):  # Вывод списка на экран
        self.cur = self.head
        while self.cur is not None:
            print(self.cur.get(), end=' ')
            self.cur = self.cur.next
        print('\n', end='')

    def add_top(self, el):  # Добавление в начало списка
        if not isinstance(el, Element):
            el = Element(el)
        if self.is_empty():
            self.add_first(el)
        else:
            self.head.prev = el
            el.next = self.head
            self.head = el

    def add_bottom(self, el):  # Добавление в конец списка
        if not isinstance(el, Element):
            el = Element(el)
        if self.is_empty():
            self.add_first(el)
        else:
            self.tail.next = el
            el.prev = self.tail
            self.tail = el

    def delete_top(self):  # Удаление первого элемента
        if self.is_empty() or self.head.next is None:
            self.head = None
            self.tail = None
            self.empty = True
        else:
            self.head.next.prev = None
            self.head = self.head.next

    def delete_bottom(self):  # Удаление последнего элемента
        if self.is_empty() or self.tail.prev is None:
            self.head = None
            self.tail = None
            self.empty = True
        else:
            self.tail.prev.next = None
            self.tail = self.tail.prev

    def get_by_index(self, index):  # Получение элемента по индексу
        if index < 0 or index >= self.get_length():
            raise Exception
        self.cur = self.head
        for i in range(index):
            self.cur = self.cur.next
        return self.cur

    def delete_by_index(self, index):  # Удаление элемента по индексу
        if index < 0 or index >= self.get_length():
            raise Exception
        elif index == 0:
            self.delete_top()
        elif index == self.get_length() - 1:
            self.delete_bottom()
        else:
            self.cur = self.get_by_index(index)
            self.cur.prev.next = self.cur.next
            self.cur.next.prev = self.cur.prev

    def add_by_index(self, index, el):  # Добавление элемента по индексу
        if not isinstance(el, Element):
            el = Element(el)
        if index < 0 or index >= self.get_length():
            raise Exception
        elif index == 0:
            self.add_top(el)
        elif index == self.get_length() - 1:
            self.add_bottom(el)
        else:
            self.cur = self.get_by_index(index)
            el.prev = self.cur.prev
            el.next = self.cur
            self.cur.prev.next = el
            self.cur.prev = el

    def delete_all(self):  # Удаление всех элементов списка
        self.head = None
        self.tail = None
        self.cur = None
        self.empty = True

    def replace_by_index(self, index, el):  # Замена элемента по индексу на передаваемый элемент
        if not isinstance(el, Element):
            el = Element(el)
        if index < 0 or index >= self.get_length():
            raise Exception
        elif index == 0:
            self.delete_top()
            self.add_top(el)
        elif index == self.get_length() - 1:
            self.delete_bottom()
            self.add_bottom(el)
        else:
            self.cur = self.get_by_index(index)
            el.prev = self.cur.prev
            el.next = self.cur.next
            self.cur.prev.next = el
            self.cur.next.prev = el

    def swap_by_index(self, index1, index2):  # Обмен двух элементов списка по индексам
        index1, index2 = min(index1, index2), max(index1, index2)
        if index1 < 0 or index2 >= self.get_length():
            raise Exception
        elif index1 == index2:
            return
        else:
            self.cur = self.head
            el1 = self.get_by_index(index1).copy()
            el2 = self.get_by_index(index2).copy()
            self.replace_by_index(index1, el2)
            self.replace_by_index(index2, el1)

    def invert(self):  # Меняет порядок элементов в списке на обратный
        self.cur = self.head
        while self.cur is not None:
            self.cur.prev, self.cur.next = self.cur.next, self.cur.prev
            self.cur = self.cur.prev
        self.head, self.tail = self.tail, self.head

    def merge_top(self, l2):  # Вставка другого списка в начало
        l2.tail.next = self.head
        self.head.prev = l2.tail
        self.head = l2.head

    def merge_bottom(self, l2):  # Вставка другого списка в конец
        l2.head.prev = self.tail
        self.tail.next = l2.head
        self.tail = l2.tail

    def merge_by_index(self, index, l2):  # Вставка другого списка начиная с индекса
        if index < 0 or index >= self.get_length():
            raise Exception
        elif index == 0:
            self.merge_top(l2)
        elif index == self.get_length() - 1:
            self.merge_bottom(l2)
        else:
            self.cur = self.get_by_index(index)
            l2.head.prev = self.cur.prev
            l2.tail.next = self.cur
            self.cur.prev.next = l2.head
            self.cur.prev = l2.tail

    def contains(self, l2):  # Проверка на содержание другого списка
        remembered = self.head
        while remembered is not None:
            self.cur = remembered
            l2.cur = l2.head
            while self.cur == l2.cur:
                self.cur = self.cur.next
                l2.cur = l2.cur.next
                if l2.cur is None:
                    return True
            remembered = remembered.next
        return False

    def find(self, l2):  # Поиск первого вхождения другого списка
        remembered = self.head
        index = 0
        while remembered is not None:
            self.cur = remembered
            l2.cur = l2.head
            while self.cur == l2.cur:
                self.cur = self.cur.next
                l2.cur = l2.cur.next
                if l2.cur is None:
                    return index
            remembered = remembered.next
            index += 1
        return -1

    def rfind(self, l2):  # Поиск последнего вхождения другого списка
        remembered = self.tail
        index = self.get_length()
        while remembered is not None:
            self.cur = remembered
            l2.cur = l2.tail
            while self.cur == l2.cur:
                self.cur = self.cur.prev
                l2.cur = l2.cur.prev
                if l2.cur is None:
                    return index - l2.get_length()
            remembered = remembered.prev
            index -= 1
        return -1


def copy(l2):  # Копирование списка
    new_list = List2()
    l2.cur = l2.head
    while l2.cur is not None:
        new_list.add_bottom(l2.cur.copy())
        l2.cur = l2.cur.next
    return new_list


def generate(N, min_el, max_el):  # Генерация случайного списка
    new_list = List2()
    for i in range(N):
        new_list.add_bottom(random.randint(min_el, max_el))
    return new_list


def get_time(func, *args):  # Получение времени выполнения функции
    ts = time.time()
    func(*args)
    return time.time() - ts


run_dict = {  # Примеры вызова методов со случайными параметрами
    "1": lambda N: get_time(generate(N, min_el, max_el).add_bottom, random.randint(min_el, max_el)),
    "2": lambda N: get_time(generate(N, min_el, max_el).add_top, random.randint(min_el, max_el)),
    "3": lambda N: get_time(generate(N, min_el, max_el).delete_bottom),
    "4": lambda N: get_time(generate(N, min_el, max_el).delete_top),
    "5": lambda N: get_time(generate(N, min_el, max_el).add_by_index, random.randint(1, N - 1), random.randint(min_el, max_el)),
    "6": lambda N: get_time(generate(N, min_el, max_el).get_by_index, random.randint(1, N - 1)),
    "7": lambda N: get_time(generate(N, min_el, max_el).delete_by_index, random.randint(1, N - 1)),
    "8": lambda N: get_time(generate(N, min_el, max_el).get_length),
    "9": lambda N: get_time(generate(N, min_el, max_el).delete_all),
    "10": lambda N: get_time(generate(N, min_el, max_el).replace_by_index, random.randint(1, N - 1), random.randint(min_el, max_el)),
    "11": lambda N: get_time(generate(N, min_el, max_el).is_empty),
    "12": lambda N: get_time(generate(N, min_el, max_el).invert),
    "13": lambda N: get_time(generate(N, min_el, max_el).merge_by_index, random.randint(1, N - 1), generate(N, min_el, max_el)),
    "14": lambda N: get_time(generate(N, min_el, max_el).merge_bottom, generate(N, min_el, max_el)),
    "15": lambda N: get_time(generate(N, min_el, max_el).merge_top,  generate(N, min_el, max_el)),
    "16": lambda N: get_time(generate(N, min_el, max_el).contains, generate(N, min_el, max_el)),
    "17": lambda N: get_time(generate(N, min_el, max_el).find, generate(N, min_el, max_el)),
    "18": lambda N: get_time(generate(N, min_el, max_el).rfind, generate(N, min_el, max_el)),
    "19": lambda N: get_time(generate(N, min_el, max_el).swap_by_index, random.randint(1, N - 1), random.randint(1, N - 1)),
    "": lambda N: exit()
}
min_el = 0  # Минимальное допустимое значение элемента
max_el = 10**6  # Максимальное допустимое значение элемента
points = range(10**5, 10**6 + 1, 10**5)  # Точки (количества элементов в списке для разных вызовов функции)

if __name__ == "__main__":
    while True:
        case = input("Enter method index to get its time to run: ")
        print("N      Time, seconds")
        for N in points:
            print(N, run_dict[case](N))


