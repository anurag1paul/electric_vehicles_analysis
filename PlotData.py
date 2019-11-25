import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_df(user_id=120000, state = "all"):
    '''
	Takes in user type and state code and creates a dataframe
	using the master_dict.npy file of cost analysis.
    '''
    assert user_id in {60000, 120000, 180000}
    
    data = np.load("master_dict.npy", allow_pickle=True).item()

    car_name = []
    base = []
    maintenance = []
    fuel_type = []
    fuel_cost = []
    env = []
    insurance = []

    for key in data:
        car_name.append(key)
        c_dict = data[key]
        base.append(c_dict["base"])
        maintenance.append(c_dict["maintenance"])
        fuel_type.append(c_dict["fuel_type"])
        user = c_dict["user_type"][user_id]
        
        if state == "all":
            if c_dict["fuel_type"] == "e":
                env_cost = 0
            else:
                env_cost = np.mean(list(user["env_cost"].values()))
            env.append(env_cost)
            insurance.append(np.mean(list(c_dict['insurance'].values())))
            fuel_cost.append(np.mean(list(user["fuel_cost"].values())))
        else:
            if c_dict["fuel_type"] == "e":
                env_cost = 0
            else:
                env_cost = user["env_cost"][state] 
            env.append(env_cost)
            insurance.append(c_dict['insurance'][state])
            fuel_cost.append(user["fuel_cost"][state])

    df = pd.DataFrame({"name": car_name,
                       "fuel_type": fuel_type,
                       "base": base,
                       "fuel": fuel_cost,
                       "maintenance": maintenance,
                       "insurance": insurance,
                       "env": env})
    
    df["total"] = df["base"] + df["fuel"] + df["maintenance"] +df["insurance"] + df["env"] 
    return df


def plot_sales():
	'''
	Plots information and saves a .png.
	List of Images created:
	ElectricSales.png
	ElectricSalesPrediction.png
	Market2011.png
	Market2021.png
	TotalSales.png
	YearlyEvG.png
	'''
	data = 'ElectricSales.csv'
	df = pd.read_csv(data,index_col=0)
	df['Electric'] = df['Electric']/1000
	df['Plug-in hybrid-electric'] = df['Plug-in hybrid-electric']/1000
	
	fig, ax = plt.subplots(dpi=200)
	ax.set_xlabel('Year',fontsize='14')
	ax.set_ylabel('Sales in Thousands',fontsize='14')
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.plot(df.index,df.Electric,label='Electric',color='limegreen')
	ax.plot(df.index,df.Electric,'.',color='limegreen')
	ax.plot(df.index,df['Plug-in hybrid-electric'],label='Hybrid-Electric(Plug-In)',color='blue')
	ax.plot(df.index,df['Plug-in hybrid-electric'],'.',color='blue')
	ax.legend(loc='upper left')
	plt.title('Electric Vehicle Sales')
	plt.tight_layout()
	plt.show()
	fig.savefig('ElectricSales.png')

	fig, ax = plt.subplots(dpi=200)
	ax.set_xlabel('Year',fontsize='14')
	ax.set_ylabel('Sales in Thousands',fontsize='14')
	ax.yaxis.set_ticks(np.arange(0, 170, 40))
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	z1 = np.polyfit(df.index,df.Electric,2)
	z2 = np.polyfit(df.index,df['Plug-in hybrid-electric'],2)
	p1 = np.poly1d(z1)
	p2 = np.poly1d(z2)
	xp = np.linspace(2011, 2022, 100)
	ax.plot(df.index,df.Electric,label='Electric',color='limegreen')
	ax.plot(df.index,df.Electric,'.',color='limegreen')
	ax.plot(df.index,df['Plug-in hybrid-electric'],label='Hybrid-Electric(Plug-In)',color='blue')
	ax.plot(df.index,df['Plug-in hybrid-electric'],'.',color='blue')
	ax.plot(xp, p1(xp),'--',label='Electric Projection',color='limegreen') 
	ax.plot(xp, p2(xp),'--',label='Hybrid Projection',color='blue')
	ax.legend(loc='upper left')
	plt.tight_layout()
	plt.show()
	fig.savefig('ElectricSalesPrediction.png')

	data1 = 'TotalSales.csv'
	data2 = 'TotalSalesFullExtra.csv'
	df2 = pd.read_csv(data1,index_col=0)
	df3 = pd.read_csv(data2,index_col=0)

	fig, ax = plt.subplots(dpi=200)
	ax.set_xlabel('Year',fontsize='14')
	ax.set_ylabel('Sales in Thousands',fontsize='14')
	ax.set_ylim([0,12000])
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.plot(df2.index,df2['Total new passenger car sales'],color='dimgrey')
	ax.plot(df2.index,df2['Total new passenger car sales'],'.',color='dimgrey')
	plt.title('Total Car Sales')
	plt.tight_layout()
	plt.show()
	fig.savefig('TotalSales.png')

	fig, ax = plt.subplots()
	ax.set_xlabel('Year')
	ax.set_ylabel('Sales in Thousands')
	ax.set_ylim([0,12000])
	z = np.polyfit(df3.index,df3['Total new passenger car sales'],2)
	p3 = np.poly1d(z)
	xp = np.linspace(1970, 2022, 100)
	ax.plot(df3.index,df3['Total new passenger car sales'],label='Total New Passenger Car Sales',color='blue')
	ax.plot(xp, p3(xp),'--',label='Total Sales Projection')
	ax.legend(loc='lower left')
	plt.show()
	fig.savefig('ElectricSalesPrediction.png')

	GraphC = pd.concat([df.T,df2.T]).T
	GraphC['Electric'] = GraphC['Plug-in hybrid-electric'] + GraphC['Electric']
	GraphC['Electric'] = GraphC['Electric']/1000
	GraphC = GraphC.iloc[:,2:]
	titles = ['Total new passenger car sales','Electric']
	GraphC = GraphC.reindex(columns=titles)
	GraphC['Percentage'] = GraphC['Electric']/GraphC['Total new passenger car sales']

	labels = ['Electric', 'Gas']
	sizes = [p1(2021)+p2(2021), (p3(2021))-(p1(2021)+p2(2021))]
	explode = (0.3,0)
	colors = ['limegreen','silver']
	fig1, ax1 = plt.subplots(dpi=200)
	ax1.pie(sizes, labels=labels, colors=colors, explode=explode, autopct='%1.1f%%', shadow=False, startangle=160, textprops={'fontsize': 14})
	ax1.axis('equal')
	plt.title('2021 (Projected)')
	plt.tight_layout()
	plt.show()
	fig1.savefig('Market2021.png')

	labels = ['Electric', 'Gas']
	sizes = [p1(2011)+p2(2011), (p3(2011))-(p1(2011)+p2(2011))]
	explode = (0.3,0)
	colors = ['limegreen','silver']
	fig1, ax1 = plt.subplots(dpi=200)
	ax1.pie(sizes, labels=labels, colors=colors, explode=explode, autopct='%1.1f%%', shadow=False, startangle=160, textprops={'fontsize': 14})
	ax1.axis('equal')
	plt.title('2011')
	plt.tight_layout()
	plt.show()
	fig1.savefig('Market2011.png')

	df1 = get_df(user_id=60000)
	df2 = get_df(user_id=120000)
	df3 = get_df(user_id=180000)

	df1['Yearly'] = (df1['total'] - df1['base'])/10
	df1 = df1.sort_values('Yearly')
	df2['Yearly'] = (df2['total'] - df2['base'])/10
	df2 = df2.sort_values('Yearly')
	df3['Yearly'] = (df3['total'] - df3['base'])/10
	df3 = df3.sort_values('Yearly')

	de1 = df1[df1['fuel_type']=='e'][:7]['Yearly'].mean()
	dg1 = df1[df1['fuel_type']=='g'][:45]['Yearly'].mean()
	de2 = df2[df2['fuel_type']=='e'][:7]['Yearly'].mean()
	dg2 = df2[df2['fuel_type']=='g'][:45]['Yearly'].mean()
	de3 = df3[df3['fuel_type']=='e'][:7]['Yearly'].mean()
	dg3 = df3[df3['fuel_type']=='g'][:45]['Yearly'].mean()

	e = (de1,de2,de3)
	g = (dg1,dg2,dg3)
	ind = np.arange(3)
	width = 0.45
	fig, ax = plt.subplots(dpi=200)
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	rects1 = ax.bar(ind+width, e, width, color='limegreen')
	rects2 = ax.bar(ind, g, width, color='dimgrey')
	ax.set_ylabel('Yearly Cost')
	ax.set_ylim([2000,3750])
	ax.yaxis.set_ticks(np.arange(2000, 3750, 400))
	ax.set_xlabel('Miles Per Year')
	ax.set_xticks(ind + width / 2)
	ax.set_xticklabels(('6000', '12000', '18000'))
	ax.legend((rects2[0], rects1[0]), ('Gas','Electric'),loc='upper left')
	plt.tight_layout()
	plt.show()
	fig.savefig('YearlyEvG.png')