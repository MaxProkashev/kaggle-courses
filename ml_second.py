# Подготовка
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import pandas as pd
from sklearn.model_selection import train_test_split
data = pd.read_csv('../data.csv')
y = data.Price
melb_predictors = data.drop(['Price'], axis=1)
X = melb_predictors.select_dtypes(exclude=['object'])
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2,random_state=0)

# Функция для сравнения разных подходов к пропущенным данным
def score_dataset(X_train, X_valid, y_train, y_valid):
    model = RandomForestRegressor(n_estimators=10, random_state=0)
    model.fit(X_train, y_train)
    preds = model.predict(X_valid)
    return mean_absolute_error(y_valid, preds)

# 1
# Удалить столбцы с пропущенными значениями
# Получить имена столбцов с пропущенными значениями
cols_with_missing = [col for col in X_train.columns if X_train[col].isnull().any()]

# Удаление столбцов в данных обучения и проверки
reduced_X_train = X_train.drop(cols_with_missing, axis=1)
reduced_X_valid = X_valid.drop(cols_with_missing, axis=1)

print("MAE из подхода 1 (удаление столбцов с пропущенными значениями):")
print(score_dataset(reduced_X_train, reduced_X_valid, y_train, y_valid))    # 183,550

# 2
# Замена на среднее по столбцу
from sklearn.impute import SimpleImputer
# Imputation
my_imputer = SimpleImputer()
imputed_X_train = pd.DataFrame(my_imputer.fit_transform(X_train))
imputed_X_valid = pd.DataFrame(my_imputer.transform(X_valid))
# Imputation удалил имена столбцов; положим их обратно
imputed_X_train.columns = X_train.columns
imputed_X_valid.columns = X_valid.columns

print("MAE из подхода 2 (Imputation):")
print(score_dataset(imputed_X_train, imputed_X_valid, y_train, y_valid))    # 178,166

# 3
# Расширение Imputation
# Impute недостающие значения, и отслеживаем, какие значения были изменены.
# Делаем копию, чтобы избежать изменения исходных данных (при изменении)
X_train_plus = X_train.copy()
X_valid_plus = X_valid.copy()

# создаем новые столбцы, указывающие, что было impute
for col in cols_with_missing:
    X_train_plus[col + '_was_missing'] = X_train_plus[col].isnull()
    X_valid_plus[col + '_was_missing'] = X_valid_plus[col].isnull()

# Imputation
my_imputer = SimpleImputer()
imputed_X_train_plus = pd.DataFrame(my_imputer.fit_transform(X_train_plus))
imputed_X_valid_plus = pd.DataFrame(my_imputer.transform(X_valid_plus))

# Imputation удалило имена столбцов; put them back
imputed_X_train_plus.columns = X_train_plus.columns
imputed_X_valid_plus.columns = X_valid_plus.columns

print("MAE из подхода 3 (Расширение Imputation):")
print(score_dataset(imputed_X_train_plus, imputed_X_valid_plus, y_train, y_valid))  # 178,927


# Количество пропущенных значений в каждом столбце обучающих данных
missing_val_count_by_column = (X_train.isnull().sum())
print(missing_val_count_by_column[missing_val_count_by_column > 0])

# Получить имена столбцов с пропущенными значениями
cols_with_missing = [col for col in X_train.columns if X_train[col].isnull().any()]

# Categorical Variable (не цифры)
# 3 способа
# 1
# просто удалить столбец
drop_X_train = X_train.select_dtypes(exclude=['object'])    # Выбирает столбцы не object
drop_X_valid = X_valid.select_dtypes(exclude=['object'])

print("MAE from Approach 1 (Drop categorical variables):")
print(score_dataset(drop_X_train, drop_X_valid, y_train, y_valid))  # 175,703
# 2
# Label Encoding - присваивает каждому уникальному значению отдельное целое число.
from sklearn.preprocessing import LabelEncoder
label_X_train = X_train.copy()
label_X_valid = X_valid.copy()
label_encoder = LabelEncoder()
s = (X_train.dtypes == 'object')
object_cols = list(s[s].index)
for col in object_cols:
    label_X_train[col] = label_encoder.fit_transform(X_train[col])
    label_X_valid[col] = label_encoder.transform(X_valid[col])

print("MAE from Approach 2 (Label Encoding):")
print(score_dataset(label_X_train, label_X_valid, y_train, y_valid))    # 165,936
# 3
# One-hot encoding - создает новые столбцы, указывающие наличие (или отсутствие) каждого возможного значения в исходных данных.
from sklearn.preprocessing import OneHotEncoder

# Применение быстрого кодировщика к каждому столбцу с категориальными данными
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[object_cols]))
OH_cols_valid = pd.DataFrame(OH_encoder.transform(X_valid[object_cols]))

# One-hot encoding removed index; put it back
OH_cols_train.index = X_train.index
OH_cols_valid.index = X_valid.index

# Remove categorical columns (will replace with one-hot encoding)
num_X_train = X_train.drop(object_cols, axis=1)
num_X_valid = X_valid.drop(object_cols, axis=1)

# Add one-hot encoded columns to numerical features
OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1)
OH_X_valid = pd.concat([num_X_valid, OH_cols_valid], axis=1)

print("MAE from Approach 3 (One-Hot Encoding):")
print(score_dataset(OH_X_train, OH_X_valid, y_train, y_valid))  # 166,089

# Получить список категориальных переменных
s = (X_train.dtypes == 'object')
object_cols = list(s[s].index)

# set(X_train[col]) == set(X_valid[col])
# Все категориальные столбцы
object_cols = [col for col in X_train.columns if X_train[col].dtype == "object"]

# Столбцы, которые можно безопасно маркировать закодированными
good_label_cols = [col for col in object_cols if set(X_train[col]) == set(X_valid[col])]

# Проблемные столбцы, которые будут удалены из набора данных
bad_label_cols = list(set(object_cols)-set(good_label_cols))

print('Categorical columns that will be label encoded:', good_label_cols)
print('\nCategorical columns that will be dropped from the dataset:', bad_label_cols)

# Столбцы, которые будут закодированы в горячем режиме
low_cardinality_cols = [col for col in object_cols if X_train[col].nunique() < 10]

# Столбцы, которые будут удалены из набора данных
high_cardinality_cols = list(set(object_cols)-set(low_cardinality_cols))

print('Categorical columns that will be one-hot encoded:', low_cardinality_cols)
print('\nCategorical columns that will be dropped from the dataset:', high_cardinality_cols)
