#Forked from https://github.com/IrinaGoloshchapova/ml_system_design_doc_ru
# ML System Design Doc - [RU]
## ML System Design Doc - \<Product\> \<MVP or Production System\> \<Number\>

* ML System Design Doc template from [Reliable ML](https://t.me/reliable_ml)* telegram channel.   

- Recommendations on the process of completing the document (workflow) - [here](https://github.com/IrinaGoloshchapova/ml_system_design_doc_ru/blob/main/ML_System_Design_Doc_Workflow.md).  
- Detailed report about what ML System Design Doc is and how, when and why to make it - [here](https://www.youtube.com/watch?v=PW9TGNr1Vqk).
    
> ## Terms and Explanations
> - Iteration is all the work that is done before the next pilot is started  
> - BT - Business Requirements 
> - EDA - Exploratory Data Analysis  
> - `Product Owner`, `Data Scientist` - the roles that populate the respective sections 
> - In this template, the `Data Scientist` role combines the competencies of the classic `Data Scientist` role with a focus on research and the `ML Engineer` & `ML Ops` roles with a focus on productization of models
> - For your organization, the role assignment can be refined depending on the operating model 

### 1. Objectives and prerequisites 
#### 1.1. Why go into product development?  

- Business objective `Product Owner'.  
- Why will it become better than it is now from using ML `Product Owner` & `Data Scientist`.  
- What we will consider the success of the iteration from the `Product Owner` business perspective  

#### 1.2 Business Requirements and Constraints  

- A brief description of BT and links to detailed `Product Owner' business requirements documents  
- `Product Owner' business constraints  
- What we expect from a particular iteration of `Product Owner`. 
- Pilot business process description as far as possible - how exactly will we use the model in an existing business process? `Product Owner`.    
- What do we consider a successful pilot? Success criteria and possible ways to develop the `Product Owner` project

#### 1.3. What is included in the project/iteration scope, what is not included   

- What BTs are subscribed to be closed in this iteration of `Data Scientist`.   
- What will not be closed by `Data Scientist`.  
- Description of the result in terms of code quality and reproducibility of the `Data Scientist` solution  
- Description of the planned technical debt (what we leave for further productization) `Data Scientist`.  

#### 1.4.Solution prerequisites- Description of all common solution assumptions used in the system - with justification from the business request: which data blocks we use, forecast horizon, model granularity, etc. ``Data Scientist''  

### 2. `Data Scientist' methodology     

#### 2.1. Problem Statement  

- What we do from a technical point of view: recommendation system, anomaly search, prediction, optimization, etc. `Data Scientist  
#### 2.2. Solution flowchart  

- Flowchart for the baseline and main MVP with key stages of the problem solution: data preparation, building predictive models, optimization, testing, technical debt closure, pilot preparation, other. `Data Scientist`.  
- [Example of a possible blockchain](https://github.com/IrinaGoloshchapova/ml_system_design_doc_ru/blob/main/product_schema.png?raw=true)
> A schema necessarily includes a baseline architecture. If the baseline and the main MVP do not differ significantly, it can be one block diagram. If significantly, draw two: one for the baseline and one for the main MVP.  
> If the flowchart is **template** - i.e. it can be copied and applied to different products - it is **incorrect**. The flowchart should show a solution diagram for the specific problem posed in part 1.    

#### 2.3 Stages of solving the `Data Scientist' problem  

- For each stage **from the EDA results**, describe - **separately for the baseline** and **separately for the main MVP** - everything about the data and the solution technique as concretely as possible. We outline the necessary inputs, the expected solution technique and what we expect to get in order to move on to the next step.  
- As a rule, a detailed and structured filling of the `2.3` section is only possible **based on the results of EDA**.  
- If the description in the design doc is **template** - i.e. it can be copied and applied to different products, it is **incorrect**. The design doc should show a solution diagram for the specific problem posed in part 1.  
    
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
  
#### 4.6. Costs  
  
- Estimated costs of running the system per month `Data Scientist`  
  
#### 4.5. Integration points  
  
- Description of interaction between services (API methods, etc.) `Data Scientist`.  
  
#### 4.6. Risks  
  
- Description of risks and uncertainties that are worth foreseeing `Data Scientist`   

> ### Materials for further diving into the topic  
> - [AWS's ML System Design Doc [EN] template](https://github.com/eugeneyan/ml-design-docs) and [article](https://eugeneyan.com/writing/ml-design-docs/) explaining each section  
> - [Google's top-level ML System Design Doc template](https://towardsdatascience.com/the-undeniable-importance-of-design-docs-to-data-scientists-421132561f3c) and [description of its general principles](https://towardsdatascience.com/understanding-design-docs-principles-for-achieving-data-scientists-53e6d5ad6f7e).
> - [ML Design Template](https://www.mle-interviews.com/ml-design-template) from ML Engineering Interviews  
> - The article [Design Documents for ML Models](https://medium.com/people-ai-engineering/design-documents-for-ml-models-bbcd30402ff7) on Medium.Top-level recommendations for the content of a design document and an explanation of why you need one in the first place  
> - [Short Canvas for ML Project from Made with ML](https://madewithml.com/courses/mlops/design/#timeline). Suitable for a top-level description of an idea to see if it makes sense to go further.  