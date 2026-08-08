import matplotlib.pyplot as plt

def plot_equity(equity_curve):
    plt.figure(figsize = (12, 6))
    plt.plot(equity_curve)
    plt.title("Equity Curve")
    plt.xlabel("Bar")
    plt.ylabel("Equity")
    plt.grid(True)

    plt.show()

def plot_drawdown(drawdown_series):
    plt.figure(figsize = (12, 6))
    plt.plot(drawdown_series)
    plt.title("Underwater Chart")
    plt.xlabel("Bar")
    plt.ylabel("Drawdowns")
    plt.grid(True)

    plt.show()