import pandas as pd
import os
from tabulate import tabulate
from detect_framework import *
import statistics


df = pd.read_table('../top_apps.txt', sep='|')

# Use the sample_outputs folder to figure that out which APKs were actually downloaded
file_names = os.listdir("../sample_outputs/")
is_package_downloaded = []
for index, row in df.iterrows():
    if row['Package Name'] + '.txt' in file_names:
        is_package_downloaded.append(1)
    else:
        is_package_downloaded.append(0)

# Add a column that indicates that we actually downloaded the APK
df['Downloaded'] = is_package_downloaded
print(df['Downloaded'].value_counts())

print('The following files were additional APK downloads that were not in top downloaded apps list:')
for file in file_names:
    if file[:-4] not in df['Package Name'].tolist():
        print(file)

# To make it easier, remove all apps that were not downloaded from the dataframe
df = df[df['Downloaded'] == 1]

category_percentages_df = pd.DataFrame({'Percentage': df.groupby('Category').size() / len(df),
                                        'Count': df.groupby('Category').size()}).sort(columns='Count', ascending=0)
print('Categories by percentage:\n\n')
print(category_percentages_df.to_latex())


# Add a column to the dataframe that indicates which frameworks were detected
detected_apps_to_frameworks, detected_frameworks_to_apps = get_detected_frameworks_for_apps()
detected_frameworks_for_df = []
for index, row in df.iterrows():
    detected_frameworks_for_df.append(detected_apps_to_frameworks[row['Package Name']])

df['Frameworks'] = detected_frameworks_for_df
print tabulate(df, headers='keys', tablefmt='psql')

# Also create a separate dataframe for framework occurrences
frameworks = []
framework_counts = []
for framework_name, matching_apps in detected_frameworks_to_apps.iteritems():
    if len(matching_apps) > 0:
        frameworks.append(framework_name)
        framework_counts.append(len(matching_apps))

framework_count_df = pd.DataFrame({'Framework': frameworks, 'Count': framework_counts}, columns=['Framework', 'Count'])

#print tabulate(framework_count_df, headers='keys', tablefmt='psql')
print(framework_count_df.to_latex(index=False))

# Create a dataframe that sees how categories correlate to framework usage
category_to_framework_usage_dict_no_kotlin = {}
category_to_kotlin_usage = {}

for index, row in df.iterrows():
    if len(row['Frameworks']) > 0 and 'kotlin' not in row['Frameworks']:
        if row['Category'] not in category_to_framework_usage_dict_no_kotlin:
            category_to_framework_usage_dict_no_kotlin[row['Category']] = 1
        else:
            category_to_framework_usage_dict_no_kotlin[row['Category']] += 1
    if 'kotlin' in row['Frameworks']:
        if row['Category'] not in category_to_kotlin_usage:
            category_to_kotlin_usage[row['Category']] = 1
        else:
            category_to_kotlin_usage[row['Category']] += 1


category_to_framework_usage_no_kotlin_df = pd.DataFrame(
    list(category_to_framework_usage_dict_no_kotlin.iteritems()),
    columns=['Category', 'Apps that used a framework']).sort(columns='Apps that used a framework', ascending=0)

category_to_kotlin_usage_df = pd.DataFrame(
    list(category_to_kotlin_usage.iteritems()),
    columns=['Category', 'Apps that used Kotlin']).sort(columns='Apps that used Kotlin', ascending=0)

#print category_to_framework_usage_no_kotlin_df.to_latex(index=False)
#print category_to_kotlin_usage_df.to_latex(index=False)

# Create a boxplot of app ratings by framework used
# The categories are Native/unkown, Kotlin, framework
framework_to_ratings_dict = {}
for fw in frameworks:
    framework_to_ratings_dict[fw] = []

framework_to_ratings_dict['native/unknown'] = []

print('------------------')
for framework_name, matching_apps in detected_frameworks_to_apps.iteritems():
    if len(matching_apps) > 0:
        for app in matching_apps:
            rating = df.loc[df['Package Name'] == app, 'Rating'].item()
            #print('RATING for ' + app + ' is ' + str(rating))
            framework_to_ratings_dict[framework_name].append(rating)

# We need to get the ratings for all native/unkown apps as a baseline
for index, row in df.iterrows():
    if len(row['Frameworks']) == 0:
        framework_to_ratings_dict['native/unknown'].append(row['Rating'])

# create a df from the dict
framework_to_ratings_df = pd.DataFrame(
    list(framework_to_ratings_dict.iteritems()),
    columns=['Framework', 'Ratings']).sort(columns='Ratings', ascending=0)

print tabulate(framework_to_ratings_df, headers='keys', tablefmt='psql')



average_ratings = []
total_ratings = []
standard_dev_ratings = []

for index, row in framework_to_ratings_df.iterrows():
    ratings_list = row['Ratings']
    total_ratings.append(len(ratings_list))
    average_ratings.append(sum(ratings_list) / len(ratings_list))
    if len(ratings_list) == 1:
        standard_dev_ratings.append(-1)
    else:
        standard_dev_ratings.append(statistics.stdev(ratings_list))

# for framework, ratings_list in framework_to_ratings_dict.iteritems():
#     total_ratings.append(len(ratings_list))
#     average_ratings.append(sum(ratings_list)/len(ratings_list))
#     if len(ratings_list) == 1:
#         standard_dev_ratings.append(-1)
#     else:
#         standard_dev_ratings.append(statistics.stdev(ratings_list))


#print(total_ratings)
#print(average_ratings)
#print(standard_dev_ratings)

framework_to_ratings_df['Total Ratings'] = total_ratings
framework_to_ratings_df['Average Rating'] = average_ratings
framework_to_ratings_df['Standard Deviation'] = standard_dev_ratings
print tabulate(framework_to_ratings_df, headers='keys', tablefmt='psql')
framework_to_ratings_df = framework_to_ratings_df.drop('Ratings', 1)
framework_to_ratings_df = framework_to_ratings_df.sort(columns='Total Ratings', ascending=0)
framework_to_ratings_df = framework_to_ratings_df.round(3)


print(framework_to_ratings_df.to_latex(index=False))
