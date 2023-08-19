#Forked from https://github.com/IrinaGoloshchapova/ml_system_design_doc_ru
# ML System Design Doc - [ENG]
## ML System Design Doc - \<Recomendation System for Ecomerce\> \<MVP\> \<1\>

* ML System Design Doc template from [Reliable ML](https://t.me/reliable_ml)* telegram channel.   

- Recommendations on the process of completing the document (workflow) - [here](https://github.com/IrinaGoloshchapova/ml_system_design_doc_ru/blob/main/ML_System_Design_Doc_Workflow.md).  
- Detailed report about what ML System Design Doc is and how, when and why to make it - [here](https://www.youtube.com/watch?v=PW9TGNr1Vqk).
    
> ## Terms and Explanations
> - Iteration is all the work that is done before the next pilot is started  
> - BR - Business Requirements 
> - EDA - Exploratory Data Analysis  
> - `Product Owner`, `Data Scientist` - the roles that populate the respective sections 
> - In this template, the `Data Scientist` role combines the competencies of the classic `Data Scientist` role with a focus on research and the `ML Engineer` & `ML Ops` roles with a focus on productization of models
> - For your organization, the role assignment can be refined depending on the operating model 

### 1. Objectives and prerequisites 
#### 1.1. Why go into product development?  

- Business objective : Building a recommendation system for personalized recommendations of goods from the site catalog to the user. As a result, we expect an improvement in user experience during the interaction with the service, which is expressed in the number of purchases of goods from the category "You may like it".


- Why will it become better than it is now from using ML : Due to the large number of products in the catalog, it is necessary to use a ranking algorithm. Large amount of data about user actions and items is available and allows to build a personalized recommendation system. RecSys will more often offer the user interesting (or potentially interesting)  products, thereby increasing user satisfaction. 

  
- What we will consider as a success of the iteration from the business perspective:
  1. The value of the ranking metric on a test sample of historical data is higher than X.
  2. The value of the target business-metric after implementation of the model is higher by X%. To assess the business effect, it is recommended to conduct an A/B controlled experiment, which is not provided in the pilot.



---
  Additional questions:
   - Should we define the business-metric, it's uplift at this stage? Possible variants: the average number of user purchases from the recommendations page, the average user bill for purchases from the recommendations page, the user's LTV.
   - Do we solve the problem only for authorized users? On the WB website (without logging in to the account) there is no see section "You may like it".
   - If we already had a recommendation system, we would compare the quality of the models with each other?
   - Are we interested in type of action which the user will perform with our recommendation list? Do we understand correct, that: we have to recommend a list of products based on the user's history, and check whether the user actually interacted with the products of this list? And what a position of the "interaction item" is?
   - Do we need to clearly define ranking metric and it's expected value at this stage? Possible variants: MAP@k, AP@k, MRR, NDCG

---

#### 1.2 Business Requirements and Constraints  

- A brief description of BR and links to detailed business requirements documents : Machine learning model works due to the "request-response" principle. A request is received from the system database with data about the history of user actions, products in the catalog (features). In response, the system issues a response with the ID numbers of the products that are relevant to the user. The list of products, their image and description are displayed on the user's website.

- `Product Owner' business constraints : "request-response" process must must take not more than X ms. 
  
- What we expect from a particular iteration : Building the RecSys itself with all stages of working with data (from database), rank and rerank stages, model validation due to the pipeline. Implementation of user interaction with the service via the web interface.
  
- Pilot business process description as far as possible : The user visits the site and logs into his account. After logging into the account, he receives a list of personalized recommendations. Recommendations are made in 2 stages: the primary list of goods is formed only on the basis of user actions; the second stage of rearrangement is made on the basis of meta-information about goods, information about user interactions with goods. The final list of top X recommended products is stored in the storage. From this storage, information about the name, images of goods is displayed on the user's page.


- What do we consider a successful pilot? Success criteria and possible ways to develop the project : A successful model will correctly gives recommendations that are potentially interesting to the client, and the user inteface works correctly.

---
  Additional questions:
   - Do we need to clearly define barrier metrics and them expected values at this stage?

---


#### 1.3. What is included in the project/iteration scope, what is not included   

- What BRs are subscribed to be closed in this iteration of `Data Scientist`.
  1. Trained model 
  2. Front and back end of the cite
  3. Model connectivity with back and front end + connectivity with Data Base (Postgre for simplicity) 
  4. Reproductible code (integrated in docker)
     
- What will not be closed by `Data Scientist`.
  1. Data engineering pipeline (ETL/ELT)
  2. SRE (recommendantions should be available 99.9% of time not to lose extra  
  3. Effective backend maybe made on more effective libraries(like fast api)/software development(programming) languages like golang
  4. Evaluation of business metrics as the proof of improvements after the implementation of the model
     
- Description of the result in terms of code quality and reproducibility of the `Data Scientist` solution
  1. Documentation for every function, class method, class object; use of dockstring and linters is obligatory
  2. Additional separation of part of the code in ipynb files
  3. Additional documentation about connectivity of files
  4. Separated files as main, eda, some other modules that could be useful
  5. Integration with docker, so you could set up solution really quick
     
- Description of the planned technical debt (what we leave for further productization) `Data Scientist`.
  1. We use data about users' actions and items with granularity: userid - itemid - status of the recommendation (was the item recommended to the user and on which position in result list it presented). Predictors ~ actions of users and items' info. Target ~ recommendation.

#### 1.4.Solution prerequisites- Description of all common solution assumptions used in the system - with justification from the business request: which data blocks we use, forecast horizon, model granularity, etc. ``Data Scientist''  

### 2. `Data Scientist' methodology     

#### 2.1. Problem Statement  


- What we do from a technical point of view: recommendation system, anomaly search, prediction, optimization, etc. `Data Scientist
- The central objective of our current project is the development of a sophisticated recommendation system. The recommendation system aims to provide tailored suggestions and insights to users, optimizing their experience and interaction with our platform. This system will leverage user behavior, preferences, historical data, and contextual information to generate accurate and relevant recommendations.
- To enhance the user experience, our recommendation system should be capable of real-time updates. This requires the development of mechanisms to incorporate new user interactions and preferences instantaneously into the recommendation generation process.
- As our user base continues to grow, it is essential that our recommendation system remains scalable. We must design an architecture that can handle increasing data volumes without compromising the responsiveness and speed of generating recommendations.
- Personalization is a crucial aspect of our recommendation system. We need to develop strategies to effectively capture individual user preferences, even when dealing with diverse and evolving user profiles.


#### 2.2. Solution flowchart  

- Flowchart for the baseline and main MVP with key stages of the problem solution: data preparation, building predictive models, optimization, testing, technical debt closure, pilot preparation, other. `Data Scientist`.  
- [Example of a possible blockchain](https://github.com/IrinaGoloshchapova/ml_system_design_doc_ru/blob/main/product_schema.png?raw=true)
> A schema necessarily includes a baseline architecture. If the baseline and the main MVP do not differ significantly, it can be one block diagram. If significantly, draw two: one for the baseline and one for the main MVP.  
> If the flowchart is **template** - i.e. it can be copied and applied to different products - it is **incorrect**. The flowchart should show a solution diagram for the specific problem posed in part 1.    

#### 2.3 Stages of solving the `Data Scientist' problem  

> - For each stage **from the EDA results**, describe - **separately for the baseline** and **separately for the main MVP** - everything about the data and the solution technique as concretely as possible. We outline the necessary inputs, the expected solution technique and what we expect to get in order to move on to the next step.  
> - As a rule, a detailed and structured filling of the `2.3` section is only possible **based on the results of EDA**.  
> - If the description in the design doc is **template** - i.e. it can be copied and applied to different products, it is **incorrect**. The design doc should show a solution diagram for the specific problem posed in part 1.  

- Stage 1 - Collection the data, preparing and analysis.

Download transaction data from the given file. We load them into Jupiter's notebook. When selecting, we check the completeness of the data, choose the strategy about working with outliers and missing data, check the data types.
Sourse of the metadata about items - **TBD**

Target variable
| Data name  | Is there any data in the company (if yes, the name of the source/storefronts) | Required resource to get data (what roles are needed) | Has the data quality been checked (yes, no) |
| ------------- | ------------- | ------------- | ------------- |
| The fact of the interaction of user with the item on website | ab_data.csv  | DE | TBD |


Features: 
| Data name  | Is there any data in the company (if yes, the name of the source/storefronts) | Required resource to get data (what roles are needed) | Has the data quality been checked (yes, no) |
| ------------- | ------------- | ------------- | ------------- |
| Data about user's actions with items (view, add to cart, buy) | ab_data.csv  | DE | TBD |
| Name of items | TBD | DE | TDB |
| Description of items | TBD | DE | TDB |
| Items reviews | TBD | DE | TDB |

MVP: Jupyter's notebook with loaded data.


- Stage 2 - EDA, feature selection

Cleaning data from outliers, filling nans and incorrect info due to the chosen strategy.
Perform EDA and plot main distributions, graphs, statistics for the understanding and the insights. Make feature selection and form the feature space (including scaling).


MVP: Jupyter's notebook with main conclusions and insights. Fixed feauture space.


- Stage 3 - Definition of train, test, validation samples.

Description and formation of samples for trainig, testing and validation.




> Examples of stages:  
> - Stage 2 - Prepare predictive models  
> - Step 3 - Interpretation of models (as agreed with the customer)  
> - Step 4 - Integration of business rules to calculate business metrics for the quality of the model  
> - Stage 5 - Preparation of model inference by iterations    
> - Stage 6 - Integration of business rules  
> - Step 7 - Optimizer development (selection of optimal iteration)  
> - Stage 8 - Preparing the final report for the business  

*Stage 1 is typically, data preparation.  

This stage should include the following:  

- The data and entities on which your machine learning model will be trained. A separate table for the target variable (or target variables of different stages), a separate table for the features.  

| Name of data | Does the data exist in the company (if yes, name of source/storefront) | Resource required to retrieve the data (what roles are needed) | Has the data quality been verified (yes, no) |
| ------------- | ------------- | ------------- | ------------- |
| Sales | DATAMARTS_SALES_PER_DAY | DE/DS | + | |
| ...  | ...  | ... | ... |
 
- Brief description of the result of the step - what should be the output: data showcases, data streams, etc.  
  
> Most of the time it is not possible to complete the section without EDA.

 **Steps 2 and beyond, in addition to data preparation.
 
Description of the technique **for each step** should include a description **separately for MVP** and **separately for baseline**:  

- Description of sample generation for training, testing, and validation. Selection of representative data for experimentation, training and pilot training (from business objective and data representativeness from technical point of view) `Data Scientist'    
- Horizon, granularity, frequency of necessary recalculation of `Data Scientist` predictive models   
- Definition of the target variable, aligned with the `Data Scientist' business   
- Which quality metrics we use and why they are related to the business outcome labeled `Product Owner` in sections `1` and `3`. Example - WAPE <= 50% for > 80% of categories, bias ~ 0. Possible formulation in terms relative to baseline, quantitatively. Baseline may have its own target metrics, or may not have any at all (if justified) `Data Scientist`.   

 - Necessary stage outcome. For example, a necessary outcome may not just be the achievement of some quality metrics, but the inclusion of certain factors in the models (promo flag for revenue forecasting, etc.) `Data Scientist'.    
- What the risks might be and what we plan to do about it. For example, a factor needed for a model (promo flag) will turn out to be insignificant for most models. Or for 50% of the models there will be insufficient data for `Data Scientist' estimation    
- Upper-level principles and rationale for: feature engineering, solution algorithm selection, cross-validation techniques, result interpretation (if applicable).  
- Whether business validation of the stage result is envisioned and how will the `Data Scientist` & `Product Owner` be conducted  
  
### 3. Preparation of the pilot  
  
#### 3.1. Method of evaluating the pilot  
  
- Brief description of the intended design and method of evaluation of the pilot `Product Owner`, `Data Scientist` with `AB Group` 
  
#### 3.2. What we consider a successful pilot  
  
Metrics formalized in the pilot for evaluating the success of `Product Owner'   
  
#### 3.3. Pilot preparation  
  
- What we can afford based on expected computational costs. If it is difficult to calculate initially, we describe the step of calculating the expected computational complexity on the baseline experiment. And provide for refining the pilot parameters and setting limits on the computational complexity of the models. ``Data Scientist'' 

### 4.
Implementation `for production systems, if required'    

> Completion of section 4 is not required for all document designs.In some cases, the result of the iteration may be the calculation of some values further used in the business process for the pilot.  
  
#### 4.1. Solution architecture   
  
- Block diagram and explanations: services, assignments, methods of `Data Scientist` API.#### 4.2.Description of infrastructure and scalability 
  
- What infrastructure is chosen and why `Data Scientist`. 
- Pros and cons of choosing `Data Scientist`. 
- Why the final choice is better than other `Data Scientist` alternatives#### 4.3.System performance requirements- SLA, throughput and latency of `Data Scientist`  
  
#### 4.4.System Security- Potential vulnerability of the `Data Scientist` system  

  
#### 4.5.Data Security   
  
- Whether there are no breaches of GDPR and other `Data Scientist` laws
- GDPR Compliance and Data Privacy:
Building a recommendation system involves collecting and processing user data. To ensure compliance with laws like GDPR (General Data Protection Regulation), it's crucial to handle user data ethically and transparently. This includes obtaining user consent for data collection, providing clear privacy policies, enabling data deletion requests, and ensuring that user data is secure.
-Ethical and Diversity Considerations:
While optimizing business metrics is important, it's also essential to maintain ethical considerations. Ensuring that the recommendation system doesn't reinforce biases or lead to filter bubbles is crucial. Diversity and fairness in recommendations should be prioritized.
  
#### 4.6. Costs  
  
- Estimated costs of running the system per month `Data Scientist`
- VC: Capacity of Data Scientist to implement model + capacity of data engenieers to provide relible ETL process via manual checking, alerting and monitoring; capacity of backend and probably frontend engeniers to integrate parts of business
- FX: increased cost on servers to make solution stable
- Extra risks ( donno how to implement)
  
  
#### 4.5. Integration points  
  
- Description of interaction between services (API methods, etc.) `Data Scientist`.
- 1. Data is going from our data base, where simple etl is made with help of Airflow
- 2. Then model is trained again using (?) Mlflow(?)
- 3. Resultat of our model is going to data base( or s3 where results is stored) and info is pushed to backend
- 4. Backend is sending info to frontend, using Fast Api/Flask
- 5. Info from the cite is send to backend and data bases
- 6. Analyst analyse the effeect of our new feature via ab test seted before or other analytical tools  
#### 4.6. Risks  
  
- Description of risks and uncertainties that are worth foreseeing `Data Scientist`
- Model risk
- Effect on other parts of business
- Data quality issues
- No effect on business metrics
- Infrastructure risk e.g need to give more operation memory for service

> ### Materials for further diving into the topic  
> - [AWS's ML System Design Doc [EN] template](https://github.com/eugeneyan/ml-design-docs) and [article](https://eugeneyan.com/writing/ml-design-docs/) explaining each section  
> - [Google's top-level ML System Design Doc template](https://towardsdatascience.com/the-undeniable-importance-of-design-docs-to-data-scientists-421132561f3c) and [description of its general principles](https://towardsdatascience.com/understanding-design-docs-principles-for-achieving-data-scientists-53e6d5ad6f7e).
> - [ML Design Template](https://www.mle-interviews.com/ml-design-template) from ML Engineering Interviews  
> - The article [Design Documents for ML Models](https://medium.com/people-ai-engineering/design-documents-for-ml-models-bbcd30402ff7) on Medium.Top-level recommendations for the content of a design document and an explanation of why you need one in the first place  
> - [Short Canvas for ML Project from Made with ML](https://madewithml.com/courses/mlops/design/#timeline). Suitable for a top-level description of an idea to see if it makes sense to go further.  
