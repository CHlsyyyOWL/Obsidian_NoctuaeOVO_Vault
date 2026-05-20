---
tags:
  - politics
Date: 2025-02-28
Paper:
  - Quantitative
  - Politics
Progress:
  - 已完成
---

**Topic: Agents of past principals: The lasting effects of incumbents on the political ideology of bureaucrats
Author: Roland Kappe, Christian Schuster
URL: 
https://onlinelibrary.wiley.com/doi/abs/10.1111/1475-6765.12473
# Why bureaucrats are more right or left-wing than citizens in some countries and points of time, yet not others.

1.[Go to annotation](zotero://open-pdf/library/items/L66BNQM3?page=807&annotation=undefined) “political ideologies of past incumbents shape this variation” ([Kappe 和 Schuster, 2022, p. 807](zotero://select/library/items/7RI2VS6K))

- “Incumbents can select ideologically aligned bureaucrats and socialize bureaucrats into ideological preferences;
    
    moreover, prospective bureaucrats may self-select into ideologically aligned governments.” ([Kappe 和 Schuster, 2022, p. 807](zotero://select/library/items/7RI2VS6K))
    

2. [Go to annotation](zotero://open-pdf/library/items/L66BNQM3?page=807&annotation=undefined) “As bureaucratic tenure exceeds political tenure, this politicization has lasting effects.” ([Kappe 和 Schuster, 2022, p. 807](zotero://select/library/items/7RI2VS6K))

incumbents ---select----bureaucrats ----influence ---incumbents2

3. “Survey data from 87 countries supports this argument:

1. in countries with longer prior rule by economically left-wing governments, bureaucrats are more left-leaning than citizens  

1. more rightwing in countries with more authoritarian pasts.” ([Kappe 和 Schuster, 2022, p. 807](zotero://select/library/items/7RI2VS6K))

economically left wing - left leaning

authoritarian past - right wing

# Literature review

existing works:

1. congruence between bureaucrats matters policy outcome --
    
    ideology congruence -divergence: quality of representation
    
    - attraction selection
        
        - the public sectors attracts who is more willing to work for public, thus might more favor public intervention
    - socialization
        
        - workplace might influence
    - occupational incentives
        
        - more public spending favor bureaucrats in terms of saving their jobs and salary
        
        … ----> shift bureaucrats ideology to the left
        
    
    [Go to annotation](zotero://open-pdf/library/items/L66BNQM3?page=809&annotation=undefined) “According to the ‘Bureau Voting Model’, self-interested bureaucrats hold leftist attitudes, as left-wing governments favour more public spending, which protects bureaucrats’ jobs and enhances their likelihood of receiving salary increases and promotions (cf. Dunleavy 1985)” ([Kappe 和 Schuster, 2022, p. 809](zotero://select/library/items/7RI2VS6K))
    
    used to
    
    - predict a range of positive outcomes, such as citizen satisfaction and trust
    
2. however:
    
    - This phenomenon: bureaucrats align with citizen is not true for all countries in all time period, why?
    - why bureaucrats can be more left wing than citizens, while more right-wing sometimes?

Hypothesis:

factors influencing ideology congruence of bts:

1. economic life/right proportion in the past
2. political left/right proportion in the past

hence

Hypothesis 1 (H1): Bureaucrats are more left (right)-leaning than citizens in countries with longer past rule by governments with left (right)-wing economic ideologies.

Hypothesis 2 (H2): Bureaucrats are more right (left)-leaning than citizens in countries with longer past rule by authoritarian (democratic) government.” ([Kappe 和 Schuster, 2022, p. 812](zotero://select/library/items/7RI2VS6K))

hence

dependent var: ideology congruence = bts - citizen

independent var: economic length[left||right] / length  

                          political length[left||right] / length

holding factors

Ideology congruence <--attraction selection, socialization,   occupational incentive

Ideology divergence <-- bureaucrats tenure longer than govt, where govt rep citizen while bureaucrats rep last govt ----govt socialized by bts?

# Empirical

[Go to annotation](zotero://open-pdf/library/items/L66BNQM3?page=808&annotation=undefined) “Empirically, the paper provides evidence for this argument through multilevel analyses of the largest dataset on ideological congruence between bureaucrats and citizens to-date, pooling 597,143 respondents in 87 countries and 332 country-years from the Comparative Study of Electoral Systems (CSES), World Value Survey (WVS) and European Social Survey (ESS).” ([Kappe 和 Schuster, 2022, p. 808](zotero://select/library/items/7RI2VS6K))

## Dependent variable

ideology congruence = ideology gap between bureaucrats and citizens

- ideology of bureaucrats: filter from WVS, ESS, CSES (work in public sector)
- ideology of citizens: surveys to independent respondents about placing its left-right scale from 1-10

critical: focus in one country, no variety, no influence from average left-right preference in this country

## Independent variable

level-1 variables: individual -level determinants of political ideology

- education
- income
- employment
- gender
- marital status
- union membership

level-2 variables: country level

Economically left/right :

[Go to annotation](zotero://open-pdf/library/items/L66BNQM3?page=813&annotation=undefined) “categorical indicator of the economic left-right orientation of governments from the Database of Political Institutions (DPI) (Cruz et al. 2016). The indicator codes whether the party of the chief executive is left, centre, or right with respect to economic policy”

Politically left/right:

[Go to annotation](zotero://open-pdf/library/items/L66BNQM3?page=814&annotation=undefined) “we rely on the combined Freedom House and Polity scale (Teorell et al. 2017) that ranges from 0 (least democratic) to 10 (most democratic). It exceeds individual indices in terms of breadth and coverage, and combines assessments of the competitiveness and openness of elections, as well as political rights and civil liberties.”

Income per capita

## Model

Multilevel models

ideologyij = β0 j + β1 j Public Sectorij + β j Level-1 Variables + εij

β0 j = γ00 + γ01 Authoritarian Government j + γ Level-2 Variables + ζ0 j

β1 j = δ10 + δ11 Authoritarian Government j + δ Level-2 Variables + ζ1 j