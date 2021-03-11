from finance.models import StockReturn,StockCorrelation
import pandas as pd

# Create your tests here.
def unique(list1):
    unique_list= []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def get_labels(stock_name):
    """Return labels."""
    obj = StockReturn.objects.get(ticker=stock_name)
    df = pd.read_json(obj.data)
    df.dropna(axis=0,inplace=True)
    df['Month'] = df.index.month
    labels = df['Month'].tolist()
    return labels

def get_chart_data(stock_name):
    """Return data points for the stock."""
    obj = StockReturn.objects.get(ticker=stock_name)
    df = pd.read_json(obj.data)
    df.dropna(axis=0,inplace=True)
    data = df['Cumulative'].tolist()
    return data

def two_lists_to_x_y_values(list_1,list_2):
    """Returns two list within a list with x and y values"""
    data_scatter=[]
    for a,b in zip(list_1,list_2):
        data_scatter.append({"x":a,"y":b})
    return data_scatter

def get_scatter_chart_data():
    """Returns the returns for the BIN index formatted for scatter graph."""
    obj = StockCorrelation.objects.get(ticker='BIN')
    #Get the return series for the BIN index
    df_bin = pd.read_json(obj.dataset)
    df_bin.dropna(axis=0,inplace=True)
    df_bin.columns=["Weight","Index Price","Index Returns","Slope Line"]
    bin_data = df_bin["Index Returns"].tolist()
    slope_data = df_bin["Slope Line"].tolist()
    #Get the return index for SPY
    df_spy = pd.read_json(obj.dataset_index)
    df_spy.dropna(axis=0,inplace=True)
    spy_data = df_spy["Returns"].tolist()
    dataset_bin_spy= two_lists_to_x_y_values(bin_data,spy_data)
    dataset_bin_slope = two_lists_to_x_y_values(bin_data,slope_data)
    return dataset_bin_spy, dataset_bin_slope
