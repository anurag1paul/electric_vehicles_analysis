# Electric Vehicles Analysis
Analyzing various factors for deciding between electric and gasoline vehicles

## Assumptions
- Good driver
- 10 year life for a vehicle
- Three types of users - 6000, 12000, 18000 miles per year

## File Structure
- data: stores all the scraped and processed data
- data_scraping
    - car_sales.py : utility functions for scrape car sales data
    - cars_price_data.py : scrape cars.com for car market prices
    - gas_prices.py : scrape gasbuddy.com for latest gas prices
    - ev_charger.py : fetch electricity prices and charging station locations
    - insurance_price.py : scrape insyre.com for insurance prices of all cars 
    in all states
    - maintenance_costs.py : scrape yourmechanic.com for maintenance costs
    - insurance_matching.py : utility for matching car names in insurance and market price datasets
- data_analysis
    - cost_model.py : build cost model
    - environmental_data_process.py : process and analyze environmental data
    - df_gen.py : generate dataframe from processed cost_model pickle
    - best_state_for_ev.py : analyze and find the best state for EV
    - critical_point_analysis.py : find critical points for each state
- data_visualization
    - plot_data.py : functions for plotting all analysis
- plots
- Project Visualizations.ipynb : notebook to check out the visulaizations

## Dependencies
The major dependencies of the project are:
- numpy
- pandas
- matplotlib
- lxml
- requests
- fuzzywuzzy
- plotly

Dependencies can be installed using:
`pip install -r requirements.txt`

## How to run the code
1. Create a virtual environment and install all dependencies
2. Scrape all data using:
    
    `python3 build_data.py`
3. Build the cost model using:
    
    `python build_cost_model.py`

4. Use the python notebook 'Project Visualizations.ipynb' to generate visualizations

