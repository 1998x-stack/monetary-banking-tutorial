(function(){
const explanations={
  transmission:{
    interest:"利率渠道：政策利率影响市场利率和融资定价，进而改变消费、投资与资产估值。传导通常存在时滞，也会受到风险溢价和银行定价影响。",
    credit:"信贷渠道：政策改变银行资金成本、风险偏好与借款人资产负债表，影响贷款可得性；它不等同于央行直接决定每一笔贷款。",
    exchange:"汇率渠道：利差与预期可能改变跨境资本流动和汇率，再影响进口价格、出口竞争力与外币债务负担。",
    expectations:"预期渠道：央行沟通影响公众对未来通胀、利率和经济活动的判断；可信度与政策行动的一致性很重要。"
  },
  moneyFunction:{
    account:"价值尺度：用同一计价单位表达商品、服务和债务的价格，让不同交易可以比较。",
    exchange:"交易媒介：买方用货币支付，卖方不必恰好想要买方手里的商品，降低物物交换的匹配成本。",
    store:"价值贮藏：把当前购买力转移到未来。能否保值取决于通胀、信用、流动性和制度稳定。",
    payment:"支付手段：用于清偿延期支付的债务，例如工资结算、贷款本息和赊销货款。",
    world:"世界货币：在跨境贸易、储备和国际结算中被广泛接受的货币或国际储备资产。"
  },
  regimes:{
    fixed:"固定或盯住汇率：降低短期汇率不确定性，但需要储备、政策一致性和可信承诺；资本流动较自由时，国内利率自主空间会受约束。",
    floating:"浮动汇率：汇率可吸收部分外部冲击，货币政策自主性通常更大，但汇率波动会影响贸易、通胀和外币债务。浮动并不意味着央行从不干预。"
  }
};
document.querySelectorAll('[data-demo="transmission"]').forEach(box=>{const out=box.querySelector("[data-demo-output]");box.querySelectorAll("button[data-channel]").forEach(btn=>btn.addEventListener("click",()=>{box.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed",String(b===btn)));out.textContent=explanations.transmission[btn.dataset.channel]}))});
document.querySelectorAll('[data-demo="money-functions"]').forEach(box=>{const out=box.querySelector("[data-demo-output]");box.querySelectorAll("button[data-function]").forEach(btn=>btn.addEventListener("click",()=>{box.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed",String(b===btn)));out.textContent=explanations.moneyFunction[btn.dataset.function]}))});
document.querySelectorAll('[data-demo="aggregate-classifier"]').forEach(box=>{const select=box.querySelector("select");const out=box.querySelector("[data-demo-output]");const map={cash:"M0、M1、M2。流通中现金属于最狭义货币。",corp_demand:"M1、M2。单位活期存款在中国现行口径中属于狭义货币。",household_demand:"自 2025 年 1 月起纳入 M1，同时属于 M2。",payment_reserve:"自 2025 年 1 月起，非银行支付机构客户备付金纳入 M1，同时属于 M2。",term_deposit:"属于 M2，但不属于 M1。",stock:"股票是金融资产，不是 M1/M2 货币余额。"};function update(){out.textContent=map[select.value]||"请选择一种金融工具。"}select.addEventListener("change",update);update()});
document.querySelectorAll('[data-demo="regimes"]').forEach(box=>{const out=box.querySelector("[data-demo-output]");box.querySelectorAll("button[data-regime]").forEach(btn=>btn.addEventListener("click",()=>{box.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed",String(b===btn)));out.textContent=explanations.regimes[btn.dataset.regime]}))});
document.querySelectorAll('[data-demo="expected-loss"]').forEach(box=>{const pd=box.querySelector('[name="pd"]'),lgd=box.querySelector('[name="lgd"]'),ead=box.querySelector('[name="ead"]'),out=box.querySelector("[data-demo-output]");const fmt=new Intl.NumberFormat("zh-CN",{style:"currency",currency:"CNY",maximumFractionDigits:0});function calc(){const p=Number(pd.value),l=Number(lgd.value),e=Number(ead.value);if(!Number.isFinite(p)||!Number.isFinite(l)||!Number.isFinite(e)||p<0||p>100||l<0||l>100||e<0){out.textContent="请输入有效数值：PD 和 LGD 为 0–100%，EAD 不得小于 0。";return}out.textContent="预期损失 = "+p.toFixed(2)+"% × "+l.toFixed(2)+"% × "+fmt.format(e)+" = "+fmt.format(e*p/100*l/100)+"。这是参数化估计，不是对某笔贷款损失的确定预测。"}[pd,lgd,ead].forEach(el=>el.addEventListener("input",calc));calc()});
})();