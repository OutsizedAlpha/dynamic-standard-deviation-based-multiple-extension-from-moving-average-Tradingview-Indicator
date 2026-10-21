# Changelog

## v6.1 — 21 October 2026 (initial public release)

- Released the **OutsizedAlpha ADR / MA Extension** Pine Script® v6 indicator.
- Added rolling/cumulative historical statistics with separate positive and downside-magnitude distributions.
- Added standard-deviation thresholds of **+1, +2 and +3 SD** and exact nearest-rank **80th/90th/95th/99th percentiles**.
- Colour price candles directly, without plotting a mismatched statistical oscillator on the price axis.
- Thresholds use **prior observations only**, not the bar currently being evaluated.
- Added a registration gate of **21 preceding chart bars**. When the user's configured lookback is larger than available history, register the available bars until the target lookback is reached.
- The chosen lookback is not capped at 504: any permitted configured value, **21–50,000**, is respected.
- Added optional adaptive early-life moving average and range calculations for short-history securities, including recent IPOs.
- Added a statistics table with **all nine TradingView anchor positions** and text sizes **Tiny, Small, Standard, Large, Extra large**.
- Kept four condition alerts for upside/downside extremes and first qualifying bars.
- Includes reference statistical contract tests; these do not compile the Pine indicator in TradingView.

The initial public release imports an existing source file developed and evaluated outside this repository. It does not retroactively recreate earlier development commits.
