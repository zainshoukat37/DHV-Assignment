from ctypes import alignment
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Load the dataset
file_path = 'dataset1.xlsx'
xls = pd.ExcelFile(file_path)

# Define the list of selected countries
selected_countries = ['China', 'Singapore', 'Germany', 'Canada', 'Australia']

# Load data from the provided Excel file sheets
education_df = pd.read_excel(xls, sheet_name='Education')
health_df = pd.read_excel(xls, sheet_name='Health')
exports_df = pd.read_excel(xls, sheet_name='Exports')
gdp_growth_df = pd.read_excel(xls, sheet_name='GDP Growth')
gdp_current_df = pd.read_excel(xls, sheet_name='Current GDP')

# Filter the data for the selected countries and pivot for easier plotting
def prepare_data(df, index_name):
    filtered_df = df[df['Country Name'].isin(selected_countries)]
    return filtered_df.melt(id_vars='Country Name', var_name='Year', value_name=index_name)

# Convert Year to string and filter based on the years of interest
years_of_interest = [str(year) for year in range(2000, 2016, 3)]
def filter_years(df):
    df['Year'] = df['Year'].astype(str)
    return df[df['Year'].isin(years_of_interest)]

# Prepare the data
education_pivot = filter_years(prepare_data(education_df, 'Education Index'))
health_pivot = filter_years(prepare_data(health_df, 'Health Index'))
exports_pivot = filter_years(prepare_data(exports_df, 'Exports'))
gdp_growth_pivot = filter_years(prepare_data(gdp_growth_df, 'GDP Growth'))

# Define the plotting function with modified legend size
def plot_line_chart(df, index_name, ax, colors):
    for i, country in enumerate(selected_countries):
        country_data = df[df['Country Name'] == country]
        ax.plot(country_data['Year'], country_data[index_name], marker='o', label=country, color=colors[i])
    ax.set_title(f'{index_name} (2000-2015)')
    ax.legend(fontsize='small')  # Adjusted legend font size
    ax.grid(True)

# New function for plotting the horizontal bar chart
def plot_horizontal_bar_chart(df, index_name, ax, colors):
    for i, country in enumerate(selected_countries):
        country_data = df[df['Country Name'] == country]
        ax.barh(country_data['Year'], country_data[index_name], color=colors[i], label=country, align='center')
    ax.set_title(f'{index_name} (2000-2015)')
    ax.legend(fontsize='small')
    ax.grid(True)

# Create a figure with an overall GridSpec
fig = plt.figure(figsize=(20, 20))

# Create a top area for the title, name, and ID
fig.suptitle('GDP Growth and their Factors(2000 - 2015)\nName: Zain Shoukat    ID: 22087011', ha='center',fontsize=26, weight='bold')

# Creating a 3x3 grid layout for the visualizations and text blocks below the title
main_gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
colors_palette = plt.cm.Dark2(range(len(selected_countries)))

# First Visualization - Education Index
ax1 = fig.add_subplot(main_gs[0, 0])
plot_line_chart(education_pivot, 'Education Index', ax1, colors_palette)

# Second Visualization - Health Index
ax3 = fig.add_subplot(main_gs[0, 2])
plot_line_chart(health_pivot, 'Health Index', ax3, colors_palette)

# Text - Education & Health Index
text = '''
Educational graph illustrates the significant strides made by
China in education between 2000 and 2015, underscoring a
strategic emphasis on educational reform  and  investment.
Other nations, such as Canada and Australia,  also exhibit
upward  trends showcasing  the global  prioritization of
educational improvement.

The Health graph for Australia, Canada, Germany sustain high
index, portrays positive trajectory in health outcomes, reflecting
comprehensive healthcare reforms and public health initiatives.
While others countries climb steadily. Notable progress also
seen in China and Poland.
'''

text_ax = plt.subplot(main_gs[0, 1])
text_ax.text(-0.24, 0.50, text, fontsize=14, ha='left', va='center',color='black')
text_ax.tick_params(length=0, width=0)
text_ax.set_facecolor('none')
text_ax.set_xticklabels([])
text_ax.set_yticklabels([])
text_ax.spines['top'].set_visible(False)
text_ax.spines['bottom'].set_visible(False)
text_ax.spines['left'].set_visible(False)
text_ax.spines['right'].set_visible(False) 

# Filter the GDP data for the selected countries and calculate growth percentage
gdp_selected = gdp_current_df[gdp_current_df['Country Name'].isin(selected_countries)].copy()
gdp_selected.loc[:, 'Growth_2000_2020'] = ((gdp_selected['2020'] - gdp_selected['2000']) / gdp_selected['2000']) * 100
gdp_growth_percentage = gdp_selected[['Country Name', 'Growth_2000_2020']]

# Visualization - Pie Chart for GDP Growth
ax5 = fig.add_subplot(main_gs[1, 1])
ax5.pie(gdp_growth_percentage['Growth_2000_2020'], labels=gdp_growth_percentage['Country Name'], autopct='%1.1f%%', labeldistance=1.15, wedgeprops = { 'linewidth' : 1, 'edgecolor' : 'white' })
ax5.set_title('GDP Growth %')
ax5.axis('off')

# Text - Pie Chart
text = '''
The pie chart provides a visual representation of the comparative
GDP  growth percentages among the selection  of countries. It 
delineates the proportionate contribution of each country to the
aggregate growth measured. China commands the majority with
61.3% of the growth, depicted in a prominent green sector.

Germany's economy is represented by a 14.5% share, marked in
purple, indicating the second-largest contribution. The orange
segment, accounting for 12.1%, corresponds to Canada. Singapore
and Australia are represented by smaller wedges, in blue and red,
constituting 5.5% and 4.5% of the growth, respectively. 
'''
text_ax = plt.subplot(main_gs[1, 0])
text_ax.text(-0.18,0.50, text, fontsize=14, ha='left', va='center', color='black')
text_ax.tick_params(length=0, width=0)
text_ax.set_facecolor('none')
text_ax.set_xticklabels([])
text_ax.set_yticklabels([])
text_ax.spines['top'].set_visible(False)
text_ax.spines['bottom'].set_visible(False)
text_ax.spines['left'].set_visible(False)
text_ax.spines['right'].set_visible(False) 
 
# Visualization - Exports (Horizontal Bar Graph)
ax7 = fig.add_subplot(main_gs[2, 0])
plot_horizontal_bar_chart(exports_pivot, 'Exports', ax7, colors_palette)


# Text - Exports (Horizental Bar Graph)
text = '''
The chart tracks China's remarkable growth in exports,
showing its development into a leading global exporter,
a change likely fueled by significant advancements in
manufacturing and technology.

Germany's consistent export figures, paired with its strong
health sector, suggest a stable and prosperous economy.
Australia's  graph demonstrates  a spirited and variable
export market,  pointing to an economy  that is adaptive
and responsive to the global trade environment. Overall,
this  visualization presents a straightforward view of each
country's export trends, highlighting their individual
economic strengths and positions within the global market.
'''

text_ax = plt.subplot(main_gs[2, 1])
text_ax.text(-0.24, 0.50, text, fontsize=15, ha='left', va='center',color='black')
text_ax.tick_params(length=0, width=0)
text_ax.set_facecolor('none')
text_ax.set_xticklabels([])
text_ax.set_yticklabels([])
text_ax.spines['top'].set_visible(False)
text_ax.spines['bottom'].set_visible(False)
text_ax.spines['left'].set_visible(False)
text_ax.spines['right'].set_visible(False) 


 
# Visualization - GDP Growth (Bar Chart)
ax9 = fig.add_subplot(main_gs[2, 2])
for i, country in enumerate(selected_countries):
    country_data = gdp_growth_pivot[gdp_growth_pivot['Country Name'] == country]
    ax9.bar(country_data['Year'], country_data['GDP Growth'], color=colors_palette[i], label=country, width=0.15, align='center')
ax9.set_title('GDP Growth (2000-2015)')
ax9.legend(fontsize='small')
ax9.grid(True)

# Text - GDP Growth (Bar Chart)
text = '''
A comprehensive analysis of global GDP growth patterns
unveils the sweeping dimensions of China's economic
resurgence, marked by some years that have registered
breathtaking growth rates. These  remarkable peaks in
China's GDP  growth signify  extraordinary episodes of
economic expansion that have significantly shaped the
global economic landscape. Germany, renowned for its
economic stability punctuated by occasional spurts of
growth. Its capacity to maintain a sturdy economic found-
ation while also experiencing intermittent bursts of
expansion underscoresits vital role in bolstering global
economic dynamics.

Furthermore, Australia and  Canada,  with their consistent
growth trajectories, contribute their threads to this rich
fabric of global economic vitality.Meanwhile, Singapore's
strategic economic management adding to overall complexity
of global economic development.
'''

text_ax = plt.subplot(main_gs[1, 2])
text_ax.text(-0.20,0.50, text, fontsize=15, ha='left', va='center', color='black')
text_ax.tick_params(length=0, width=0)
text_ax.set_facecolor('none')
text_ax.set_xticklabels([])
text_ax.set_yticklabels([])
text_ax.spines['top'].set_visible(False)
text_ax.spines['bottom'].set_visible(False)
text_ax.spines['left'].set_visible(False)
text_ax.spines['right'].set_visible(False) 


# Save the figure
plt.savefig('22087011.png', dpi=300)