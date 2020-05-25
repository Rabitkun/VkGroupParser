import vk
import vk_api


def getMembers(groupId): #какой-то метод из туториала
    first = vkApi.groups.getMembers(group_id = groupId, v=5.92)  # Первое выполнение метода
    data = first["items"]  # Присваиваем переменной первую тысячу id'шников
    count = first["count"] // 1000  # Присваиваем переменной количество тысяч участников
    # С каждым проходом цикла смещение offset увеличивается на тысячу
    # и еще тысяча id'шников добавляется к нашему списку.
    for i in range(1, count+1):  
        data = data + vkApi.groups.getMembers(group_id = groupId, v=5.92, offset=i*1000)["items"]
    print('Already taken members')
    return data

def getMembersNames(data, token): # получаем список ФИ по списку айдишников пользователей
    names = []
    vk = vk_api.VkApi(token=token)
    fullpercent = len(data)
    lastpercent = -1
    count = 0
    for i in data:
        user = vk.method("users.get", {"user_ids": i}) # i - user ID
        fullname = user[0]['first_name'] +  ' ' + user[0]['last_name']
        names.append(fullname)
        count += 1
        percent = (count/fullpercent)*100
        percent = round(percent,2)
        if lastpercent != percent:
            lastpercent = percent
            print(str(percent) + "%")
    print('Finished taking names')
    return names

def saveData(data, fileName = "members.txt"): #сохраняем список фамилий-имен в файл
    with open(fileName, "w", encoding = "utf-8") as file:  # Открываем файл на запись
        fullpercent = len(data)
        lastpercent = -1
        count = 0
        for item in data:   
            count += 1
            percent = (count/fullpercent)*100
            percent = round(percent)
            if lastpercent != percent:
                lastpercent = percent
                print(str(percent) + "%")
            file.write(str(item) + "\n")
    print('All names saved')
    
def enterData(fileName = "members.txt"):
    pass


if __name__ == "__main__":
    token = "353c538************************************9a3ae411cff90973" #токен приложения, либо токен частной группы
    session = vk.Session(access_token = token) #задаем сессию
    vkApi = vk.API(session) 
    data = getMembers(0) #получаем айдишники членов группы, в качестве аргумента метода у нас ID группы
                                 #(пример ID: vk.com/club1814355 -> все числа после слова club - это Id группы "1814355"
    data = getMembersNames(data, token) #получаем имена пользователей вк по списку айдишников
    saveData(data, "экстра.txt") #сохраняем список
