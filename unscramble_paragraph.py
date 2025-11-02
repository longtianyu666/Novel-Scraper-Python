from lxml import etree
def unscramble_paragraph_final(paragraphs:list, chapter_id=296843):
    """
    最终版本的段落还原函数
    完全逆向JS中的Fisher-Yates洗牌算法
    """
    if not paragraphs:
        return paragraphs
    # print(f'段落长度{len(paragraphs)}')
    THRESHOLD = 20
    if len(paragraphs) <= THRESHOLD:
        return paragraphs
    
    # 分离固定段落和乱序段落
    fixed = paragraphs[:THRESHOLD]
    scrambled = paragraphs[THRESHOLD:]
    n = len(scrambled)
    # print(f'乱序长度{n}')
    # 计算种子
    seed = int(chapter_id) * 127 + 235
    # print(f'种子={seed}')
    # 重现洗牌过程
    indices = list(range(n))
    for i in range(n - 1, 0, -1):
        seed = (seed * 9302 + 49397) % 233280
        # print(f'种子{seed}')
        swap_idx = int(seed / 233280 * (i + 1))
        # print(f'交换：位置{i}<->位置{swap_idx}')
        indices[i], indices[swap_idx] = indices[swap_idx], indices[i]
    
    # 关键：创建正确的逆映射
    # indices 表示：原位置i的段落现在在 indices[i] 位置
    # 我们需要：现在在位置j的段落原来的位置是 inverse[j]
    inverse = [0] * n
    for original_pos, current_pos in enumerate(indices):
        inverse[current_pos] = original_pos
    
    # 还原段落顺序
    restored = [scrambled[inverse[i]] for i in range(n)]
    
    return fixed + restored

    
content_container='''<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>愿意认输的话，就让你摸个够喔？ 杂鱼♡ 第一卷 第1章 雌小鬼收藏序说（3）_哔哩轻小说</title>
<meta name="keywords" content="愿意认输的话，就让你摸个够喔？ 杂鱼♡,哔哩轻小说" />
<meta name="description" content="哔哩轻小说提供了ちゅるけ创作的GA文库《愿意认输的话，就让你摸个够喔？ 杂鱼♡》小说干净清爽无错字的文字章节：《愿意认输的话，就让你摸个够喔？ 杂鱼♡》第一卷 第1章 雌小鬼收藏序说（3）在线阅读。" />
<meta property="og:url" content="https://www.linovelib.com/novel/4862/296843_3.html" id="ogurl"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="applicable-device" content="pc" />
<meta name="mobile-agent" content="format=html5; url=https://w.linovelib.com/novel/4862/296843_3.html" />
<meta http-equiv="Cache-Control" content="no-transform" />
<meta http-equiv="Cache-Control" content="no-siteapp" />
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
<meta name="renderer" content="webkit">
<link rel="stylesheet" type="text/css" href="https://www.linovelib.com/themes/zhpc/css/chapter.css?v1126a8" />
<script language="javascript" type="text/javascript" src="https://www.linovelib.com/themes/zhpc/js/jquery-1.8.3.min.js"></script>
<script async src="../scripts/lazysizes.min.js"></script>
<script language="javascript" type="text/javascript" src="https://www.linovelib.com/themes/zhpc/js/pctheme.js?v0917"></script>
</head>
<body class="bg6" id="readbg" onselectstart="return false">
<div class="top"><div class="bar"><div class="chepnav"><i>当前位置:</i><a href="https://www.linovelib.com">哔哩轻小说</a> > <a href="/wenku/gagraphicbunko/1.html" title="GA文库">GA文库</a> > <a href="/novel/4862.html">愿意认输的话，就让你摸个够喔？ 杂鱼♡</a> > <a href="/novel/4862/vol_296840.html">愿意认输的话，就让你摸个够喔？ 杂鱼♡ 第一卷</a></div><ul></ul></div></div>
<div class="mainbody mlfy_main "><script>name="《愿意认输的话，就让你摸个够喔？ 杂鱼♡》 第1章 雌小鬼收藏序说";aid="/book";bid="4862";cid="296843";page="3";shezhi();</script>
<script type="text/javascript">var ReadParams={articleid:'4862',articlename:'愿意认输的话，就让你摸个够喔？ 杂鱼♡',subid:'/4',author:'ちゅるけ',chapterid:'296843',page:'3',chaptername:'第一卷 第1章 雌小鬼收藏序说（3）',chapterisvip:'0',userid:'0',readtime:'1760976980'}</script>
  <div id="mlfy_main_text">
   <h1>第1章 雌小鬼收藏序说（3/6）</h1>
   <div id="TextContent" class="read-content8">
  <p>我全身的鸡皮疙瘩都竖起来了。</p>
<p>「是啊，毕竟那是我人生中第一次收到爱的告白嘛！哎呀，真抱歉呢？那时候我忍不住大笑了。」</p>
<p>「第一次听说。是这样吗？」</p>
<p>荆木睁大了杏眼。这家伙，一听到对我不利的话题就马上有了精神。</p>
<p>这是事实。我以前曾经迷恋过这个雌小鬼兼青梅竹马。</p>
<p>小学六年级的校外教学时，我偷偷把她叫出来，鼓起人生最大的勇气向她告白。</p>
<p>「是营火晚会那天晚上的事吧。」</p>
<p>「等等，别再挖出来了。回忆就收进回忆的架子上吧。」</p>
<p>「怎么办呢，小羽羽？」</p>
<p>「问我啦！」</p>
<p>「继续说。」</p>
<p>「好喔！我们躲过老师巡视，女生们聚在一起聊恋爱话题时，八寻寻突然一脸认真地打开门，吓了我一跳呢。你只把我一个人带出去对吧。虽然其他人也跟在后面就是了。」</p>
<p>「咦？我们不是两人独处吗？」</p>
<p>「我拜托有带相机的同学帮我们拍了照喔！外面有很多铃虫，星星也很漂亮，八寻寻真是个浪漫主义者呢。然后啊，因为你一直不说重点，我就推了你一把！要是你在那里退缩，惊喜就失败了喔，八寻寻。」</p>
<p>「不，等等，我现在正在被妳惊喜耶，封口有意义吗？」</p>
<p>「我把影片发给所有六年级生了喔！那句经典台词是什么呢，呃～是『请和我交往』吗？不对，你搬出我小时候讲的『人家要和八寻寻结婚！』这句话，说『请妳遵守约定』对吧！呀～♡」</p>
<p>「呜哇啊啊啊啊啊啊！」</p>
<p>丢脸的过去从记忆深处，带着可怕的新情报回到地表了！</p>
<p>我错判了！</p>
<p>这家伙在小学的时候就已经是雌小鬼的萌芽期了嘛！</p>
<p>我知道叶月的成长过程。我们两个曾经一起洗澡，也曾经扭打在一起吵架，还曾经搂着彼此睡午觉。</p>
<p>＊</p>
<p>肉感的两条大腿固定住我的左脚，弹性和压迫感直接扑来，不容分说地让我深陷其中。裙子就像门帘一样往内侧掀起。唷！妳当自己是大王吗？我要选孩子王中的女生脸蛋！</p>
<p>「住手！前面是楼梯！」</p>
<p>「我有长成八寻寻喜欢的样子了吗？是说，只要是女生，八寻寻都喜欢吧！毕竟你一年到头都在不知节制地扭屁股嘛。嘻嘻嘻，这么好搞定，真可爱～♡」</p>
<p>幸好，我就在极近之处得到了疗愈。</p>
<p>她迅速移开脚，轻轻推开我。</p>
<p>雌小鬼从下方捧起那个部位，在大腿上滑动。用肥嫩的肉摩擦背面所带来的刺激难以估计。要是用数字表示的话会显得更色，所以我不想估计。虽然不知道能不能当作参考，但我喷出了泡沫。</p>
<p>「你看起来很累呢。呵呵，你又去跟小羽玩了吧？」</p>
<p>「叶、叶月、小姐!? 」</p>
<p>「您说得对。」</p>
<p>「没有，不是那样啦，啊噫！」</p>
<p>我因为太过痛苦而甩着头，眼前一阵闪烁。</p>
<p>「虽然你发呆的表情也很可爱，但如果不保留上课的精神，会被老师骂喔。」</p>
<p>下半身紧贴着，上半身也一样。</p>
<p>和刚才相反，现在变成我的一只脚侵入了她的胯下。</p>
<p>哪里无所谓了？所谓的青梅竹马就是这样才猛啊！</p>
<p>「不、不用在意！我没有输！」</p>
<p>「在八寻寻变成野兽前，人家要闪人了！反正已经拿到目标物了！」</p>
<p>我没有错。错的是准备了青梅竹马这种剧毒的神明。</p>
<p>细长的手指在薄薄的布料中蠢动，指甲刮过一旁的重要部位。这不是偶然。她的食指和中指就像在跳踢踏舞一样，精准地、执拗地戳着我。</p>
<p>叶月的脚伸进我的双腿之间。</p>
<p>「好大……」</p>
<p>她静静地把橡皮擦放在我手心。</p>
<p>「……到此为止。上课要迟到──」</p>
<p>「我的钱包！妳竟然偷了它！」</p>
<p>「──时候到了。看在小羽羽的份上，人家就放你一马吧。随时等你告白喔！」</p>
<p>她和荆木不同，个性温柔；和叶月不同，气质高雅。古典的黑长发充满静谧，或者该说是楚楚可怜的魅力。胸部也充满魅力。</p>
<p>「怎么……」</p>
<p>叶月也干脆得令人惊讶地抛弃了我。</p>
<p>教良寺天菜同学。</p>
<p>这里是走廊。经过的学生无一不被我们吓到。</p>
<p>那些应该都是令人莞尔的回忆。然而，当其中一方开始散发出性感魅力，记忆就会变成补完对方情色感的参考资料。朦胧中记得那家伙的扁平身体竟然变得这么……这种落差感正是胯下最喜欢的。</p>
<p>「你们两个都是。我嫉妒能抓住小羽的心的纪伊同学，也嫉妒独占你的小羽。」</p>
<p>「噫！」</p>
<p>「来，拿去。」</p>
<p>下午的课堂上，有人从右边敲了敲我的上臂，同时传来银铃般的悦耳嗓音。我转过头，隔壁的女生正看着我，露出充满慈爱的笑容。</p>
<p>好大。超大的。</p>
<p>她疑惑地歪着头，我的心脏立刻开始狂跳。</p>
<p>烦人的女人降低了声调。我们三个人之间的气氛改变了。</p>
<p>那种随兴又极度友善的态度，玩弄着许多男人。虽然和荆木类型不同，但雌小鬼就是麻烦。</p>
<p>「万年小鬼的家伙给我闭嘴！」</p>
<p>「毕竟八寻寻在那之后也变帅了嘛。要是再次被你示爱，搞不好人家会出乎意料地轻易上钩喔。」</p>
<p>「咿嘻嘻，怎么样？人家也变得很色了吧！」</p>
<p>「嘿嘿♡和纯真的八寻寻不一样，小弟弟很老实呢♡你好像很清楚要怎么做才能被欺负呢♡八寻寻也老实点嘛♡要是你紧紧抱住人家，一边说喜欢一边磨蹭，会很舒服喔♡」</p>
<p>叶月的手中握着我熟悉的茶色长夹。</p>
<p>「咿嘻嘻嘻嘻，里面有不少钱嘛！谢啦，放学后会还你！」</p>
<p>叶月从左边绕过手臂，经过我的背后，用力抓住我右边的腋下，就这样拉进怀里。发育得恰到好处的美乳被我的上臂压扁。</p>
<p>叶月用双脚支撑着因为兴奋和羞耻而摇摇晃晃的我。</p>
<p>叶月将一只手伸进我的裤子口袋，借此回应我的要求。</p>
<p>「事、事到如今，妳怎样都无所谓啦！」</p>
<p>「输？」</p>
<p>失去支撑的我靠在墙上，滑落下去，一屁股跌坐在地。</p>
<p>制服外套被撑得鼓鼓的，衬衫看起来很紧绷，领带弯成钝角。那紧绷的模样让我移不开目光。上课时也一直出现在视野的角落，让我烦恼不已。而且那东西还会配合呼吸晃动，甚至让我感受到生命的神秘。</p>
<p>她很用功，成绩不输荆木。而且会爽快地教人，不会自以为了不起。总而言之，教良寺同学是个出类拔萃的好女孩。胸部也出类拔萃。</p>
<p>和雌小鬼的战斗，无论输赢都很累人。</p>
<p>「来嘛来嘛，你试着告白看看啊！这次人家说不定会遵守约定喔！」</p>
<p>「我真是罪孽深重的女人！以前掳获了迷你八寻寻，现在又诱惑了各种男生……可是可是，人家还是单身喔。所以八寻寻，你要再挑战一次也可以喔。」</p>
<p>「咕呜呜呜呜！」</p>
<p>「对吧！你最喜欢最喜欢人家，喜欢到欲火焚身了对吧♡每次见到我，你都会变得硬邦邦的，怎么可能会讨厌我嘛！现在也因为碰到我的大腿，一副很开心的样子嘛♡噗噗噗，好𫫇心喔～！」</p>
<p>简单来说，就是奶子很大。</p>
<p>「哈啊、啊、住手啊叶月！」</p>
<p>教良寺同学腼腆地笑着，接着转向前方。</p>
<p>她完全不知道我的邪念，轻声笑了起来。</p>
<p>「纪伊同学、纪伊同学，你的橡皮擦掉了喔。」</p>
<br>
<p>她是校内不分年级人人憧憬的美少女。我也发挥容易迷上人的本领。</p>
<br>
<p>「可恶，谢啦荆木。不好意思，可以顺便帮我个忙吗？我腿软了。」</p>
<p>「放手，快放手！妳把手伸进哪里了！」</p>
<p>我的胯下热得像是被营火烤过。</p>
<p>她上下都发育得好到爆！</p>
<p>「羡慕？我吗？」</p>
<p>新学期一开始，她就立刻换到我旁边的座位。</p>
<p>另一边的五根手指则搔着我的腋下。我痒得扭动身体，胸部和腹部就软绵绵地变形，让我愈来愈明显地感受到触感。</p>
<p>天蓝色的眼眸清澈无比。</p>
<p>被指甲勾住的布料、内裤，以及胯下的触感，全都传到了我的要害。令人难耐的快感将我的神经搅得一团乱，让我的腰往后缩。</p>
<p>让我的精神陷入机能不全状态后，窃贼雌小鬼跑走了。</p>
<p>「噗呼呼呼呼，你当真啦～♡笨蛋～♡要自慰的话，你自己一个人去喔♡竟然会被这种话钓到，八寻寻果然很可爱呢♡杂鱼～♡杂鱼～♡」</p>
<p>「呼唔唔！」</p>
<p>「纪伊同学和小羽总是在一起呢。真羡慕你们感情这么好。」</p>
<p>绅士们在对抗世上的雌小鬼时，追求着疗愈。如果没有疗愈，精神总有一天会因为严苛的日子而崩溃。</p>
<p>不喜欢争执与吵闹，总是带着稳重的笑容，没见过她生气。尽管如此，有主张的时候会确实表达。胸部也充满强烈的主张。</p>
<p>「对了，你早上去了保健室吧？身体还好吗？如果觉得不舒服，我会陪你，不用客气，尽管告诉我。」</p>
<p>她踏到几乎快碰到裤子的地方，用脚跟碰了碰我的脚跟，亲昵地蹭了过来。姿势就像柔道的大内割一样。</p>
<p>「八寻从小就很杂鱼。」</p>
<p>乌黑的长发，以及清纯女演员般端正的五官。</p>
<p>但是叶月不允许我逃跑，她把脚靠得更近了。</p>
<p>比荆木还要有肉且色泽健康的丰腴大腿通过我的胯下。</p>
<p>「还是说，你讨厌人家了？」</p>
<p>我的兴奋达到极限，因为被嘲弄而快要突破临界点的时候──</p>
<p>突然出现，像暴风雨般扫倒一切，然后装作与自己无关。叶月就是这样的女人。</p>
<p>蜂蜜色的眼睛带着黏腻感看着我。</p>
<p>我们两人的左脚碰到了彼此的大腿。叶月那边很顺，但我那边有个叶月没有的障碍物，像安全气囊一样膨胀着。</p>
<p>「怎么了吗？」</p>
<br>
<img src="https://img3.readpai.com/4/4862/296841/297090.jpg" class="imagecontent">
<br>
<p>「我拖你走。」</p>
<p>简单来说，就是奶子很大。</p>
<p>蹲在角落的荆木意外地制止了她。</p>
<p>在那底下，被手臂夹住的胸部柔软地强调着存在感。</p>
<p>「什么？」</p>
<p>在情绪起伏不定的时期，要是身边配置了一个随时都玩在一起的女孩子，没有喜欢上她才叫失礼吧。那种剧毒还装模作样。</p>
<p>难怪她会自己讲。叶月的身体比年轻时犯错的那一天还要洗练。隔着衬衫毫不保留地压上来的凹凸曲线，紧紧贴着我，用柔软的反弹力道逐渐夺走我的判断力。</p>
	<div class="dag"><script>style_tp();</script><script src="/modules/article/scripts/fsdoa.js?v0222.1"></script></div><!-- <script async src="https://fundingchoicesmessages.google.com/i/pub-5520793375276242?ers=1" nonce="woTUo9qj1HYeLZtw0esVrA"></script><script nonce="woTUo9qj1HYeLZtw0esVrA">(function() {function signalGooglefcPresent() {if (!window.frames['googlefcPresent']) {if (document.body) {const iframe = document.createElement('iframe'); iframe.style = 'width: 0; height: 0; border: none; z-index: -1000; left: -1000px; top: -1000px;'; iframe.style.display = 'none'; iframe.name = 'googlefcPresent'; document.body.appendChild(iframe);} else {setTimeout(signalGooglefcPresent, 0);}}}signalGooglefcPresent();})();</script> -->
    </div>
  </div>
</div>
<div class="mlfy_page"><a href="/novel/4862/296843_2.html">上一页</a><a onclick="tjp('4862');" class="hidden">点赞</a><a href="/novel/4862/catalog" rel="nofollow">目录</a><a onclick="sq('4862','296843','3');">+书签</a><a href="/novel/4862/296843_4.html">下一页</a></div>

<script type="text/javascript" src="../scripts/json2.js"></script>
<script type="text/javascript" src="../scripts/chapterlog.js"></script>
<script type="text/javascript" src="../scripts/GB_BIG5.js"></script>
<script type="text/javascript">var defaultEncoding=1;var translateDelay=0;var cookieDomain="linovelib.com";var msgToTraditionalChinese="繁體化";var msgToSimplifiedChinese="简体化";var translateButtonId="GB_BIG";translateInitilization();</script>
<script>yuedu();</script><script>tj();</script>
<script>var _hmt=_hmt||[];(function(){var hm=document.createElement("script");hm.src="https://hm.baidu.com/hm.js?ef8d5b3eafdfe7d1bbf72e3f450ad2ed";var s=document.getElementsByTagName("script")[0];s.parentNode.insertBefore(hm,s)})();</script>
<script>$(document).ready(function(){var prevpage="/novel/4862/296843_2.html";var nextpage="/novel/4862/296843_4.html";var bookpage="/novel/4862.html";$("body").keydown(function(event){var isInput=event.target.tagName==='INPUT'||event.target.tagName==='TEXTAREA';if(!isInput){if(event.keyCode==37){location=prevpage}else if(event.keyCode==39){location=nextpage}}})});</script>
<script>eval(function(p,a,c,k,e,r){e=String;if('0'.replace(0,e)==0){while(c--)r[e(c)]=k[c];k=[function(e){return r[e]||e}];e=function(){return'[0-3]'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('if(\'0\'in 1){1.0.getRegistrations().then(function(2){for(let 3 of 2){3.unregister()}})}',[],4,'serviceWorker|navigator|registrations|registration'.split('|'),0,{}))</script>

<script defer src="https://static.cloudflareinsights.com/beacon.min.js/vcd15cbe7772f49c399c6a5babf22c1241717689176015" integrity="sha512-ZpsOmlRQV6y907TI0dKBHq9Md29nnaEIPlkf84rnaERnq6zvWvPUqr2ft8M1aS28oN72PdrCzSjY4U6VaAw1EQ==" data-cf-beacon='{"version":"2024.11.0","token":"192783771d59492782cd05bd12eb61b9","r":1,"server_timing":{"name":{"cfCacheStatus":true,"cfEdge":true,"cfExtPri":true,"cfL4":true,"cfOrigin":true,"cfSpeedBrain":true},"location_startswith":null}}' crossorigin="anonymous"></script>
</body>
</html>'''

if __name__=='__main__':
    original_paragraph=[]
    root=etree.HTML(content_container)
    paragraph_nodes=root.xpath('.//p|.//img')
    
    for p_node in paragraph_nodes:
        full_text=""
        if p_node.tag=='img' and p_node.text.startswith('--IMAGE-PLACEHOLDER-<'):
            full_text=p_node.text.strip()
        else:
            full_text=p_node.xpath('string(.)').strip()
            
            
        if full_text:
            original_paragraph.append(full_text)
    
    if original_paragraph:
        try:
            correctly_ordered_paragraph=unscramble_paragraph_final(original_paragraph,296843)
        except Exception as e:
            correctly_ordered_paragraph=original_paragraph
    else:
        correctly_ordered_paragraph=[]
    print(correctly_ordered_paragraph)