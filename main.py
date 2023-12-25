from flask import Flask, jsonify, request
from random import randint, sample
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge



def mlEngine(x1, y1, category):
    path = category+'.csv'
    data = pd.read_csv(path, sep=';')
    data = data.sample(frac=1)
    X = data[['id', 'category']]
    y = data[['id', 'rec']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)
    return model.predict(pd.DataFrame({'id': [x1], 'category': [y1]})).tolist()

user_data1 = {'statues': 5, 'nature': 4, 'churches': 4, 'sites': 3, 'theatres': 2, 'museums': 2, 'galleries': 1,
         'shopping': 1, 'national_cuisine': 1, 'fastfood': 1, 'cafe': 1, 'bars': 1}

points1 = ['museums', 'statues', 'statues', 'statues', 'statues']

id_bias = {'statues': 0, 'nature': 10, 'churches': 20, 'sites': 30, 'theatres': 40, 'museums': 50, 'galleries': 60,
         'shopping': 70, 'national_cuisine': 80, 'fastfood': 90, 'cafe': 100, 'bars': 110}

def getIds(user_data, points):
    category_count = {}
    resList = []
    for i in set(points):
        count = 0
        for j in points:
            if j == i:
                count += 1
        category_count[i] = count
    for i in range(len(category_count)):

        elem = (category_count.popitem())
        userCategory = elem[0]
        pointsNumber = elem[1]
        userRating = user_data.get(userCategory)
        resDict = {}
        for i in range(1, 10):
            a = mlEngine(i, userRating, userCategory)
            resDict[round(a[0][0]) + id_bias.get(userCategory)] = (a[0][1])
        topPoints = list((sorted(resDict.items(), key=lambda x: x[1]))[::-1][:pointsNumber])
        for j in topPoints:
            resList.append(j[0])
    return resList




def responseMl(inputData):
    typeData = inputData.get('type')
    typeCategories = inputData.get('categories')
    points = randint(3, 6)
    topCategories = list(sorted(typeCategories.items(), key=lambda x: x[1]))[::-1]
    arr = sample([i[0] for i in topCategories], points, counts=[i[1] for i in topCategories])
    return getIds(typeCategories, arr)



app = Flask(__name__)
points = [
  {
    "name": "Музей археологии Москвы",
    "coords": "55.75632,37.617132",
    "description": "мать жива?",
    "category": "Музеи",
    "address": " Манежная площадь, 1А, Москва"
  },
  {
    "name": "Музей Отечественной войны 1812 года",
    "coords": "55.756305,37.61865",
    "description": "мать жива?",
    "category": "Музеи",
    "address": "площадь Революции, 2/3, Москва"
  },
  {
    "name": "Музей Оружейный подвал",
    "coords": "55.756842,37.62175",
    "description": "мать жива?",
    "category": "Музеи",
    "address": "Никольская ул., 11-13с1, Москва"
  },
  {
    "name": "Музей уникальных кукол",
    "coords": "55.759334,37.644486",
    "description": "мать жива?",
    "category": "Музеи",
    "address": "ул. Покровка, 13, стр. 2, Москва"
  },
  {
    "name": "Мемориальный музей-квартира художника А.М. Васнецова",
    "coords": "55.763741,37.648546",
    "description": "мать жива?",
    "category": "Музеи",
    "address": "Фурманный переулок, 6, Москва"
  },
  {
    "name": "Иннопарк",
    "coords": "55.760135,37.624957",
    "description": "мать жива?",
    "category": "Музеи",
    "address": "Театральный пр., 5, стр. 1, Москва"
  },
  {
    "name": "Музей МАРХИ",
    "coords": "55.763022,37.622558",
    "description": "мать жива?",
    "category": "Музеи",
    "address": "ул. Рождественка, 11, стр. 2, Москва"
  },
  {
    "name": "Музей уникальных кукол",
    "coords": "55.759334,37.644486",
    "description": "мать жива?",
    "category": "Музеи",
    "address": "ул. Покровка, 13, стр. 2, Москва"
  },
  {
    "name": "Музей скорой помощи",
    "coords": "55.773697,37.637407",
    "description": "мать жива?",
    "category": "Музеи",
    "address": "1-й Коптельский пер., 3, стр. 1, Москва"
  },
  {
    "name": "Музей нонконформизма",
    "coords": "55.76331,37.635925",
    "description": "мать жива?",
    "category": "Музеи",
    "address": "Мясницкая ул., вл24/7с2, Москва"
  },
  {
    "name": "Стела в память Сухаревой башни",
    "coords": "55.772299,37.634317",
    "description": "мать жива?",
    "category": "Памятники",
    "address": "Большая Сухаревская площадь, Москва"
  },
  {
    "name": "Памятник В. Г. Шухову",
    "coords": "55.766157,37.634739",
    "description": "мать жива?",
    "category": "Памятники",
    "address": "Москва, Сретенский бульвар, Москва"
  },
  {
    "name": "Атом Солнца о. Табакова",
    "coords": "55.773575,37.62952",
    "description": "мать жива?",
    "category": "Памятники",
    "address": "Малая Сухаревская площадь, 3, Москва"
  },
  {
    "name": "Памятник А. С. Грибоедову",
    "coords": "55.762637,37.642025",
    "description": "мать жива?",
    "category": "Памятники",
    "address": "Чистопрудный бульвар, Москва"
  },
  {
    "name": "Памятник С.Я. Маршаку",
    "coords": "55.759947,37.652804",
    "description": "мать жива?",
    "category": "Памятники",
    "address": "Малый Казённый пер., 2, Москва"
  },
  {
    "name": "Девушка кормит голубей",
    "coords": "55.763812,37.63517",
    "description": "мать жива?",
    "category": "Памятники",
    "address": "Мясницкая ул., 17, стр. 3, Москва"
  },
  {
    "name": "Памятник В. В. Воровскому",
    "coords": "55.762004,37.626448",
    "description": "мать жива?",
    "category": "Памятники",
    "address": "ул. Кузнецкий Мост, 21/5, Москва"
  },
  {
    "name": "Памятник Н.К. Крупской",
    "coords": "55.766610,37.632024",
    "description": "мать жива?",
    "category": "Памятники",
    "address": "Москва, Сретенский бульвар"
  },
  {
    "name": "Памятник советской семье",
    "coords": "55.769013,37.629313",
    "description": "мать жива?",
    "category": "Памятники",
    "address": "Пушкарёв пер., 15, Москва"
  },
  {
    "name": "Памятник А. П. Чехову",
    "coords": "55.759395,37.612964",
    "description": "мать жива?",
    "category": "Памятники",
    "address": "Камергерский пер., 2, Москва"
  },
  {
    "name": "Зарядье",
    "coords": "55.75167,37.629053",
    "description": "мать жива?",
    "category": "Сады, парки, скверы",
    "address": "ул. Варварка, 6, стр. 1, Москва"
  },
  {
    "name": "Парк Горка",
    "coords": "55.756437,37.635197",
    "description": "мать жива?",
    "category": "Сады, парки, скверы",
    "address": "Большой Спасоглинищевский пер., 3, стр. 5, Москва"
  },
  {
    "name": "Чистые пруды",
    "coords": "55.762637,37.642025",
    "description": "мать жива?",
    "category": "Сады, парки, скверы",
    "address": "Чистопрудный бульвар, Москва"
  },
  {
    "name": "Сквер Полководцев",
    "coords": "55.761269,37.640911",
    "description": "мать жива?",
    "category": "Сады, парки, скверы",
    "address": "Потаповский переулок, Москва"
  },
  {
    "name": "Музейный парк",
    "coords": "55.758954,37.627822",
    "description": "мать жива?",
    "category": "Сады, парки, скверы",
    "address": "Музейный парк, Москва"
  },
  {
    "name": "Анин сад",
    "coords": "55.762242,37.640165",
    "description": "мать жива?",
    "category": "Сады, парки, скверы",
    "address": "Потаповский пер., 3, стр. 1, Москва"
  },
  {
    "name": "Лермонтовский сквер",
    "coords": "55.769504,37.651565",
    "description": "мать жива?",
    "category": "Сады, парки, скверы",
    "address": "Лермонтовская площадь, Москва"
  },
  {
    "name": "Сквер Мандельштама",
    "coords": "55.755115,37.638566",
    "description": "мать жива?",
    "category": "Сады, парки, скверы",
    "address": "ул. Забелина, 3, стр. 7"
  },
  {
    "name": "Сад культуры и отдыха имени Н.Э. Баумана",
    "coords": "55.767261,37.659578",
    "description": "мать жива?",
    "category": "Сады, парки, скверы",
    "address": "сад культуры и отдыха имени Н.Э. Баумана, Москва"
  },
  {
    "name": "Цветной бульвар",
    "coords": "55.770471,37.622199",
    "description": "мать жива?",
    "category": "Сады, парки, скверы",
    "address": "Цветной бульвар, Москва"
  },
  {
    "name": "Галерея современного искусства Чиж",
    "coords": "55.760905,37.622881",
    "description": "мать жива?",
    "category": "Галереи",
    "address": "Пушечная улица, 7/5с2, Москва"
  },
  {
    "name": "Галерея на Чистых прудах",
    "coords": "55.763726,37.642366",
    "description": "мать жива?",
    "category": "Галереи",
    "address": "Гусятников переулок, 10, Москва"
  },
  {
    "name": "Sistema Gallery",
    "coords": "55.764931,37.634012",
    "description": "мать жива?",
    "category": "Галереи",
    "address": "Бобров переулок, 4с4, Москва"
  },
  {
    "name": "Dc Gallery",
    "coords": "55.766592,37.649013",
    "description": "мать жива?",
    "category": "Галереи",
    "address": "Хоромный тупик, 6, Москва"
  },
  {
    "name": "Любовь24",
    "coords": "55.762363,37.645393",
    "description": "мать жива?",
    "category": "Галереи",
    "address": "Чистопрудный бул., 15, стр. 2, Москва"
  },
  {
    "name": "ВХУТЕМАС",
    "coords": "55.763614,37.622351",
    "description": "мать жива?",
    "category": "Галереи",
    "address": "ул. Рождественка, 11/4к1с4, Москва"
  },
  {
    "name": "Vladey",
    "coords": "55.764273,37.620393",
    "description": "мать жива?",
    "category": "Галереи",
    "address": "Неглинная ул., 14, стр. 1А, Москва"
  },
  {
    "name": "Галерея",
    "coords": "55.768122,37.629089",
    "description": "мать жива?",
    "category": "Галереи",
    "address": "Колокольников пер., 17, Москва"
  },
  {
    "name": "Sareh Арт галерея",
    "coords": "55.767939,37.634047",
    "description": "мать жива?",
    "category": "Галереи",
    "address": "Луков пер., 8, Москва"
  },
  {
    "name": "Zimova Art Buro",
    "coords": "55.768076,37.61441",
    "description": "мать жива?",
    "category": "Галереи",
    "address": "ул. Петровка, 30/7, Москва"
  },
  {
    "name": "Новый театр",
    "coords": "55.760616,37.631029",
    "description": "мать жива?",
    "category": "Театры",
    "address": "Мясницкая улица, 7с2, Москва"
  },
  {
    "name": "Et Cetera",
    "coords": "55.765053,37.635664",
    "description": "мать жива?",
    "category": "Театры",
    "address": "Фролов пер., 2, Москва"
  },
  {
    "name": "Театр Crave",
    "coords": "55.756538,37.632592",
    "description": "мать жива?",
    "category": "Театры",
    "address": "Лубянский пр., 15, стр. 2, Москва"
  },
  {
    "name": "Московский академический театр имени В. Маяковского",
    "coords": "55.769064,37.630715",
    "description": "мать жива?",
    "category": "Театры",
    "address": "Пушкарёв пер., 21/24, Москва"
  },
  {
    "name": "Российский академический молодёжный театр",
    "coords": "55.758975,37.617294",
    "description": "мать жива?",
    "category": "Театры",
    "address": "Театральная площадь, 2, Москва"
  },
  {
    "name": "Московский государственный академический театр оперетты",
    "coords": "55.760201,37.616243",
    "description": "мать жива?",
    "category": "Театры",
    "address": "ул. Большая Дмитровка, 6, Москва"
  },
  {
    "name": "Московский театр школа современной пьесы",
    "coords": "55.76604,37.620267",
    "description": "мать жива?",
    "category": "Театры",
    "address": "Неглинная ул., 29, Москва"
  },
  {
    "name": "ГБУК Московский театр Современник",
    "coords": "55.761781,37.645941",
    "description": "мать жива?",
    "category": "Театры",
    "address": "Чистопрудный бульвар, 19с1, Москва"
  },
  {
    "name": "Государственный академический Большой театр России",
    "coords": "55.760221,37.618561",
    "description": "мать жива?",
    "category": "Театры",
    "address": "Театральная площадь, 1, Москва"
  },
  {
    "name": "Московский театр Олега Табакова",
    "coords": "55.773292,37.630903",
    "description": "мать жива?",
    "category": "Театры",
    "address": "Малая Сухаревская площадь, 5, Москва"
  },
  {
    "name": "Аполлинария",
    "coords": "55.76566,37.644585",
    "description": "мать жива?",
    "category": "Театры",
    "address": "Малый Харитоньевский переулок, 10с2, Москва"
  },
  {
    "name": "Дом Лансере",
    "coords": "55.765372,37.63288",
    "description": "мать жива?",
    "category": "Достопримечательности",
    "address": "Бобров переулок, 2, Москва"
  },
  {
    "name": "Жилой дом Фроловых - Бари",
    "coords": "55.762409,37.638557",
    "description": "мать жива?",
    "category": "Достопримечательности",
    "address": "Кривоколенный пер., 11/13с1, Москва"
  },
  {
    "name": "Руины стены дома",
    "coords": "55.758519,37.635557",
    "description": "мать жива?",
    "category": "Достопримечательности",
    "address": "ул. Маросейка, 13А, стр. 1, Москва"
  },
  {
    "name": "Доходный дом В.И. Фирсановой",
    "coords": "55.764273,37.620393",
    "description": "мать жива?",
    "category": "Достопримечательности",
    "address": "Неглинная ул., 14/1А, Москва"
  },
  {
    "name": "Главный дом городской усадьбы И.И. Воронцова",
    "coords": "55.763022,37.622558",
    "description": "мать жива?",
    "category": "Достопримечательности",
    "address": "улица Рождественка, 11с2, Москва"
  },
  {
    "name": "Юго-восточная башня Богородице-Рождественского монастыря",
    "coords": "55.764987,37.62581",
    "description": "мать жива?",
    "category": "Достопримечательности",
    "address": "Большой Кисельный пер., 5, стр. 3, Москва"
  },
  {
    "name": "Дом Центросоюза",
    "coords": "55.767494,37.641144",
    "description": "мать жива?",
    "category": "Достопримечательности",
    "address": "Мясницкая ул., 39, стр. 1, Москва"
  },
  {
    "name": "Городская усадьба Высоцких",
    "coords": "55.76522,37.642375",
    "description": "мать жива?",
    "category": "Достопримечательности",
    "address": "пер. Огородная Слобода, 6, Москва"
  },
  {
    "name": "Особняк Павлова-Севрюговых",
    "coords": "55.767767,37.646175",
    "description": "мать жива?",
    "category": "Достопримечательности",
    "address": "Большой Козловский пер., 4, стр. 1, Москва"
  },
  {
    "name": "Дом с беременными кариатидами",
    "coords": "55.769302,37.630113",
    "description": "мать жива?",
    "category": "Достопримечательности",
    "address": "Большой Головин пер., 22, Москва"
  },
  {
    "name": "Метехи",
    "coords": "55.772421,37.649723",
    "description": "мать жива?",
    "category": "Рестораны национальной кухни",
    "address": "Орликов пер., 5, стр. 2, Москва"
  },
  {
    "name": "Каприз",
    "coords": "55.771393,37.64701",
    "description": "мать жива?",
    "category": "Бары",
    "address": "Орликов пер., 3Б, Москва"
  },
  {
    "name": "Мята Lounge",
    "coords": "55.768795,37.6433",
    "description": "мать жива?",
    "category": "Бары",
    "address": "просп. Академика Сахарова, 12, стр. 3, Москва"
  },
  {
    "name": "Коллеги",
    "coords": "55.769869,37.632763",
    "description": "мать жива?",
    "category": "Бары",
    "address": "Селивёрстов пер., 2/24, Москва"
  },
  {
    "name": "Hola Bar Tacos & Tapas",
    "coords": "55.766992,37.632251",
    "description": "мать жива?",
    "category": "Бары",
    "address": "Сретенский бул., 1, корп. 4, Москва"
  },
  {
    "name": "Dream",
    "coords": "55.763467,37.635305",
    "description": "мать жива?",
    "category": "Бары",
    "address": "Мясницкая ул., 17, стр. 1, Москва"
  },
  {
    "name": "Широкую на широкую",
    "coords": "55.761659,37.636042",
    "description": "мать жива?",
    "category": "Бары",
    "address": "Кривоколенный пер., 10, стр. 5, Москва"
  },
  {
    "name": "Зинзивер",
    "coords": "55.758894,37.645393",
    "description": "мать жива?",
    "category": "Бары",
    "address": "Покровский бул., 2/14, Москва"
  },
  {
    "name": "Бар 1929",
    "coords": "55.753038,37.635009",
    "description": "мать жива?",
    "category": "Бары",
    "address": "Славянская площадь, 2, Москва"
  },
  {
    "name": "Барвиха Lounge",
    "coords": "55.75511,37.622396",
    "description": "мать жива?",
    "category": "Бары",
    "address": "Ветошный пер., 13, Москва"
  },
  {
    "name": "Гадкий Койот",
    "coords": "55.762227,37.612847",
    "description": "мать жива?",
    "category": "Бары",
    "address": "Столешников пер., 8, Москва"
  },
  {
    "name": "Узбекистан",
    "coords": "55.76604,37.620267",
    "description": "мать жива?",
    "category": "Рестораны национальной кухни",
    "address": "Неглинная ул., 29, стр. 5, Москва"
  },
  {
    "name": "Frank by Баста",
    "coords": "55.761153,37.623304",
    "description": "мать жива?",
    "category": "Рестораны национальной кухни",
    "address": "ул. Рождественка, 5/7с2, Москва"
  },
  {
    "name": "Стейк Хаус Бутчер",
    "coords": "55.756538,37.632592",
    "description": "мать жива?",
    "category": "Рестораны национальной кухни",
    "address": "Лубянский пр., 15, стр. 2, Москва"
  },
  {
    "name": "Золотая Вобла",
    "coords": "55.757997,37.639051",
    "description": "мать жива?",
    "category": "Рестораны национальной кухни",
    "address": "ул. Покровка, 2/1с1, Москва"
  },
  {
    "name": "J'pan",
    "coords": "55.762145,37.63447",
    "description": "мать жива?",
    "category": "Рестораны национальной кухни",
    "address": "Мясницкая ул., 22, стр. 1, Москва"
  },
  {
    "name": "Valenok",
    "coords": "55.768846,37.620492",
    "description": "мать жива?",
    "category": "Рестораны национальной кухни",
    "address": "Москва, Цветной бульвар, 5"
  },
  {
    "name": "Эндис энд френдс",
    "coords": "55.763624,37.642393",
    "description": "мать жива?",
    "category": "Рестораны национальной кухни",
    "address": "Москва, Чистопрудный бульвар, 5"
  },
  {
    "name": "Паста",
    "coords": "55.754005,37.636823",
    "description": "мать жива?",
    "category": "Рестораны национальной кухни",
    "address": "ул. Солянка, 2/6, Москва"
  },
  {
    "name": "Kaif Provenance",
    "coords": "55.761958,37.613692",
    "description": "мать жива?",
    "category": "Рестораны национальной кухни",
    "address": "ул. Большая Дмитровка, 11, Москва"
  },
  {
    "name": "Салют",
    "coords": "55.766932,37.612461",
    "description": "мать жива?",
    "category": "Кафе",
    "address": "Москва, Страстной бульвар, 12с5"
  },
  {
    "name": "from Berlin.",
    "coords": "55.773231,37.619459",
    "description": "мать жива?",
    "category": "Кафе",
    "address": "Садовая-Самотёчная ул., 20, стр. 1, Москва"
  },
  {
    "name": "Ланч поинт",
    "coords": "55.769383,37.638521",
    "description": "мать жива?",
    "category": "Кафе",
    "address": "Москва, Даев переулок, 20"
  },
  {
    "name": "Ycp",
    "coords": "55.763204,37.633616",
    "description": "мать жива?",
    "category": "Кафе",
    "address": "Москва, Мясницкая улица, 13с21"
  },
  {
    "name": "Smart Coffee Lab",
    "coords": "55.757805,37.635772",
    "description": "мать жива?",
    "category": "Кафе",
    "address": "ул. Маросейка, 11/4с1, Москва"
  },
  {
    "name": "Просвет",
    "coords": "55.753625,37.625882",
    "description": "мать жива?",
    "category": "Кафе",
    "address": "ул. Ильинка, 4, Москва"
  },
  {
    "name": "Cups&Hugs",
    "coords": "55.770801,37.648699",
    "description": "мать жива?",
    "category": "Кафе",
    "address": "Москва, Орликов переулок, 6"
  },
  {
    "name": "Надин",
    "coords": "55.758975,37.617294",
    "description": "мать жива?",
    "category": "Кафе",
    "address": "Театральная площадь, 2, Москва"
  },
  {
    "name": "Sweet Cup",
    "coords": "55.772026,37.631451",
    "description": "мать жива?",
    "category": "Кафе",
    "address": "ул. Сретенка, 27, стр. 2, Москва"
  },
  {
    "name": "Surf Coffee",
    "coords": "55.764273,37.620393",
    "description": "мать жива?",
    "category": "Кафе",
    "address": "Неглинная ул., 14, стр. 1А, Москва"
  },
  {
    "name": "ГУМ",
    "coords": "55.75474,37.621408",
    "description": "мать жива?",
    "category": "Шопинг",
    "address": "Москва, Красная площадь, 3"
  },
  {
    "name": "ЦУМ",
    "coords": "55.760798,37.619773",
    "description": "мать жива?",
    "category": "Шопинг",
    "address": "ул. Петровка, 2, Москва"
  },
  {
    "name": "ЦДМ ",
    "coords": "55.760135,37.624957",
    "description": "мать жива?",
    "category": "Шопинг",
    "address": "Театральный пр., 5, стр. 1, Центральный административный округ, Тверской район, Москва"
  },
  {
    "name": "Пассаж Кузнецкий Мост",
    "coords": "55.762308,37.625837",
    "description": "мать жива?",
    "category": "Шопинг",
    "address": "ул. Кузнецкий Мост, 19, стр. 1, Москва"
  },
  {
    "name": "Петровский пассаж",
    "coords": "55.762394,37.618291",
    "description": "мать жива?",
    "category": "Шопинг",
    "address": "ул. Петровка, 10, Москва"
  },
  {
    "name": "Наутилус",
    "coords": "55.759122,37.624777",
    "description": "мать жива?",
    "category": "Шопинг",
    "address": "Москва, Никольская улица, 25"
  },
  {
    "name": "Неглинная",
    "coords": "55.766491,37.622333",
    "description": "мать жива?",
    "category": "Шопинг",
    "address": "Трубная площадь, 2"
  },
  {
    "name": "ТЦ Казанский",
    "coords": "55.773611,37.65567",
    "description": "мать жива?",
    "category": "Шопинг",
    "address": "Комсомольская площадь, 2"
  },
  {
    "name": "Атриум",
    "coords": "55.757339,37.659173",
    "description": "мать жива?",
    "category": "Шопинг",
    "address": "ул. Земляной Вал, 33"
  },
  {
    "name": "Галерея Тверская 9",
    "coords": "55.759861,37.610557",
    "description": "мать жива?",
    "category": "Шопинг",
    "address": "Тверская ул., 9"
  },
  {
    "name": "Вкусно — и точка",
    "coords": "55.764703,37.603092",
    "description": "мать жива?",
    "category": "Фастфуд",
    "address": "Большая Бронная ул., 29"
  },
  {
    "name": "БлинБери",
    "coords": "55.763741,37.606281",
    "description": "мать жива?",
    "category": "Фастфуд",
    "address": "Москва, Тверская улица, 17"
  },
  {
    "name": "Burger Heroes",
    "coords": "55.759952,37.614114",
    "description": "мать жива?",
    "category": "Фастфуд",
    "address": "ул. Большая Дмитровка, 5/6с3"
  },
  {
    "name": "Chuburu",
    "coords": "55.762986,37.63562",
    "description": "мать жива?",
    "category": "Фастфуд",
    "address": "Мясницкая ул., 24/7с8"
  },
  {
    "name": "Шаверма по-московски",
    "coords": "55.759086,37.645106",
    "description": "мать жива?",
    "category": "Фастфуд",
    "address": "ул. Покровка, 14/2с1"
  },
  {
    "name": "Subway",
    "coords": "55.768441,37.647145",
    "description": "мать жива?",
    "category": "Фастфуд",
    "address": "Мясницкий пр., 4, стр. 1"
  },
  {
    "name": "Soul Burger",
    "coords": "55.770851,37.632044",
    "description": "мать жива?",
    "category": "Фастфуд",
    "address": "Большой Сухаревский пер., 25, стр. 1"
  },
  {
    "name": "From",
    "coords": "55.766749,37.624211",
    "description": "мать жива?",
    "category": "Фастфуд",
    "address": "Рождественский бул., 1"
  },
  {
    "name": "МосДонер",
    "coords": "55.758402,37.638844",
    "description": "мать жива?",
    "category": "Фастфуд",
    "address": "ул. Покровка, 1/13с1"
  },
  {
    "name": "МитПоинт",
    "coords": "55.75899,37.605697",
    "description": "мать жива?",
    "category": "Фастфуд",
    "address": "Вознесенский пер., 14"
  },
  {
    "name": "Церковь Успения Пресвятой Богородицы",
    "coords": "55.766997,37.631083",
    "description": "мать жива?",
    "category": "Церкви",
    "address": "ул. Сретенка, 3, стр. 4"
  },
  {
    "name": "Церковь Архангела Гавриила - Меншикова башня",
    "coords": "55.763194,37.63897",
    "description": "мать жива?",
    "category": "Церкви",
    "address": "Архангельский пер., 15А, стр. 9"
  },
  {
    "name": "Евангелическо-лютеранский кафедральный собор святых Петра и Павла",
    "coords": "55.75671,37.640785",
    "description": "мать жива?",
    "category": "Церкви",
    "address": "Старосадский пер., 7/10с10, Москва"
  },
  {
    "name": "Церковь Георгия Победоносца на Псковской Горке",
    "coords": "55.752612,37.630661",
    "description": "мать жива?",
    "category": "Церкви",
    "address": "ул. Варварка, 12"
  },
  {
    "name": "Церковь Рождества Богородицы на Сенях",
    "coords": "55.749547,37.61344",
    "description": "мать жива?",
    "category": "Церкви",
    "address": "Кремлёвская наб., 1, стр. 3"
  },
  {
    "name": "Храм-часовня святых благоверных мучеников князей Бориса и Глеба",
    "coords": "55.751528,37.601924",
    "description": "мать жива?",
    "category": "Церкви",
    "address": "Арбатская площадь, 4"
  },
  {
    "name": "Церковь Иоанна Богослова на Бронной",
    "coords": "55.762181,37.600864",
    "description": "мать жива?",
    "category": "Церкви",
    "address": "Богословский пер., 4"
  },
  {
    "name": "Церковь Владимира Равноапостольного при Епархиальном доме",
    "coords": "55.772067,37.612901",
    "description": "мать жива?",
    "category": "Церкви",
    "address": "Лихов пер., 6, стр. 1"
  },
  {
    "name": "Церковь святого Людовика",
    "coords": "55.762647,37.631344",
    "description": "мать жива?",
    "category": "Церкви",
    "address": "ул. Малая Лубянка, 12/7с8"
  },
  {
    "name": "Церковь Космы и Дамиана",
    "coords": "55.75787,37.638494",
    "description": "мать жива?",
    "category": "Церкви",
    "address": "ул. Маросейка, 14/2с3"
  }
]


@app.route('/points', methods=['GET'])
def hello_world():
    args = request.args
    print(args)
    query = {}
    if 'type' in args:
        query['type'] = args['type']
    else:
        query['type'] = 'long'
    query['categories'] = {i: int(args[i]) for i in filter(lambda x: x != 'type', args.keys())}
    print(query)
    res = responseMl(query)
    res = [points[i - 1] for i in res]
    response = jsonify(res)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run()