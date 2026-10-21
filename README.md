# OutsizedAlpha ADR / MA Extension

**Dynamic, standard-deviation-based price extension from a moving average — for TradingView (Pine Script® v6).**

Colour candles when the share price is unusually far above (or optionally below) its moving average **relative to its own typical candle range and historical extension distribution**. Compare against **+1, +2 or +3 standard deviations**, or empirical **80th, 90th, 95th or 99th percentiles**. An optional compact statistics table can occupy any of TradingView's nine table anchors.

[**Pine source**](./OutsizedAlpha_ADR_Extension_v6_1.pine) · [Changelog](./CHANGELOG.md) · [Contributing](./CONTRIBUTING.md) · [Licence](./LICENSE) · [Reference tests](./tests/test_reference_statistics.py)

> **Standalone research indicator.** This project is separate from the [OutsizedAlpha DeMARK indicator](https://github.com/OutsizedAlpha/DeMark-S-C-Tradingview-Indicator). Price extension is not itself evidence of a likely reversal or a trading recommendation.

## Quick installation

1. Open a chart in [TradingView](https://www.tradingview.com/).
2. Open **Pine Editor**, create a new indicator and copy the entire [`OutsizedAlpha_ADR_Extension_v6_1.pine` source](./OutsizedAlpha_ADR_Extension_v6_1.pine).
3. Save the script and choose **Add to chart**.
4. Open **Settings → Inputs** to select your preferred historical comparison, threshold, colours and table position.
5. Start with a standard **daily OHLC** chart for daily-range interpretation.

The indicator is an **overlay**, not a separate oscillator pane. It calls `barcolor()` to colour qualifying price candles without plotting ADR multiples onto the share-price axis. As a result, the original statistical plot lines are absent from the Style menu.

## How the extension multiple works

For each chart candle:

```text
Average candle range = SMA(high − low, Range length)
Moving average       = SMA(close, MA length)
ADR multiple         = (close − moving average) / average candle range
```

For example, a close of $112, a 50-bar moving average of $100 and a 14-bar average high–low range of $4 yield **+3.00 ADR multiples**. A result of −2.00 means price is two average ranges below the moving average.

The configurable range normaliser can instead be **ATR (true range)**, which uses Wilder's smoothed true range and includes gaps. It is **ADR only on a daily chart**; on intraday or weekly charts the same calculation applies to that chart's bars.

### Comparison against historical extensions

The script builds **separate statistical distributions** for each direction:

- **Upside:** historical ADR multiples strictly greater than zero.
- **Downside:** absolute magnitudes of historical ADR multiples strictly less than zero.
- Exact zero and unavailable values do not enter either directional distribution.
- The current candle is **not** included in the sample used to judge that candle.

For the chosen historical sample, a standard-deviation threshold is:

```text
Threshold = mean(qualifying extensions)
          + selected SD multiplier × population standard deviation
```

The mean and SD are calculated using a numerically stable incremental Welford calculation. The SD multiplier can be **1, 2 or 3**. A candle is highlighted at or above its configured threshold (inclusive equality). These are distribution-based extension thresholds, **not** normal-distribution tail probabilities.

Alternatively, the indicator uses an **exact nearest-rank empirical percentile** of that direction's qualifying observations. For example, the 95th-percentile setting uses the sorted observed values, not a Gaussian approximation.

A high reading can signal **strong trend momentum**, **extended price action**, or both. It is not necessarily an overbought sell signal. Rising volatility can reduce an ADR multiple even if price continues rising.

## Automatic historical registration (especially for IPOs)

Your configured **Rolling lookback (bars)** is the **target comparison window**, *not a minimum required to start*. The configured value can be **21 to 50,000 bars**. It is **not hard-coded to 504**.

On the first candle with **21 preceding chart bars**, the indicator may begin producing statistics and highlights. If fewer historical bars than your target are available, it uses all the preceding available bars; the sample grows automatically until it reaches the target.

| Configured lookback | Prior chart bars available | Bars in statistical window |
| ---: | ---: | ---: |
| 1,000 | 15 | **Not registered** (fewer than 21) |
| 1,000 | 21 | 21 |
| 1,000 | 75 | 75 |
| 1,000 | 504 | 504 |
| 1,000 | 1,500 | 1,000 |
| 2,000 | 1,500 | 1,500 |

There is a **second, independent minimum:** each directional distribution needs at least **two qualifying observations** by default (configurable to a higher number). Thus, 21 prior bars can be registered without yet having enough *positive* or *negative* extensions to estimate the corresponding threshold.

**Cumulative mode** uses all preceding loaded valid observations instead of expiring observations beyond a rolling lookback; the 21-bar minimum still applies.

### Early-life averages

The option **IPO: use available bars until full MA / range lengths** is on by default. If only 25 chart candles exist while the MA length is 50, the moving average temporarily uses the 25 available closes. The range average similarly uses available candles until its selected period is reached; early ATR is an average of observed true ranges, then transitions to normal Wilder ATR.

This makes the 21-prior-bar registration useful for newly listed companies, rather than waiting for a full 50-bar MA first. **Early-life shorter-period calculations are not mathematically identical to the mature 50-bar indicator.**

> **Bars versus days:** the threshold is **21 prior chart candles**, not 21 calendar days. On a daily chart it corresponds to 21 trading sessions; on a weekly chart it is 21 weeks, and on an hourly chart it is 21 hourly candles.

## Input reference

### 01 · Price Extension

| Input | Default | Meaning |
| --- | --- | --- |
| Moving average length | 50 | SMA of close used as the trend reference |
| ADR / ATR length | 14 | Number of chart candles used for the range normaliser |
| IPO: use available bars until full MA / range lengths | On | Partial-history averages before full periods exist |
| Range normaliser | ADR (high − low) | Can select ATR (true range), including gaps |

### 02 · Historical Statistics

| Input | Default | Meaning |
| --- | --- | --- |
| Historical comparison | Rolling | Rolling or cumulative comparison history |
| Rolling lookback (bars) | 252 | Target window, **21–50,000**; automatically shrinks for insufficient history |
| Minimum qualifying observations per side | 2 | The upside and downside distributions qualify separately |

### 03 · Candle Highlight Thresholds

| Input | Default | Meaning |
| --- | --- | --- |
| Threshold method | Standard deviation | SD thresholds or empirical percentiles |
| Upside: at least | +1 SD | **+1, +2, +3 SD**; a minimum threshold, not an exclusive band |
| Upside percentile | 95th | **80th / 90th / 95th / 99th**; active when percentile mode selected |
| Also colour extreme downside candles | Off | Enables an independent downside threshold |
| Downside magnitude: at least | +1 SD | Uses the distribution of *absolute negative* extensions |
| Downside magnitude percentile | 95th | Selectable downside percentile |
| Colour only confirmed (closed) candles | On | Avoid provisional intrabar highlights |

### 04 · Appearance

| Input | Default | Meaning |
| --- | --- | --- |
| Upside extension candle | Blue | Price-candle colour for positive extreme |
| Downside extension candle | Orange | Price-candle colour for negative extreme (if enabled) |
| Show compact statistics table | Off | Show or hide the readout |
| Table: vertical position | Top | Top, Middle, Bottom |
| Table: horizontal position | Right | Left, Centre, Right |
| Table: text size | Tiny | Tiny, Small, Standard, Large, Extra large |

The table has **nine positions**:

| | Left | Centre | Right |
| --- | --- | --- | --- |
| **Top** | Top left | Top centre | Top right |
| **Middle** | Middle left | Middle centre | Middle right |
| **Bottom** | Bottom left | Bottom centre | Bottom right |

These are selectable **anchors**. Pine tables cannot be freely dragged pixel-by-pixel with a mouse. Text sizes map to TradingView's `tiny`, `small`, `normal`, `large` and `huge` settings.

### Compact table readouts

The optional table reports current ADR/MA multiple, the **effective** moving-average/range lengths, configured lookback, **registered prior bars**, separate directional qualifying-observation counts, and current upside/downside thresholds. The threshold/status can be unavailable even after registration if that side has too few qualifying observations.

## Worked threshold example

Suppose the positive-extension distribution has a historical mean of **1.60 ADRs** and a standard deviation of **0.80 ADRs**.

| Selected minimum | Required multiple | A current +3.00 ADR reading |
| --- | ---: | --- |
| +1 SD | 2.40 | **Blue** |
| +2 SD | 3.20 | Not highlighted |
| +3 SD | 4.00 | Not highlighted |

This example illustrates the selection logic only; the indicator computes its own historical values for the chart in use.

## Alerts

The Pine file defines four independent TradingView alert conditions:

1. **ADR upside extension — qualifying bar**
2. **ADR upside extension — first qualifying bar**
3. **ADR downside extension — qualifying bar**
4. **ADR downside extension — first qualifying bar**

The first-qualifying-bar condition fires at the first qualifying reading after a previous non-qualifying reading. Downside alerts depend on enabling downside highlighting. Alert timing follows the TradingView alert frequency and the **Colour only confirmed (closed) candles** setting. These are notifications, not broker orders.

## Implementation boundaries and cautions

- **Price-chart colours only:** there are no legacy `plot()`/`hline()` statistical traces. Use the optional table to inspect current thresholds.
- **Prior-bar sampling:** the current observation never sets its own comparison threshold. Historical signals can still vary when loaded history, input settings, chart type or exchange adjustments change.
- **IPO registration ≠ statistical reliability:** two observations define a population SD but are a very small sample. Consider increasing **Minimum qualifying observations per side** where robustness matters.
- **Population SD and empirical percentiles are different concepts:** a +2 SD threshold should not be interpreted mechanically as a 97.7th percentile.
- **Different volatility regimes:** short-window ADR/ATR and long-window extension distributions adapt at different speeds. A rapidly increasing denominator can lower the normalised extension without a price reversal.
- **Very long windows:** higher `lookbackBars` values consume more Pine history/storage and computation. The configured input permits up to 50,000; TradingView platform resource limits still apply.
- **Non-daily timeframes:** the indicator operates in current chart bars; the term ADR only means *daily* on daily candles.
- **Validation:** the author reports the chart indicator working, but the public Python tests below check reference mathematical rules; they do **not** compile the Pine source or certify realtime behaviour, backtest returns or execution characteristics.
- **No profit guarantee:** this is an analytical research tool, not a complete trading system or investment recommendation.

## Testing the statistical contract

A small standard-library Python test suite documents the independent mathematical expectations, including the 21-bar registration gate, user lookbacks larger than available history, partial IPO histories, prior-bar-only calculations, rolling expiry, cumulative history, nearest-rank percentiles, downside magnitudes and minimum qualifying samples.

```bash
python -m unittest discover -s tests -v
```

These **14 reference tests** are intentionally independent of the Pine implementation. They passed when prepared for this release. A passing result is **not** evidence of native TradingView compilation or statistical identity on every OHLC series.

For code changes, use [CONTRIBUTING.md](./CONTRIBUTING.md) and record the affected formulas, new fixtures and native Pine Editor test results.

## Further references

- [TradingView Pine Script documentation](https://www.tradingview.com/pine-script-docs/)
- [TradingView tables](https://www.tradingview.com/pine-script-docs/visuals/tables/)
- [TradingView bar colouring](https://www.tradingview.com/pine-script-docs/visuals/bar-coloring/)
- [Mozilla Public License 2.0](https://www.mozilla.org/MPL/2.0/)

## Licence and attribution

© **OutsizedAlpha**. Distributed under the **Mozilla Public License 2.0**; see [LICENSE](./LICENSE). Keep the source licence and attribution notices in modified/distributed source files.

**TradingView and Pine Script are names of their respective owners. This project is not affiliated with or endorsed by TradingView.**

*For chart research and education. Not financial advice.*
