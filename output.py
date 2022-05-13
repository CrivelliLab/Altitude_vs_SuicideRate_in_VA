import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

## this file contains the output for 50 quantiles/beta value and AUC

"""50 quantile value"""

#get the 50 quantile dataset
def output_50_elevation(df_,smr_,ele_):
	df_=df_.groupby(pd.qcut(df_[smr_],50,precision=0))[ele_].agg(['median','mean','max','min','std','size']).reset_index()
	return df_

df_50_quantile=output_50_elevation(df_,'smr','elevation')
df_50_quantile_lm=output_50_elevation(df_,'pred_smr','elevation')
df_50_quantile_spatial=output_50_elevation(df_,'pred_queeen_smr','elevation')


#visulization of the plot by using matplotlib ggplot version
def visulization(df_,linear_df_,spatial_df_):
	X=np.arange(50)
	plt.style.use('ggplot')
	ind=np.arange(len(x))
	wdith=0.1
	spare_width=(1-width*2)/2

	y_axis=df_['mean'].tolist() #or ['median']
	y_axis_lm=linear_df_['mean'].tolist()
	y_axis_spatial=spatial_df_['mean'].tolist()

	fig=plt.figure(figsize(25,15),dpi=800)
	ax=fig.add_subplot(111)
	ax.plot(ind,y_axis_spatial,marker='o',label='VA_SMR_spatial',color='b')
	ax.plot(ind,y_axis_lm,marker='*',label='VA_SMR_lm',color='r')
	ax.plot(ind,y_axis,,label='VA_SMR',color='#ff0000')

	ax.legend(fontsize=10,loc=1)
	ax.set_xlim(spare_width,len(ind)-spare_width)
	ax.set_ylim(0,8000)
	ax.set_xlabel('County SMR rate per 100000',fontsize=15)
	ax.set_ylabel('Mean altitude(feet)')

	#if you are trying to insert the table inside the figure, can use plt.figure
	the_table=plt.table()

	return fig

visulization(df_50_quantile,df_50_quantile_lm,df_50_quantile_spatial)




"""beta value"""
#get the increasement dataset
def output_increasement(df_,smr_,ele_):
	#cuz there is few datapoints for altitude larger than 8000 feet
	bins=pd.IntervalIndex.from_tuples([(0,1000),(1001,2000),(2001,3000),(3001,4000),
										(4001,5000),(5001,6000),(6001,7000),(7001,8000),
										(8001,11000)])
	df_.groupby(pd.cut(df[ele_],bins))[smr_].agg(['median','mean','max','min','std','size']).reset_index()
	return df_

SMR_increase=output_increasement(VA_SMR,'pred_smr','elevation')


#calculate for the beta value
def beta(df_,):
	df_=df[['elevation','mean','size','std']]
	ci95_hi=[]
	ci95_lo=[]
	for i in df_.index:
    	a,m,c,s = df_.loc[i]
    	ci95_hi.append(m+1.95*s/math.sqrt(c))
   	    ci95_lo.append(m-1.95*s/math.sqrt(c))
	print("-"*30)
	df_['ci95_lo']=ci95_lo
	df_['ci95_hi']=ci95_hi
	print(df_)
	df_['ci95_lo']=df_['ci95_lo'].apply(lambda x:x-df_.iloc[0]['ci95_lo']).round(2)
	df_['ci95_hi']=df_['ci95_hi'].apply(lambda x:x-df_.iloc[0]['ci95_hi']).round(2)
	df_['beta']=(df_['ci95_hi']+df_['ci95_lo'])/2
	print("-"*30)
	print(df_)
	df_=df_.rename_axis('2000_2018_VA_Beta',axis=1)
	print("-"*30)
	print(df_[['elevation','size','beta']])
	return df_

beta(SMR_increase)








