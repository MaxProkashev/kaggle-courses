from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import pandas as pd     # Для работы с данными

# Сохранить путь к файлу в переменную для облегчения доступа
file_path = '../data.csv'
# Прочитать данные и сохранить их в DataFrame
data = pd.read_csv(file_path)
# Распечатать сводку данных
data.describe()
# Возвращает имена колонок
data.columns()
# Убирает строчки с пропущенными значениями
data.dropna(axis=0)
# Выбрать Series колонку с названием price
y = data.Price
# Выбрать Features
data_features = ['Rooms', 'Bathroom', 'Landsize', 'Lattitude', 'Longtitude']
X = data[data_features]
X.describe()
# Первые несколько строк
X.head()


# Пример DecisionTreeRegressor и RandomForestRegressor

# Подключение библиотек

# Путь к файлу для чтения
file_path = '../data.csv'

data = pd.read_csv(file_path)
# Создает целевой объект y
y = data.SalePrice
# Создает X
features = ['LotArea', 'YearBuilt', '1stFlrSF',
            '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']
X = data[features]

# Разделяем данные на проверку и обучение
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

# Выбираем модель DecisionTreeRegressor
model = DecisionTreeRegressor(random_state=1)
# Обучаем модель
model.fit(train_X, train_y)

# Сделать прогноз на проверчных данных и вычислить абсолютную среднюю ошибку
# (без вычисления наилучшей длины дерева)
val_predictions = model.predict(val_X)
val_mae = mean_absolute_error(val_predictions, val_y)
print("Проверка MAE без указания max_leaf_nodes: {:,.0f}".format(val_mae))

# Пример как можно вычислить наилучшую длину дерева для DecisionTreeRegressor


def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):
    model = DecisionTreeRegressor(
        max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(train_X, train_y)
    preds_val = model.predict(val_X)
    mae = mean_absolute_error(val_y, preds_val)
    return(mae)


for max_leaf_nodes in [5, 50, 500, 5000]:
    my_mae = get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y)
    print("Max leaf nodes: %d  \t\t Mean Absolute Error:  %d" %
          (max_leaf_nodes, my_mae))

# Использование лучшего значения для max_leaf_nodes
model = DecisionTreeRegressor(max_leaf_nodes=100, random_state=1)
model.fit(train_X, train_y)
val_predictions = model.predict(val_X)
val_mae = mean_absolute_error(val_predictions, val_y)
print(
    "Проверка MAE для лучшего значения max_leaf_nodes: {:,.0f}".format(val_mae))

# Модель RandomForestRegressor
rf_model = RandomForestRegressor(random_state=1)
rf_model.fit(train_X, train_y)
rf_val_predictions = rf_model.predict(val_X)
rf_val_mae = mean_absolute_error(rf_val_predictions, val_y)
print("Validation MAE for Random Forest Model: {:,.0f}".format(rf_val_mae))

# В строках ниже показано, как сохранять прогнозы в формате, используемом для оценки соревнований
rf_model_on_full_data = RandomForestRegressor(random_state=1)
rf_model_on_full_data.fit(X, y)
test_data_path = '../input/test.csv'
test_data = pd.read_csv(test_data_path)
test_X = test_data[features]
test_preds = rf_model_on_full_data.predict(test_X)

output = pd.DataFrame({'Id': test_data.Id,
                       'SalePrice': test_preds})
output.to_csv('submission.csv', index=False)

