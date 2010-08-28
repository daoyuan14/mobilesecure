/*
 * Logs:
 * 2010-04-11:	1. ��TestLock.java��TestFullScreen.java��ֲ����
 * 2010-04-12:	1. ���ն���ָ�������unlock�ˣ�
 * 				2. add onKeyDown()
 * 
 * ToDo:
 * 1. ֱ�������������unlock
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
    
    /*	���ˣ���Ҳ��������service����onStart()�н��в��������ǲ��У�������û��intent	*/
    
    
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        return true;      	
    }
}







