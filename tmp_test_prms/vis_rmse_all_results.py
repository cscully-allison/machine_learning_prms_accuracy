from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import pandas as pd
import numpy as np
from datetime import datetime
import os

app_path = os.path.dirname(os.path.abspath('__file__'))

def vis_3D(filename):
	'''
	this function visualizes
	RMSE, alpha, window_size
	'''
	df = pd.read_csv(filename)

	a = df['alpha'].tolist()
	b = df['window_size'].tolist()
	c = df['rmse'].tolist()

	a = np.asarray(a)
	b = np.asarray(b)
	c = np.asarray(c)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')


	ax.scatter(a, b, c)

	ax.set_xlabel('Alpha')
	ax.set_ylabel('Window Per')
	ax.set_zlabel('RMSE')

	plt.show()

	# fig = plt.figure()
	# ax = fig.gca(projection='3d')

	# # Plot the surface.
	# surf = ax.plot_surface(np.asarray(a), np.asarray(b), np.asarray(c), cmap=cm.coolwarm,
	#                        linewidth=0, antialiased=False)


	# ax.set_zlim(3.0, 7.0)
	# ax.zaxis.set_major_locator(LinearLocator(10))
	# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

	# fig.colorbar(surf, shrink=0.5, aspect=5)

	# plt.show()

def improved_predication(original_file, input_file, output_file):
	'''
	this function generates improved predicion file
	based on original_file (orginal prediction) and input_file (delta prediction file)
	results are outputed into output_file
	'''
	# TODO, need to have orginal predictions in inputfile
	# hint: use id
	df_original = pd.read_csv(original_file)
	df_input = pd.read_csv(input_file)
	df_output = pd.DataFrame({})

def convert_str_into_time(input_list):
	result_list = []
	for i in input_list:
		result_list.append(datetime.strptime(i, '%Y--%m--%d'))
	return result_list

def vis_error_prediction_PI(input_file, fig_title):
	'''
	this function vis error prediction boundary
	'''
	df = pd.read_csv(input_file)
	x_id = convert_str_into_time(df['time'].tolist())
	lower = df['lower'].tolist()
	upper = df['upper'].tolist()
	prediction = df['prediction'].tolist()
	ground_truth = df['ground_truth'].tolist()

	fig, ax = plt.subplots()
	ax.plot(x_id,lower, '-',linewidth=2, label='lower_bound')
	ax.plot(x_id,upper, '--',linewidth=2, label='upper_bound')
	ax.plot(x_id,prediction, ':',linewidth=2, label='predict_error')
	ax.plot(x_id,ground_truth, 'r--',linewidth=2, label='ground_truth')
	legend = ax.legend(loc='lower right', shadow=True)
	# legend = ax.legend(bbox_to_anchor=(0., 0.0, 1.0, .050), loc=3, ncol=1, mode="expand", borderaxespad=0.)

	plt.xlabel('time')
	plt.ylabel('value')
	plt.title(fig_title)
	plt.show()

def collect_corresponding_obs_pred(input_df, time_list):
	'''
	this function collects corresponding values
	based on time info, and return obs and original pred
	'''
	obs_list = []
	original_pred_list = []
	for i in time_list:
		time_info = i.split('--')
		year = time_info[0]
		month = time_info[1]
		day = time_info[2]
		aim_df = input_df.query('year=='+year+' & month=='+month+' & day=='+day)
		obs_list.append(float(aim_df['runoff_obs']))
		original_pred_list.append(float(aim_df['basin_cfs_pred']))
	return obs_list, original_pred_list


def vis_improved_prediction_PI(original_model_output, input_file, fig_title):
	'''
	this function vis improved prediction boundary
	'''
	df_origin = pd.read_csv(original_model_output)
	df = pd.read_csv(input_file)
	time_list = df['time'].tolist()

	truth,origin_pred = collect_corresponding_obs_pred(df_origin,time_list)
	x_id = convert_str_into_time(time_list)
	lower_error = df['lower'].tolist()
	lower = [x + y for x, y in zip(lower_error,origin_pred)]

	upper_error = df['upper'].tolist()
	upper = [x + y for x, y in zip(upper_error,origin_pred)]

	prediction_error = df['prediction'].tolist()
	prediction = [x + y for x, y in zip(prediction_error,origin_pred)]

	ground_truth = truth

	fig, ax = plt.subplots()
	ax.plot(x_id,lower, '-',linewidth=2, label='lower_bound')
	ax.plot(x_id,upper, '--',linewidth=2, label='upper_bound')
	ax.plot(x_id,prediction, ':',linewidth=2, label='improved_prediction')
	ax.plot(x_id,truth, 'r--',linewidth=2, label='ground_truth')
	legend = ax.legend(loc='upper right', shadow=True)
	# legend = ax.legend(bbox_to_anchor=(0., 0.0, 1.0, .050), loc=3, ncol=1, mode="expand", borderaxespad=0.)

	plt.xlabel('time')
	plt.ylabel('value')
	plt.title(fig_title)
	plt.show()
	# fig.savefig(app_path+'/'+fig_title+'.png')

# vis_error_prediction_PI('bound.csv','predicted_error_PI')
vis_improved_prediction_PI('prms_input.csv', 'bound.csv','predicted_error_PI')
# improved_predication('prms_input.csv','bound.csv','improved_PI')
# vis_3D('rmse_all_results.csv')


