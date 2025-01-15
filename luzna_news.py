from requests_html import HTMLSession
import hashlib
import sqlite3


 
def get_news():
    connection_obj = sqlite3.connect('luznanews.db', isolation_level=None)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("CREATE TABLE IF NOT EXISTS novinky(hash VARCHAR(64) NOT NULL)")



    session = HTMLSession()

    URL = 'https://www.obec-luzna.cz/'
    print(f"Fetching data from: {URL} ...")
    r = session.get(URL)

    test = r.html.find('#pozicovani', first=True) # ID filer
    test = test.find("li") # li array

    resultArray = []
    message = ""
    for res in test:
        resultArray.append(res.find("a", first=True))

    print(f"Found {len(resultArray)} links ...")

    for res in resultArray:

        articleHash: str = hashlib.sha256(bytes(res.text, 'utf-8')).hexdigest()
        sql = "SELECT (hash) FROM novinky where hash = ?"
        data = (articleHash,)
        cursor_obj.execute(sql, data)
        results = cursor_obj.fetchall()
        if len(results) <= 0:
            print(f"Inserting to DB >> {res.text}")
            message = message + res.text + ",\n"
            sql = "INSERT INTO novinky (hash) VALUES(?)"
            cursor_obj.execute(sql,data)


    cursor_obj.close()


    if len(message) > 0: 
        print("New messages:")
        print(message)
        # message news
        # ....
    else:
        print("No new messages ...")
    
    
def main():
    print("Import get_news")
    
if __name__ == "__main__":
    main()