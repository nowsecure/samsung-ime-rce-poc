#! /bin/bash

#$adb shell kill `adb shell ps | grep inputmethod | tr -s ' ' | cut -d' ' -f2` && \
adb shell pm clear com.sec.android.inputmethod && \
adb shell am start -n "com.android.settings/com.android.settings.GridSettings" &&
sleep 1
adb shell input touchscreen swipe 1000 1000 0 0 && adb shell input touchscreen swipe 1000 1000 0 0 && adb shell input touchscreen tap 200 1300 && adb shell input touchscreen tap 1000 750 &&
sleep 2
adb shell input tap 200 650 &&
sleep 2 &&
adb shell input tap 800 1500 &&
sleep 3 &&
adb shell input tap 200 1500
sleep 1
adb shell input tap 700 1600

# adb shell su -c "am start -n com.sec.android.inputmethod/com.sec.android.inputmethod.SamsungKeypadSettings" &&
#adbx shell uiautomator dump && adbx pull /storage/emulated/legacy/window_dump.xml /tmp/window_dump.xml
#xmllint --pretty 1 /tmp/window_dump.xml | grep languages

