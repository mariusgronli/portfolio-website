from django_cron import CronJobBase, Schedule
import yfinance as yf
import numpy as np
from finance.models import Stock,Detail,DisplaySr,DisplayMo,StockReturn,StockCorrelation
from django.utils import timezone
from scipy import stats


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        #Retrive a list of all available tickers
        for ticker in Stock.objects.all():
            y_stock = ticker.ticker
            #Retrive data for each ticker in the Stock
            #and format for to be input in the StockAnalysis clas
            stock_df = yf.download(tickers=y_stock,period="6mo",interval="1d")
            stock_df.drop(labels=["Open","High","Low","Close","Volume"],axis=1,inplace=True)

            #Calculate the
            #Calculate the expected_return
            stock_df['returns'] = stock_df.pct_change(1)
            daily_return = stock_df['returns'].mean()
            annual_return = round(((daily_return+1)**252-1)*100,2)


            #Calculate the standard deviation
            daily_std = np.std(stock_df['returns'])
            annual_std = round(np.sqrt(252)*daily_std*100,2)

            #Calculate the expected_return
            sharpe = round(annual_return/annual_std,2)

            #Calculate the Momentumscore
            # Make a list of consecutive numbers
            x = np.arange(len(stock_df["Adj Close"]))
            # Get logs
            log_ts = np.log(stock_df["Adj Close"])
            # Calculate regression values
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, log_ts)
            # Annualize percent
            annualized_slope = (np.power(np.exp(slope), 252) - 1) * 100
            #Adjust for fitness
            score = round(annualized_slope * (r_value ** 2),2)

            ###############################
            #### POPULATE THE DATABASE ####
            ###############################

            nytt_obj, created = Detail.objects.get_or_create(analyzed_stock_id=y_stock)
            nytt_obj.expected_return = annual_return
            nytt_obj.volatility = annual_std
            nytt_obj.sharperatio = sharpe
            nytt_obj.momentum = score
            nytt_obj.created_date = timezone.now()
            nytt_obj.slug =y_stock
            nytt_obj.save()

            #########################################
            #### POPULATE THE momentum highlight ####
            #########################################

            top_momentum = Detail.objects.order_by('-momentum')[1]
            nytt_obj_to, created_to = DisplayMo.objects.get_or_create(pk=1)
            nytt_obj_to.momentum_score = top_momentum.momentum
            nytt_obj_to.analyzed_stock = top_momentum.analyzed_stock
            nytt_obj_to.created_date = top_momentum.created_date
            nytt_obj_to.save()

            #########################################
            #### POPULATE THE sharpe highlight   ####
            #########################################

            top_sharpe = Detail.objects.order_by('-sharperatio')[0]
            nytt_obj_tre, created_tre = DisplaySr.objects.get_or_create(pk=1)
            nytt_obj_tre.sharperatio = top_sharpe.sharperatio
            nytt_obj_tre.analyzed_stock = top_sharpe.analyzed_stock
            nytt_obj_tre.created_date = top_sharpe.created_date
            nytt_obj_tre.save()

            ###############################################
            #### Save the cumulative returns for graph ####
            ###############################################

            stock_df['Cumulative']= (1+stock_df['returns']).cumprod()
            obj, created = StockReturn.objects.get_or_create(ticker=y_stock)
            obj.ticker = y_stock
            obj.data = stock_df.to_json()
            obj.save()

        #Create BIN(Battery Index) and Spy for correlation
        raw_data = yf.download(tickers=["tsla","enr","enph","pcrfy","jci","alb","sqm"],period="6mo",interval="1d")
        raw_data.drop(labels=["Open","High","Low","Close","Volume"],axis=1,inplace=True)
        raw_data.dropna(inplace=True)

        raw_data_spy = yf.download(tickers='SPY',period="6mo",interval="1d")
        raw_data_spy.drop(labels=["Open","High","Low","Close","Volume"],axis=1,inplace=True)
        raw_data_spy.dropna(inplace=True)

        raw_data["Weight"]=float(1/7)
        raw_data["Index Price"]=raw_data["Adj Close"]["TSLA"]*raw_data["Weight"]+raw_data["Adj Close"]["ENR"]*raw_data["Weight"]+raw_data["Adj Close"]["ENPH"]*raw_data["Weight"]+raw_data["Adj Close"]["PCRFY"]*raw_data["Weight"]+raw_data["Adj Close"]["JCI"]*raw_data["Weight"]+raw_data["Adj Close"]["ALB"]*raw_data["Weight"]+raw_data["Adj Close"]["SQM"]*raw_data["Weight"]
        raw_data["Index Returns"]=raw_data["Index Price"].pct_change(1)


        raw_data_spy["Returns"]=raw_data_spy["Adj Close"].pct_change(1)

        raw_data.dropna(inplace=True)
        raw_data.drop(labels=["Adj Close"],axis=1,inplace=True)
        raw_data_spy.dropna(inplace=True)

        battery_index = raw_data["Index Returns"]
        spy = raw_data_spy["Returns"]

        slope, intercept, r, p, stderr = stats.linregress(battery_index, spy)
        raw_data["Slope Line"]=raw_data["Index Returns"]*slope+intercept

        #Store the information in the database
        obj_cor, created = StockCorrelation.objects.get_or_create(ticker='BIN')
        obj_cor.dataset = raw_data.to_json()
        obj_cor.ticker_index = 'SPY'
        obj_cor.dataset_index = raw_data_spy.to_json()
        obj_cor.slope = slope
        obj_cor.intercept = intercept
        obj_cor.stderr = stderr
        obj_cor.save()
