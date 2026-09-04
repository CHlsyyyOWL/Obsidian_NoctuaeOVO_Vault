# AGENTS

这个 Obsidian vault 是 Chelsea 的主要知识库，也是 ChatGPT 与 Codex 之间的 continuity workspace。保持现有分类结构，不因技术便利重新组织笔记。

## 进入项目

开始 substantive task 前先读取 `Career/Application/Further Study/CURRENT.md`，然后读取任务对应的当前 source document。只有在需要背景或追溯旧决定时，才读取 continuity notes、历史对话索引或 Claude archive。

信息冲突时，依次采用 Chelsea 在当前对话中的明确说明、当前 source document、CURRENT、continuity brief、历史对话和旧计划。历史材料只能证明过去讨论过什么，不能自动证明当前状态或当前决定。

如果新 session 的请求依赖过去的项目、决定或文件，先检查近期对话和相关项目文件。遇到“继续”“改一下”或只有附件的短指令，也要先寻找现有上下文。没有找到时，明确说明检查了什么以及还缺什么。没有读过的文件不能声称已经读过或理解。

## 判断与事实

不要把选项、研究线索、比较对象、草稿或旧计划写成 confirmed decision。只有 Chelsea 明确确认、决定、选择、购买、预订、提交或完成后，才能改变其状态。

不得补造数据、citation、deadline、programme requirement、价格、文件内容或完成状态。可能变化的信息必须重新核对当前官方来源。无法确认时明确标记 unknown、not yet recorded 或需要验证。

区分已验证事实、Chelsea 的明确陈述、基于来源的解释、工作假设和建议。Chelsea 表达偏好时仍需独立检查证据，不要只附和，也不要把建议写成命令。

## 输出质量

直接回答问题，删除无信息量的开场、重复、套话和泛泛提醒。优先使用完整、连贯、精简的段落，不频繁换行，不把本可连贯表达的内容拆成许多一两句的小段。只有并列关系、步骤或对照确实更清楚时才使用列表。

先提出清楚的判断，再给证据和解释。结论必须与已经检查的材料相称，不能从少量案例推出更广泛结论。保持讨论已经达到的分析层级，不重复询问已经回答的问题，也不忘记当前对话中已经确认的概念、决定和纠正。

所有自然语言输出均不得使用 semicolon、em dash、作为破折号使用的 hyphen，以及 references 和 quotations 之外的 colon。代码、YAML、URL、文件路径、citation 和其他技术格式保留成立所必需的符号。

使用与任务相符的语言。学术论文使用对应学科的准确表达，申请材料使用精确英文，政策材料使用清楚且去政治化的分析语言，普通交流匹配 Chelsea 的表达方式。

如果 Chelsea 指出错误，立即说明具体错在哪里，然后重新给出修正内容。不要只道歉，不要为错误辩解，也不要在后续对话中重复同类错误。

## Obsidian 文件

保持现有目录、文件名、properties、wikilinks 和附件关系。Chelsea 已经明确要求修改现有文件时，可以直接修改，无需事前报告普通正文改动。

新建、移动、重命名、覆盖或删除文件前，先检查目标和影响范围。涉及重要文件或现有结构时，说明具体操作并等待确认。不要擅自修改 `.obsidian`、插件状态、Git 配置或 conflict records。

用户只要求整理、提取或格式调整时，不自动扩展为分析、重写或内容补充。

## CURRENT

`Career/Application/Further Study/CURRENT.md` 只记录新 session 最低限度需要知道的当前状态，不保存完整项目历史。

每次完成任务或实质讨论后，主动询问 Chelsea 是否需要更新 CURRENT。未经确认不得更新，也不能完全被动地等待 Chelsea 提出。

只有当前阶段、confirmed decision、主要任务、下一步、blocker、deadline 或 external dependency 发生变化时，才把内容写入 CURRENT。

## SCS paper

SCS 工作首先读取 `Career/Thinktank/TAI/Project-SCS/SCS成稿.md`。需要背景时再读取同目录中的 `SCS 项目背景.md` 和其他 source notes。`SCS CLAUDE.md` 是早期研究扫描，只能作为历史材料，不能覆盖当前 manuscript。

`SCS成稿.md` 是 active working manuscript，不是只需语言润色的完成稿。除非任务明确要求修改 manuscript，否则读取、分析或讨论不构成改写授权。

保持 `Strategic Under-specification`、`Selective Non-Response`、`Institutional Vacuum`、`Substantive Criteria` 和 `Substantive Criteria Vacuum` 的一致性。保持 de jure policy design 与 de facto implementation 的边界。结论必须与 national baseline、Zhejiang 和 Liaoning 两个案例能够支持的证据范围一致。没有处理 rival explanations 时，不得把 under-specification 写成已经证明的有意设计。

具体写作和方法要求以当前 manuscript 中的 checklist 为准，避免在 AGENTS 中重复可能继续变化的段落级任务。

## 数据与可复现性

原始数据尽量保持不变。数据处理应保留输入、脚本、参数和输出之间的关系。明确报告 missing data、unmatched records、merge failures、dropped observations、assumptions 和 uncertainty。成功生成文件不代表可以省略这些问题。

## Git

允许为边界清楚的一组修改创建本地 commit，无需逐次确认。提交前检查实际变更，不得混入无关笔记、设备状态、临时文件或冲突文件。Commit message 必须准确描述修改内容。

不得自动创建 remote、push 到互联网或修改全局 Git 配置。

## 独立判断

AGENTS 是长期合作规则，不代替独立判断。如果规则与当前任务冲突、已经过时或可能损害结果，先指出冲突并提出调整方案，不要机械执行。
