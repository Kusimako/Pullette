# Pullette
Pyxel製試作ゲームというほどでもない弾幕シミュレーション

600fで切り替わる、ランダムに生成した9タイプの弾幕をひたすら吐きます。  
特定のタイプを生成したい場合は、0~8の数字キーを押すと強制的に切り替えられます。(具体的な内容は後日追記します)  

Active modeはゲーム風に被弾数をカウントします。プレイヤーからの攻撃システムはありません。  
目に悪かったりあからさまにヌルゲーだったりどう足掻いても避けられない弾幕が生成される可能性もあります。  
ある程度配慮してはいますが、ランダム生成故ご容赦ください。  
参考程度に変数や式を表示しているので、弾幕のアイデア出しなんかに使えるかもしれません。間違っていたらすみません。  

View modeは弾のみを表示します。花火代わりにどうぞ。  

スクリーンショットの公開、コード改造、改造したコードの公開等はご自由にどうぞ。  
原型が8割ぐらい残っているような改造コードを公開する場合、何らかの形で改造元に言及していただけると幸いです。  
「原型が8割ぐらい残っている」とは、主に以下のような場合を想定しています。   

	*パレットのみの変更  
	*画像や弾のサイズなど、グラフィックのみの変更  
	*弾幕生成用変数のみの変更  
	*弾幕タイプのうち、1~3タイプのみの差し替え  
	*全体の構造を大きく変えない程度の、不要または冗長な記述の整理  

以下のような場合は、むしろ言及しない方が自然かと思います。(無論していただく分には構いませんが)  

	*弾幕の関数を自作のゲームに使用する  
	*このコードを参考にしながら、内容や構造が大きく異なるゲームを作成する  
	(初心者が思い付きで組んだコードなので、参考になるかはともかく……)
