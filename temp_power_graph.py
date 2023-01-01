import pandas as pd
import glob
import numpy as np
import datetime


# 電力　
date_list = []
ave_power_list = []

# csv呼び出し、必要な行と列の抽出
for i in glob.glob("*_power_usage*"):
    df = pd.read_csv(i,encoding='ANSI', header=9, usecols=[0,1,2])
    df = df.iloc[0:24]
    
    # date_list作成
    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce") #csvを読み込むときにdatetimeにできなかったのでここで行う
    date_list.append(df.iat[0,0])
    
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

# # df_ave_power_temp = px.data.stocks()
df_ave_power_temp = df_ave_power_temp.set_index('DATE')

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(df_ave_power_temp["AVE_TEMP"])
# ax2.bar(df_ave_power_temp["DATE"], height=df_ave_power_temp["AVE_POWER"])
ax2.bar(df_ave_power_temp.index, height=df_ave_power_temp["AVE_POWER"])
plt.show()


# # # ax1.bar(df_ave_power_temp.index,df_ave_power_temp["AVE_POWER"],color="lightblue",label="A")
# ax1.bar(df_ave_power_temp.index, df_ave_power_temp["AVE_POWER"],color="lightblue",label="A")
# ax2.plot(df_ave_power_temp.index, df_ave_power_temp["AVE_TEMP"],linestyle="solid",color="k",marker="^",label="B")

# ax1.set_ylim(0,10)
# ax2.set_ylim(100,110)
# handler1, label1 = ax1.get_legend_handles_labels()
# handler2, label2 = ax2.get_legend_handles_labels()
# ax1.legend(handler1+handler2,label1+label2,borderaxespad=0)
# ax1.grid(True)
# plt.show()

# # 2軸グラフの本体設定
# # ax1.plot(df_ave_power_temp.to_pydatetime(), df["AVE_TEMP"], color=cm.Set1.colors[1], label="AVE_TEMP(℃)")
# ax1.plot(df_ave_power_temp["AVE_TEMP"], color=cm.Set1.colors[1], label="AVE_TEMP(℃)")
# # ax2.bar(df_ave_power_temp.to_pydatetime(), df["AVE_POWER"], color=cm.Set1.colors[0], alpha=0.4, width=25, label="AVE_POWER((万kW))")
# ax2.bar(df_ave_power_temp["AVE_POWER"], heightcolor=cm.Set1.colors[0], alpha=0.4, width=25, label="AVE_POWER((万kW))")
# plt.tick_params(labelsize = 10) #目盛線ラベルのフォントサイズ

# #グラフタイトルを付ける
# plt.title("2020年各月の平均気温と降水量の推移", fontsize=15)
# # 凡例の表示のため、handler1と2にはグラフオブジェクトのリスト情報が入る
# # label1と2には、凡例用に各labelのリスト情報が入る
# handler1, label1 = ax1.get_legend_handles_labels()
# handler2, label2 = ax2.get_legend_handles_labels()

# # 凡例をまとめて出力する
# ax1.legend(handler1 + handler2, label1 + label2, loc=2, borderaxespad=0.)
# temperature_max = 10 + max(df["月平均気温"])
# rainfall_max = 1.2 * max(df["月間降水量"])
# ax1.set_ylim([0, temperature_max])
# ax2.set_ylim([0, rainfall_max])

# plt.show()

# # # # csvへ出力
# # # # df_ave_power = pd.DataFrame({'DATE':date_list,'AVE_POWER':ave_power_list})
# # # # print(df_ave_power)
# # # # df_ave_power.to_csv('df_ave_power.csv',encoding='cp932', errors='ignore')