# Grafana-Import-Export

Simple script in Python 

This one does backup/restore  dashboards, datasources and folders from [Grafana](http://grafana.org/)

Support organization through of their API Key only.

Inspired in scripts written in Shell Script from [hagen1778](https://github.com/hagen1778/grafana-import-export) 

**This version just works, for the time being, in Linux plataforms**

Written for python version 2.7.x. Come soon, it'll be compatible for python 3.x

## Dependencies
For install requirements run `pip install -r requirements.txt` as root

Reminder, this script just works in ***Python 2.7.x*** version.
If you don't have this version in your environment you'll need install it.

## Commands

For you use it need passing some arguments for `./config.py`. Below is explained as do it.

Before, you'll need create the **API_KEY** in your Grafana Organization that you wanna make backup.

For this, following how to do [here](https://grafana.com/docs/http_api/auth/#create-api-token)


> ./config.py
> 
> `usage: config.py [-h] -k KEY -H HOST -d DIRECTORY [-p PROXY] (-b | -r)`
> 
>   -k --key **API_KEY** of ***Organization*** from Grafana that you wanna make backup/restore
> 
>    -H --host **HOST** for to make backup/restore
> 
>    -d --directory **DIRECTORY** where it'll storage yous backup or get your restore
> 
>    -p --proxy `host:port` Use if your environment has proxy.
>   
>    -b Flag for backup panels, datasources and folders
> 
>   -r Flag for restore every all



