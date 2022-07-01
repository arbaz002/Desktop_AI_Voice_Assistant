from dependency_assets import *


def google_search(q,engine,r):
	driver=sel_dri()
	print("In Google: \n")
	temp=q.lower().split()
	idx=temp.index('google')
	query=' '.join(temp[idx+1:])
	say("You made a Google Search For: "+query,engine)
	url="https://www.google.com/search?q="+query
	driver.get(url)
	request_result=requests.get(url,headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'})
	soup=bs4.BeautifulSoup(request_result.text,"html.parser")
	headings_object=soup.find_all('h3')

	say("The following search results were found: ",engine)
	for i in headings_object:
		head=i.getText()
		say(head,engine)
		break

	sleep(5)
	driver.close()
	return


	flag="y"
	while flag=="y":
		flag=yes_or_no(engine,r,"Would you like to close google, Say yes or no: ")
		if flag=="y": sleep(10)

	return