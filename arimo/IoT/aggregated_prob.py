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


##### Compute mean using 'weight' or 'harmonic' method
def compute_mean(list_array, weights, method= None):
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
w12: weights on the 'prob' when average, for example w12=[1,1], w15=[1,1], w125=[1,1,1]
method: 'weight' or 'harmonic'  
"""
def combined_anom_score(stores=None, ad_gr1=None, ad_gr2=None, ad_gr5=None, w12=None, w15=None, w125=None, method=None):
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

