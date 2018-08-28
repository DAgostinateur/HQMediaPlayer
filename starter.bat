echo off
IF EXIST hqmediaplayer.py (
	python hqmediaplayer.py
	EXIT
)
IF EXIST hqmediaplayer.pyw (
	START "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python35\python.exe" hqmediaplayer.pyw
	EXIT
)
