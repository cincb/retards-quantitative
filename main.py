from queue import Queue
from data.loader import csvLoader
from data.data_handler import dataHandler
from execution.execution import executionSim
from portfolio.portfolio import Portfolio
from strategy.moving_average import movingAverageStrategy
from events.events import eventType, marketEvent, signalEvent, orderEvent, fillEvent
from performance.metrics import total_return, maximum_drawdown, drawdown_series
from performance.plots import plot_equity, plot_drawdown

def main():
    events = Queue()

    loader = csvLoader("data/sample_data.csv")
    data = loader.load()

    data_handler = dataHandler(data, events)

    print(len(data))
    print(data.head())

    strategy = movingAverageStrategy(
        event_queue = events,
        fast_period = 10,
        slow_period = 30
    )

    port = Portfolio(
        event_queue = events,
        init_cash = 100000,
        position_size = 100
    )

    execution = executionSim(
        event_queue = events,
        commission = 1.0,
        slippage_bps = 5
    )

    current_price = None

    while data_handler.has_next():
        data_handler.next()

        while not events.empty():
            event = events.get()

            match event.type:
                case eventType.MARKET:
                    current_price = event.close
                    strategy.on_market(event)

                case eventType.SIGNAL:
                    port.on_signal(event, current_price)

                case eventType.ORDER:
                    execution.execute(event, current_price)

                case eventType.FILL:
                    port.on_fill(event)

        port.update_equity(current_price)

    print("Cash:", port.cash)
    print("Realized PnL:", port.realized_pnl)
    print("Final Position:", port.position("AAPL"))
    print("Total Return:", total_return(port._equity_curve))
    print("Maximum Drawdown:", maximum_drawdown(port._equity_curve))

    plot_equity(port._equity_curve)
    plot_drawdown(drawdown_series(port._equity_curve))

if __name__ == "__main__":
    main()