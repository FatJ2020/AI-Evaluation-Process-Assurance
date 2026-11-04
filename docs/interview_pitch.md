# AEPA — 60–90 second pitch

## English

Most portfolios stop at “is the model output good?”  
I also treat the evaluation process as something that can fail — the same way manufacturing treats measurement systems and process steps.

AEPA is a small rule-based prototype. It reads synthetic review-session records, flags evaluation-side risks such as position bias, length bias, untagged hard faults, unstable gates, and unverified agent artifacts, then assigns a severity band and a recommendation: accept, re-review, or hold batch.

It pairs with my other work: evaluating industrial answers, governing operational AI decisions, and gating agent releases. The shared idea is simple: critical process failures should not be hidden by averages, and humans remain accountable.

Synthetic data only; transparent rules; not a certification.

## 中文要点

多数作品集只问模型输出好不好。  
我把「评测过程」也当成会失效的对象——类似制造里对测量系统与工序的管理。

AEPA 用规则检查合成评测会话：位置偏差、长度偏差、硬伤未标记、门禁不稳定、Agent 结果未核实等，给出 H/M/L 与 accept / re-review / hold。

与另外三个项目一起：评回答、治决策、管 Agent 发布、保评测过程。合成数据；规则透明；不是认证。
