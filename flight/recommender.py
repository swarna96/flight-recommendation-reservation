import pandas as pd
#Math functions, we'll only need the sqrt function so let's import only that
from math import sqrt
import numpy as np
class flightRecommender:
    

    def preprocessing(self, input_data,list_flight):

        df=pd.read_csv("E:/level 4 term 2/software project/dataset/skytrax-reviews-dataset-master/data/airline.csv")
        df=df[df['airline_name'].isin(list_flight)]
        df.drop(columns=['ground_service_rating','wifi_connectivity_rating'],inplace=True)
        df["overall_rating"]=df["overall_rating"].replace(np.NaN,df["overall_rating"].mean())
        df["seat_comfort_rating"]=df["seat_comfort_rating"].replace(np.NaN,df["seat_comfort_rating"].mean())
        df["cabin_staff_rating"]=df["cabin_staff_rating"].replace(np.NaN,df["cabin_staff_rating"].mean())
        df["food_beverages_rating"]=df["food_beverages_rating"].replace(np.NaN,df["food_beverages_rating"].mean())
        df["inflight_entertainment_rating"]=df["inflight_entertainment_rating"].replace(np.NaN,df["inflight_entertainment_rating"].mean())
        df["value_money_rating"]=df["value_money_rating"].replace(np.NaN,df["value_money_rating"].mean())

        user_df=pd.DataFrame(df)
        user_df['id']=df.groupby('author').ngroup()
        inputflights = pd.DataFrame(input_data)
        inputId = user_df[user_df['airline_name'].isin(inputflights['airline_name'].tolist())]
        user_df['flight_id']=df.groupby('airline_name').ngroup()
        inputId = user_df[user_df['airline_name'].isin(inputflights['airline_name'].tolist())]
        id_df=inputId[['airline_name','flight_id']]
        id_df.drop_duplicates(inplace=True)
        inputflights=pd.merge(inputflights,id_df)
        userSubset = user_df[user_df['flight_id'].isin(inputflights['flight_id'].tolist())]
        userSubset.drop(columns=['link','title','author_country','date','content','aircraft','type_traveller','cabin_flown','route','seat_comfort_rating','cabin_staff_rating','food_beverages_rating','inflight_entertainment_rating','value_money_rating','recommended'],inplace=True)
        userSubsetgroup = userSubset.groupby(['id'])
        userSubsetgroup = sorted(userSubsetgroup,  key=lambda x: len(x[1]), reverse=True)
        userSubsetgroup = userSubsetgroup[0:100]
        return userSubsetgroup,inputflights,user_df

    def recommend(self,userSubsetgroup,inputflights,user_df):

        pearsonCorrelationDict = {}

#For every user group in our subset
        for name, group in userSubsetgroup:
        #Let's start by sorting the input and current user group so the values aren't mixed up later on
            group = group.sort_values(by='flight_id')
            inputflights = inputflights.sort_values(by='flight_id')
            #Get the N for the formula
            nRatings = len(group)
            #Get the review scores for the movies that they both have in common
            temp_df = inputflights[inputflights['flight_id'].isin(group['flight_id'].tolist())]
            #And then store them in a temporary buffer variable in a list format to facilitate future calculations
            tempRatingList = temp_df['overall_rating'].tolist()
            #Let's also put the current user group reviews in a list format
            tempGroupList = group['overall_rating'].tolist()
            #Now let's calculate the pearson correlation between two users, so called, x and y
            Sxx = sum([i**2 for i in tempRatingList]) - pow(sum(tempRatingList),2)/float(nRatings)
            Syy = sum([i**2 for i in tempGroupList]) - pow(sum(tempGroupList),2)/float(nRatings)
            Sxy = sum( i*j for i, j in zip(tempRatingList, tempGroupList)) - sum(tempRatingList)*sum(tempGroupList)/float(nRatings)
            
            #If the denominator is different than zero, then divide, else, 0 correlation.
            if Sxx != 0 and Syy != 0:
                pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
            else:
                pearsonCorrelationDict[name] = 0
        pearsonDF = pd.DataFrame.from_dict(pearsonCorrelationDict, orient='index')
        pearsonDF.columns = ['similarityIndex']
        pearsonDF['id'] = pearsonDF.index
        pearsonDF.index = range(len(pearsonDF))
        topUsers=pearsonDF.sort_values(by='similarityIndex', ascending=False)[0:50]
        topUsersRating=topUsers.merge(user_df, left_on='id', right_on='id', how='inner')
        topUsersRating.drop(columns=['link','title','author_country','date','content','aircraft','type_traveller','cabin_flown','route','seat_comfort_rating','cabin_staff_rating','food_beverages_rating','inflight_entertainment_rating','value_money_rating','recommended'],inplace=True)
        topUsersRating['weightedRating'] = topUsersRating['similarityIndex']*topUsersRating['overall_rating']
        tempTopUsersRating = topUsersRating.groupby('flight_id').sum()[['similarityIndex','weightedRating']]
        tempTopUsersRating.columns = ['sum_similarityIndex','sum_weightedRating']
        recommendation_df = pd.DataFrame()
    #Now we take the weighted average
        recommendation_df['weighted average recommendation score'] = tempTopUsersRating['sum_weightedRating']/tempTopUsersRating['sum_similarityIndex']
        recommendation_df['flight_id'] = tempTopUsersRating.index
        recommendation_df = recommendation_df.sort_values(by='weighted average recommendation score', ascending=False)
        user_df.drop(columns=['link','title','author_country','date','content','aircraft','type_traveller','cabin_flown','route','seat_comfort_rating','cabin_staff_rating','food_beverages_rating','inflight_entertainment_rating','value_money_rating','recommended'],inplace=True)
        recommended=user_df.loc[user_df['flight_id'].isin(recommendation_df.head(10)['flight_id'].tolist())]
    #recommended
        recommended=pd.DataFrame(recommended.drop_duplicates(subset=['flight_id']))
        return recommended
#recommended.sort_values(by=['overall_rating'])