import requests
from prettytable import PrettyTable

# Get your free API key from https://www.alphavantage.co/support/#api-key
API_KEY = 'YOUXAXZH9YA24XDDFC7'
BASE_URL = 'https://www.alphavantage.co/query'


class StockPortfolio:
    def __init__(self):
        self.portfolio = {}

    def add_stock(self, symbol, shares):
        """Add stock to the portfolio"""
        if symbol in self.portfolio:
            self.portfolio[symbol]['shares'] += shares
        else:
            self.portfolio[symbol] = {'shares': shares}

    def remove_stock(self, symbol):
        """Remove stock from the portfolio"""
        if symbol in self.portfolio:
            del self.portfolio[symbol]
        else:
            print(f"Stock {symbol} not found in the portfolio.")

    def fetch_stock_price(self, symbol):
        """Fetch the current stock price from Alpha Vantage API"""
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': '5min',
            'apikey': API_KEY
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        # Check if the response contains valid data
        if 'Time Series (5min)' not in data:
            print(f"Error fetching data for {symbol}.")
            return None

        latest_time = list(data['Time Series (5min)'].keys())[0]
        stock_price = float(data['Time Series (5min)'][latest_time]['4. close'])
        return stock_price

    def display_portfolio(self):
        """Display the current stock portfolio with real-time prices"""
        table = PrettyTable()
        table.field_names = ["Symbol", "Shares", "Current Price (USD)", "Total Value (USD)"]

        total_portfolio_value = 0.0

        for symbol, details in self.portfolio.items():
            shares = details['shares']
            stock_price = self.fetch_stock_price(symbol)

            if stock_price is not None:
                total_value = shares * stock_price
                total_portfolio_value += total_value
                table.add_row([symbol, shares, f"${stock_price:.2f}", f"${total_value:.2f}"])
            else:
                table.add_row([symbol, shares, "N/A", "N/A"])

        print(table)
        print(f"Total Portfolio Value: ${total_portfolio_value:.2f}")

    def portfolio_summary(self):
        """Display summary of all stocks"""
        if not self.portfolio:
            print("Your portfolio is empty.")
        else:
            self.display_portfolio()


# Example usage
if __name__ == '__main__':
    portfolio = StockPortfolio()

    while True:
        print("\n1. Add Stock\n2. Remove Stock\n3. View Portfolio\n4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol (e.g., AAPL, TSLA): ").upper()
            shares = int(input("Enter number of shares: "))
            portfolio.add_stock(symbol, shares)

        elif choice == '2':
            symbol = input("Enter stock symbol to remove: ").upper()
            portfolio.remove_stock(symbol)

        elif choice == '3':
            portfolio.portfolio_summary()

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice! Please select a valid option.")
