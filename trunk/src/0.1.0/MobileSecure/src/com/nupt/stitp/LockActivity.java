/*
 * Logs:
 * 2010-04-11:	1. 从TestLock.java和TestFullScreen.java移植过来
 * 2010-04-12:	1. 接收短信指令后，正常unlock了！
 * 				2. add onKeyDown()
 * 
 * ToDo:
 * 1. 直接在这里面进行unlock
 */
package com.nupt.stitp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.Window;
import android.view.WindowManager;

public class LockActivity extends Activity {
	
	private static final boolean DEBUG = false;
	private static final String TAG = "LockActivity";
	
	/** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
    	super.onCreate(savedInstanceState);   	
    	if (DEBUG)	Log.i(TAG, "============> " + TAG + ".onCreate()");
        
    	requestWindowFeature(Window.FEATURE_NO_TITLE);  
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,   
                                WindowManager.LayoutParams.FLAG_FULLSCREEN);
        
        getWindow().setType(WindowManager.LayoutParams.TYPE_KEYGUARD);
//        getWindow().setType(WindowManager.LayoutParams.TYPE_KEYGUARD_DIALOG);
        setContentView(R.layout.lock);
    }
    
    @Override
    protected void onNewIntent (Intent intent) {
    	super.onNewIntent(intent);
    	if (DEBUG)	Log.i(TAG, "============> " + TAG + ".onNewIntent()");
    	
    	if ( intent.getAction().equals("com.nupt.stitp.action.UNLOCK") ) {
    		finish();
    		if (DEBUG)	Log.i(TAG, "unlock success!");
    	}
    }
    
    /*	有了，我也可以类似service，在onStart()中进行操作，但是不行，参数里没有intent	*/
    
    
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        return true;      	
    }
}







