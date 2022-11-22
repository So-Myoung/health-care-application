import investpy

import matplotlib.pyplot as plt
import mpld3
import pandas as pd
from django.http import HttpResponse
from sklearn.preprocessing import MinMaxScaler
from keras.layers import LSTM
from keras.models import Sequential
from keras.layers import Dense
import keras.backend as K
from keras.callbacks import EarlyStopping
from django.shortcuts import render
from time import strptime
from django.contrib.auth.decorators import login_required
@login_required
def maker(request): #
    return render(request,'maker.html')
def index(request): #
    return render(request,'bmi2.html')

def predict(request):
    try:
        x1 = request.GET['x1']
    except:
        x1 = '0'
    x1 = str(x1)
    try:
        x2 = request.GET['x2']
    except:
        x2 = '0'
    x2 = str(x2)
    try:
        x3 = request.GET['x3']
    except:
        x3 = '0'
    x3 = str(x3)
    try:
        x4 = request.GET['x4']
    except:
        x4 = '0'
    x4 = str(x4)

    try:
        x5 = request.GET['x5']
    except:
        x5 = '0'
    x5 = int(x5)
    # country = 'united states'
    # from_date ='12/09/2015'
    # to_data = '08/10/2022'
    stockPrice = investpy.get_stock_historical_data(x1, country=x2
                                                    , from_date=x3, to_date=x4)
    plt.figure(figsize=(18, 9))
    df = stockPrice.copy()
    plt.plot(df.index, (df['Low'] + df['High']) / 2.0)
    plt.xticks(df.iloc[::50, :].index, rotation=45)
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Mid Price', fontsize=18)

    stockPriceClose = stockPrice[['Close']]
    split_date = pd.Timestamp('01-01-2019')
    # 학습용 데이터와 테스트용 데이터로 분리
    train_data = pd.DataFrame(stockPriceClose.loc[:split_date, ['Close']])
    test_data = pd.DataFrame(stockPriceClose.loc[split_date:, ['Close']])
    # 분리된 데이터 시각화
    ax = train_data.plot()
    test_data.plot(ax=ax)
    plt.legend(['train', 'test'])
    scaler = MinMaxScaler()
    train_data_sc = scaler.fit_transform(train_data)
    test_data_sc = scaler.transform(test_data)
    # 학습 데이터와 테스트 데이터( ndarray)를 데이터프레임으로 변형한다.
    train_sc_df = pd.DataFrame(train_data_sc, columns=['Scaled'], index=train_data.index)
    test_sc_df = pd.DataFrame(test_data_sc, columns=['Scaled'], index=test_data.index)
    # LSTM은 과거의 데이터를 기반으로 미래을 예측하는 모델이다. 따라서, 과거 데이터를 몇 개 사용해서 예측할 지 정해야 한다. 여기서는 30개(한 달)를 사용한다.
    for i in range(1, (x5+1)):
        train_sc_df['Scaled_{}'.format(i)] = train_sc_df['Scaled'].shift(i)
        test_sc_df['Scaled_{}'.format(i)] = test_sc_df['Scaled'].shift(i)

    # nan 값이 있는 로우를 삭제하고 X값과 Y값을 생성한다.
    x_train = train_sc_df.dropna().drop('Scaled', axis=1)
    y_train = train_sc_df.dropna()[['Scaled']]

    x_test = test_sc_df.dropna().drop('Scaled', axis=1)
    y_test = test_sc_df.dropna()[['Scaled']]

    # 대부분의 기계학습 모델은 데이터프레임 대신 ndarray구조를 입력 값으로 사용한다.
    # ndarray로 변환한다.
    x_train = x_train.values
    x_test = x_test.values

    y_train = y_train.values
    y_test = y_test.values

    # LSTM 모델에 맞게 데이터 셋 변형
    x_train_t = x_train.reshape(x_train.shape[0], x5, 1)
    x_test_t = x_test.reshape(x_test.shape[0], x5, 1)

    K.clear_session()
    # Sequeatial Model
    model = Sequential()
    # 첫번째 LSTM 레이어
    model.add(LSTM(x5, return_sequences=True, input_shape=(x5, 1)))
    # 두번째 LSTM 레이어
    model.add(LSTM(42, return_sequences=False))
    # 예측값 1개
    model.add(Dense(1, activation='linear'))
    # 손실함수 지정 - 예측 값과 실제 값의 차이를 계산한다. MSE가 사용된다.
    # 최적화기 지정 - 일반적으로 adam을 사용한다.
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.summary()

    # 손실 값(loss)를 모니터링해서 성능이 더이상 좋아지지 않으면 epoch를 중단한다.
    # vervose=1은 화면에 출력
    early_stop = EarlyStopping(monitor='loss', patience=5, verbose=1)

    # epochs는 훈련 반복 횟수를 지정하고 batch_size는 한 번 훈련할 때 입력되는 데이터 크기를 지정한다.
    model.fit(x_train_t, y_train, epochs=50,
              batch_size=20, verbose=1, callbacks=[early_stop])

    y_pred = model.predict(x_test_t)

    t_df = test_sc_df.dropna()
    y_test_df = pd.DataFrame(y_test, columns=['close'], index=t_df.index)
    y_pred_df = pd.DataFrame(y_pred, columns=['close'], index=t_df.index)

    ax1 = y_test_df.plot()
    y_pred_df.plot(ax=ax1)
    plt.legend(['테스트', '예측'])
    mpld3.show()
    return render(request, 'predict.html')
