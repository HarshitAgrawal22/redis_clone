# from icecream import ic

# setter: set[dict[str:str]] = set({("name", "c"), ("name", "c")})
# print(setter)

# mystr = "               herllo\r\n             "
# print(mystr)
# ic(mystr.strip(" "))

import threading

# import try:
#     pass
# except Exception as error:
#     pass


def func():
    i = 0
    while True:
        i += 1
        if i == 1000:
            raise Exception("Bhaang")
        print(i)


def func2():
    i = 0
    while True:
        i -= 1
        if i == -1010:
            raise Exception("Bhaang")
        print(i)


T1 = threading.Thread(target=func)
T2 = threading.Thread(target=func2)

T1.start()
T2.start()
