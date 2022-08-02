from time import sleep
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime


def __start__():
    #Connect TO the data Base
    db_con = sqlite3.connect('rss_feeds.db')
    db_cur = db_con.cursor()

    #Create TAble
    try:
        db_cur.execute(''' CREATE TABLE news (title text,link text)''')
    except:
        pass

    #Methods For telegram BOt


    def url_box(method_name):
        #************************** SET YOUR TELEGRAM_BOT_API ******************
        
        url = "https://api.telegram.org/{{YOUR TELEGRAM BOT API}}/"+method_name
        return url

    ########################
    web_url = "https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx"
    ##################################
    
    #******************** YOUR CUSTOMIZED CATEGORY******************
    
    list_medium_rss = ['YOUR','CATEGORY']
    list_rss_content = ["",""]

    while True:
        #****************** YOUR WEBSITE LINK FOR CHEKCING THE CONNECTION******************
        connect_to_medium = requests.get("{{WEBSITE LINK}}").status_code
        if (connect_to_medium == 200):
            print("Connection Has Been Established=> Status Code 200  "+datetime.now().strftime("%H"))
            url_box_send_message = f"sendMessage?chat_id=124044961&text=I'M Crawling {{WEBSITE NAME }} \n \n"
            payload = {
                "UrlBox": url_box(url_box_send_message),
                "AgentList": "Mozilla Firefox",
                "VersionsList": "HTTP/1.1",
                "MethodList": "POST" 
            }
            requests.post(web_url, payload)

            for i in list_medium_rss:
                content = requests.get("https://{{RSS FEED LINK}}"+i+"/").text
                soup = BeautifulSoup(content, 'xml')
                md_found_data = soup.find_all(['title', 'link'])


                counter = 0
                for i in md_found_data:
                    string = str(i)
                    if '<title>' in string:
                        striped_string = string.replace('<title>', " ")
                        striped_string = striped_string.replace('</title>', ' ')
                    elif '<link>' in string:
                        striped_string = string.replace('<link>', " ")
                        striped_string = striped_string.replace('</link>', ' ')


                    list_rss_content[counter]=striped_string
                    counter +=1
                    if counter > 1:
                        list_rss_content = tuple(list_rss_content)
                        print(list_rss_content)
                        db_cur.execute("SELECT * FROM news where title=? and link=?;", list_rss_content)
                        fetched_data = db_cur.fetchall()

                        if fetched_data == []:
                            db_cur.execute("INSERT INTO news VALUES (?,?);", list_rss_content)
                            db_con.commit()

                            url_box_send_message = f"sendMessage?chat_id=124044961&text=Heyy New Article From {{WEBSITE NAME} \n \n \n %s"%(str(list_rss_content))
                            payload = {
                                "UrlBox": url_box(url_box_send_message),
                                "AgentList": "Mozilla Firefox",
                                "VersionsList": "HTTP/1.1",
                                "MethodList": "POST" 
                            }
                            requests.post(web_url, payload)
                        else:
                            print("Already Exists")

                        list_rss_content = ["",""]
                        counter = 0
                    sleep(0.5)
                print(f"Adding Tag {i} To Data base has been finished ")
            break


    
__start__()
