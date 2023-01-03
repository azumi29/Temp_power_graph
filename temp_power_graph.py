import pandas as pd
import glob
import numpy as np
import datetime


# 電力　
date_list = []
ave_power_list = []
week_name_list = []

# csv呼び出し、必要な行と列の抽出
for i in glob.glob("*_power_usage*"):
    df = pd.read_csv(i,encoding='ANSI', header=9, usecols=[0,1,2])
    df = df.iloc[0:24]
    
    # date_list作成
    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce") #csvを読み込むときにdatetimeにできなかったのでここで行う
    date_list.append(df.iat[0,0]) # iatで任意の位置を取得
    
    # 1日の平均を計算してave_result_list作成
    df['当日実績(万kW)'] = df['当日実績(万kW)'].astype(int) # '当日実績(万kW)'を文字列から数値へ変換
    ave_power_list.append(df['当日実績(万kW)'].mean()) # 1日の平均
    ave_power_list = list(np.round(ave_power_list,2)) # 小数第二位まで表記

df_ave_power = pd.DataFrame({'DATE':date_list,'AVE_POWER':ave_power_list})

# 気温　CSV呼び出し、必要な行と列の抽出
df_ave_temp = pd.read_csv('Hotaka_temp_202202.csv',encoding='ANSI', header=3, usecols=[0,1], skiprows=[4], parse_dates=['年月日'])
df_ave_temp = df_ave_temp.rename(columns={'年月日': 'DATE','平均気温(℃)':'AVE_TEMP'})

# DataFrameの結合
df_ave_power_temp = pd.merge(df_ave_temp, df_ave_power)
print(df_ave_power_temp)



import matplotlib.pyplot as plt
import japanize_matplotlib
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import matplotlib.dates as mdates

df_ave_power_temp = df_ave_power_temp.set_index('DATE')

fig, ax1 = plt.subplots()
ax2 = ax1.twinx() # 二つのグラフを書く指令

# 折れ線グラフを出力
ax1.plot(df_ave_power_temp["AVE_TEMP"], linestyle="solid",color="b")
ax1.set_ylabel('AVE_TEMP')

# 棒グラフを出力
ax2.bar(df_ave_power_temp.index, height=df_ave_power_temp["AVE_POWER"], align="center", color="lightblue", linewidth=0)
ax2.set_ylabel('AVE_POWER')
ax2.set_ylim(1200,2200) # Y軸の目盛指定

# 時間軸目盛を月曜日のみ表示
locator = mdates.WeekdayLocator(byweekday=(MO))
ax1.xaxis.set_major_locator(locator)
ax1.grid(axis='x')
ax1.set_xlabel('DATE (tick_grid=monday)')

# グラフの見せ方調整
ax1.set_zorder(2) # 線グラフax1を再前面へ
ax2.set_zorder(1)
ax1.patch.set_alpha(0) # 線グラフax1のバックの透過性
plt.title('2022年2月の気温と電力')

# グラフをpngに保存
plt.savefig("temp_power_graph.png")

plt.show()