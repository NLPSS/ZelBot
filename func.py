import csv
import qwests

# Открытие файла
def open_file(name):
    input_file = open(name)
    input_read = csv.reader(input_file)
    name = list(input_read)
    return name

# Закрытие файла
def save_file(name):
    with open('db.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for i in range(len(name)):
            csv_writer.writerow(name[i])
    csv_file.close()

# Преобразование локации
def norm_loc(loc_ex):
    loc_str = str(loc_ex)
    lon = float(loc_str[14:22])
    lan = float(loc_str[37:45])
    my_loc = [lon, lan]
    return my_loc

# Добавление в базу
def ent_user(Uid_int, db):
    Uid = str(Uid_int)
    ent = False
    print(db)
    for i in range(len(db)):
        if db[i][1] == Uid:
            ent = True
    if ent == False:
        db.append([str(len(db)), str(Uid), 'Current', 'None', 'None'])
    return ent

#  Запрос текущего квеста
def my_qwest(Uid_int, db):
    Uid = str(Uid_int)
    global Qno
    Qno = False
    for i in range(len(db)):
        if db[i][1] == Uid:
            Uno = i
    for j in range(len(db[Uno])):
        if db[Uno][j] == 'Current':
            Qno = j - 1
    print(Qno)
    return Qno


#  Сравнение геолокации
def in_right_place(Uid_int, db, loc, CQ):
    u_lon = loc[0]
    u_lan = loc[1]
    if CQ == 1:
        q_lon = qwests.qwest_loc_1[0]
        q_lan = qwests.qwest_loc_1[1]
    if CQ == 2:
        q_lon = qwests.qwest_loc_2[0]
        q_lan = qwests.qwest_loc_2[1]
    er = 0.0005
    if u_lon <= (q_lon + er) and u_lon >= (q_lon - er) and u_lan <= (q_lan + er) and u_lan >= (q_lan - er):
        return(True)
    else:
        print(False)

#  Следующий квест
def next_qwest(Uid_int, db):
    Uid = str(Uid_int)
    global Qno
    Uno = False
    CQ = False
    for i in range(len(db)):
        if db[i][1] == Uid:
            Uno = i
    for j in range(len(db[Uno])):
        if db[Uno][j] == 'Current':
            CQ = j
    if CQ != 4:
        db[Uno][CQ] = 'Done'
        db[Uno][CQ+1] = 'Current'
