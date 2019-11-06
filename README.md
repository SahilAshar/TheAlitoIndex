# TheAlitoIndex

## What it does

Justice Samuel Alito is one of the most pro-corporate justices in the Supreme Court, paving the way for better tax and social benefits for them while not being as friendly to most middle class Americans.

We hypothesized - what if there was a way to tell, based on the make-up of Congress in a specific cycle, if the market would react a specific way? More specifically, would the make-up of the Congressional class, in relation to have similar physical features as Justice Samuel Alito, have an effect on the market and its trends?

## How we built it

We built it in two-fold - Mahir spent his time organizing 5 years worth of quantitative data from over 100 securities (kindly provided by Goldman Sachs) to understand what kind of effects a specific Alito Index would have on an industry and it's related securities.

On my end, I spent my time classifying 3500 unique data points of Congressional photos, from 6 different Congressional classes. I trained a facial recognition model and image classification model to understand who Samuel Alito was, and what his physical features were, and then fed massive datasets to eventually get an Alito Index for each member of Congress. 

Once each member of Congress was assigned an Alito Index, we could simply average each Congressional Classes Alito Index, and apply it to the 5 year dataset of Securities, and look for instances of correlation. 

Our end goal was to show that diversity in Congress _does_ play a fundamental role in how markets move and how your vote (and every vote) counts, especially with voting season right on top of us.

## Challenges we ran into

Our next step was to build a Predictive Regression Model with Azure AutoML, but due to technical difficulties and Azure not working nicely with us in the end, we were unable to get one up and running in the end. 

## Accomplishments that we're proud of

Neither of us are Data Science folk - I'm mostly infrastructure and cloud computing,  and Mahir is more of a software generalist. This entire challenge was a new foray for us, but we learned a ton in 24 hours, and we're both super proud of the work we accomplished.

## What's next for The Alito Index

The inclusion and correlation of the DW-Nominate scores! Are these scores statistically significant to market shifts as well? Do Congressmen/women with higher scores  tend to look more like Samuel Alito? The possibilities are endless.
