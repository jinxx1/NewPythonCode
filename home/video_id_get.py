# -*- coding: utf-8 -*-
import re
hhtml = '''
<div class="tpc_content do_not_catch"><br><span style="display:inline-block;color:#FF0000">NTR这个系列是我最喜欢的一个系列，并且这个系列会有一些剧情，也比较考验女优的演技。我收集来的一些高质量的女优，在这里给大家做一个分享。</span><br><span style="display:inline-block;color:#FF33CC">关于下载，这里提供番号，喜欢的朋友可以根据社区一些聚聚提供的磁力搜索地址自行搜索。</span><br><br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa4n3o.jpg" ess-data="https://louimg.com/u/2020/10/30/fa4n3o.jpg" src="https://louimg.com/u/2020/10/30/fa4n3o.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa4n3o.jpg">链接</div></div>&nbsp;<br>番号：SSNI-619<br>出演女优:&nbsp; 葵つかさ<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa53hl.jpg" ess-data="https://louimg.com/u/2020/10/30/fa53hl.jpg" src="https://louimg.com/u/2020/10/30/fa53hl.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa53hl.jpg">链接</div></div>&nbsp;<br>番号：MIDE-705<br>出演女优:&nbsp; 水卜さくら<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa5g61.jpg" ess-data="https://louimg.com/u/2020/10/30/fa5g61.jpg" src="https://louimg.com/u/2020/10/30/fa5g61.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa5g61.jpg">链接</div></div>&nbsp;<br>番号：MEYD-544<br>出演女优:&nbsp; 希島あいり<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa5s1h.jpg" ess-data="https://louimg.com/u/2020/10/30/fa5s1h.jpg" src="https://louimg.com/u/2020/10/30/fa5s1h.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa5s1h.jpg">链接</div></div>&nbsp;<br>番号：IPX-403<br>出演女优:&nbsp; 岬ななみ 花宮レイ<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa5xlk.jpg" ess-data="https://louimg.com/u/2020/10/30/fa5xlk.jpg" src="https://louimg.com/u/2020/10/30/fa5xlk.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa5xlk.jpg">链接</div></div>&nbsp;<br>番号：IPX-398<br>出演女优:&nbsp; 楓カレン<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa6n9m.jpg" ess-data="https://louimg.com/u/2020/10/30/fa6n9m.jpg" src="https://louimg.com/u/2020/10/30/fa6n9m.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa6n9m.jpg">链接</div></div>&nbsp;<br>番号：SSPD-148<br>出演女优:&nbsp; 希崎ジェシカ<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa73ek.jpg" ess-data="https://louimg.com/u/2020/10/30/fa73ek.jpg" src="https://louimg.com/u/2020/10/30/fa73ek.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa73ek.jpg">链接</div></div>&nbsp;<br>番号：MIDE-700<br>出演女优:&nbsp; 由愛可奈<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa74pa.jpg" ess-data="https://louimg.com/u/2020/10/30/fa74pa.jpg" src="https://louimg.com/u/2020/10/30/fa74pa.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa74pa.jpg">链接</div></div>&nbsp;<br>番号：CAWD-020<br>出演女优:&nbsp; 伊藤舞雪<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa7dmc.jpg" ess-data="https://louimg.com/u/2020/10/30/fa7dmc.jpg" src="https://louimg.com/u/2020/10/30/fa7dmc.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa7dmc.jpg">链接</div></div>&nbsp;<br>番号：IPX-389<br>出演女优:&nbsp; 明里つむぎ<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa7ybh.jpg" ess-data="https://louimg.com/u/2020/10/30/fa7ybh.jpg" src="https://louimg.com/u/2020/10/30/fa7ybh.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa7ybh.jpg">链接</div></div>&nbsp;<br>番号：JUY-996<br>出演女优:&nbsp; 神宮寺ナオ<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa84oy.jpg" ess-data="https://louimg.com/u/2020/10/30/fa84oy.jpg" src="https://louimg.com/u/2020/10/30/fa84oy.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa84oy.jpg">链接</div></div>&nbsp;<br>番号：SSNI-569<br>出演女优:&nbsp; 橋本ありな<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa85sq.jpg" ess-data="https://louimg.com/u/2020/10/30/fa85sq.jpg" src="https://louimg.com/u/2020/10/30/fa85sq.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa85sq.jpg">链接</div></div>&nbsp;<br>番号：MEYD-526<br>出演女优:&nbsp; 希島あいり<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa8o22.jpg" ess-data="https://louimg.com/u/2020/10/30/fa8o22.jpg" src="https://louimg.com/u/2020/10/30/fa8o22.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa8o22.jpg">链接</div></div>&nbsp;<br>番号：STARS-115<br>出演女优:&nbsp; 古川いおり<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa8t7s.jpg" ess-data="https://louimg.com/u/2020/10/30/fa8t7s.jpg" src="https://louimg.com/u/2020/10/30/fa8t7s.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa8t7s.jpg">链接</div></div>&nbsp;<br>番号：SSNI-542<br>出演女优:&nbsp; 三上悠亜<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa97ye.jpg" ess-data="https://louimg.com/u/2020/10/30/fa97ye.jpg" src="https://louimg.com/u/2020/10/30/fa97ye.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa97ye.jpg">链接</div></div>&nbsp;<br>番号：MIDE-673<br>出演女优:&nbsp; 七沢みあ<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa9d67.jpg" ess-data="https://louimg.com/u/2020/10/30/fa9d67.jpg" src="https://louimg.com/u/2020/10/30/fa9d67.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa9d67.jpg">链接</div></div>&nbsp;<br>番号：IPX-358<br>出演女优:&nbsp; 相沢みなみ<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/fa9qph.jpg" ess-data="https://louimg.com/u/2020/10/30/fa9qph.jpg" src="https://louimg.com/u/2020/10/30/fa9qph.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/fa9qph.jpg">链接</div></div>&nbsp;<br>番号：SSNI-521<br>出演女优:&nbsp; 吉高寧々<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/faa1fz.jpg" ess-data="https://louimg.com/u/2020/10/30/faa1fz.jpg" src="https://louimg.com/u/2020/10/30/faa1fz.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/faa1fz.jpg">链接</div></div>&nbsp;<br>番号：SSNI-518<br>出演女优:&nbsp; 葵つかさ<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/faa62o.jpg" ess-data="https://louimg.com/u/2020/10/30/faa62o.jpg" src="https://louimg.com/u/2020/10/30/faa62o.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/faa62o.jpg">链接</div></div>&nbsp;<br>番号：SSNI-516<br>出演女优:&nbsp; 三上悠亜<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/faaf1e.jpg" ess-data="https://louimg.com/u/2020/10/30/faaf1e.jpg" src="https://louimg.com/u/2020/10/30/faaf1e.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/faaf1e.jpg">链接</div></div>&nbsp;<br>番号：IPX-340<br>出演女优:&nbsp; 希崎ジェシカ<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/faappw.jpg" ess-data="https://louimg.com/u/2020/10/30/faappw.jpg" src="https://louimg.com/u/2020/10/30/faappw.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/faappw.jpg">链接</div></div>&nbsp;<br>番号：SSNI-496<br>出演女优:&nbsp; 夢乃あいか<br><div class="image-big"><img iyl-data="http://a.d/adblo_ck.jpg" data-link="https://louimg.com/i/?i=u/2020/10/30/faavfe.jpg" ess-data="https://louimg.com/u/2020/10/30/faavfe.jpg" src="https://louimg.com/u/2020/10/30/faavfe.jpg" style="cursor: pointer;"><div class="image-big-text" title="链接: https://louimg.com/i/?i=u/2020/10/30/faavfe.jpg">链接</div></div>&nbsp;<br>番号：IPX-321<br>出演女优:&nbsp; 桜空もも
			<br><br><div onclick="clickLike(4157716, 'h', 't')" class="t_like" id="like4157716">赞(20)</div>
</div>
'''.encode('utf-8').decode('utf-8')


aaa= 'MIDE——705'
regx=re.findall("[A-Za-z]{1,10}-[0-9]{1,5}",hhtml)
print(regx)