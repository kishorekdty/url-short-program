import webapp2
import random
import cgi
from google.appengine.ext import db

class data(db.Model):
	longurl=db.StringProperty(multiline=True)
	shorturl=db.StringProperty()

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('<html><body>')
		self.response.out.write("""<br><br><br><br><br><br><br><br><br><br><br><form>
				<div align="center"><h1>Url Shortner</h1><br><Textarea name='longurl' row="1" cols="100"></Textarea><div><input type="submit" value="Create"></div></div>
				</form>""")
		i='a'
		j=0
		asso={}
		while i<='z':
			asso[j]=i
			i=chr(ord(i)+1)
			j=j+1
		i='A'
		while i<='Z':
			asso[j]=i
			i=chr(ord(i)+1)
			j=j+1
		i=0
		while i<=9:
			asso[j]=i
			i=i+1
			j=j+1
		
		lurl=self.request.get('longurl')

		s=random.Random()
		s=int(s.random()*10000)

		short=""
		while s>0:
			rem=s%62
			short=short+str(asso[rem])
			s=s/62

		if lurl != "":
			datastore=data(parent=db.Key.from_path('URL',lurl))
			datastore.longurl=lurl
			datastore.shorturl=short
			url=db.GqlQuery("SELECT * FROM data WHERE ANCESTOR IS :c",c=db.Key.from_path('URL',lurl))
			count =0
			for i in url:
				count=count+1
			if count==0:
				datastore.put()
			url1=db.GqlQuery("SELECT * FROM data WHERE ANCESTOR IS :c",c=db.Key.from_path('URL',lurl))
			
			for i in url1:
				
				self.response.out.write("""<div align="center"><br>Your short url is:<br><font size="5" face="philosopher" color="blue" >kishoreshortner.appspot.com/""")
				self.response.out.write(i.shorturl)
				self.response.out.write("""<br>""")
			self.response.out.write("""</font></br></body></html>""")
		if self.request.path[1:]!="":
			whole=data.all()
			s = whole.filter("shorturl =",self.request.path[1:]).get()
			self.redirect(str(s.longurl))			

app=webapp2.WSGIApplication([('/.*',MainPage)],debug=True)		
