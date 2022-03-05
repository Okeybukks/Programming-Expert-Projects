def flatten_lists(func):
    def wrapper(*args):
        print(args)
        new = []
        for i in args:
            if type(i) != list:
                new.extend([i])
            else:
                new.extend(i)

        result = func(new)
        return result

    return wrapper


def convert_strings_to_ints(func):
    def wrapper(*args):

        new = args[0][:]
        print(args)
        for val in new:
            if type(val) == str and val.isdigit() != True:
                args[0].remove(val)
        print(args)
        new = [int(i) if type(i) == str or type(i) == bool else i for i in args[0]]

        result = func(new)
        return result

    return wrapper


def filter_integers(func):
    def wrapper(*args):
        print(args)
        args = list(filter(lambda x: type(x) == int, args[0]))
        result = func(args)
        return result

    return wrapper


def generate_string(string, frequency):
    # Write your code here.
    n_string = ""
    for i in range(len(string)):
        n_string += (string[i]) * frequency
    yield n_string


class GenerateString:
    def __init__(self, string, frequency):
        # Write your code here.
        self.string = string
        self.frequency = frequency
        self.n_string = ""
        self.count = 0

    # Write your code here.
    def __iter__(self):
        self.current_char_index = 0
        self.char_counter = 0
        return self

    def __next__(self):
        if self.char_counter >= self.frequency:
            self.char_counter = 0
            self.current_char_index += 1

        if self.current_char_index >= len(self.string):
            raise StopIteration

        self.char_counter += 1
        return self.string[self.current_char_index]


class WordCounter:
    def __init__(self):
        # Write your code here.
        self.text_list = []

    # Write your code here.
    def process_text(self, text):
        # text = text.lower()
        self.text_list = text.split()

    def get_word_count(self, word):

        word_count = self.text_list.count(word)

        return word_count


import asyncio


class BatchFetcher:
    # The `database` has an `async_fetch` method
    # that you should use in your code. This method
    # takes in a record id and returns a record.
    def __init__(self, database):
        # Write your code here.
        self.database = database
        self.records = []

    # Write your code here.
    async def async_fetch(self, record_id):

        return self.database.records.get(record_id)

    async def fetch_records(self, record_ids):
        for id in record_ids:
            task = asyncio.create_task(self.async_fetch(id))
            record = await (task)

            self.records.append(record)

        return self.records


# async def t1():
#     await t3()
#     print("t1")

# async def t2():
#     print("t2")

# async def t3():
#     await t2()
#     print("t3")

# asyncio.run(t1())


# async def fetch_data():
#     print("Fetching data...")
#     await asyncio.sleep(6)

#     return ({"data":100})

# async def counter():

#     for val in range(1, 11):
#         print(val)
#         await asyncio.sleep(2)

# async def main():
#     task = asyncio.create_task(fetch_data())
#     task2 = asyncio.create_task(counter())

#     data = await task
#     print(data)
#     await task2

# asyncio.run(main())


import os

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

print(f"Username: {username}")
print(f"Password: {password}")
