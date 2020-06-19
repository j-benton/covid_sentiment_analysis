# COVID-19 Sentiment Analysis of Social Media Posts


## Problem Statement

The COVID-19 response has been largely regional and state-based in nature. Some states have enacted strictly enforced stay-at-home policies, while others have provided guidelines. Will a sentiment analysis of social media posts across geographic regions reflect both local policies on social distancing and the occurrences of the pandemic in those areas?


## Executive Summary

Our world is more connected than ever, and these connections are increasingly being made in real time. It is possible to react instantaneously to events happening all over the world and share those reactions with thousands, if not millions, of people. This provides ample sources of data for data scientists interested in Natural Language Processing and sentiment analysis. During the recent global pandemic, regions in the United States responded in a variety of ways, and like any other major event, it has consumed the conversations happening on social media. Our project aims at capturing the tone of those conversations and analyzing  online reactions to state leadership, as well as the pandemic itself, changed depending on what was happening around them. Understanding how large disasters affect the citizenry is very important for organizations seeking to tailor their response in times of crisis.

Our first task was to choose the scope of our project. The terrain of social media is vast and varied, and each platform has its own ways of ordering and making available their data. Twitter data seemed the most accessible, and our personal experiences with posts on Twitter indicate that they are reliably text- and opinion-based. Facebook and Instagram had tighter restrictions on their data, and Reddit is organized into themed subreddits that wouldn't give us general or stream-of-consciousness data that we think would most accurately reflect users' reactions to specific current events.

To get our tweet data, we used a third-party program called Get Old Tweets 3 (GOT3), which bypasses the Twitter API and uses Twitter's advanced search function to pull data. This allowed us to go back farther than the Application Programming Interface (API),which is limited to seven days, but it has limitations as well. The geo function that provides location data is currently defunct, so we had to pull tweets by specified locations to know where they came from. Since our aim is to compare tweets by region (specifically, regions with differing lockdown measures), we looked up articles that ranked states by how aggressively they responded to the pandemic. A Wallet Hub article, linked below, has many such rankings, and their methodology was robust and clear. From this site we chose twenty states: the ten states with the most aggressive policies and the ten states with the least aggressive policies.

From here, GOT3 dictated how we searched for tweets. To specify location, we had to set a base point (e.g. a city) and set a radius around that location from which to pull data. Since we had our states picked out, we decided to choose the largest city from each state to serve as proxy for the state (and its corresponding lockdown ranking). Thus, "New York" became "New York City," "Texas" became "Houston," and so on. Choosing the largest city for each state also had the advantage of ensuring we were selecting more densely populated areas of our states. More people means more twitter users and that means more data. 

We also needed to specify a timeline. If we pulled tweets that were too recent, it wouldn't reflect many states' lockdown policy differences, since states have been relaxing their shelter-in-place orders over the last six weeks. Tweets that were too early would have the opposite problem: many states that had strong lockdown policies didn't start as early as others. To find our timeline, we looked up when the last states that instituted sweeping lockdown measures put those policies in place. This happened to be on April 8 (see the Wiki article linked below). We closed our timeline on April 30, since May 1 was when many states began to relax (or plan to relax) their measures.

From these cities and from within this timeline, we pulled nearly 400,000 tweets. However, while these tweets could tell us how sentiments compare across regions, they wouldn't tell us how these sentiments compared in the same region with tweets posted in non-pandemic times. So we pulled a similar number of tweets from the same cities and from the same April dates for 2019 to serve as a sort of sentiment control group. Finally, we decided to pull 2020 tweets again, this time searching only for tweets containing words directly related to COVID-19. To do this, we collected a list of COVID-related words (built largely on a list found at the github repo linked below), found the most frequently used ones in our existing 2020 corpus, and then re-pulled data from our cities/timeline that contained those words. This gave us a dataset of over 37,000 tweets that were COVID-related.

We also compiled infection rate data for each of our cities and for each date in our timeline to see how sentiment changed as infections increased. (We also compiled weekly death rate data by state from the CDC, but we realized shortly before our deadline that this data had not been updated/was not accurate and so we did not use it in any final analysis).

For sentiment analysis, we used the Vader Sentiment compound score, which is a "normalized, weighted composite score" of positive and negative polarity (quoted from the documentation, linked below). 

## Conclusions

As our data visualizations notebook shows, there was very little to be seen in our sentiment analysis. Despite differing lockdowns, varying infection rates, and a wide geographic spread (from Honolulu to Boston), sentiments did not change much on Twitter for nearly any of our data points in any of our datasets. This was true for our general 2020 tweets, 2019 tweets, and our COVID-specific 2020 tweets. The one exception are tweets from our COVID-specific dataset pulled from Cheyenne, WY. In mid-April, tweet sentiments drop, rise a little, and plummet by the end of the month. Nothing in our COVID-19 data suggest why, but Cheyenne is also an outlier in that it produced very few tweets compared to most of our other cities. It's hard to conclude much from these facts. (A similar, though not as strong, deviation occurred in COVID-specific tweets from Sioux Falls, but this city also has low/stable infection rates and produced very few tweets compared to other cities.)

Overall, we feel strongly that this project is a proof of concept, and hopefully our process will spur others on to similar projects that will yield more interesting and useful results.

## Data Dictionary
|Feature|Type|Description|
|---|---|---|
|**text**|*object*|The raw tweet text, unprocessed|
|**lemmata**|*object*|Processed text (lemmatized, stopwords/url/email removed, lowercase)|
|**text_polarity**|*float64*|Vader Sentiment compound score denoting positivity/negatvity of 'text' document|
|**lemmata_polarity**|*float64*|Vader Sentiment compound score denoting positivity/negatvity of 'lemmata' document|
|**top_10**|*int*|Flags whether the city associated with document is from a state with stricter lockdown policies (1) or looser lockdown policies (0)|

## Sources
Chief data source:
https://twitter.com

Death by week/state (not ultimately used):
https://catalog.data.gov/dataset/provisional-covid-19-death-counts-by-week-ending-date-and-stateBaseline

Infection increases by day/state:
http://www.healthdata.org/covid/data-downloads

State rankings by COVID response:
https://wallethub.com/edu/most-aggressive-states-against-coronavirus/72307/

Timeline data:
https://en.m.wikipedia.org/wiki/U.S._state_and_local_government_response_to_the_COVID-19_pandemic

City population figures (used in presentation):
https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population

Starter list of COVID words:
https://github.com/echen102/COVID-19-TweetIDs

Information about Vader Sentiment compound score:
https://github.com/cjhutto/vaderSentiment#about-the-scoring
