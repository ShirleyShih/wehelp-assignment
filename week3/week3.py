# Task 1
# https://www.youtube.com/watch?v=sUzR3QVBKIo&list=PL-g0fdC5RMboYEyt6QS2iLb_1m7QcgfHk&index=16
import urllib.request as req
import csv
import json

#下載連結後，自己加副檔名.json，vscode開啟、右鍵format document
src1="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
with req.urlopen(src1) as response:
    data1=json.load(response)
clist1=data1["data"]["results"]
# print(clist1)

src2="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
with req.urlopen(src2) as response:
    data2=json.load(response)
clist2=data2["data"]
# print(clist2)

Station={}
with open("spot.csv", mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    for spot in clist1:
        SpotTitle=spot["stitle"]
        Longitude=spot["longitude"]
        Latitude=spot["latitude"]

        picture=spot["filelist"]
        ImageURL="https:"+picture.split("https:")[1] #scan(picture,1,"https:")

        SERIAL_NO=spot["SERIAL_NO"]
        for address in clist2:
            if address["SERIAL_NO"]==spot["SERIAL_NO"]:
                District=address["address"][5:8] # extract the 5th to 7th characters
                writer.writerow([SpotTitle,District,Longitude,Latitude,ImageURL])
                # print(SpotTitle,District,Longitude,Latitude,ImageURL)

                MRT=address["MRT"]
                if MRT not in Station:
                    Station[MRT]=[SpotTitle]
                else:
                    Station[MRT].append(SpotTitle)

with open("mrt.csv", mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    for key,item in Station.items():
        writer.writerow([key]+item) #csv withou "" mark
        # print(attraction)



# Task 2
# https://www.youtube.com/watch?v=9Z9xKWfNo7k&list=PL-g0fdC5RMboYEyt6QS2iLb_1m7QcgfHk&index=19
# https://www.youtube.com/watch?v=BEA7F9ExiPY&list=PL-g0fdC5RMboYEyt6QS2iLb_1m7QcgfHk&index=21

def getData(url):
    # Create and open a CSV file in write mode
    with open("article.csv", mode="a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        request=req.Request(url, headers={
            "cookie":"over18=1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data=response.read().decode("utf-8")

        import bs4
        root=bs4.BeautifulSoup(data,"html.parser")
        # titles=root.find("div",class_="title") #尋找class="title"的div標籤
        # print(root.title.string) #title: 標籤；string: 標籤裡的文字
        titles=root.find_all("div",class_="title")
        # 刪除html中包含"本文已被刪除"的元素
        titles=[element for element in titles if "本文已被刪除" not in element.text]
        # print(titles)

        # 取得文章網址並繼續爬蟲
        articlelinks = [link for link in root.find_all("a") if "[" in link.text]
        articlefulllinks=["https://www.ptt.cc"+elem["href"] for elem in articlelinks]
        # print(articlefulllinks)

        for title, articlefulllink in zip(titles, articlefulllinks):
            # print(title, articlefulllink)
            if title.a != None: # 如果標題包和a標籤(沒有被刪除)，印出來
                # title
                titles=root.find_all("div",class_="title")

                ## like/dislike count, and publish time
                request=req.Request(articlefulllink, headers={
                    "cookie":"over18=1",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                })
                with req.urlopen(request) as response:
                    data2=response.read().decode("utf-8")
                root2=bs4.BeautifulSoup(data2,"html.parser")

                #time
                timeall=root2.find_all("span",class_="article-meta-value")
                #找出EEE MMM DD HH:MM:SS YYYY格式的span
                import re
                pattern = r'(?:\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b)\s+(?:\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b)\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\d{4}'
                time=[element.text for element in timeall if re.match(pattern, element.text)]

                #like
                likeall=root2.find_all("span",class_="hl push-tag")
                like=len(likeall)

                #dislike
                dislikeall=root2.find_all("span",class_="f1 hl push-tag")
                # 回文、噓的class都是"f1 hl push-tag"，刪掉包含回文的element
                dislikeall = [element for element in dislikeall if "→ " not in element]
                dislike=len(dislikeall)
                
                # Write data to CSV file
                writer.writerow([title.a.string,str(like+dislike),','.join(time)]) #', '.join(time): turn time from array into a string

        # 抓取上一頁的連結
        nextLink=root.find("a", string="‹ 上頁") #找到內文是 < 上頁 的a標籤
        return nextLink["href"]

pageURL="https://www.ptt.cc/bbs/Lottery/index.html"
count=0
# getData(pageURL)
while count<3: #爬前三頁
    # print(count)
    pageURL="https://www.ptt.cc"+getData(pageURL)
    count+=1 