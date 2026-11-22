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

const money=new Intl.NumberFormat("zh-CN",{maximumFractionDigits:2});
const yuan=new Intl.NumberFormat("zh-CN",{style:"currency",currency:"CNY",maximumFractionDigits:2});
document.querySelectorAll('[data-demo="fisher"]').forEach(box=>{const nominal=box.querySelector('[name="nominal"]'),inflation=box.querySelector('[name="inflation"]'),out=box.querySelector("[data-demo-output]");function calc(){const i=Number(nominal.value)/100,p=Number(inflation.value)/100;if(!Number.isFinite(i)||!Number.isFinite(p)||i<=-1||p<=-1){out.textContent="请输入大于 -100% 的有效利率和通胀率。";return}const exact=(1+i)/(1+p)-1,approx=i-p;out.textContent="精确实际利率约 "+(exact*100).toFixed(2)+"%；近似值 "+(approx*100).toFixed(2)+"%。两者差异来自复利交叉项。"}[nominal,inflation].forEach(x=>x.addEventListener("input",calc));calc()});
document.querySelectorAll('[data-demo="yield-curve"]').forEach(box=>{const out=box.querySelector("[data-demo-output]");const copy={normal:"向上倾斜：长期收益率高于短期收益率，可能同时反映未来短端预期和期限溢价。",flat:"平坦：长短端收益率接近，可能对应短端预期与期限溢价的组合趋于平缓；不等于经济必然停滞。",inverted:"倒挂：部分短端收益率高于长端，常与市场预期未来短期利率下降有关；它是风险信号，不是衰退日期预报。"};box.querySelectorAll("button[data-shape]").forEach(btn=>btn.addEventListener("click",()=>{box.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed",String(b===btn)));out.textContent=copy[btn.dataset.shape]}))});
document.querySelectorAll('[data-demo="nim"]').forEach(box=>{const income=box.querySelector('[name="interest-income"]'),expense=box.querySelector('[name="interest-expense"]'),assets=box.querySelector('[name="earning-assets"]'),out=box.querySelector("[data-demo-output]");function calc(){const a=Number(income.value),b=Number(expense.value),c=Number(assets.value);if(![a,b,c].every(Number.isFinite)||a<0||b<0||c<=0){out.textContent="请输入非负利息收入、非负利息支出和大于零的平均生息资产。";return}const nii=a-b;out.textContent="净利息收入 "+money.format(nii)+" 亿元；NIM = "+(nii/c*100).toFixed(2)+"%。该简化结果未计税费、减值和非利息项目。"}[income,expense,assets].forEach(x=>x.addEventListener("input",calc));calc()});
document.querySelectorAll('[data-demo="capital-ratio"]').forEach(box=>{const capital=box.querySelector('[name="cet1"]'),rwa=box.querySelector('[name="rwa"]'),out=box.querySelector("[data-demo-output]");function calc(){const c=Number(capital.value),r=Number(rwa.value);if(!Number.isFinite(c)||!Number.isFinite(r)||c<0||r<=0){out.textContent="请输入非负 CET1 资本和大于零的风险加权资产。";return}const ratio=c/r*100;const status=ratio<4.5?"低于 4.5% 的巴塞尔最低基准。":ratio<7?"达到 4.5% 最低基准，但低于含 2.5% 留存缓冲的 7.0% 基准。":"达到 4.5% 最低基准及含 2.5% 留存缓冲的 7.0% 基准。";out.textContent="CET1 比率 = "+ratio.toFixed(2)+"%；"+status+" 未计系统重要性银行、逆周期缓冲或本地附加要求。"}[capital,rwa].forEach(x=>x.addEventListener("input",calc));calc()});
document.querySelectorAll('[data-demo="central-bank"]').forEach(box=>{const out=box.querySelector("[data-demo-output]");const text={buy:"买入证券：央行资产端证券增加，负债端银行准备金通常增加。若卖方为非银行机构，结算还可能同时增加其银行存款。",repo:"逆回购投放：央行通过有期限的回购安排向交易对手提供资金，银行体系准备金通常暂时增加；到期时资金回笼。",drain:"回笼流动性：央行通过正回购、发行央票或其他吸收流动性的操作，通常使银行体系准备金暂时减少。"};box.querySelectorAll("button[data-operation]").forEach(btn=>btn.addEventListener("click",()=>{box.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed",String(b===btn)));out.textContent=text[btn.dataset.operation]}))});
document.querySelectorAll('[data-demo="repo-cost"]').forEach(box=>{const principal=box.querySelector('[name="principal"]'),rate=box.querySelector('[name="rate"]'),days=box.querySelector('[name="days"]'),out=box.querySelector("[data-demo-output]");function calc(){const p=Number(principal.value),r=Number(rate.value),d=Number(days.value);if(![p,r,d].every(Number.isFinite)||p<0||r<0||d<=0){out.textContent="请输入非负本金、非负利率和正的占款天数。";return}const cost=p*r/100*d/365;out.textContent="按 ACT/365 简化计息：利息约 "+yuan.format(cost)+"；到期偿还约 "+yuan.format(p+cost)+"。实际合同的日数基准和费用可能不同。"}[principal,rate,days].forEach(x=>x.addEventListener("input",calc));calc()});
document.querySelectorAll('[data-demo="bond-price"]').forEach(box=>{const face=box.querySelector('[name="face"]'),coupon=box.querySelector('[name="coupon"]'),yieldInput=box.querySelector('[name="yield"]'),years=box.querySelector('[name="years"]'),out=box.querySelector("[data-demo-output]");function calc(){const f=Number(face.value),c=Number(coupon.value)/100,y=Number(yieldInput.value)/100,n=Number(years.value);if(![f,c,y,n].every(Number.isFinite)||f<0||c<0||y<=-1||n<1||n>50||!Number.isInteger(n)){out.textContent="请输入有效面值、非负票息、收益率大于 -100% 和 1–50 的整数年限。";return}let price=0;for(let t=1;t<=n;t++)price+=f*c/Math.pow(1+y,t);price+=f/Math.pow(1+y,n);const state=Math.abs(price-f)<0.005?"接近平价":price>f?"溢价":"折价";out.textContent="理论价格约 "+yuan.format(price)+"；"+state+"。当市场收益率高于票面利率时，固定票息债券通常折价交易。"}[face,coupon,yieldInput,years].forEach(x=>x.addEventListener("input",calc));calc()});
document.querySelectorAll('[data-demo="fx-parity"]').forEach(box=>{const usd=box.querySelector('[name="usd"]'),spot=box.querySelector('[name="spot"]'),domestic=box.querySelector('[name="domestic-rate"]'),foreign=box.querySelector('[name="foreign-rate"]'),out=box.querySelector("[data-demo-output]");function calc(){const u=Number(usd.value),s=Number(spot.value),rd=Number(domestic.value)/100,rf=Number(foreign.value)/100;if(![u,s,rd,rf].every(Number.isFinite)||u<0||s<=0||rd<=-1||rf<=-1){out.textContent="请输入非负美元金额、正即期汇率以及大于 -100% 的利率。";return}const amount=u*s,forward=s*(1+rd)/(1+rf);out.textContent="即期兑换成本 "+yuan.format(amount)+"；CIP 理论一年期远期汇率约 "+forward.toFixed(4)+" CNY/USD。理论值忽略交易成本、基差、信用与资本约束。"}[usd,spot,domestic,foreign].forEach(x=>x.addEventListener("input",calc));calc()});


document.querySelectorAll('[data-demo="nbfi-risk"]').forEach(box=>{const out=box.querySelector("[data-demo-output]");const text={liquidity:"赎回压力：投资者集中赎回，基金需要出售资产或动用现金；若底层资产交易不活跃，折价出售可能压低净值并诱发更多赎回。",leverage:"杠杆与保证金：资产价格下跌会降低抵押品价值，融资方可能提高折扣或追加保证金；机构若快速卖出资产筹集现金，市场价格可能进一步承压。",linkage:"机构关联：银行授信、回购融资、共同持仓和托管服务把银行与非银行机构连接起来；一方资产出售或融资中断，可能通过价格和抵押品传给另一方。"};box.querySelectorAll("button[data-risk]").forEach(btn=>btn.addEventListener("click",()=>{box.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed",String(b===btn)));out.textContent=text[btn.dataset.risk]}))});
document.querySelectorAll('[data-demo="money-multiplier"]').forEach(box=>{const c=box.querySelector('[name="currency-ratio"]'),rr=box.querySelector('[name="reserve-ratio"]'),e=box.querySelector('[name="excess-ratio"]'),base=box.querySelector('[name="base-money"]'),out=box.querySelector("[data-demo-output]");function calc(){const cv=Number(c.value)/100,rv=Number(rr.value)/100,ev=Number(e.value)/100,bv=Number(base.value),den=cv+rv+ev;if(![cv,rv,ev,bv].every(Number.isFinite)||cv<0||rv<0||ev<0||bv<0||den<=0){out.textContent="请输入非负比率和基础货币；现金、法定准备金与超额准备金比率之和必须大于零。";return}const m=(1+cv)/den;out.textContent="乘数约 "+m.toFixed(2)+"；模型货币量约 "+(m*bv).toFixed(2)+" 个单位。该结果依赖固定比率假设，不是现实银行贷款的自动倍数。"}[c,rr,e,base].forEach(x=>x.addEventListener("input",calc));calc()});
document.querySelectorAll('[data-demo="money-demand"]').forEach(box=>{const y=box.querySelector('[name="income"]'),i=box.querySelector('[name="interest-rate"]'),a=box.querySelector('[name="income-sensitivity"]'),b=box.querySelector('[name="rate-sensitivity"]'),out=box.querySelector("[data-demo-output]");function calc(){const vals=[y,i,a,b].map(x=>Number(x.value));const [Y,I,A,B]=vals;if(!vals.every(Number.isFinite)||Y<0||I<0||A<0||B<0){out.textContent="请输入非负收入、利率和敏感度参数。";return}const demand=A*Y-B*I;if(demand<0){out.textContent="当前参数会产生负的线性需求值；请降低利率敏感度或提高收入系数。";return}out.textContent="实际货币需求约为 "+demand.toFixed(2)+" 个单位。提高收入会增加需求，提高利率会按该教学函数减少需求。"}[y,i,a,b].forEach(x=>x.addEventListener("input",calc));calc()});
document.querySelectorAll('[data-demo="policy-tools"]').forEach(box=>{const out=box.querySelector("[data-demo-output]");const text={rate:"调整政策利率：改变短期资金价格信号，影响货币市场利率、存贷款定价和资产估值；它并不直接决定每笔贷款的实际利率。",omo:"开展逆回购：央行通过有期限的回购交易向交易对手提供资金，银行体系准备金通常暂时增加；到期时资金按约定回笼。",rrr:"调整准备金率：改变存款类机构的法定准备金需求和可用流动性空间；信贷结果仍取决于资本、风险、资金需求与银行决策。",targeted:"结构性再贷款：央行按规则向符合条件的机构提供资金或激励，引导其支持特定领域；需要检查资金是否到达目标部门以及风险如何承担。"};box.querySelectorAll("button[data-tool]").forEach(btn=>btn.addEventListener("click",()=>{box.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed",String(b===btn)));out.textContent=text[btn.dataset.tool]}))});
document.querySelectorAll('[data-demo="transmission-lab"]').forEach(box=>{const out=box.querySelector("[data-demo-output]");const text={interest:"利率渠道：检查货币市场、债券和银行贷款利率是否跟随政策变化；再观察浮动与固定利率合同的重定价速度，以及家庭和企业的支出响应。",credit:"信贷渠道：检查银行资本、融资成本、风险偏好和借款人抵押品；贷款可得性可能放大或抵消政策利率变化。",asset:"资产价格渠道：观察债券、住房和股票估值如何改变家庭财富、企业净资产和抵押品价值；价格上涨不必然转化为新增实体投资。",exchange:"汇率渠道：观察利差、资本流动预期和外币融资如何影响汇率，再分析进口价格、出口需求和外币债务的本币负担。",expectations:"预期渠道：观察企业定价、工资谈判和家庭消费计划是否调整；政策沟通只有在可信且与行动一致时才更容易影响长期预期。"};box.querySelectorAll("button[data-channel]").forEach(btn=>btn.addEventListener("click",()=>{box.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed",String(b===btn)));out.textContent=text[btn.dataset.channel]}))});
document.querySelectorAll('[data-demo="islm"]').forEach(box=>{const g=box.querySelector('[name="government-spending"]'),m=box.querySelector('[name="real-money"]'),out=box.querySelector("[data-demo-output]");function calc(){const G=Number(g.value),M=Number(m.value);if(!Number.isFinite(G)||!Number.isFinite(M)||G<0||M<=0){out.textContent="请输入非负政府购买和大于零的实际货币供给。";return}const c=.8,C0=20,T=20,I0=30,b=10,k=.5,h=20,A=C0-c*T+I0+G;const Y=(A+b*M/h)/((1-c)+b*k/h),r=(k*Y-M)/h;if(!Number.isFinite(Y)||!Number.isFinite(r)){out.textContent="参数无法得到有效均衡。";return}out.textContent="均衡产出 Y≈"+Y.toFixed(1)+"；均衡利率 r≈"+r.toFixed(2)+"。该线性结果基于封闭经济、固定价格和给定行为参数。"}[g,m].forEach(x=>x.addEventListener("input",calc));calc()});
document.querySelectorAll('[data-demo="inflation-rate"]').forEach(box=>{const p=box.querySelector('[name="previous-index"]'),c=box.querySelector('[name="current-index"]'),out=box.querySelector("[data-demo-output]");function calc(){const a=Number(p.value),b=Number(c.value);if(!Number.isFinite(a)||!Number.isFinite(b)||a<=0||b<=0){out.textContent="请输入大于零的价格指数。";return}const rate=(b/a-1)*100;out.textContent="累计通胀率为 "+rate.toFixed(2)+"%。指数从 "+a.toFixed(2)+" 变为 "+b.toFixed(2)+"，价格水平"+(rate>=0?"上升":"下降")+Math.abs(rate).toFixed(2)+"%。"}[p,c].forEach(x=>x.addEventListener("input",calc));calc()});
document.querySelectorAll('[data-demo="deflation"]').forEach(box=>{const i=box.querySelector('[name="nominal-rate"]'),pi=box.querySelector('[name="expected-inflation"]'),d=box.querySelector('[name="nominal-debt"]'),out=box.querySelector("[data-demo-output]");function calc(){const I=Number(i.value),P=Number(pi.value),D=Number(d.value);if(![I,P,D].every(Number.isFinite)||I<=-100||P<=-100||D<0){out.textContent="请输入大于 -100% 的利率与通胀率，以及非负名义债务。";return}const real=I-P,burden=D/(1+P/100);out.textContent="实际利率约 "+real.toFixed(2)+"%；若价格水平变化 "+P.toFixed(2)+"%，实际债务负担约为 "+burden.toFixed(2)+" 万个当前价格基期单位。这里使用费雪近似和固定名义本金。"}[i,pi,d].forEach(x=>x.addEventListener("input",calc));calc()});


document.querySelectorAll('[data-demo="crisis-leverage"]').forEach(box=>{
 const a=box.querySelector('[name="assets"]'),d=box.querySelector('[name="debt"]'),s=box.querySelector('[name="shock"]'),out=box.querySelector("[data-demo-output]");
 function update(){const A=Number(a.value),D=Number(d.value),shock=Number(s.value);
 if(![A,D,shock].every(Number.isFinite)||A<=0||D<0||D>=A||shock<0||shock>100){out.textContent="请输入大于负债的正资产、非负债务和 0–100% 的资产跌幅。";return;}
 const before=A-D,after=A*(1-shock/100)-D,loss=(before-after)/before*100;
 out.textContent="初始净资产 "+before.toFixed(2)+"；冲击后净资产 "+after.toFixed(2)+"；净资产损失 "+loss.toFixed(2)+"%。"+(after<0?" 该假设场景下净资产转负。":" 该结果是教学压力测试，不是未来价格预测。");
 }[a,d,s].forEach(x=>x.addEventListener("input",update));update();
});
document.querySelectorAll('[data-demo="report-reading"]').forEach(box=>{
 const out=box.querySelector("[data-demo-output]");
 const texts={
 action:"本次操作：例如“决定将政策利率调整至 X%”是已公布的政策决定；需要核对发布日期、适用对象和生效时间。",
 condition:"条件性表述：例如“根据经济形势变化适时采取措施”是政策反应的条件句，不保证某月必定行动。",
 projection:"成员预测：SEP 点阵图体现参与者各自假设下的判断，并非 FOMC 对未来政策的投票结果或承诺。",
 risk:"风险判断：例如“关注融资收紧风险”指出需监测的不确定性，不等于央行已经决定开展某项具体操作。"
 };
 box.querySelectorAll("button[data-kind]").forEach(btn=>btn.addEventListener("click",()=>{
 box.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed",String(b===btn)));
 out.textContent=texts[btn.dataset.kind];
 }));
});
document.querySelectorAll('[data-demo="fin-data-growth"]').forEach(box=>{
 const fields=["tsf-old","tsf-new","m2-old","m2-new"].map(n=>box.querySelector('[name="'+n+'"]')),out=box.querySelector("[data-demo-output]");
 function update(){const [to,tn,mo,mn]=fields.map(x=>Number(x.value));
 if(![to,tn,mo,mn].every(Number.isFinite)||to<=0||tn<=0||mo<=0||mn<=0){out.textContent="请为四个存量输入大于零的有效数字。";return;}
 const a=(tn/to-1)*100,b=(mn/mo-1)*100,diff=Math.abs(a-b)<1e-9?0:a-b;
 out.textContent="社融存量同比 "+a.toFixed(2)+"%；M2 同比 "+b.toFixed(2)+"%；增速差 "+diff.toFixed(2)+" 个百分点。差值本身不是资金供求缺口。";
 }fields.forEach(f=>f.addEventListener("input",update));update();
});
document.querySelectorAll('[data-demo="taylor-rule"]').forEach(box=>{
 const fields=["neutral-rate","inflation","target-inflation","output-gap"].map(n=>box.querySelector('[name="'+n+'"]')),out=box.querySelector("[data-demo-output]");
 function update(){const [r,p,target,gap]=fields.map(x=>Number(x.value));
 if(![r,p,target,gap].every(Number.isFinite)||Math.abs(r)>100||Math.abs(p)>100||Math.abs(target)>100||Math.abs(gap)>100){out.textContent="请输入合理范围内的有限数值（各参数绝对值不超过 100）。";return;}
 const rate=r+p+0.5*(p-target)+0.5*gap;
 out.textContent="简化泰勒规则名义利率 = "+rate.toFixed(2)+"%。这只是模型基准，不能当作央行决定。参数 r* 和产出缺口均需估计。";
 }fields.forEach(f=>f.addEventListener("input",update));update();
});
document.querySelectorAll('[data-demo="digital-money"]').forEach(box=>{
 const out=box.querySelector("[data-demo-output]");
 const texts={
 cash:"现钞：中央银行发行的货币，通常不计息；持有者需承担遗失、盗窃等实体保管风险。",
 deposit:"银行存款：商业银行对客户的存款负债；可能计息，适用的存款保险与账户规则须按所在司法辖区判断。",
 ecny:"银行实名 e-CNY 钱包：2026 年新框架对商业银行运营的相关钱包按存款负债管理，并规定计息、准备金和存款保险；不能推广到所有钱包类型。",
 stable:"法币稳定币：私人发行人依合同和监管安排对持有人承担相关义务；不因锚定法币就自动享有央行负债地位或存款保险。"
 };
 box.querySelectorAll("button[data-kind]").forEach(btn=>btn.addEventListener("click",()=>{
 box.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed",String(b===btn)));
 out.textContent=texts[btn.dataset.kind];
 }));
});
document.querySelectorAll('[data-demo="stablecoin-cover"]').forEach(box=>{
 const fields=["liabilities","reserves","haircut"].map(n=>box.querySelector('[name="'+n+'"]')),out=box.querySelector("[data-demo-output]");
 function update(){const [l,r,h]=fields.map(x=>Number(x.value));
 if(![l,r,h].every(Number.isFinite)||l<=0||r<0||h<0||h>100){out.textContent="请输入正负债、非负储备和 0–100% 的折价率。";return;}
 const stressed=r*(1-h/100),coverage=stressed/l*100;
 out.textContent="压力后储备价值 "+stressed.toFixed(2)+"，覆盖率 "+coverage.toFixed(2)+"%。"+(coverage<100?" 低于 100% 说明本简化场景下储备价值不足以覆盖全部面值负债，但不等于真实发行人必然违约。":" 该比率仅反映简化市值覆盖，不代表赎回流动性、托管安排或实际监管合规。");
 }fields.forEach(f=>f.addEventListener("input",update));update();
});
document.querySelectorAll('[data-demo="macro-scenarios"]').forEach(box=>{
 const out=box.querySelector("[data-demo-output]");
 const texts={
 base:"基准情景：先核对实际产出、通胀趋势、银行贷款定价和风险溢价；不要仅凭政策利率推断资产价格。",
 demand:"需求疲弱情景：观察订单、就业、贷款需求和企业投资是否同步转弱；利率下降不一定克服风险溢价上升或去杠杆。",
 supply:"供给冲击情景：同时检查投入成本、总体及核心通胀、企业利润率和生产活动；价格压力与增长疲弱可能并存。",
 credit:"金融压力情景：检查银行流动性、信用利差、抵押品折扣和企业续贷条件；融资渠道可能在市场压力下同步收紧。"
 };
 box.querySelectorAll("button[data-scenario]").forEach(btn=>btn.addEventListener("click",()=>{
 box.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed",String(b===btn)));
 out.textContent=texts[btn.dataset.scenario];
 }));
});

})();