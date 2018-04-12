# sync-lunch
Get lunch weekly lunch orders and sync it to a calendar

* Create a new service account in google cloud console in a new project
* Get the json file with the key locally
* Create a new calendar
* Give access r/w to your google account
* Run 
```
python lunch.py |python googleupdate.py
```

