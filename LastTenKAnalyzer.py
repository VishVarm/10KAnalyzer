import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import os

import pathlib
import textwrap

import google.generativeai as genai



def getData():
	"""
		Analyzes the 10-K documents of Pfizer and Zoom over the past 5 years
		and tracks the net income and revenue per year of both companies and
		uses the Google Gemini Pro LLM model to analyze this information of 
		both companies to give an explanation of the data in the context of 
		the COVID-19 pandemic. This function returns a dictionary of data for
		the two companies to be used in the front end of a Flask web app.
		
		Returns:
			A dictionary containing 4 dictionaries, 2 being the mapping of 
			year to the revenue of that year for both companies and the other
			2 being the mapping of year to the net income of that year for
			both companies. The other 2 entries of the dictionary are the 
			LLM analyses of both companies.
		
		
	"""
	
	# Initializing the dictionaries to contain Zoom's revenue and net income per year
	revenue_by_year = {}
	net_income_by_year = {}
	folder_path = "sec-edgar-filings/ZM/10-K"
	# Looping over every Zoom 10K document downloaded
	for folder_name in os.listdir(folder_path):
		if os.path.isdir(os.path.join(folder_path, folder_name)):
			doc_year = int(folder_name[11:13])
			file_name = "full-submission.txt"
			file_path = os.path.join(folder_path + "/" + folder_name, file_name)
			
			with open(file_path, "r") as file:
				text = file.read()
			# Using Soup lxml parser to parse the documents
			soup = BeautifulSoup(text, "lxml")
			
			# Finding the table in the 10-K detailing the revenue of Zoom for that year
			table_cell = soup.find('td', string="Revenue")
			if table_cell:
				table = table_cell.find_parent('table')
				html_table_io = StringIO(str(table))
				# Converting this html table to a panda dataframe
				dfs = pd.read_html(html_table_io)
				df_cleaned = dfs[0].dropna(axis=0, how='all')
				# Drop columns with NaN or '$' values	
				nan_counts = df_cleaned.isna().sum()
				dollar_counts = (df_cleaned == '$').sum()
				threshold = .5
				columns_to_drop_nan = nan_counts[nan_counts / len(df_cleaned) > threshold].index
				columns_to_drop_dollar = dollar_counts[dollar_counts / len(df_cleaned) > threshold].index
				# Combine columns to drop based on NaN and "$" counts
				columns_to_drop = set(columns_to_drop_nan) | set(columns_to_drop_dollar)
			
				# Remove the columns from the DataFrame
				df_cleaned = df_cleaned.drop(columns=columns_to_drop)
				# Remove duplicated columns from the DataFrame
				unique_percentage = df_cleaned.nunique() / len(df_cleaned)
				columns_to_drop_unique = unique_percentage[unique_percentage < threshold].index
				df_cleaned = df_cleaned.drop(columns=columns_to_drop_unique)
				# Remove every other column in the DataFrame
				df_cleaned = df_cleaned.iloc[:, ::2]
				# Remove the first column of the DataFrame
				df_cleaned = df_cleaned.drop(df_cleaned.columns[0], axis=1)
				
				# Adding the revenue data to the dictionary
				if doc_year == 20:
					revenue_by_year[2020] = int(df_cleaned.iloc[4, 1])
					revenue_by_year[2019] = int(df_cleaned.iloc[4, 2])
					revenue_by_year[2018] = int(df_cleaned.iloc[4, 3])
				elif doc_year == 21:
					revenue_by_year[2021] = int(df_cleaned.iloc[4, 1])
				else:
					revenue_by_year[2000 + doc_year] = int(df_cleaned.iloc[3, 1])
			else:
				print("Table data cell not found.")
		
			# Finding the net income per year of Zoom
			if doc_year == 23:
				# Finding the table in the 2023 10-K detailing the net income of Zoom for that year
				table_cell = soup.find('td', string="Adjustments to reconcile net income to net cash provided by operating activities:")
				if table_cell:
					table = table_cell.find_parent('table')
					html_table_io = StringIO(str(table))
					dfs = pd.read_html(html_table_io)
					df_cleaned = dfs[0].dropna(axis=0, how='all')
					# Drop columns with NaN or '$' values
					nan_counts = df_cleaned.isna().sum()
					dollar_counts = (df_cleaned == '$').sum()
					threshold = .5
					columns_to_drop_nan = nan_counts[nan_counts / len(df_cleaned) > threshold].index
					columns_to_drop_dollar = dollar_counts[dollar_counts / len(df_cleaned) > threshold].index
					# Combine columns to drop based on NaN and "$" counts
					columns_to_drop = set(columns_to_drop_nan) | set(columns_to_drop_dollar)
				
					# Remove the NaN and $ columns from the DataFrame
					df_cleaned = df_cleaned.drop(columns=columns_to_drop)
				
					# Remove duplicate columns from the DataFrame
					unique_percentage = df_cleaned.nunique() / len(df_cleaned)
					columns_to_drop_unique = unique_percentage[unique_percentage < threshold].index
					df_cleaned = df_cleaned.drop(columns=columns_to_drop_unique)
				
					# Remove every other column in the DataFrame
					df_cleaned = df_cleaned.iloc[:, ::2]
					
					# Remove the first column of the DataFrame
					df_cleaned = df_cleaned.drop(df_cleaned.columns[0], axis=1)
					# Add net income data to the dictionary
					net_income_by_year[2023] = int(df_cleaned.iloc[3, 1])
					net_income_by_year[2022] = int(df_cleaned.iloc[3, 2])
					net_income_by_year[2021] = int(df_cleaned.iloc[3, 3])
				else:
					print("Table data cell not found.")
			
			if doc_year == 20:
				# Finding the table in 2020 10-K detailing the net income of Zoom for that year
				table_cell = soup.find('td', string="Adjustments to reconcile net income (loss) to net cash provided by operating activities:")
				if table_cell:
					table = table_cell.find_parent('table')
					html_table_io = StringIO(str(table))
					dfs = pd.read_html(html_table_io)
					df_cleaned = dfs[0].dropna(axis=0, how='all')
					# Drop columns with NaN or '$' values
					nan_counts = df_cleaned.isna().sum()
					dollar_counts = (df_cleaned == '$').sum()
					threshold = .5
					columns_to_drop_nan = nan_counts[nan_counts / len(df_cleaned) > threshold].index
					columns_to_drop_dollar = dollar_counts[dollar_counts / len(df_cleaned) > threshold].index
					
					# Combine columns to drop based on NaN and "$" counts
					columns_to_drop = set(columns_to_drop_nan) | set(columns_to_drop_dollar)
				
					# Remove the NaN and $ columns from the DataFrame
					df_cleaned = df_cleaned.drop(columns=columns_to_drop)
				
					# Remove duplicate columns from the DataFrame
					unique_percentage = df_cleaned.nunique() / len(df_cleaned)
					columns_to_drop_unique = unique_percentage[unique_percentage < threshold].index
					df_cleaned = df_cleaned.drop(columns=columns_to_drop_unique)
					
					# Remove every other column from the DataFrame
					df_cleaned = df_cleaned.iloc[:, ::2]
					# Remove the first column from the DataFrame
					df_cleaned = df_cleaned.drop(df_cleaned.columns[0], axis=1)
					# Add net income data to the dictionary
					net_income_by_year[2020] = int(df_cleaned.iloc[3,1])
					net_income_by_year[2019] = int(df_cleaned.iloc[3,2])
					net_income_by_year[2018] = int("-" + df_cleaned.iloc[3,3][1:-1].replace(",",""))
				else:
					print("Table data cell not found.")

	# Sort the Zoom data dictionaries
	revenue_by_year = dict(sorted(revenue_by_year.items()))
	net_income_by_year = dict(sorted(net_income_by_year.items()))



	# Start LLM API usage
	# Input Google API key
	GOOGLE_API_KEY = "AIzaSyAgh2xEpGk53TmhMki0WNVZFVR0C9UX_kg"
	
	# Configure the Google genai LLM to use gemini-pro
	genai.configure(api_key=GOOGLE_API_KEY)
	model = genai.GenerativeModel('gemini-pro')
	
	
	# Generate an AI analysis of Zoom's financial information in the context of COVID-19 
	response = model.generate_content("Perform an analysis on Zoom's financial information over the last few years. \
		Specifically, analyze the impact of the COVID-19 pandemic on Zoom as a company based on the following data. \
		The dollar amounts are in thousands. \
		Revenue By Year: " + str(revenue_by_year) + "\n \
		Net Income By Year: " + str(net_income_by_year))


	# Initializing the dictionaries to contain Pfizer's revenue and net income per year
	pfe_revenue_by_year = {}
	pfe_net_income_by_year = {}
	folder_path = "sec-edgar-filings/PFE/10-K"
	# Looping over every Pfizer 10K document downloaded
	for folder_name in os.listdir(folder_path):
		if os.path.isdir(os.path.join(folder_path, folder_name)):
			doc_year = int(folder_name[11:13])
			file_name = "full-submission.txt"
			file_path = os.path.join(folder_path + "/" + folder_name, file_name)
	
			# Only analyzing the recent 10-K documents		
			if doc_year > 20:
				with open(file_path, "r") as file:
					text = file.read()
				# Using Soup lxml parser to parse the documents
				soup = BeautifulSoup(text, "lxml")
				
				# Search for the same Pfizer revenue table in each document
				if doc_year != 21:
					table_cell = soup.find('td', string="Income from continuing operations before provision/(benefit) for taxes on income")
				else:
					table_cell = soup.find('td', string="Income/(loss) from continuing operations attributable to Pfizer Inc. common shareholders")
				if table_cell:
					table = table_cell.find_parent('table')
					html_table_io = StringIO(str(table))
					# Converting html table to a panda dataframe
					dfs = pd.read_html(html_table_io)
					df_cleaned = dfs[0].dropna(axis=0, how='all')

					# Drop columns with NaN or "$" values
					nan_counts = df_cleaned.isna().sum()
					dollar_counts = (df_cleaned == '$').sum()
					threshold = .5
					columns_to_drop_nan = nan_counts[nan_counts / len(df_cleaned) > threshold].index
					columns_to_drop_dollar = dollar_counts[dollar_counts / len(df_cleaned) > threshold].index
				
					# Combine columns to drop based on NaN and "$" counts
					columns_to_drop = set(columns_to_drop_nan) | set(columns_to_drop_dollar)
				
					# Remove the NaN and $ columns from the DataFrame
					df_cleaned = df_cleaned.drop(columns=columns_to_drop)
					# Remove duplicate columns from the DataFrame
					unique_percentage = df_cleaned.nunique() / len(df_cleaned)
					columns_to_drop_unique = unique_percentage[unique_percentage < threshold].index
					df_cleaned = df_cleaned.drop(columns=columns_to_drop_unique)
					if doc_year != 21:
					# Delete every other column from the DataFrame
						df_cleaned = df_cleaned.iloc[:, ::2]
					else:
					# Delete every other column from the DataFrame starting from the first column
						df_cleaned = df_cleaned.iloc[:, 1::2]
					# Delete the first column from the DataFrame
					df_cleaned = df_cleaned.drop(df_cleaned.columns[0], axis=1)
					# Add revenue data to the dictionary
					if doc_year == 21:
						pfe_revenue_by_year[2020] = int(df_cleaned.iloc[2, 0])
						pfe_revenue_by_year[2019] = int(df_cleaned.iloc[2, 1])
						pfe_revenue_by_year[2018] = int(df_cleaned.iloc[2, 2])
					else:
						pfe_revenue_by_year[1999+doc_year] = int(df_cleaned.iloc[2, 1])
						# Add net income data to the dictionary (stored in same table)
						pfe_net_income_by_year[1999+doc_year] = int(df_cleaned.iloc[15, 1])
				
				# Searching for older net income data to the dictionary
				if doc_year == 21:
					table_cell = soup.find('td', string="Net income before allocation to noncontrolling interests")
					if table_cell:
						table = table_cell.find_parent('table')
						html_table_io = StringIO(str(table))
						# Converting html table to a panda dataframe
						dfs = pd.read_html(html_table_io)
						df_cleaned = dfs[0].dropna(axis=0, how='all')

						# Drop columns with NaN or '$' values
						nan_counts = df_cleaned.isna().sum()
						dollar_counts = (df_cleaned == '$').sum()
						threshold = .5
						columns_to_drop_nan = nan_counts[nan_counts / len(df_cleaned) > threshold].index
						columns_to_drop_dollar = dollar_counts[dollar_counts / len(df_cleaned) > threshold].index
						
						# Combine columns to drop based on NaN and "$" counts
						columns_to_drop = set(columns_to_drop_nan) | set(columns_to_drop_dollar)
						
						# Remove the NaN and $ columns from the DataFrame
						df_cleaned = df_cleaned.drop(columns=columns_to_drop)
						# Remove duplicate columns from the DataFrame
						unique_percentage = df_cleaned.nunique() / len(df_cleaned)
						columns_to_drop_unique = unique_percentage[unique_percentage < threshold].index
						df_cleaned = df_cleaned.drop(columns=columns_to_drop_unique)
						# Remove every other column from the Data Frame
						df_cleaned = df_cleaned.iloc[:, ::2]
						# Remove the first column from the DataFrame
						df_cleaned = df_cleaned.drop(df_cleaned.columns[0], axis=1)
						# Add the net income to the dictionary
						pfe_net_income_by_year[2020] = int(df_cleaned.iloc[15,1])
						pfe_net_income_by_year[2019] = int(df_cleaned.iloc[15,2])
						pfe_net_income_by_year[2018] = int(df_cleaned.iloc[15,3])
			
	# Sort both of the Pfizer data dictionaries
	pfe_revenue_by_year = dict(sorted(pfe_revenue_by_year.items()))

	pfe_net_income_by_year = dict(sorted(pfe_net_income_by_year.items()))

	
	# Generate an AI analysis of Pfizer's financial information in the context of COVID-19 
	pferesponse = model.generate_content("Perform an analysis on Pfizer's financial information over the last few years. \
		Specifically, analyze the impact of the COVID-19 pandemic on Pfizer as a company based on the following data. \
		The dollar amounts are in thousands. \
		Revenue By Year: " + str(pfe_revenue_by_year) + "\n \
		Net Income By Year: " + str(pfe_net_income_by_year))

	# Initialize the final dictionary to contain all previous data and analyses for both companies
	# to be returned
	finalData = {}	
	finalData["PFERev"] = pfe_revenue_by_year
	finalData["PFENet"] = pfe_net_income_by_year
	finalData["PFEResponse"] = pferesponse.text
	finalData["ZMRev"] = revenue_by_year
	finalData["ZMNet"] = net_income_by_year
	finalData["ZMResponse"] = response.text
	return finalData