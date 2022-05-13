import pandas as pd
import geopandas as gpd
from sklearn import linear_model
from pysal.lib import weights
from sklearn.metrcs import mean_squared_error as mse
from sklearn.metrcs import r2_score as r2
#input is geospatial level VA suicide ideation/Suicide Attempts/Suicide Mortality/Combined of all suicide situations

variable_names=['%_male','%_larger_50','%_not_hispanic','%_white','population_density','med_income','elevation']


def linear_model(df_,outstr_):
	X=df_[[variable_names]]
	y=df_[outstr_]
	lm=linear_model.LinearRegression().fit(X,y)
	df_[f'pred_{outstr_}']=lm.predict(X)
	return df_

def spatail_model(df_,outstr_):
	weight_=weights.Queen.from_dataframe(df_)
	weight_.transform='R'
	X=df_[[variable_names]].values
	y=df_[[outstr_]].values
	name_y=outstr_
	name_x=variable_names
	w=weight_
	model=spreg.ML_Lag(y,X,name_y,name_x,w)
	df_[f'pred_queen_{outstr_}']=model.predy
	return (df_,model)


performance=pd.Series({'spreg+Queen':mse(df_['outstr_'],model.predy.flatten()),
					   'spreg+Queen':mse(df_['outstr_'],model.predy.flatten())})