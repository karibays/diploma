from sklearn.preprocessing import StandardScaler
import pandas as pd

def scaler_data():

    df = pd.read_excel('dataset/cleaned_data/cleaned_building_v2.xlsx')

    df = df.drop(df.sort_values(by='price', ascending=True).head(200).index.values.tolist())
    df = df.drop(df.sort_values(by='price', ascending=False).head(1000).index.values.tolist())

    df = df.drop(df.sort_values(by='Потолки', ascending=False).head(10).index.values.tolist())

    df = df.drop(df.sort_values(by='Общая площадь, м²', ascending=True).head(160).index.values.tolist())
    df = df.drop(df.sort_values(by='Общая площадь, м²', ascending=False).head(40).index.values.tolist())

    df = df.drop(df[df['статус']== 0].index.values.tolist())
    df = df.drop(df[df['статус']== -1].index.values.tolist())

    df = df.drop(['решетки на окнах', 'Год постройки (сдачи в эксплуатацию)','region', 'nan', 'В залоге', 'Кол-во телефонных линий', 'через TV кабель', 'ADSL', 'проводной', 'регион', 'статус'], axis=1)
    df = df.astype(float)

    df['price'] = np.log1p(df['price'])
    df = df.reset_index(drop=True)

    X = df.drop(['price'], axis=1)
    y = df['price']

    Scaler = StandardScaler()

    # X.loc[-1] = data

    X = Scaler.fit_transform(X)

    means = Scaler.mean_ 
    vars = Scaler.var_   
    print(means, vars)


scaler_data()