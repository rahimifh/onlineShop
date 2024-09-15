import os

from startup.settings import BASE_DIR


def loging(phone, id):
    path = os.path.join(BASE_DIR, "log/page3")
    try:
        x = open(f"{path}/{id}.txt", "r")
        y = x.read()
        x.close()
    except:
        y = "0"
    f = open(f"{path}/{id}.txt", "w+")
    if y == "0":
        f.write("1")
    else:
        total = eval(y) + 1
        f.write(str(total))
    f.close()
    p = open(f"{path}/ac{id}.txt", "a")
    p.write(f"{phone}\n")
    p.close()


def page4Log(phone, id):
    path = os.path.join(BASE_DIR, "log/page4")
    p = open(f"{path}/ac{id}.txt", "a")
    p.write(f"{phone}\n")
    p.close()


def clicklog(code):
    path = os.path.join(BASE_DIR, f"log/{code}")
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
        x = open(f"{path}/{code}.txt", "w")
        x.write("0")
        x.close()
    try:
        x = open(f"{path}/{code}.txt", "r")
        y = x.read()
        x.close()
    except:
        y = "0"
    f = open(f"{path}/{code}.txt", "w+")
    if y == "0":
        f.write("1")
    else:
        total = eval(y) + 1
        f.write(str(total))
    f.close()
