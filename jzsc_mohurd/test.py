import requests


HEA = {"Accept":"text/html, application/xhtml+xml, image/jxr, */*",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3",
"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 10.0; WOW64; Trident/7.0)",
"Cookie":"saplb_*=(J2EE204289720)204289751; JSESSIONID=pJqoUhF2SBphocz_liQIFcwpT78AdAHYNi0M_SAPUNGL-mfbYouQy-PP8K4tjapx; LS2cj8YxOIT5P=5UuXM2TZ4b_Eqqqm0qVsa5GLyDA.Ix6JUNZMVkolBOoHzM_yBG6PfNwTHJwWV1kbQe.8vZjcAdOjDFSjf6FXOO7XlsRyaRSHblfJEGrTmQw0ktIqpGNqrZA5KZ4skNrZSxVF5.sC4gFaS1eWVpB7Z5zmwjXBEucX6sV67XcHkem1RHeqDiPX8g7EWERQ9xW9M9jXz44AKqe0Mv15tiEeGS8X8XgHaZy9_dwwNY1LR.CuYUOoXn0qHumLWBx66ihW_q; LS2cj8YxOIT5O=59JfZueJ3CYnm0w_W1w1ogvo0Q5ds6fygTa2w4NlLDl5zbUE4.j5rAhqIECHuACkeTHR.hWTRbSFQr71RkdyV0q",
"Connection":"Keep-Alive",
"Host":"b2b.10086.cn"}
# url = "https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=683567"
url = "https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2#this"
brow = requests.get(url=url,verify=False,headers = HEA)
print(brow.status_code)
print(brow.text)