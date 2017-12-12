1) Install Python 3.6.0
2) Install VirtualEnv
3) Install VirtualEnvWrapper-win
4) Create VirtualEnv - DjangoAssign
	>mkvirtualenv DjangoAssign
5) Create Project Dir : 
	>mkdir DjangoAssignment
	>cd DjangoAssignment
6) bind our virtualenv with our current working directory we simply enter 
	>setprojectdir .
7) Install:
	>pip install -r requirement.txt

# In DjangoAssignment/DjangoTwitterAssignment is project dir
# twitterApp is our app 

8) To Create New DB:
	> python manage.py makemigrations
	> python manage.py migrate
9) Run Server
	> Python manage.py runserver

10) Open below urlS in browser:

>http://localhost:8000/twitter/follower/?twitterhandle=netflix

>http://localhost:8000/twitter/following/?twitterhandle=netflix

>http://localhost:8000/twitter/toptweets/?twitterhandle=SirJadeja

>http://localhost:8000/twitter/savetweetcount
#In This Post method add any twitter handle name i.e. netflix and press enter
# For PUT method, open http://localhost:8000/twitter/savetweetcount/1



Open below url to GET tweets from DB:
>localhost:8000/twitter/tweettrends/
>> in filter enter name

