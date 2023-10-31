#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# - Your analysis here
# 1.A significant conclusion that can be drawn from this dataset is that schools that spend more per student achieve lower test results and passing percentages. 
# This fact is mitigated by the fact that charter schools, on average, spent significantly less per student than District schools, and had fewer students. This could be an area for future study.
# 2. An extremely obvious conclusion that is linked to my last one, is that charter schools perform better on every metric, including average spent per student. The causes for this performance should certainly be studied further.
# ---

# Dependencies and Setup
import pandas as pd

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv("PyCitySchools\Resources\schools_complete.csv")
student_data = pd.read_csv("PyCitySchools\Resources\students_complete.csv")

# Combine the data into a single dataset.  
school_data_combined_df = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_combined_df.head()


# ## District Summary


# Calculate the total number of unique schools
school_count = school_data.school_name.nunique()
school_count




student_count = school_data["size"].sum()
student_count


# # Calculate the total number of students
# student_count = school_data["size"].sum()
# student_count


# Calculate the total budget
total_budget = school_data["budget"].sum()
total_budget

# Calculate the average (mean) math score
average_math_score = student_data['math_score'].mean()
average_math_score


# Calculate the average (mean) reading score
average_reading_score = student_data['reading_score'].mean()
average_reading_score

# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = school_data_combined_df[(school_data_combined_df["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage


# Calculate the percentage of students who passed reading (hint: look at how the math percentage was calculated)  
passing_reading_count = school_data_combined_df[(school_data_combined_df["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_reading_count / float(student_count) * 100
passing_reading_percentage


# Use the following to calculate the percentage of students that passed math and reading
passing_math_reading_count = school_data_combined_df[
    (school_data_combined_df["math_score"] >= 70) & (school_data_combined_df["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(student_count) * 100
overall_passing_rate



# Create a high-level snapshot of the district's key metrics in a DataFrame
summary = [school_count, student_count, total_budget, average_math_score, average_reading_score, passing_math_percentage, passing_reading_percentage, overall_passing_rate]
           
district_summary=pd.DataFrame([summary],columns=['Total Schools', 'Total Students','Total Budget','Average Math Score','Average Reading Score','Passing Math Percentage',
                                               'Passing Reading Percentage','Overall Passing Rate'])
# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)
district_summary['Average Math Score']=district_summary['Average Math Score'].map("{:,.2f}".format)
district_summary['Average Reading Score']=district_summary['Average Reading Score'].map("{:,.2f}".format)
district_summary['Passing Math Percentage']=district_summary['Passing Math Percentage'].map("{:,.2f}%".format)
district_summary['Passing Reading Percentage']=district_summary['Passing Reading Percentage'].map("{:,.2f}%".format)
district_summary['Overall Passing Rate']=district_summary['Overall Passing Rate'].map("{:,.2f}%".format)
# Display the DataFrame
district_summary


# ## School Summary



per_school=school_data_combined_df.groupby('school_name').first()
per_school=per_school[['type','size','budget']]


# ### Use the code provided to select all of the school types
# 
# school_types = per_school['type']
# school_types



school_types =per_school['type'] 


# Calculate the total student count per school
per_school_counts = per_school['size']



# Calculate the total school budget and per capita spending per school
per_school_budget = per_school['budget']
per_school_capita = (per_school_budget/per_school_counts)


# Calculate the average test scores per school
school_scores=school_data_combined_df.groupby(['school_name'])
per_school_math = school_scores['math_score'].mean()
per_school_reading =school_scores['reading_score'].mean()


# Calculate the number of students per school with math scores of 70 or higher


students_passing_math = school_data_combined_df.loc[(school_data_combined_df['math_score']>=70)]
school_students_passing_math = students_passing_math.groupby('school_name').size()


# Calculate the number of students per school with reading scores of 70 or higher
students_passing_reading = school_data_combined_df.loc[(school_data_combined_df['reading_score']>=70)]
school_students_passing_reading = students_passing_reading.groupby('school_name',as_index=True).size()


# Use the provided code to calculate the number of students per school that passed both math and reading with scores of 70 or higher

students_passing_math_and_reading = school_data_combined_df[
    (school_data_combined_df["reading_score"] >= 70) & (school_data_combined_df["math_score"] >= 70)]
school_students_passing_math_and_reading = students_passing_math_and_reading.groupby(["school_name"]).size()


# Use the provided code to calculate the passing rates
per_school_passing_math = school_students_passing_math / per_school_counts * 100
per_school_passing_reading = school_students_passing_reading / per_school_counts * 100
overall_passing_rate = school_students_passing_math_and_reading / per_school_counts * 100


# Create a DataFrame called `per_school_summary` with columns for the calculations above.
per_school_summary=pd.concat({'School Type':school_types,'Total Students':per_school_counts, 'Total School Budget':per_school_budget, 'Per Student Budget':per_school_capita, 
                'Average Math Score':per_school_math, 'Average Reading Score':per_school_reading, '% Passing Math':per_school_passing_math, 
                         '% Passing Reading':per_school_passing_reading, '% Overall Passing':overall_passing_rate},axis=1)

per_school_summary.index.name=None
# Formatting
per_school_summary["Total School Budget"] = per_school_summary["Total School Budget"].map("${:,.2f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("${:,.2f}".format)
# Display the DataFrame
per_school_summary


# ## Highest-Performing Schools (by % Overall Passing)


# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
top_schools = per_school_summary.sort_values(by='% Overall Passing',ascending=False)
top_schools.head(5)


# ## Bottom Performing Schools (By % Overall Passing)


# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
bottom_schools = per_school_summary.sort_values(by='% Overall Passing',ascending=True)
bottom_schools.head(5)


# ## Math Scores by Grade



# Use the code provided to separate the data by grade
ninth_graders = school_data_combined_df[(school_data_combined_df["grade"] == "9th")]
tenth_graders = school_data_combined_df[(school_data_combined_df["grade"] == "10th")]
eleventh_graders = school_data_combined_df[(school_data_combined_df["grade"] == "11th")]
twelfth_graders = school_data_combined_df[(school_data_combined_df["grade"] == "12th")]

# Group by `school_name` and take the mean of the `math_score` column for each.
ninth_grader_math_scores = ninth_graders.groupby('school_name').mean('math_score')[['math_score']].rename(columns={'math_score':'9th'})
tenth_grader_math_scores = tenth_graders.groupby('school_name').mean('math_score')[['math_score']].rename(columns={'math_score':'10th'})
eleventh_grader_math_scores = eleventh_graders.groupby('school_name').mean('math_score')[['math_score']].rename(columns={'math_score':'11th'})
twelfth_grader_math_scores = twelfth_graders.groupby('school_name').mean('math_score')[['math_score']].rename(columns={'math_score':'12th'})
# Combine each of the scores above into single DataFrame called `math_scores_by_grade`
math_scores_by_grade = pd.concat([ninth_grader_math_scores,tenth_grader_math_scores,eleventh_grader_math_scores,twelfth_grader_math_scores],axis=1)

# Minor data wrangling
math_scores_by_grade.index.name = None

# Display the DataFrame
math_scores_by_grade


# ## Reading Score by Grade 


# Use the code provided to separate the data by grade
ninth_graders = school_data_combined_df[(school_data_combined_df["grade"] == "9th")]
tenth_graders = school_data_combined_df[(school_data_combined_df["grade"] == "10th")]
eleventh_graders = school_data_combined_df[(school_data_combined_df["grade"] == "11th")]
twelfth_graders = school_data_combined_df[(school_data_combined_df["grade"] == "12th")]

# Group by `school_name` and take the mean of the the `reading_score` column for each.
ninth_grader_reading_scores = ninth_graders.groupby('school_name').mean('reading_score')[['reading_score']].rename(columns={'reading_score':'9th'})
tenth_grader_reading_scores = tenth_graders.groupby('school_name').mean('reading_score')[['reading_score']].rename(columns={'reading_score':'10th'})
eleventh_grader_reading_scores = eleventh_graders.groupby('school_name').mean('reading_score')[['reading_score']].rename(columns={'reading_score':'11th'})
twelfth_grader_reading_scores = twelfth_graders.groupby('school_name').mean('reading_score')[['reading_score']].rename(columns={'reading_score':'12th'})

# Combine each of the scores above into single DataFrame called `reading_scores_by_grade`
reading_scores_by_grade = pd.concat([ninth_grader_reading_scores,tenth_grader_reading_scores,eleventh_grader_reading_scores,twelfth_grader_reading_scores],axis=1)

# Minor data wrangling
#reading_scores_by_grade = reading_scores_by_grade.rename(columns={"reading_score":'9th','reading_score':'10th'})
reading_scores_by_grade.index.name = None

# Display the DataFrame
reading_scores_by_grade


# ## Scores by School Spending

# Establish the bins 
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]


# Create a copy of the school summary since it has the "Per Student Budget" 
school_spending_df = per_school_summary.copy()


# Use `pd.cut` to categorize spending based on the bins.
school_spending_df["Spending Ranges (Per Student)"] = pd.cut(school_spending_df['Per Student Budget'].replace("[$,]","",regex=True).astype(float), spending_bins, labels=labels)
school_spending_df



#  Calculate averages for the desired columns. 
spending_math_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"])["Average Math Score"].mean()
spending_reading_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"])["Average Reading Score"].mean()
spending_passing_math = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Passing Math"].mean()
spending_passing_reading = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Passing Reading"].mean()
overall_passing_spending = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Overall Passing"].mean()



# Assemble into DataFrame
spending_summary = pd.concat([spending_math_scores,spending_reading_scores,spending_passing_math,spending_passing_reading,overall_passing_spending],axis=1)

# Display results
spending_summary


# ## Scores by School Size



# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]



# Categorize the spending based on the bins
# Use `pd.cut` on the "Total Students" column of the `per_school_summary` DataFrame.

per_school_summary["School Size"] = pd.cut(per_school_summary['Total Students'], size_bins,labels=labels)
per_school_summary



# Calculate averages for the desired columns. 
size_math_scores = per_school_summary.groupby(["School Size"])["Average Math Score"].mean()
size_reading_scores = per_school_summary.groupby(["School Size"])["Average Reading Score"].mean()
size_passing_math = per_school_summary.groupby(["School Size"])["% Passing Math"].mean()
size_passing_reading = per_school_summary.groupby(["School Size"])["% Passing Reading"].mean()
size_overall_passing = per_school_summary.groupby(["School Size"])["% Overall Passing"].mean()



# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`
size_summary = pd.concat([size_math_scores,size_reading_scores,size_passing_math,size_passing_reading,size_overall_passing],axis=1) 

# Display results
size_summary


# ## Scores by School Type


# Group the per_school_summary DataFrame by "School Type" and average the results.
average_math_score_by_type = per_school_summary.groupby(["School Type"])["Average Math Score"].mean()
average_reading_score_by_type = per_school_summary.groupby(["School Type"])["Average Reading Score"].mean()
average_percent_passing_math_by_type = per_school_summary.groupby(["School Type"])["% Passing Math"].mean()
average_percent_passing_reading_by_type = per_school_summary.groupby(["School Type"])["% Passing Reading"].mean()
average_percent_overall_passing_by_type = per_school_summary.groupby(["School Type"])["% Overall Passing"].mean()



# Assemble the new data by type into a DataFrame called `type_summary`
type_summary = pd.concat([average_math_score_by_type,average_reading_score_by_type,average_percent_passing_math_by_type,average_percent_passing_reading_by_type,average_percent_overall_passing_by_type],axis=1)

# Display results
type_summary




