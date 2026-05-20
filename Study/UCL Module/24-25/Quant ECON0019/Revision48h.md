---
tags: 
Module: "ECON0019"
Daily Notes: 2025-08-19
---
⬇️Download Course Material
	https://moodle.ucl.ac.uk/my/

---
# **🚑 2-Day Crash Study Plan for ECON0019 Exam**
### **🎯 Core Philosophy**

1. **Don’t try to learn everything** → focus on what is actually tested (see exam breakdown).
    
2. **Cycle between theory and past questions** → every concept you read, immediately connect it to an exam question.
    
3. **Cheat-sheet building** → by the end you’ll have 2 pages of formulas + assumptions to bring to memory.
    

---

## **🔹 Day 1 (12 hours total, split into 3 blocks)**

  

### **Block 1 OLS Basics & Assumptions**

- Read notes on:
    
    - SLR (simple regression): assumptions SLR.1–SLR.5
        
    - OLS formulas (β̂₀, β̂₁) and why they are unbiased/consistent
        
    - Gauss-Markov theorem → OLS is BLUE
        
    
- Write these **on one A4 page**:
    
    - Assumptions list (strict exogeneity = Cov(x,u)=0)
        
    - OLS formulas
        
    - Unbiasedness proof skeleton: E[β̂]=β
        
    - Variance formula of OLS
        
    
- Practice with **Exam A1 parts (a)-(c)**. Even if you don’t understand fully, memorize the structure:
    
    - Write down assumption
        
    - Show OLS formula
        
    - Apply LLN to get consistency
        

⚡ Goal: Be able to recognize when the exam is just asking you to “state assumptions and show consistency.”

---

### **Block 2 Inference & Errors**

- Read notes on:
    
    - LLN, CLT, Slutsky → how asymptotics work
        
    - Standard errors: homoskedastic vs heteroskedastic (robust SE)
        
    - HAC/HAR for panel/time series
        
    
- Practice with **Exam A2 (a)-(c)**: interpret coefficients, test significance, explain robust SE.
    
- Write down **keywords you must memorize**:
    
    - “Heteroskedasticity: OLS still unbiased/consistent but variance wrong → robust SE needed.”
        
    - “Autocorrelation: robust SE not valid → HAC needed.”
        
    - “Measurement error → bias towards zero.”
     
⚡ Goal: Be able to look at regression output and say: sign is expected, significant/not significant, SEs trusted/not trusted.

---

### **Block 3 Endogeneity, IV & Extensions**

 - Plan
        - Endogeneity (simultaneity, omitted variable bias, measurement error).
        - Instrumental Variables (conditions: relevance + exogeneity).
        - Weak instruments (F < 10 rule).
        - Nonlinear models: Probit vs LPM.
        - Tobit (censoring).
        
    - Practice with **Exam B1**:
        - Log-likelihood for Probit (just memorize template).
        - TSLS procedure.
        - IV conditions & weak IV test.
      
    - Practice with **Exam B2** (skim):
        - Recognize inflation = endogenous → OLS invalid.
        - IV relevance/exogeneity.
        - Dynamic multiplier formula.
    
    ⚡ Goal: Be able to **spot the endogeneity assumption violation** and say: “Need IV, must check relevance + exogeneity, weak instrument = high variance.”

#### Note

---

# **After IV: Next Topics in Block 3**

  

## **1. Weak Instruments**

  

**Problem:** If the instrument is only weakly correlated with the endogenous regressor x, the IV estimator becomes unstable.

  

IV estimator:

\hat{\beta}_{IV} = \frac{\operatorname{Cov}(z,y)}{\operatorname{Cov}(z,x)}.

  

If \operatorname{Cov}(z,x) is close to 0, the denominator is tiny, so \hat{\beta}_{IV} is biased and has huge variance (even asymptotically).

  

**Rule of thumb (Staiger & Stock):**

- First-stage regression:
    
    x = \pi_0 + \pi_1 z + v
    
- Check the F-statistic for \pi_1=0.
    
- If F < 10, instruments are **weak** → IV unreliable.
    

  

**Example:** Using rainfall as an instrument for education — if rainfall barely affects schooling decisions, the IV estimate of returns to education is meaningless.

---

## **2. Two-Stage Least Squares (TSLS)**

  

This is the **multi-regressor extension of IV**.

- **Stage 1 (first-stage regression):**
    
    x = Z\pi + v, \quad \hat{x} = P_Z x
    
    where Z are instruments and P_Z = Z(Z^\top Z)^{-1}Z^\top is the projection matrix.
    
- **Stage 2:**
    
    y = X\beta + u, \quad \hat{\beta}_{2SLS} = (X^\top P_Z X)^{-1} X^\top P_Z y
    

  

Interpretation: Replace endogenous regressors x with their **predicted values** \hat{x} from the first stage, then run OLS.

---

## **3. Nonlinear Models**

  

### **(a) Linear Probability Model (LPM)**

- Regression when y \in \{0,1\}.
    
- OLS formula: P(y=1|x)=x^\top \beta.
    
- Problems: predictions may lie outside [0,1]; errors heteroskedastic.
    
- Advantage: simple to estimate and interpret marginal effects.
    

  

### **(b) Probit Model**

- Latent variable model:
    
    y_i^* = x_i^\top \beta + u_i, \quad u_i \sim N(0,1)
    
    y_i = 1\{y_i^* > 0\}
    
- Probability:
    
    P(y_i=1|x_i) = \Phi(x_i^\top \beta)
    
    where \Phi(\cdot) is the standard normal cdf.
    
- Log-likelihood:
    
    \ell(\beta) = \sum_{i=1}^n \Big[ y_i \log \Phi(x_i^\top \beta) + (1-y_i)\log(1-\Phi(x_i^\top \beta)) \Big]
    

  

### **(c) Tobit Model (censoring)**

- Latent model:
    
    y_i^* = x_i^\top \beta + u_i
    
- Observed variable:
    
    y_i = \max(0, y_i^*)
    

  

Used when dependent variable is censored (e.g. wages ≥ 0, corner solutions in consumption). Estimated by ML.

---

## **4. Dynamic Multipliers (time-series models)**

  

Suppose:

y_t = \alpha + \beta_0 x_t + \beta_1 x_{t-1} + \beta_2 x_{t-2} + \dots + u_t

- **Impact multiplier:** effect of x_t on y_t = \beta_0.
    
- **Cumulative multiplier up to lag k:**
    
    M_k = \beta_0 + \beta_1 + \dots + \beta_k
    
- **Long-run multiplier:** sum of all lag coefficients (possibly scaled if AR terms in y are present).
    

---

Do you want me to now take these four (weak IV, TSLS, LPM/Probit/Tobit, multipliers) and create a **condensed exam cheat sheet** in the same style as we did for expectations/covariances? That way you’ll have Block 3 fully summarized in one place.
---

## **🔹 Day 2 (12 hours total, revision & practice)**

  

### **Block 1 (Morning, ~3h):** 

### **Re-do Part A Questions**

- Go through **A1 and A2 fully**.
    
- Write down bullet-point answers as if in exam.
    
- Don’t aim for derivation perfection, aim to **write structured answers**:
    
    - State assumption → write OLS formula → invoke LLN/CLT → conclude consistency.
        
    - Interpret regression → check signs and t-stats → discuss SE validity.
        
    

---

### **Block 2 (Midday, ~4h):** 

### **Re-do Part B Questions**

- Pick **either B1 (micro/IV)** or **B2 (macro/time series)** — don’t try to master both.
    
- If you’re weak at math, pick **B1** (Probit/IV) because the logic is more verbal.
    
- If you’re okay with some matrix variance math, pick **B2**.
    
- Write bullet-point templates for each sub-question.
    

---

### **Block 3 (Afternoon, ~3h):** 

### **Cheat-Sheet Consolidation**

- Reduce all notes to **2 A4 pages**:
    
    - Page 1 = Assumptions + OLS formulas + variance formulas + inference (LLN, CLT, SEs).
        
    - Page 2 = Endogeneity, IV (conditions, weak IV), Probit vs LPM, Tobit, distributed lags, PCA.
        
    
- Practice writing them from memory once.
    

---

### **Block 4 (Evening, ~2h):** 

### **Simulation**

- Set timer → try one A question + one B question in timed conditions (write fast bullet-point answers).
    
- Compare with exam answers.
    

  

⚡ Goal: Enter exam knowing:

1. What every question type is asking.
    
2. The skeleton of the answer (assumption → formula → inference → conclusion).
    

---


# **Formula**
