# Contributing

Contributions, reproducible bug reports and additional reference tests are welcome.

## Reporting an issue

Please include: symbol and exchange, chart timeframe, session and data source, whether the price series is adjusted, and whether you're using standard candles. Include the configured **MA/range lengths**, ADR/ATR choice, **rolling or cumulative**, lookback target, sample minimum, SD/percentile choice, early-life averaging setting, closed-bar setting and screenshot if possible.

For compiler problems, paste the **exact Pine Editor error and line number**. For statistical discrepancies, provide a small OHLC example or an anonymised series of ADR/MA multiples, the preceding history, the intended output and the observed result.

Avoid uploading trading credentials, personal portfolio details or other non-public data.

## Proposing a change

1. Keep the canonical script in `OutsizedAlpha_ADR_Extension_v6_1.pine` unless renaming is an explicit part of the change.
2. Preserve the source copyright and **MPL-2.0** notice.
3. Explain the statistical effect and whether the change is **calculation**, **signal**, **presentation** or **performance** related.
4. Avoid allowing the current candle into its own historical reference distribution.
5. Check **21-prior-bar registration**, partial histories with large user-selected lookbacks, strictly positive/negative sample separation, minimum qualifying samples, constant-series SD, rolling eviction, percentile nearest-rank, candle colour, and table positions.
6. Run `python -m unittest discover -s tests -v`. This checks an **independent reference calculation**, not the Pine runtime.
7. Test the candidate script in TradingView's native Pine Editor and report whether compilation and visual/alert checks succeeded. A secondary language runtime cannot certify native Pine compatibility.
8. Update the README and CHANGELOG when user-facing behaviour changes.

## Scope and licensing

Contributions should be original, reviewable source. No proprietary indicator code or protected TradingView account information should be committed. The project is licensed under the Mozilla Public License 2.0.
