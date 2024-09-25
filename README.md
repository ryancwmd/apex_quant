# Software Assessment
My implementation of the software assessment uses a class based approach that has a base engine
and extends the engine to create new trading strategies. The design is extremely simple and does not support buying
more than one stock at a time. My implementation is only functional with strategies that can be implemented with the
 following basic procedure:

    iterate through idx 0-n, 
    for each index i, perform some processing
    generate a bullish, bearish, or none signal
        buy or sell and store data

To demonstrate, I have included two demo trading strategies, the Simple Moving Average specified in the requirements
and a Moving Average Convergence Divergence strategy. 

Specific implementation is commented throughout the code, but the engine structure follows the procedure I described
previously.

## Structure
~/assets 
* Contains the forex pair data retrieved from yfinance, the risk management profile, and any risk assessment logs.
* To edit risk management attributes simply open the json file and change the values as desired.

~/src
* Contains source code.

    /data_pipeline
    * Contains the pipeline that retrieves the data from yfinance.
    * Is created separately in case the user wants to retrieve data but not process it or create a whole class to do so.

    /backtesting_engine
    * Contains the backtesting engine and the trading strategies I have implemented

## Running
To run the engine, simple navigate to the ~/src directory in a terminal and execute 

    python main.py

Command line arguments that can be provided can be found by running:

    python main.py --help

You can find the default values in the `read_clargs()` function in main.py. 

