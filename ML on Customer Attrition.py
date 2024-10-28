# -*- coding: utf-8 -*-
"""Data Science Final Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1l7YnpkhDzcCwQYaF6llDSk2WscE8H_Zy

**Introduction/Background**

Customer attrition is one of the biggest expenditures of any organization. Customer churn otherwise known as customer attrition or customer turnover is the percentage of customers that stopped using your company's product or service within a specified timeframe.
For instance, if you began the year with 500 customers but later ended with 480 customers, the percentage of customers that left would be 4%. If we could figure out why a customer leaves and when they leave with reasonable accuracy, it would immensely help the organization to strategize their retention initiatives manifold.

In this project, we aim to find the likelihood of a customer leaving the organization, the key indicators of churn as well as the retention strategies that can be implemented to avert this problem.


**Business Understanding**

The objective of this project aims to throw more light on the churn rate of the customer, the reasons for churn and possible ways to avert more customers from churning and improve the customer attrition. It is important to uunerstand the constumer behaviour which may lead to this outcome, identifying key indicators from our data.

**Data Understanding**

The data for this project is in a csv format. The following describes the columns present in the data.

Gender -- Whether the customer is a male or a female

SeniorCitizen -- Whether a customer is a senior citizen or not

Partner -- Whether the customer has a partner or not (Yes, No)

Dependents -- Whether the customer has dependents or not (Yes, No)

Tenure -- Number of months the customer has stayed with the company

Phone Service -- Whether the customer has a phone service or not (Yes, No)

MultipleLines -- Whether the customer has multiple lines or not

InternetService -- Customer's internet service provider (DSL, Fiber Optic, No)

OnlineSecurity -- Whether the customer has online security or not (Yes, No, No Internet)

OnlineBackup -- Whether the customer has online backup or not (Yes, No, No Internet)

DeviceProtection -- Whether the customer has device protection or not (Yes, No, No internet service)

TechSupport -- Whether the customer has tech support or not (Yes, No, No internet)

StreamingTV -- Whether the customer has streaming TV or not (Yes, No, No internet service)

StreamingMovies -- Whether the customer has streaming movies or not (Yes, No, No Internet service)

Contract -- The contract term of the customer (Month-to-Month, One year, Two year)

PaperlessBilling -- Whether the customer has paperless billing or not (Yes, No)

Payment Method -- The customer's payment method (Electronic check, mailed check, Bank transfer(automatic), Credit card(automatic))

MonthlyCharges -- The amount charged to the customer monthly

TotalCharges -- The total amount charged to the customer

Churn -- Whether the customer churned or not (Yes or No)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import cufflinks as cf
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN
from sklearn.pipeline import Pipeline
import matplotlib.ticker as mtick
from sklearn.compose import ColumnTransformer
from sklearn.neural_network import MLPClassifier
import pickle
import warnings
import os
import glob
from scipy import stats

warnings.filterwarnings('ignore')

# Load the dataset
file_path = '/content/LP2_Telco-churn-last-2000.csv'
data = pd.read_csv(file_path)

data.head()

# Listing the columns in the data
data.columns.to_list()

data.shape

data.info()

"""From the above information, it appears tenure,MonthlyCharges, TotalCharges columns are objet, hence we will have to turn them into a numeric variable, preferably a float"""

# Change the TotalCharges column into a float
data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce').astype(np.float64)
data['MonthlyCharges'] = pd.to_numeric(data['MonthlyCharges'], errors='coerce').astype(np.float64)
data['tenure'] = pd.to_numeric(data['tenure'], errors='coerce').astype(np.float64)

#investigating missing valyues
data.isna().sum()

"""After changing the data type of the TotalCharges column, we observe that there are 3 missing values. This may not have been discovered if the data type remained as an object

Ususally, we would replace the missing values with the mean of the values of the column, but since the number of missing values are only eleven, we will go ahead and remove those rows from our data set
"""

# Remove rows with missing values
data = data.dropna()

data.info()

"""Now, our data frame size reduces in rows from 2043 to 2040"""

# checking for unique values
data.nunique()

"""Univariate analysis"""

# Plotting Senior Citizen Proportion

senior_citizen_counts = data['SeniorCitizen'].value_counts()
labels = ['Not Senior Citizen', 'Senior Citizen']
colors = ['#008fd5', '#fc4f30']
explode = (0, 0.1)
plt.pie(senior_citizen_counts, labels=labels, explode=explode, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.title('Senior Citizen Proportion')
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
plt.ylabel('')
plt.show()

"""The pie chart tells us the customers are predominantly non-senior citizens. Senior citizens only accounts for 16.8% of the customers"""

#Plotting the proportion of multiple lines

multiple_lines_counts = data['MultipleLines'].value_counts()
labels = ['No', 'Yes', 'No phone service']
colors = ['#008fd5', '#fc4f30', '#6d904f']
explode = (0.03, 0.03, 0.1)
plt.pie(multiple_lines_counts, labels=labels, explode=explode, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.title('Multiple Lines Proportion')
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
plt.ylabel('')
plt.show()

"""48.3% of customers do not have multiple lines, whereas, 40.9% have multiple lines. This may be becuase these customers have dependents who may also have phone lines registered in the customers' name.

Also we see that 10.8% of customers do not have a any phone service. We might have to investigate further at some ponint to find out if this group of customers use just internet, without a phone line. Either fiber optic or DSL which do not necessarily require a phone line.
"""

# Plotting Gender Proportion

gender_counts = data['gender'].value_counts()
labels = ['Female', 'Male']
colors = ['#008fd5', '#fc4f30']
explode = (0, 0.05)
plt.pie(gender_counts, labels=labels, explode=explode, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.title('Gender Proportion')
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
plt.ylabel('')
plt.show()

"""It appears the ration of Female to Male is balanced"""

# Plotting the proportion of Internet Service Users

internet_service_counts = data['InternetService'].value_counts()
labels = ['DSL', 'Fiber optic', 'No']
colors = ['#008fd5', '#fc4f30','#6d904f']
explode = (0.03, 0.03, 0.1)

percentages = round(internet_service_counts/internet_service_counts.sum()*100, 2).astype(str) + '%'

ax = internet_service_counts.plot(kind='bar', color=colors, edgecolor='black', linewidth=1.2,
                                  figsize=(8,6), rot=0)
ax.set_title('Internet Service Proportion', fontsize=14)
ax.set_xlabel('Internet Service Type', fontsize=12)
ax.set_ylabel('Number of Customers', fontsize=12)
ax.set_ylim(0, 5000)

for i, p in enumerate(ax.patches):
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy()
    ax.annotate(f'{height}\n{percentages[i]}', (x + 0.15, y + height + 200))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.show()

"""905 representing 44.3% of customers use Fiber optic internet service, while customers who use DSL and those wthout (No) internet service are 34.7% and 21.0% respectively."""

# Plotting the ratio of customer churn

customer_churn_counts = data['Churn'].value_counts()
labels = ['No', 'Yes']
colors = ['#008fd5', '#fc4f30']
explode = (0.03, 0.03)

percentages = round(customer_churn_counts/customer_churn_counts.sum()*100, 2).astype(str) + '%'

ax = customer_churn_counts.plot(kind='bar', color=colors, edgecolor='black', linewidth=1.2,
                                  figsize=(8,6), rot=0)
ax.set_title('Customer Churn Proportion', fontsize=14)
ax.set_xlabel('Customer Churn', fontsize=12)
ax.set_ylabel('Number of Customers', fontsize=12)
ax.set_ylim(0, 7000)

for i, p in enumerate(ax.patches):
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy()
    ax.annotate(f'{height}\n{percentages[i]}', (x + 0.15, y + height + 200))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.show()

"""The churn distibtion plot shows the proportion of customers who churn vs those who do not. __1487__ customers representing __72.79%__ stayed and 556 representing 27.21% of the customers churned."""

# Numeric variables
num_vars = ['tenure', 'MonthlyCharges', 'TotalCharges']

plt.figure(figsize=(15,5))
for i, var in enumerate(num_vars):
    plt.subplot(1,3,i+1)
    sns.histplot(data[var], kde=True)
    plt.xlabel(var)

plt.show()

"""From the above plots, we can see that the variables "Tenure" and "MonthlyCharges" have a relatively normal distribution, while the variable "TotalCharges" has a skewed distribution.

###Bivariate Analysis
"""

# Create a boxplot of MonthlyCharges by Churn status
sns.boxplot(x='Churn', y='MonthlyCharges', data=data)
plt.show()

# select relevant columns for pair plot
columns = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Churn']

# create pair plot using seaborn
sns.pairplot(data[columns], hue='Churn', corner=True)

# Add title to plot
plt.suptitle('Pairplot of data Dataset', fontsize=12)

plt.show()

"""**From this plot, we observe three key things;**

1. There is a higher proportion of customers who do not churn.

2. Those who churn pay about the same amount in monthly charges as those that do not churn.

3. Customers who do not churn stay longer on the network (i.e longer tenure)
"""

# Create a boxplot of TotalCharges by Churn status
sns.boxplot(x='Churn', y='TotalCharges', data=data, flierprops={'markerfacecolor': 'magenta', 'marker': 'o'})
plt.title('Churn by Total Charges')

plt.show()

"""Our churn box plot shows us two distinctive boxplots. i.e for csutomers who churned and those that did not churn. Those that churned average about 1000 in total charges while those who remained averaged about almost 2000, twice as much as those who churned. Suprisingly, some outliers, who churned, indicated by he purple dots, had much higher total charges.Since they appear to be high paying customers, it would be a good idea to offer them customized products/service in order to retain them."""

# Correlation matrix between monthly charges and total charges
sns.scatterplot(data=data, x='MonthlyCharges', y='TotalCharges')
plt.title('Monthly Charges vs. Total Charges')
plt.show()

"""Here, we see that the more customers pay on a monthly basis, the more they accrue in total charges. Whereas customers who pay less per month, also tend to pay less over time."""

# Convert Churn column to binary encoding
data['Churn_bin'] = data['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

# Bar chart of churn rate by internet service type
sns.barplot(data=data, x='InternetService', y='Churn_bin')
plt.title('Churn Rate by Internet Service Type')
plt.show()

"""From this bar plot, we see that the group of customers with the most churn are those who use the fiber optic internet service. Now this may not be the actual/only reason they churn but it gives us an idea of some possible issue they may need adressing. About 40% of the those with internet service is a huge number proportion which calls for some attention.

##Multivariate Analysis
"""

# ##
corr = data[['tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen']].corr()
sns.heatmap(corr, cmap='coolwarm', annot=True)
plt.show()

"""In the multivariate analysis, Total Charges has a stronger correlation with tenure than the Monthly charges. From the above heatmap, we observe that there is a higher correlation between the "tenure" and the "TotalCharges" variables of up to 83%. This indicates that the longer a customer stays with the network, the more total charges they accrue."""

# Pairwise scatterplot of monthly charges, total charges, and tenure
sns.pairplot(data[['MonthlyCharges', 'TotalCharges', 'tenure']])
plt.show()

"""The series of suubplots show how Monthly charges and Total Charges compare to each other against the Tenure of the cutomers."""

# Boxplot of tenure by gender
sns.boxplot(data=data, x='gender', y='tenure', hue='Churn')
plt.title('Tenure by Gender')
plt.show()

"""The duration of stay on the network is just about the same for both female and male. Also, there is o indication that either gender churned mmore than the other

**Research Questions and hypothesis Testing**
1. What categories of contracts generate the most revenue?
2. How much is generated from customers with internet service?
3. Do high paying customers use Stream TV or/and Stream movies?
4.How much do senior citizens and non-senior citizens pays on a monthly basis?
"""

# Calculate mean monthly charges and total charges for each contract type
contract_revenue = data.groupby('Contract').agg({'MonthlyCharges':'mean', 'TotalCharges':'mean'}).reset_index()

# Create bar plots to visualize the mean monthly charges and total charges for each contract type
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
sns.barplot(data=contract_revenue, x='Contract', y='MonthlyCharges', ax=ax[0])
ax[0].set_xlabel('Contract Type')
ax[0].set_ylabel('Mean Monthly Charges')
ax[0].set_title('Mean Monthly Charges by Contract Type')

sns.barplot(data=contract_revenue, x='Contract', y='TotalCharges', ax=ax[1])
ax[1].set_xlabel('Contract Type')
ax[1].set_ylabel('Mean Total Charges')
ax[1].set_title('Mean Total Charges by Contract Type')

plt.show()

# Calculate total revenue generated by customers with internet service
internet_service_revenue = data[data['InternetService'] != 'No'][['MonthlyCharges', 'InternetService']].groupby('InternetService').agg('count') * data[data['InternetService'] != 'No'][['MonthlyCharges', 'InternetService']].groupby('InternetService').agg('mean')
internet_service_revenue.columns = ['TotalRevenue']

# Plot the total revenue generated by customers with internet service
sns.barplot(data=internet_service_revenue, x=internet_service_revenue.index, y='TotalRevenue')
plt.xlabel('Internet Service Type')
plt.ylabel('Revenue Generated')
plt.title('Total Revenue Generated From Monthly Charges by Customers with Internet Service')
plt.show()

# Define high-paying customers as those who pay more than the median monthly charges
median_monthly_charges = data['MonthlyCharges'].median()
data['HighPaying'] = data['MonthlyCharges'] > median_monthly_charges
#data.head()
# Create a crosstab between HighPaying and StreamingTV columns
streaming_crosstab = pd.crosstab(data['HighPaying'], [data['StreamingTV']])
# Create a stacked bar chart
streaming_crosstab.plot(kind='bar', stacked=False)

# Add labels and title
plt.xlabel('High-Paying')
plt.ylabel('Number of Customers')
plt.title('Usage of Stream TV by High-Paying Customers')

# Show the plot
plt.show()

# Identify senior and non-senior customers
senior_citizens = data[data['SeniorCitizen'] == 1]
non_senior_citizens = data[data['SeniorCitizen'] == 0]

# Calculate the mean monthly charges for senior citizens and non-senior citizens
mean_monthly_charges_senior = senior_citizens['MonthlyCharges'].mean()
mean_monthly_charges_non_senior = non_senior_citizens['MonthlyCharges'].mean()

# Create a bar plot
x_labels = ['Senior Citizens', 'Non-Senior Citizens']
y_values = [mean_monthly_charges_senior, mean_monthly_charges_non_senior]

plt.bar(x_labels, y_values, color=['skyblue', 'lightgreen'])
plt.xlabel('Customer Type')
plt.ylabel('Average Monthly Charges')
plt.title('Average Monthly Charges by Customer Type')
plt.show()

"""### Hypothesis Testing

### Hypothesis 1: Contract Categories and Revenue


**Null Hypothesis (H0):** The revenue generated by different contract categories (Month-to-month, One year, Two year) is the same.

**Alternative Hypothesis (H1):** The revenue generated by at least one contract category is significantly different from the others.
"""

# Hypothesis 1 Testing
# ANOVA to test if there is a significant difference in revenue across contract categories
anova_result = stats.f_oneway(data[data['Contract'] == 'Month-to-month']['MonthlyCharges'],
                              data[data['Contract'] == 'One year']['MonthlyCharges'],
                              data[data['Contract'] == 'Two year']['MonthlyCharges'])

print(f"F-statistic: {anova_result.statistic}, P-value: {anova_result.pvalue}")

"""F-statistic: 12.29

P-value: 4.97e-06

## **Interpretation:**

1. The F-statistic is quite large, which suggests that there is significant variability in the revenue across different contract categories.

2. The P-value is very small (less than 0.05), which means that we can reject the null hypothesis.

# **Conclusion: **

 There is a significant difference in the revenue generated by different contract categories (Month-to-month, One year, Two year). At least one contract category generates significantly different revenue compared to the others.

### **Hypothesis 2: Internet Service and Revenue**


**Null Hypothesis (H0):** There is no difference in the revenue generated between customers with internet service and those without.
**Alternative Hypothesis (H1):** Customers with internet service generate significantly more revenue than those without.
"""

# Hypothesis 2 Testing
# T-test to compare the revenue between customers with and without internet service
internet_customers = data[data['InternetService'] != 'No']['MonthlyCharges']
no_internet_customers = data[data['InternetService'] == 'No']['MonthlyCharges']
t_stat_internet, p_value_internet = stats.ttest_ind(internet_customers, no_internet_customers)


print(f"T-statistic: {t_stat_internet}, P-value: {p_value_internet}")

data['Churn']

"""T-statistic: 51.59

P-value: 0.0

## **Interpretation:**

1. The T-statistic is very high, indicating a strong difference between the two groups (customers with internet service vs. those without).

2. The P-value is effectively zero, which means we can reject the null hypothesis.

# **Conclusion:**
Customers with internet service generate significantly more revenue than those without internet service.

### **Hypothesis 3: High Paying Customers and Streaming Services**


**Null Hypothesis (H0):** High paying customers do not use Stream TV or Stream Movies more than lower-paying customers.

**Alternative Hypothesis (H1):** High paying customers are more likely to use Stream TV and/or Stream Movies.
"""

# Hypothesis 3 Testing
# Define high-paying customers as those with MonthlyCharges above the median
median_monthly_charge = data['MonthlyCharges'].median()
high_paying_customers = data[data['MonthlyCharges'] > median_monthly_charge]

# Chi-square test to determine if high paying customers use Stream TV or/and Stream Movies more often
contingency_table_tv = pd.crosstab(high_paying_customers['StreamingTV'], high_paying_customers['StreamingMovies'])
chi2_stat, p_value_tv, dof, expected = stats.chi2_contingency(contingency_table_tv)

print(f"Chi-square Statistic: {chi2_stat}, P-value: {p_value_tv}")

"""Chi-square Statistic: 109.09

P-value: 1.55e-25

## **Interpretation:**

1. The Chi-square statistic is large, suggesting a strong association between being a high-paying customer and using streaming services (Stream TV and/or Stream Movies).
2. The P-value is extremely small, much less than 0.05, so we can reject the null hypothesis.

## Conclusion:

High-paying customers are significantly more likely to use Stream TV and/or Stream Movies compared to lower-paying customers.

### **Hypothesis 4: Monthly Charges for Senior Citizens vs. Non-Senior Citizens**


**Null Hypothesis (H0):** There is no significant difference in the monthly payments between senior citizens and non-senior citizens.

**Alternative Hypothesis (H1):** There is a significant difference in the monthly payments between senior citizens and non-senior citizens.
"""

# Hypothesis 4 Testing
# T-test to compare the monthly payments between senior and non-senior citizens
senior_charges = data[data['SeniorCitizen'] == 1]['MonthlyCharges']
nonsenior_charges = data[data['SeniorCitizen'] == 0]['MonthlyCharges']
t_stat_senior, p_value_senior = stats.ttest_ind(senior_charges, nonsenior_charges)



print(f"T-statistic: {t_stat_senior}, P-value: {p_value_senior}")

"""T-statistic: 10.24

P-value: 5.17e-24

## **Interpretation:**

1. The T-statistic is large, indicating a significant difference between the monthly charges of senior citizens and non-senior citizens.

2. The P-value is very small, much less than 0.05, so we can reject the null hypothesis.

## Conclusion:

There is a significant difference in the monthly payments between senior citizens and non-senior citizens. Senior citizens and non-senior citizens pay different amounts on a monthly basis.
"""

data.head()

# Convert 'Churn' to numerical values (target variable)
data['Churn'] = data['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)
data = data.drop('customerID', axis=1)
data.info()

data.corr()

non_numeric_cols = data.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

# Convert boolean columns to integers
for col in non_numeric_cols:
    if data[col].dtype == 'bool':
        data[col] = data[col].astype(int)

# Apply Label Encoding to categorical data
for col in non_numeric_cols:
    if data[col].dtype == 'object' or data[col].dtype.name == 'category':
        data[col] = pd.Categorical(data[col]).codes

# Compute the correlation matrix
corr_matrix = data.corr()

# Extract the correlation of all variables with the 'Churn' variable
churn_corr = corr_matrix['Churn'].sort_values(ascending=False)

# Plotting the correlation of all features with 'Churn'
plt.figure(figsize=(10, 8))
sns.barplot(x=churn_corr.index, y=churn_corr.values, palette='coolwarm')
plt.xticks(rotation=90)
plt.title('Correlation of Features with Churn')
plt.xlabel('Features')
plt.ylabel('Correlation with Churn')
plt.tight_layout()
plt.show()

"""from the correlation graph above
Contract,
tenure,
OnlineSecurity,
TechSupport,
TotalCharges
shows strong negative correlation with the churn

PaperlessBilling,
MonthlyCharges;
SeniorCitizen,
PaymentMethod also shows strong positive correlation

Hence these will be used as the features for training the model
"""

selected_features = [
    'Contract',
    'tenure',
    'OnlineSecurity',
    'TechSupport',
    'TotalCharges',
    'PaperlessBilling',
    'MonthlyCharges',
    'SeniorCitizen',
    'PaymentMethod',

]

X = data[selected_features]  # Now 'Churn' is excluded
y = data['Churn']

# Plot the distribution of churn values
plt.figure(figsize=(8, 6))
sns.countplot(x='Churn', data=data, palette='viridis')
plt.title('Distribution of Churn Values')
plt.xlabel('Churn')
plt.ylabel('Count')
plt.show()

"""Given the significant imbalance between the churn values, we applied SMOTE to increase the representation of the minority class (churned customers) in the dataset."""

# Extract the features and target variable
X = data[selected_features]
y = data['Churn']  # Assuming 'Churn' is the target variable

# Split the data into training and test sets before applying SMOTE
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


# Apply SMOTE to the training data to balance it
smote = SMOTE(random_state=42)
X_train_feature, y_train_feature = smote.fit_resample(X_train, y_train)

# Assuming 'X_train_balanced', 'y_train_balanced', 'X_test', and 'y_test' are available from previous steps


models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Random Forest': RandomForestClassifier(random_state=42),
    'Support Vector Machine': SVC(random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42),
    'Neural Network': MLPClassifier(hidden_layer_sizes=(64, 64), max_iter=1000, random_state=42)
}


best_model_name = None
best_model = None
best_score = 0.0

for name, model in models.items():
    # Create a pipeline with scaling and the model
    pipeline = Pipeline([
        ('scaler', StandardScaler()),  # Scaling the features
        ('model', model)
    ])

    # Train the model
    pipeline.fit(X_train_feature, y_train_feature)

    # Evaluate the model
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"{name} Accuracy: {accuracy:.4f}")

    # Check if this model is the best so far
    if accuracy > best_score:
        best_score = accuracy
        best_model_name = name
        best_model = pipeline

# Save the best-performing model as a pickle file
if best_model is not None:
    with open(f'best_model_{best_model_name}.pkl', 'wb') as file:
        pickle.dump(best_model, file)

    print(f"The best-performing model, {best_model_name}, has been saved as 'best_model_{best_model_name}.pkl' with an accuracy of {best_score:.4f}.")

"""From our model after using the SMOTE sampling, we had the Random Forest and Gradient Boosting giving us a higher accuracy value of about 76%. We then decided to check other approaches for the most efficient model.



"""

# Check cross-validation scores for the best model
cross_val_scores = cross_val_score(best_model, X_train_feature, y_train_feature, cv=10)
print(f"Cross-validation scores: {cross_val_scores}")
print(f"Average cross-validation score: {cross_val_scores.mean():.4f}")

"""We applied the cross-validation scores to the models and noticed that the average score was around 81.6%. From here, we decided to apply other sampling techniques to further see which model best work for our data set. We used the ADASYN method of sampling."""

adasyn = ADASYN(random_state=42)
X_res, y_res = adasyn.fit_resample(X, y)

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Random Forest': RandomForestClassifier(random_state=42),
    'Support Vector Machine': SVC(random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42),
    'Neural Network': MLPClassifier(hidden_layer_sizes=(64, 64), max_iter=1000, random_state=42)
}


best_model_name = None
best_model = None
best_score = 0.0

for name, model in models.items():

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', model)
    ])

    # Train the model
    pipeline.fit(X_res, y_res)

    # Evaluate the model
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"{name} Accuracy: {accuracy:.4f}")

    # Check if this model is the best so far
    if accuracy > best_score:
        best_score = accuracy
        best_model_name = name
        best_model = pipeline

# Step 3: Save the best-performing model as a pickle file
if best_model is not None:
    with open(f'best_model_{best_model_name}.pkl', 'wb') as file:
        pickle.dump(best_model, file)

    print(f"The best-performing model, {best_model_name}, has been saved as 'best_model_{best_model_name}.pkl' with an accuracy of {best_score:.4f}.")

"""Finally, we realised the Random Forest model was truly the best model as it appears to have 99.75% accuracy in the ADASYN sampling method.

# CONCLUSIONS AND INFERENCE
Our analysis of customer churn in the telecommunications industry has revealed crucial insights for improving customer retention. Through comprehensive data analysis and machine learning modeling, we identified key factors influencing churn, with the Random Forest model emerging as the most effective predictor. Contract type, tenure, and value-added services strongly correlate with customer retention, while paperless billing and higher monthly charges are associated with increased churn risk. Notably, fiber optic internet users showed the highest churn propensity, highlighting a critical area for service improvement. Our findings revealed that the Random Forest model consistently outperformed other models, achieving an impressive accuracy of 99.75% with the initial dataset and 75.98% after applying ADASYN sampling.

These findings provide a clear roadmap for strategic action. By focusing on enhancing service quality, particularly in fiber optic offerings, developing targeted retention strategies for high-value customers, and tailoring services based on contract types and customer demographics, the company can significantly reduce churn rates. This data-driven approach to customer retention positions the company to maintain a competitive edge in the evolving telecommunications landscape, ultimately enhancing customer lifetime value and overall business performance.
"""