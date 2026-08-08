def total_return(equity_curve):
    if not equity_curve:
        return 0.0

    return (equity_curve[-1] / equity_curve[0]) - 1.0

def drawdown_series(equity_curve):
    if not equity_curve:
        return []

    peak = equity_curve[0]
    drawdowns = []

    for equity in equity_curve:
        peak = max(peak, equity)
        drawdowns.append((equity - peak) / peak)

    return drawdowns

def maximum_drawdown(equity_curve):
    drawdowns = drawdown_series(equity_curve)

    if not drawdowns:
        return 0.0

    return min(drawdowns)