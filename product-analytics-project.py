import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Loading cohort data...")
df = pd.read_csv(
    r'C:\Users\Mane Chaitanya\Desktop\product-analytics-project\data\processed\cohort_data.csv'
)

print(f"✅ Loaded {len(df)} rows")
print(df.head())

# Pivot for heatmap
pivot = df.pivot_table(
    index='cohort_month',
    columns='month_number',
    values='retention_pct'
)
pivot.columns = [f'M{int(c)}' for c in pivot.columns]

# Plot
fig, ax = plt.subplots(figsize=(16, 8))
sns.heatmap(
    pivot,
    annot=True,
    fmt='.0f',
    cmap='RdYlGn',
    linewidths=0.5,
    linecolor='white',
    vmin=0,
    vmax=100,
    ax=ax
)
ax.set_title(
    'Customer Cohort Retention Rate (%)',
    fontsize=16,
    fontweight='bold'
)
ax.set_xlabel('Months Since First Purchase')
ax.set_ylabel('Cohort Month')

plt.tight_layout()
plt.savefig(
    r'C:\Users\Mane Chaitanya\Desktop\product-analytics-project\data\processed\cohort_heatmap.png',
    dpi=150,
    bbox_inches='tight'
)
print("✅ Heatmap saved!")
plt.show()