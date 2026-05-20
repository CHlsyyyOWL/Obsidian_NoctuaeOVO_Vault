---
tags:
  - France/SciencePo
Module: CulSoc
Daily Notes: 2026-04-10
WOS:
  - Module Essay
Progress:
  - 已完成
---
⬇️Download Course Material From UCL
	https://moodle.ucl.ac.uk/my/
⬇️Download Course Material From Scpo
	https://moodle.sciences-po.fr/my/

🎓DashBoard: [[Academia.components]]

---
[[Culsoc idea]]
## 方法论文献依据

**1. SAGE社交媒体研究方法论（最权威）**

《The SAGE Handbook of Social Media Research Methods》的Weibo章节明确指出，Weibo数据研究需要从"设计到数据收集、分析和解释"的完整研究循环，并强调hashtag是封装主题内容的有效方法。

**2. 哈希标签作为事件表现的有效性**

Song et al.（2025）的PLOS ONE论文指出，"高质量的hashtags可以作为子事件代表（story nodes）来构建事件序列，因为hashtag本身封装了主题内容"。这篇论文使用的方法完全类似：时间窗口内搜索特定hashtags，按新旧排序，收集相关数据。

**3. 数据质量筛选标准的文献依据**

Chen et al.（2023）的PMC论文讨论了社交媒体研究的普遍做法："大多数学者不使用整个时期的全部数据；相反，他们寻找特定位置或参考特定关键词或hashtags的子集"。你的三层筛选标准（100+优先，20-100都记，<20有讨论就记）就是这个逻辑。

### (定量 + 定性混合)

**Zhang et al. (2018)** _"Nationalism on Weibo"_ (China Quarterly) — 分析6000+条微博tweets from 146位意见领袖，使用content analysis按具体主题分解民族主义讨论 [Cambridge Core](https://www.cambridge.org/core/journals/china-quarterly/article/nationalism-on-weibo-towards-a-multifaceted-understanding-of-chinese-nationalism/2E3D5ECDBF8EF105F507BBF58006B9CB)

**PMC 2024/2025 COVID研究** — 50,249条评论，用SnowNLP (情感分析) + LDA (主题聚类，定量部分) + **sampling coding** (样本编码，定性部分) [PubMed Central](https://pmc.ncbi.nlm.nih.gov/articles/PMC11983825/)

**Zhao et al. (2025)** _"Boosting popularity"_ (SAGE) — Netnographic approach + **thematic analysis**，分析900条评论和492条讨论贴 [Sage Journals](https://journals.sagepub.com/doi/10.1177/20539517251331949)

> [!note]-
> 方案 A: Sampling-based Content Analysis（推荐）
> 
> 从196条帖子中，随机抽取或策略性选择 10-15 条关键帖
> 深度分析这些帖子的话语特征 (discourse patterns)
> 每条帖分析:
> 
> 使用了什么论证方式? (法律论证 vs 文化论证 vs 情感论证)
> 核心关键词?
> 作者身份暗示?
> 
> 
> 
> 方案 B: Case Study对比
> 
> 高赞帖 vs 低赞帖对比分析
> 不同Theme的典型案例 (e.g., "抄袭指控"主题中最有说服力的帖子是怎样的?)
> 意见领袖的话语特征 vs 普通用户
> 
> 方案 C: Discourse Analysis片段
> 
> 从词云和高频词出发，分析话语权的权力运作
> 例如: 为什么"文化"词频最高，而"法律"词频低? → 说明什么?

## 前人研究现状

### ✓ 有大量研究的主题

1. **Hanfu + 民族主义/国家认同** ← 直接相关
    - Frontiers最新综述（2026）指出："许多研究探讨了Hanfu作为国家认同符号的使用（Cui 2023, Fu 2023, Law & Qin 2023）"，但同时指出"关于Hanfu和社交媒体的研究很少（Qu et al. 2019）"——这是你可以fill的gap
2. **Hanfu + 社交媒体身份呈现*
    - 2023年一篇论文《An Exploration of the Identity of Contemporary Chinese Hanfu Enthusiasts On Chinese Social Platform Weibo》专门分析了Weibo上的Hanfu博主自我呈现，表明"Hanfu条目为表达身份提供了多样的机会"
3. **Weibo网络舆情 + 民族主义**
    - Zhang et al.（2018）在《China Quarterly》上发表了关于"Nationalism on Weibo"的大型研究，分析了超过6000条tweets和146个意见领袖的政治舆论
4. **Hanfu + embodied nationalism**（你的理论切口）
    - Ip & Fan（2024）的论文"Reinventing Fashion as an Affective Apparatus"分析了Bilibili上的国风汉服仪式，表明"Hanfu充当了affective apparatus，通过文化自信的概念唤起民族主义感受"
### **✗ 没有研究的主题（你的机会）：**
1. **Dior 2022年马面裙事件的具体舆论分析** ← 没找到
2. **Weibo+小红书双平台的汉服舆情对比** ← 没找到
3. **Dior事件中意见领袖的role mapping** ← 没找到
## Methodology的三个层次结构：
**3.1 Hashtag Selection Justification**
- 文献支持：引用Song et al. (2025)和Chen et al. (2023)关于hashtag作为事件代表的effectiveness
- 你的选择：#迪奥马面裙（直接事件）、#汉服（背景社群）、#文化挪用（理论维度）
- 时间窗口：2022.04-08（Dior事件前后）
**3.2 Data Collection Methodology**
- 参考SAGE Handbook的Weibo数据收集标准规范
- 清楚说明：搜索策略（按新旧排序）、时间范围、平台（Weibo + XHS）
- 质量筛选标准（3-tier）
**3.3 Content Coding Framework**
- 这个brief中你没详细说，但你需要说：帖子怎么分类？什么是"赞成"vs"批评"？
- 这决定了你的CSV columns

## Findings

### 1. Dataset Overview

206 posts were collected from Xiaohongshu using the xiaohongshu-cli tool across three keyword searches ("迪奥 马面裙", "文化挪用", "#迪奥马面裙"). After binary relevance screening, 196 posts (95.1%) were included in the analysis. The remaining 10 irrelevant posts were advertisements, unrelated fashion content, or off-topic mentions. The data spans July 2022 to December 2025.

---

### 2. Yearly Distribution

|Year|Total|Relevant|Irrelevant|
|---|---|---|---|
|2022|37|37|0|
|2023|8|8|0|
|2024|53|52|1|
|2025|70|68|2|
|No date|38|31|7|

2022 produced an initial spike (37 posts) driven by the controversy's outbreak in July (18 posts in July alone, 12 in August, then a sharp drop to 4 in September and near-zero through the rest of the year). 2023 saw a dramatic collapse to just 8 posts across the entire year. From 2024, post volume rebounded to 52 relevant posts, rising further to 68 in 2025. This suggests that the topic did not disappear but underwent a transformation: the Dior controversy itself was largely forgotten, but the _mǎmiànqún_ as a cultural object became a persistent topic of discussion in its own right.

---

### 3. Thematic Distribution

#### 3.1 Overall (n=196)

|Theme|Count|%|
|---|---|---|
|Other|113|57.7%|
|Plagiarism Accusation|56|28.6%|
|National Pride|15|7.7%|
|Cultural Appropriation|7|3.6%|
|Commercial Critique|5|2.6%|

#### 3.2 Thematic Shift by Year

|Theme|2022|2023|2024|2025|
|---|---|---|---|---|
|Other|4 (10.8%)|2 (25.0%)|30 (57.7%)|54 (79.4%)|
|Plagiarism Accusation|32 (86.5%)|5 (62.5%)|10 (19.2%)|5 (7.4%)|
|National Pride|0|0|9 (17.3%)|5 (7.4%)|
|Cultural Appropriation|1 (2.7%)|1 (12.5%)|2 (3.8%)|2 (2.9%)|
|Commercial Critique|0|0|1 (1.9%)|2 (2.9%)|

The thematic shift is stark. In 2022, Plagiarism Accusation dominated at 86.5%, with "Other" accounting for only 10.8%. By 2025, these proportions were reversed: "Other" reached 79.4% while Plagiarism Accusation collapsed to 7.4%. National Pride, entirely absent in 2022 and 2023, emerged in 2024 (17.3%) and persisted into 2025 (7.4%). The controversy began as a confrontation with Dior and ended as a celebration of Hanfu.

#### 3.3 Thematic Engagement

|Theme|n|Mean Likes|Median Likes|Mean Comments|Median Comments|Mean Collected|Mean Shared|
|---|---|---|---|---|---|---|---|
|Other|113|1,175|107|56|5|292|77|
|Plagiarism Accusation|56|1,496|105|50|14|128|52|
|National Pride|15|518|116|41|7|245|113|
|Cultural Appropriation|7|1,259|1,040|106|30|189|89|
|Commercial Critique|5|189|95|6|2|94|10|

Plagiarism Accusation posts drew the highest mean likes (1,496), confirming that morally charged content attracts more immediate engagement. However, National Pride posts had the highest mean shares (113), suggesting that positive cultural content is more likely to be forwarded to others, extending beyond the platform. Cultural Appropriation posts, though fewest in number (n=7), had the highest median likes (1,040) and mean comments (106), indicating that this more analytical frame attracted consistently engaged audiences. Commercial Critique posts were marginal across all engagement metrics.

---

### 4. Sentiment Distribution

#### 4.1 Overall (n=196)

| Sentiment  | Count | %     |
| ---------- | ----- | ----- |
| Neutral    | 96    | 49.0% |
| Critical   | 50    | 25.5% |
| Supportive | 37    | 18.9% |
| Confused   | 13    | 6.6%  |

#### 4.2 Sentiment Shift by Year

|Sentiment|2022|2023|2024|2025|
|---|---|---|---|---|
|Neutral|5 (13.5%)|1 (12.5%)|26 (50.0%)|44 (64.7%)|
|Critical|29 (78.4%)|3 (37.5%)|11 (21.2%)|5 (7.4%)|
|Supportive|2 (5.4%)|3 (37.5%)|13 (25.0%)|15 (22.1%)|
|Confused|1 (2.7%)|1 (12.5%)|2 (3.8%)|4 (5.9%)|

In 2022, 78.4% of posts were Critical and only 13.5% Neutral. By 2025, these proportions had inverted: 64.7% Neutral and only 7.4% Critical. Supportive sentiment rose from 5.4% in 2022 to 22.1% in 2025. The emotional temperature of the discourse declined dramatically over three years.

#### 4.3 Sentiment Engagement

|Sentiment|n|Mean Likes|Median Likes|Mean Comments|Mean Collected|Mean Shared|
|---|---|---|---|---|---|---|
|Critical|50|1,587|130|54|144|54|
|Supportive|37|1,342|116|51|314|116|
|Neutral|96|1,037|129|55|272|70|
|Confused|13|417|35|53|49|19|

Critical posts attracted the highest mean likes (1,587), but Supportive posts had the highest mean collected (314) and mean shared (116). This divergence reveals two distinct engagement logics: Critical content provokes immediate reaction (like), while Supportive content provokes preservation and dissemination (collect and share). Users bookmark and forward content that celebrates Hanfu; they like but do not save content that criticises Dior. Confused posts had the lowest engagement across all metrics.

---

### 5. Engagement Metrics

#### 5.1 Overall (n=196)

|Metric|Mean|Median|Min|Max|Std Dev|Total|
|---|---|---|---|---|---|---|
|Likes|1,194|112|2|19,425|3,082|234,014|
|Comments|54|6|0|1,812|160|10,554|
|Collected|233|31|0|5,106|609|45,623|
|Shared|71|12|0|1,674|187|13,921|

The extreme gap between mean and median across all metrics (likes: 1,194 vs 112; comments: 54 vs 6) confirms a long-tail distribution where a small number of viral posts account for the majority of total engagement.

#### 5.2 Yearly Engagement Trends

|Year|n|Mean Likes|Median Likes|Mean Comments|Median Comments|
|---|---|---|---|---|---|
|2022|37|1,764|440|53|21|
|2023|8|1,759|1,465|94|27|
|2024|52|1,204|104|90|9|
|2025|68|1,207|110|39|5|

Median likes dropped from 440 in 2022 to 104-110 in 2024-2025. Median comments fell even more sharply, from 21 in 2022 to 5 in 2025. While post volume increased, per-post engagement declined, indicating that later posts reached smaller audiences. This is consistent with algorithmic decay: as the topic aged, the platform's recommendation algorithm gave it less visibility.

#### 5.3 Engagement Ratios

|Ratio|Overall|2022|2023|2024|2025|
|---|---|---|---|---|---|
|Comment/Like|4.5%|3.0%|5.4%|7.5%|3.2%|
|Collected/Like|19.5%|9.5%|14.5%|23.6%|24.9%|
|Shared/Like|5.9%|3.7%|2.8%|7.2%|7.0%|

The collected-to-like ratio nearly tripled from 9.5% (2022) to 24.9% (2025). This shift is significant: in 2022, users engaged primarily through likes (quick reaction); by 2025, users increasingly collected posts (bookmarking for later reference). This suggests a transformation in engagement mode from reactive consumption to active curation. Users were treating _mǎmiànqún_ content as reference material, saving it for personal use, fashion inspiration, or cultural knowledge.

#### 5.4 Decentralisation

Of 196 relevant posts, only 4 authors appeared more than once (@小红薯68CE673A, @Fashion Area, @咩咕拉斯, @Ran.), each contributing exactly 2 posts. Decentralisation Index: 98.0%.

---

### 6. Content Length and Engagement

|Category|n|Mean Likes|Median Likes|
|---|---|---|---|
|Short posts (≤254 chars)|98|1,412|153|
|Long posts (>254 chars)|98|976|103|

Median content length: 254 characters. The top 10 most-liked posts averaged 234 characters, shorter than the overall mean of 325. Correlation between content length and likes: -0.104 (weak negative). Correlation between content length and comments: -0.075.

Shorter posts attracted higher engagement. This is consistent with platform affordances: Xiaohongshu's visual-first, scroll-heavy interface rewards punchy, immediately legible content over long-form analysis. The implication is that the posts driving the most engagement in terms of likes were not the most analytically rich, but the most emotionally compressed.

---

### 7. Highest and Lowest Engagement Posts

#### 7.1 Top 5 by Likes

|Date|Likes|Comments|Collected|Shared|Theme|Sentiment|Title|
|---|---|---|---|---|---|---|---|
|2022-09-13|19,425|180|814|41|Plagiarism|Critical|女人只能侧骑的文化，怎敢抢我们马面裙？！|
|2025-03-22|18,805|408|872|233|Other|Supportive|迪奥又闹笑话|
|2025-07-20|17,986|365|4,326|958|Other|Neutral|实物美得无以复加|
|2025-08-06|14,557|295|5,106|1,674|Other|Supportive|"百年前，我爱过一只东方来的金孔雀"|
|2024-05-16|12,863|325|192|193|Plagiarism|Critical|给这位着马面裙"Not Dior" 男生手动点赞|

The top-liked post (19,425 likes) was from 2022, critical in tone, with an emotionally charged title. But three of the top five were from 2024-2025 and categorised as "Other" or Supportive, focusing on Hanfu aesthetics rather than Dior criticism. The highest-collected post ("百年前，我爱过一只东方来的金孔雀", 5,106 collections) was a Supportive "Other" post celebrating the beauty of the garment, not criticising Dior.

#### 7.2 Top 5 by Comments

|Date|Likes|Comments|Theme|Sentiment|Title|
|---|---|---|---|---|---|
|2024-05-07|12,511|1,812|Other|Neutral|穿马面裙拍毕业照最大的弊端出现了|
|2024-03-16|1,300|710|Other|Neutral|千万不要穿马面裙去迪士尼！！|
|2023-11-23|3,837|493|Cultural Appropriation|Confused|在大英博物馆穿马面被问为什么要穿这个|
|2024-03-16|833|447|Other|Supportive|关于马面裙...|
|2025-03-22|18,805|408|Other|Supportive|迪奥又闹笑话|

The most-commented post (1,812 comments) was neutral, about wearing _mǎmiànqún_ to graduation photos. The second most-commented (710) was about wearing it to Disneyland. Neither was about Dior. This demonstrates that the posts generating the most discussion were experiential and lifestyle-oriented, not political or confrontational. Genuine dialogue was provoked by shared experience, not by outrage.

#### 7.3 Bottom 5 by Likes

The five least-liked posts (2-3 likes each) were all categorised as Other/Neutral, with no date metadata. They included a design sketch, a Disneyland outfit post, and a brief mention of Dior's 2026 collection. These posts had no emotional charge and no cultural argument, suggesting that purely functional or informational content attracted minimal attention.

---

### 8. Conclusions

#### Conclusion 1: Who imagines? Everyone, equally.

The Decentralisation Index of 98.0% demonstrates that national imagination on Xiaohongshu was a genuinely bottom-up process. No single influencer, opinion leader, or institutional account drove the discussion. Each of the 196 posts represented a distinct individual contributing to a shared discursive space. This is the digital equivalent of what Anderson (1983) described as horizontal solidarity among strangers: a community imagined not through elite direction but through the simultaneous, parallel participation of ordinary people. The platform's algorithmic structure, which promotes content discovery over follower-based amplification, facilitated this democratic participation in ways that Anderson's original print capitalism framework could not have anticipated.

#### Conclusion 2: How do they imagine? Rationally, not angrily.

49.0% of posts were Neutral in sentiment, and only 25.5% were Critical. But the yearly trend reveals a deeper pattern. In 2022, 78.4% of posts were Critical; by 2025, this had fallen to 7.4%, while Neutral rose from 13.5% to 64.7%. The initial outrage was intense but brief. What replaced it was not silence or indifference but sustained, analytical engagement with traditional culture. This is precisely the dynamic Billig (1995) identifies in banal nationalism: national consciousness is maintained not through dramatic episodes of collective emotion but through mundane, everyday cultural practices. The data shows this transition happening in real time across three years. The median comment count falling from 21 (2022) to 5 (2025) while post volume tripled further confirms that the mode of engagement shifted from active debate to quiet consumption and curation.

#### Conclusion 3: What do they imagine? Not the enemy, but themselves.

The thematic shift from Plagiarism Accusation (86.5% in 2022) to Other (79.4% in 2025) demonstrates that the object of national imagination changed. Early discourse was oriented outward: what did Dior do wrong, and how should China respond? Later discourse was oriented inward: how beautiful is the _mǎmiànqún_, how should it be worn, and what does it mean for Chinese cultural identity? The engagement data reinforces this. Critical posts attracted the most likes (mean 1,587), but Supportive posts attracted the most collections (mean 314) and shares (mean 116). Users clicked "like" on anger, but they saved and forwarded pride. The collected-to-like ratio nearly tripling from 9.5% (2022) to 24.9% (2025) quantifies this shift: by 2025, users were treating _mǎmiànqún_ content as cultural knowledge to be preserved, not outrage to be amplified.

This answers the problematique directly. Ordinary internet users participate in the construction of the imagined community not primarily through confrontation with external threats, but through the positive, everyday, embodied practice of wearing, photographing, discussing, saving, and sharing traditional clothing. The nation is not imagined against Dior. The nation is imagined through Hanfu. The imagined community is worn.



## 📋 数据到论文的映射表

|Findings 部分|需要的数据|对应图表|对应CSV列|
|---|---|---|---|
|4.1 主题分布|Theme 频数统计|A + F|Theme|
|4.2 情感倾向|Sentiment频数 + Theme×Sentiment|B + C|Sentiment, Theme|
|4.3 参与度|Likes, Comments, Author重复度|D + E + H|Likes, Comments, Author|
|4.4 话语权|词频|G + 表格|Title, Content|
|4.5 时间维度|Date分组统计|F + 表格|Date, Theme, Sentiment|

