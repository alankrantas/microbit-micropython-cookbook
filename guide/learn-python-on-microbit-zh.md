# 在 BBC micro:bit 上學 Python

作：Alan Wang, Feb 2021

本指南採用 [GNU 3.0 通用公共授權](https://www.chinasona.org/gnu/gnulgpl-v3-tc.html)

![01](https://user-images.githubusercontent.com/44191076/107118869-ab2f2280-68be-11eb-9a6d-87b02939a7e2.png)

## 關於本指南

網路上的 micro:bit 教材眾多，但主要是以兒童教學為設計目的，因此大多著重在 micro:bit 自身的功能，較少解釋程式語言本身。而 Python 語言儘管看似易學，一開始也確實能學得很快，許多教材（包括書籍）卻很少能正確交代關鍵的概念。

本指南是寫給成人或青少年，包括有意學習 Python 並投入教學的教師，而不是寫給兒童閱讀。在此筆者會嘗試將傳統的 Python 教學與 micro:bit 融合，並在盡量只使用 micro:bit 本身的前提下帶過 Python 至少入門到中階的語言功能。等到各位對 Python 的運作有足夠了解後，就可以用自己的方式教導兒童了。

目前 micro:bit 的 MakeCode 圖形編輯器（使用 TypeScript/JavaScript 語言）也「支援」Python，但這個 Python 版本只是單純從 JavaScript 轉換過來而已，它並不支援 Python 語言的一些特色。因此筆者並不鼓勵將該編輯器的 Python 當成學習目標。

## 為何要學 Python？

最簡單的答案是：因為大家都在學，包括非理工背景的人士。學 [Python](https://zh.wikipedia.org/zh-tw/Python) 的人是如此之多，它在職場已經逐漸被視為如英語或數學一樣的重要技能。且既然 Python （一開始）相對容易學，它也成為新一代資訊教育經常用來教學生的語言。

Python 理論上是多用途的系統語言，但它在企業系統的用處正在慢慢被像是 Go、Rust 之類的語言取代。目前學 Python 的最主要回報，是有機會成為資料科學家／資料分析師／機器學習專家：這類工作在 2010 年代前期到中期的需求與薪資達到了驚人的高峰。這歸功於針對 Python 設計的大量第三方套件，讓任何人都能進行資料分析以及資料視覺化，甚至跨進人工智慧領域。簡單地說，不管你（誤）讀什麼科系，學 Python 都是個讓自己非常難餓死的好辦法。

不過，筆者認為 Python 的另一個選擇是「嵌入式 Python」──在 micro:bit 這樣的微控制器／開發板上用 Python 控制它。由於其設計特性，Python 執行起來比 Arduino 的 C++ 語言慢上不少，但寫起來卻容易很多。此外，既然開發板得和人類互動，你往往還得給程式「降速」，所以大多時候運作效能其實並不重要。比起純粹處理資料的純電腦程式，嵌入式 Python 賦予了我們跟真實世界互動、解決生活問題的機會，而且對於撰寫程式上也能訓練出更靈活的思維。

那麼，孩子多小可以學 Python 呢？這大概得看個人資質，不過國高中以下恐怕都不是好主意。一來學寫程式仰賴英文閱讀及打字能力，二來它需要抽象思考。坊間有很多兒童教育單位會用遊戲式方式教導運算思維等等，但那和真正寫程式是有差距的。我自己也是直到兩年前才開始學 Python，所以只要年紀夠大，什麼時候開始並不會有差別。

## 事前準備

你需要一片 [BBC micro:bit](https://microbit.org/zh-tw/new-microbit/)，本指南會使用 2020 年 10 月後上市的第二版（V2），不過筆者會確保大部分的程式仍能與一代相容。既然二代擁有更大的記憶體、更快的處理器和更多功能，價格也與一代無異，使用二代自然是更合理的選擇。

你也需要一條 micro USB 線，以及一台擁有 Google Chrome 瀏覽器、可上網的電腦。之後我們也許會討論到更多外部硬體器材的控制，但這會是講完 Python 語言主要部分之後的事了。

接著打開 https://python.microbit.org/v/2 ，這是 micro:bit 基金會提供的線上官方編輯器，你不需要在電腦上安裝額外的程式或驅動程式。

### Python 編輯器

![02](https://user-images.githubusercontent.com/44191076/107118877-baae6b80-68be-11eb-8bda-aa8013b3698f.png)

這是個很簡單的 Python 編輯器，但其功能已經合乎學習需求。在這個指南中，筆者會著重在某些方面，目的是讓你將來能將操作套用到其他 Python 編輯器上（不只是 micro:bit 用的編輯器）。

畫面上方有五個大按鈕：

* Download/Flash (下載/燒錄)
* Connect/Disconnect (連線/解除連線)
* Load/Save (上載檔案/存檔)
* Open Serial/Close Serial (打開 REPL/關閉 REPL)
* Help (線上說明)

按鈕的內容會因與 micro:bit 連線與否而有所不同。下面我們會再找機會說明這些功能。

### 與 micro:bit 連線

micro:bit 的硬體設計有點特別，因為它有兩個微控制器而不是一個。不過，真正用來執行程式的只有一個，另一個負責扮演程式燒錄介面。

微控制器一次只能儲存一個程式，而你要從電腦把寫好的程式上傳或燒錄到微控制器，就得透過一個通訊界面才行。這意味著你必須在電腦上安裝這個介面的驅動程式。

為避免這種麻煩，micro:bit 的第二微控制器會模擬出一個 USB 磁碟區，你只要用複製貼上的方式把程式檔（從線上編輯器下載的檔案）丟進去，該程式就會燒錄到主控制器上。只是貼上或拖曳檔案的動作對某些小孩來說仍然有點吃力，因此後來加入了個新功能，叫做 WebUSB。簡單地說，這能讓 Chrome 瀏覽器直接跟 micro:bit 的 USB 磁碟區連線，把檔案下載到那兒，跳過了手動搬動檔案的動作。

比較舊的 micro:bit 可用更新韌體的方式來獲得這種支援，不過現在販賣的 V1 或 V2 版本大多都是已經安裝有新版韌體的產品，因此這裡就跳過不談。

現在，用 USB 線將你的 micro:bit 接上電腦，你應該會看到 micro:bit 開始顯示一些東西（這是它出場時預先安裝好的示範程式），電腦上也會跳出它的 USB 磁碟區。稍待片刻等電腦準備好，然後按編輯器的 **Connect**：

![05](https://user-images.githubusercontent.com/44191076/107119477-c4d26900-68c2-11eb-94fd-6ad62ec2e567.png)

點選 micro:bit 後按「連線」即可。

### 燒錄第一支 Python 程式

在進行以下課程之前，你應該先在 micro:bit 上用 Python 編輯器燒錄一隻程式，即使是完全空白的程式也無妨。或者你可用 Python 編輯器打開時已經填入畫面的程式：

```python
# Add your Python code here. E.g.
from microbit import *


while True:
    display.scroll('Hello, World!')
    display.show(Image.HEART)
    sleep(2000)
```

確定 micro:bit 已經連線，然後按 **Flash**。等待畫面上的程式燒錄作業結束。

## REPL - Python 直譯器的窗口

燒錄好程式後，我們要先來看一樣東西。

點 **Open Serial**，然後點按鈕下方右側的「Send CTRL-C for REPL」或直接在鍵盤上按 Ctrl+C。你應該會看到以下畫面：

![04](https://user-images.githubusercontent.com/44191076/107119544-44603800-68c3-11eb-9f0a-6305b40195ea.png)

這幾行文字

```
MicroPython v1.13 on 2020-12-21; micro:bit v2.0.0-beta.3 with nRF52833
Type "help()" for more information.
>>> 
```

是 Python 直譯器的 **REPL**（Read-Eval-Print Loop，讀取-求值-輸出循環）提示，這模式又稱為互動模式。要解釋這個東西，我們得先從 Python 的運作特性說起。

目前所謂的程式語言，其實是經過設計好讓人類撰寫的一系列語法，那不是電腦能直接解讀的格式。傳統上像 C++ 之類的語言，必須在寫完程式後編譯（compile）它，把程式轉成二進位的機器碼（machine code）。如果編譯過程中發現程式有問題，編譯就會失敗，並試著告訴你哪幾行程式有問題。這類語言也稱為編譯式語言。

但也有一些語言，包括 Python 在內，是直譯式語言，也就是不事先編譯，而是現場一行行程式去執行，遇到問題時才停下來。（當然實際上沒有這麼簡單，不過我們可以先這樣認定就好。）直譯式語言的優勢是不必等待編譯就能馬上執行，這對於撰寫一些簡單的程式和做測試非常方便。




（持續寫作中...）

