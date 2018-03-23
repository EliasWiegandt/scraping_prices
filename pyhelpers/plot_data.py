import os
import pandas as pd
import matplotlib.pyplot as plt

base_dir = "H:/HBS Data/Crawlers/pricebot/pricedata/"

name = "prices_20180323.csv"
df = pd.read_csv(open(base_dir + name), sep=",", index_col=0, header=0)

retailer = "Elgiganten"
product = 'KG49EBI40'

retailers = df['retailer'].unique()
products = df['product'].unique()

# for product in products:
#     df_product = df[df['product'] == product]
#     df_product = df_product.pivot(
#         index='date', columns='retailer', values='price')
#     axes = df_product.plot(use_index=True, title=product)
#     axes.set_xticklabels(df_product.index)
#     plt.draw()

# plt.show()

for retailer in retailers:
    df_retailer = df[df['retailer'] == retailer]
    df_retailer = df_retailer.pivot(
        index='date', columns='product', values='price')
    axes = df_retailer.plot(use_index=True, title=retailer)
    axes.set_xticklabels(df_retailer.index)
    plt.draw()

plt.show()
