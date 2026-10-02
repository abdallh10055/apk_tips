[app]
title = نصائح اليوم
package.name = dailytips
package.domain = org.inlex
source.dir = .
source.include_exts = py,json
version = 0.1
requirements = python3,kivy==2.3.0,plyer,pyjnius,android,arabic-reshaper==3.0.0,python-bidi==0.4.2
orientation = portrait
fullscreen = 0
android.permissions = POST_NOTIFICATIONS,FOREGROUND_SERVICE,RECEIVE_BOOT_COMPLETED,WAKE_LOCK
android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
services = run:service/main.py:foreground

[buildozer]
log_level = 2
warn_on_root = 1
