# 1. Loading Data and preprocessing:

import pandas as pd

df = pd.read_csv('House-pricing-prediction/House-prising-prediction/raw_housing_price.csv', index_col=0)
zip_obj = zip(list(df.columns), ['usable_area', 'land_area', 'bedroom', 'bathroom', 'legal',
                                       'date', 'id', 'address', 'price'])
dict_obj = dict(zip_obj)
df.rename(dict_obj, axis=1, inplace=True)
print(df['address'][:5])

# 2. Data Inspection:


# 3. Finding & Handling Missing Data:
# 4. Data Cleaning and Preprocessing:
# 5. Data Visualization:
# 6. Univariate Analysis:
# 7. Multivariate Analysis:
# 8. Feature Engineering:
# 9. Statistical Analysis:
# 10. Outlier Detection: