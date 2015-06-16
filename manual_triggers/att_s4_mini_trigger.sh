#! /bin/bash

#$adb shell kill `adb shell ps | grep inputmethod | tr -s ' ' | cut -d' ' -f2` && \
adb shell pm clear com.sec.android.inputmethod && \
adb shell am start -n "com.android.settings/com.android.settings.Settings" &&
sleep 1
adb shell input tap 200 90 && \
adb shell input touchscreen swipe 280 840 280 190 && \
adb shell input touchscreen tap 270 540 && \
adb shell input touchscreen tap 510 400 && \
adb shell input touchscreen tap 280 290 && \
adb shell input touchscreen tap 260 300 && \
adb shell input touchscreen tap 390 795 && \
sleep 5 && \
adb shell input touchscreen tap 270 865



#adb shell input touchscreen tap 200 1300 &&
#adb shell input touchscreen tap 1000 750 &&
#sleep 2
#adb shell input tap 200 650 &&
#sleep 2 &&
#adb shell input tap 800 1500 &&
#sleep 3 &&
#adb shell input tap 200 1500
#sleep 1
#adb shell input tap 700 1600

# adb shell su -c "am start -n com.sec.android.inputmethod/com.sec.android.inputmethod.SamsungKeypadSettings" &&
#adbx shell uiautomator dump && adbx pull /storage/emulated/legacy/window_dump.xml /tmp/window_dump.xml
#xmllint --pretty 1 /tmp/window_dump.xml | grep languages

