#!/usr/bin/env python
# coding: utf-8

# # Assigment 5
# 
# This assigment will be graded if everything works well. I will run the script as once and everything should be done without errors and mistakes. I should be able to run your scripts in my computer and get all the results. **USE RELATIVE PATHS**. An error or exception or anything that breaks the code will means NO GRADE (0). Additionally, you are not able to modify any file handly. It also means NO GRADE (0). Comment everything you think will help others read your script. We expect 0 errors using GitHub. Everything will be graded!
# 
# **ASK EVERYTHING! WE ARE HERE TO HELP YOU!**

# In this path **..\_data\sbs\B_RawData\bancos** you will find scraped data from [this link](https://www.sbs.gob.pe/app/pp/EstadisticasSAEEPortal/Paginas/TIActivaTipoCreditoEmpresa.aspx?tip=B). We get all the information of the last available day of every each month.
# 
# 1. Generate a function called **import_data_sbs_banks** that take as arguments `start_month`, `start_year`, `end_month` and `end_year`. This function should be able to import the files in **..\_data\sbs\B_RawData\bancos** taking into consideration these arguments. Additionally, it should work if it is only given the first two arguments `(start_mont, start_year)`. The function should `returns` a nested dictionary. The `main key` must be year and `second key` must be `month`. The values should be the dataframes.
