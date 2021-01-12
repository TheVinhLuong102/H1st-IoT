#!/usr/bin/env python
# coding: utf-8

# import libraries
from collections import Counter
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('ggplot')
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
pd.set_option('display.max_columns', 999)
pd.set_option('display.max_rows', 2000)

##### configurarion files
# group_1_cols = ['condensing_pressure', 'evaporation_pressure', 'return_gas_temp',
                # '30_minutes_accumulated_power_consumption',
                # 'showcase_temp1_f5', 'showcase_temp1_f7', 'showcase_temp1_f9']

# group_2_cols = ['condensing_pressure', 'evaporation_pressure', 'return_gas_temp',
                # '30_minutes_accumulated_power_consumption',
                # 'showcase_temp1_f5', 'showcase_temp1_f7', 'showcase_temp1_f9', 'showcase_temp1_f11']

# group_5_cols = ['condensing_pressure', 'evaporation_pressure', 
                # '30_minutes_accumulated_power_consumption', 
                # 'showcase_temp1_f5', 'showcase_temp1_f7', 'showcase_temp1_f9', 'showcase_temp1_f17', 'showcase_temp2_f18']

# stores = {'dalian_lawson_kaifaqujumeidongwan':[1,2],
# 'dalian_lawson_dongruanruanjianyuan':[1,2],
# 'dalian_lawson_renminlubaiyujie':[1,2],
# 'dalian_lawson_qixianlingruifengyuan':[1,2],
# 'dalian_lawson_guangxianlusaiboledaxia':[1,2],
# 'dalian_lawson_huangpuluyinhaiwanxiang':[1,5],
# 'dalian_lawson_caishijiezhenfudaxia':[1,5],
# 'dalian_lawson_jiazhaoyeguangchang':[1,2],
# 'dalian_lawson_hongxinghailangu':[1,2],
# 'dalian_lawson_xiandaifuwuyedaxia':[1,2],
# 'dalian_lawson_kaifaqujiangchengguangchang':[1,2],
# 'dalian_lawson_jinzhouwankecheng':[1,2],
# 'dalian_lawson_qingnierjie':[1,2],
# 'dalian_lawson_rongshengjie':[1,5],
# 'dalian_lawson_tianjinjietianheguangchang':[1,5],
# 'dalian_lawson_taidedasha':[1,2,5],
# 'dalian_lawson_kaifaqushuiyulanting':[1,2],
# 'dalian_lawson_xinghaibainianhui':[1,5],
# 'dalian_lawson_titanlunuodedaxia':[1,2],
# 'dalian_lawson_haikoulupenghui':[1,2],
# 'dalian_lawson_xiaopingdaobofeilandao':[1,2],
# 'dalian_lawson_huashunjiexiangzhouxincheng':[1,5],
# 'dalian_lawson_kaifaqupuxiangitzhongxin':[1,2],
# 'dalian_lawson_huarunkaixuanmenyiqi':[1,5],
# 'dalian_lawson_yuanyangfengjing':[1,2],
# 'dalian_lawson_jinzhouxinxiwangcheng':[1,2],
# 'dalian_lawson_shandongluhuananzhongxue':[1,2],
# 'dalian_lawson_renminluanlejie':[1,2],
# 'dalian_lawson_songjiangluhuazhongjie':[1,2],
# 'dalian_lawson_yidaeryuan':[1,2],
# 'dalian_lawson_xianlukejiguangchang':[1,2],
# 'dalian_lawson_xianluxingzhengdaxia':[1],
# 'dalian_lawson_huanghelujiaotongdaxue':[1,2],
# 'dalian_lawson_xiaopingdaohaijun':[1,5],
# 'dalian_lawson_dunhuangluhuaxinyuan':[1,2],
# 'dalian_lawson_xinggongjie':[1,2],
# 'dalian_lawson_changpingjie':[1,2],
# 'dalian_lawson_donggangshuijingliwan':[1,2],
# 'dalian_lawson_haizhongguoxingyunjie':[1,2],
# 'dalian_lawson_shenyangsanhaojieqinghuatongfang':[1,2],
# 'dalian_lawson_hutanlubitaobeiyuan':[1,2],
# 'dalian_lawson_ganjingzitiyuzhongxin':[1,5],
# 'dalian_lawson_jinzhouwenrunjinchen':[1,5],
# 'dalian_lawson_ganjingziqufengdanlicheng':[1,2],
# 'dalian_lawson_jiefangluqingyunyingshan':[1,2],
# 'dalian_lawson_kaifaquwanda':[1],
# 'dalian_lawson_fujingjiexingfuejia':[1,2],
# 'dalian_lawson_shenyangcaifuzhongxin':[1,5],
# 'dalian_lawson_shengliqiaobei':[1,2],
# 'dalian_lawson_jinzhouhepingliyuan':[1,2],
# 'dalian_lawson_kaifaquxinjie':[1,2],
# 'dalian_lawson_gaoxinqujingxianjie':[1,5],
# 'dalian_lawson_hongxinghaishiguanghai':[1,2],
# 'dalian_lawson_kaifaqubenxijie':[1,2],
# 'dalian_lawson_shenyangxita':[1,2],
# 'dalian_lawson_shenyangjiandayunfeng':[1,2],
# 'dalian_lawson_xiuyuejiemingxiushanzhuang':[1,2],
# 'dalian_lawson_shenyangyunfengbeijie':[1,2],
# 'dalian_lawson_huitongjieyuanyangrongyu':[1,2],
# 'dalian_lawson_gaoxinyuanquziyuguandi':[1,2],
# 'dalian_lawson_dashangqingnijie':[1,2],
# 'dalian_lawson_kaifaquxingchenglu':[1,2],
# 'dalian_lawson_tianheluhuadongrenjia':[1,2]}


##### read the raw data
# all_parquet = pd.read_csv('30_minute_based_test_AD.csv')

## read anomaly score from 3 groups
# ad_gr1 = pd.read_parquet('./Jupyter_server/VAEAnomScores30Minutes_group_1_op=cooling.parquet')
# ad_gr2 = pd.read_parquet('./Jupyter_server/VAEAnomScores30Minutes_group_2_op=cooling.parquet')
# ad_gr5 = pd.read_parquet('./Jupyter_server/VAEAnomScores30Minutes_group_5_op=cooling.parquet')
# print('The number of stores in: ', '\n',  
                # 'Group1: ', len(ad_gr1['store_name'].unique()), '\n', 
                # 'Group2: ', len(ad_gr2['store_name'].unique()), '\n',
                # 'Group5: ', len(ad_gr5['store_name'].unique()))

##### Compute mean using 'weight' or 'harmonic' method
def compute_mean(list_array, weights, method='weight'):
    if len(list_array) == len(weights):
        if method == 'weight':
            weight_avg = np.sum((np.array(list_array))*(np.array(weights).reshape(-1,1)), axis=0)/np.sum(weights)
        elif method == 'harmonic':            
            weight_avg = np.sum(weights)/np.sum(np.array(weights).reshape(-1,1)/(np.array(list_array)), axis=0)
        else:
            print('There are only two methods to compute mean: "weight" and "harmonic".')
            return None
        return weight_avg
    else:
        print('Please check, length of list_array and length of weights must be equal, check weights!!')
        return None

##### combine anomaly score from different groups by using 'weight' or 'harmonic' mean
"""
stores: 'store_name':[group_x,group_y]
ad_gr1: anomaly score from model vae, having three features ['store_name', 'date_time', 'prob']
w12: weights on the 'prob' when average
method: 'weight' or 'harmonic'  
"""
def combined_anom_score(stores, ad_gr1, ad_gr2, ad_gr5, w12=[1,1], w15=[1,1], w125=[1,1,1], method='weight'):
    # copy dataframe to avoid override their values
    ad_g1 = ad_gr1.copy()
    ad_g2 = ad_gr2.copy()
    ad_g5 = ad_gr5.copy()
    # offset to adjust probability to positive
    offset = np.ceil(abs(min([ad_g1.prob.min(), ad_g2.prob.min(), ad_g5.prob.min()]))) 
    ad_g1['prob'] = ad_g1[['prob']] + offset
    ad_g2['prob'] = ad_g2[['prob']] + offset
    ad_g5['prob'] = ad_g5[['prob']] + offset
    # start to combine probability
    df = pd.DataFrame(columns=['store_name','date_time','prob'])
    for shop_name, list_group in stores.items():
        if len(list_group) == 1:
            tmp_df = ad_g1[ad_g1['store_name']==shop_name].copy()
            df = df.append(tmp_df[['store_name','date_time','prob']], ignore_index=True)
        elif len(list_group) == 2:
            if list_group == [1,2]:
                tmp_df = ad_g1[ad_g1['store_name']==shop_name].copy()
                if (len(ad_g1[ad_g1['store_name']==shop_name].prob.values) 
                    == len(ad_g2[ad_g2['store_name']==shop_name].prob.values)):
                    weight_avg = compute_mean([ad_g1[ad_g1['store_name']==shop_name].prob.values, 
                                               ad_g2[ad_g2['store_name']==shop_name].prob.values], w12, method)
                    if weight_avg is not None:
                        tmp_df['prob'] = weight_avg
                    else:
                        return
                else: 
                    print('lack of data in anomaly group: ', shop_name, list_group)
                df = df.append(tmp_df[['store_name','date_time','prob']], ignore_index=True)
            elif list_group == [1,5]:
                tmp_df = ad_g1[ad_g1['store_name']==shop_name].copy()
                if (len(ad_g1[ad_g1['store_name']==shop_name].prob.values) 
                    == len(ad_g5[ad_g5['store_name']==shop_name].prob.values)):
                    weight_avg = compute_mean([ad_g1[ad_g1['store_name']==shop_name].prob.values, 
                                               ad_g5[ad_g5['store_name']==shop_name].prob.values], w15, method)
                    if weight_avg is not None:
                        tmp_df['prob'] = weight_avg
                    else:
                        return
                else: 
                    print('lack of data in anomaly group: ', shop_name, list_group)
                df = df.append(tmp_df[['store_name','date_time','prob']], ignore_index=True)
            else: 
                print('Please check the unique list groups! There is no: ', list_group)
        elif len(list_group) == 3:
            if list_group == [1,2,5]:
                tmp_df = ad_g1[ad_g1['store_name']==shop_name].copy()
                if ((len(ad_g1[ad_g1['store_name']==shop_name].prob.values) 
                    == len(ad_g2[ad_g2['store_name']==shop_name].prob.values)) and
                   (len(ad_g2[ad_g2['store_name']==shop_name].prob.values) 
                    == len(ad_g5[ad_g5['store_name']==shop_name].prob.values))):
                    weight_avg = compute_mean([ad_g1[ad_g1['store_name']==shop_name].prob.values, 
                                               ad_g2[ad_g2['store_name']==shop_name].prob.values,
                                               ad_g5[ad_g5['store_name']==shop_name].prob.values], w125, method)
                    if weight_avg is not None:
                        tmp_df['prob'] = weight_avg
                    else:
                        return
                else: 
                    print('lack of data in anomaly group: ', shop_name, list_group)
                df = df.append(tmp_df[['store_name','date_time','prob']], ignore_index=True)
            else:
                print('Please check the unique list groups! There is no: ', list_group) 
        else:
            print('Please check the unique list groups! There is no: ', list_group)
    return df
 
##### run combined 3 groups: group1, group2, and group5 
# combined_df = combined_anom_score(stores, ad_gr1, ad_gr2, ad_gr5, w12=[0.4,0.6], w15=[0.4,0.6], w125=[0.2,0.4,0.4], method='harmonic')        

##### plot to quickview for first store in all stores
# threshold = np.quantile(combined_df.prob.values, 0.015, axis=0)
# combined_df['threshold'] = threshold
# for store in combined_df.store_name.unique():
    # combined_df.set_index('date_time', drop=True).plot(title=store)
    # break

