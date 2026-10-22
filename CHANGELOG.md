# Changelog

## v6.2 — 22 October 2026 (tested update)

- Added an empirical **current-extension directional percentile** alongside the multiple in the optional table, e.g. `1.64× (P63.4)`.
- Ranks positive extensions against preceding **positive** observations; negative extensions are ranked by **absolute magnitude** against preceding negative observations.
- Uses the selected rolling or cumulative prior-bar comparison window, excludes the current bar, and applies midpoint ranking to exact ties.
- Maintains sorted comparison data in either **standard-deviation** or **empirical-percentile** highlight mode.
- Leaves the 21-prior-bar registration rule, MA/ADR/ATR calculations, highlight thresholds, colour settings and alert conditions unchanged.
- User confirmed the v6.2 indicator working correctly in TradingView. This report does not independently certify every market/timeframe.

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
