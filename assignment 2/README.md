# Optional: log-scale version (recommended)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df_all["peak_market_cap"], bins=80, log=True)
axes[0].set_title("The Graveyard (All Tokens) – Log Count")
axes[0].set_xlabel("Peak Market Cap ($)")
axes[0].set_ylabel("Count (log)")

axes[1].hist(df_survivors["peak_market_cap"], bins=40, log=True)
axes[1].set_title("Survivors (Top 1%) – Log Count")
axes[1].set_xlabel("Peak Market Cap ($)")
axes[1].set_ylabel("Count (log)")

plt.tight_layout()
plt.show()
=== Survivorship Bias Check ===

Total tokens (df_all):        10,000
Survivors (top 1%):              100
Top 1% cutoff:          $9,134,108.54

Mean Peak Market Cap (ALL):       $1,936,723.29
Mean Peak Market Cap (SURVIVORS): $16,549,004.95

Bias factor (Survivors / All): 8.54
