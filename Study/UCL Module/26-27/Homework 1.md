---
tags:
  - UK/ucl
Module: ECON0117
Daily Notes: 2026-10-19
---
⬇️Download Course Material From UCL
	https://moodle.ucl.ac.uk/my/
⬇️Download Course Material From Scpo
	https://moodle.sciences-po.fr/my/

🎓DashBoard: [[Academia.components]]

---
![[How does the Social Credit System in China affect connected firms.docx]]
1.     Li, Meng, Wang and Zhou (2008), _Political connections, financing and firm performance: Evidence from Chinese private firms_, Journal of Development Economics. [Political connections, financing and firm performance: Evidence from Chinese private firms](zotero://select/library/items/ULMY9E2Z)

This paper was selected because it interestingly shows that political connections help Chinese private entrepreneurs obtain bank loans, and proved that the contribution of connections to firm performance is greater in regions where market and legal institutions are weaker. This pattern suggests that connections partly substitute for weaker institutions. As this kind of substitution works by giving banks assurance about firms that they cannot otherwise assess, then a public credit record backed up by the local government will let banks assess any firm, and therefore should narrow the gap in bank credit between connected and unconnected firms.

**1.**     **Wang, Chen, Lai & Anderson (2026)****,****_Social Credit and Trade Credit: A Coevolutionary Perspective_****,**Journal of Business Ethics** [Social credit and trade credit: A coevolutionary perspective](zotero://select/library/items/3PZUFGWM)

This paper was selected because it shows that after China’s social credit reform, firms in pilot cities obtain more trade credit from their suppliers, and this increase is larger for young, small, private and politically unconnected firms. This pattern suggests that increase in public credit information accessibility helps lenders assess firms of weak political connections to assure themselves. If the same mechanism applies to banks, the Social Credit System should narrow the gap in bank credit between connected and unconnected firms

**2.**     **Lin and Milhaupt (2023), _China's corporate social credit system: the dawn of surveillance state capitalism?_, The China Quarterly.** [China's Corporate Social Credit System: The Dawn of Surveillance State Capitalism?](zotero://select/library/items/K6RCW94D)

This paper was selected because it shows that, among 531 listed firms in Zhejiang, politically connected firms receive credit scores about 10.5 points higher, and that the whole gap comes from a social responsibility score (a sub-filed of the SCS scoring system) valorizes awards from the government and contributions to causes sanctioned by the Chinese Communist Party, while connected firms have no better compliance records. This pattern suggests that credit system can still embrace political alignment rather than compliance alone. If credit scores carry political loyalty in this way, then the Social Credit System may preserve or even widen the advantage of connected firms, and therefore needs to test this possibility as a rival hypothesis.
### Research question
How does the Social Credit System affect connected firms' advantage in bank credit?


# Research Design

## Research question
How does the Social Credit System affect connected firms' advantage in bank credit?

## Sample
- Private (non-state-owned) A-share listed firms, excluding financial and ST firms
- Firms listed before 2014, so that every firm has pre-reform observations
- Years 2010–2019, with 2016 dropped as the transition year

## Variables

**Outcome**
$$
Loan_{it} = \frac{\text{Short-term borrowings}_{it} + \text{Long-term borrowings}_{it}}{\text{Total assets}_{it}}
$$

**Treatment**
- $Pilot_c = 1$ if the firm is registered in a city or district designated as an SCS pilot in 2015 or 2016
- $Post_t = 1$ for 2017–2019, and 0 for 2010–2015

**Political connection** (fixed in 2014, before any designation)
- $Connected_i = 1$ if the firm's chairman or CEO is a deputy to a people's congress or political consultative conference, or a current or former government official

**Controls** (lagged one year)
- Log total assets, return on assets, tangible assets ratio, firm age

## Model
$$
Loan_{it} = \beta\,(Pilot_c \times Post_t \times Connected_i) + \gamma_1 (Pilot_c \times Post_t) + \gamma_2 (Post_t \times Connected_i) + X_{i,t-1}'\theta + \alpha_i + \delta_t + \varepsilon_{it}
$$

- $\alpha_i$ firm fixed effects absorb $Pilot_c$, $Connected_i$ and $Pilot_c \times Connected_i$
- $\delta_t$ year fixed effects absorb $Post_t$
- Standard errors clustered at the city level
- $\beta$ measures how much more the loan gap between connected and unconnected firms changes in pilot cities than in non-pilot cities

## Hypotheses
- **H1 (information substitution)** $\beta < 0$. The loan advantage of connected firms shrinks in pilot cities
- **H2 (political control)** $\beta \geq 0$. The advantage persists or grows, because the state still controls credit records, rewards and punishments

## Checks
- **Event study** Replace $Post_t$ with year dummies (2015 as base year) and plot the coefficients. Pre-2016 coefficients should be close to zero
- **City × year fixed effects** Replace $\delta_t$ and $Pilot_c \times Post_t$ with city × year fixed effects, which absorb all city-level shocks
- **Alternative connection measure** Use only people's congress and political consultative conference membership

## Data
- Pilot lists from the NDRC notices of 2015 and 2016
- Financial statements and executive backgrounds from CSMAR (access to be confirmed), with annual reports from CNINFO as a fallback