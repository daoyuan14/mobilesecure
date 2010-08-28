/*
 * Author: 	clzqwdy@gmail.com
 * 
 * Logs:
 * 2010-04-10:	1. 把TestLogin整合进来，将它写在LoginActivity中，
 * 				注册登录好了再跳回到主界面MobileSecure中，注意添加相应的权限
 * 				Success!
 * 				2. LoginActivity一旦成功注册后，则再也不启动它了！
 * 				用了个猥琐的方法搞定了！一旦isLogined变成true后，就再也不会启动它了！
 * 				3. 将TestUI整合进来，修改了一下arrays.xml，success!
 * 				4. 将TestPostXml整合进来！
 * 				5. 在onCreate()中增加开启后台服务，又去掉了，应该是在BootUpReceiver中开启这个服务.
 * 				6. 获取手机中的SIM卡号
 * 
 * ToDo:
 * 1. layout文件夹中是不是有的xml没用到？问马哲超
 * 2. delete sms时还存在一条指令短信，这个也要删除
 * 3. 应该再加个[追踪]，即track SIM卡的功能！
 * 
 */
package com.nupt.stitp;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import android.app.ListActivity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ListView;
import android.widget.SimpleAdapter;

public class MobileSecure extends ListActivity {
	
	private static final boolean DEBUG = false;
	private static final String TAG = "MobileSecure";
	
//	public static boolean isLogined = false;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
    	if (DEBUG)	Log.i(TAG, "============> MobileSecure.onCreate()");
    	super.onCreate(savedInstanceState);
    	
    	SharedPreferences sharedData = getSharedPreferences(LoginActivity.PREF, 0);
    	boolean isLogined = sharedData.getBoolean(LoginActivity.PREF_LOGIN, false);
    	
    	if (!isLogined) {		// 用户还没注册
    		Intent intent = new Intent(this, LoginActivity.class);
			startActivity(intent);
			finish();
    	} else {
            setContentView(R.layout.main);
    	}
    	
    	int i;
    	int[] icons = new int[] {
        		R.drawable.backup,
        		R.drawable.lock,
        		R.drawable.wipe
        		};
        final int N = icons.length;
        
        String[] texts = getResources().getStringArray(R.array.row_texts);
        String[] contents = getResources().getStringArray(R.array.row_contents);
        
        /**
         * 给这些data映射上统一的标记，方便下面提取。
         */
        List< Map<String, Object> > entries = new ArrayList< Map<String, Object> >();
        for (i = 0; i < N; i++) {
        	// Object好万能啊！
        	Map<String, Object> entry = new HashMap<String, Object>();
        	
            entry.put("icon", icons[i]);
            entry.put("text", texts[i]);
            entry.put("content", contents[i]);

            entries.add(entry);
        }
        String[] from = new String[] {"icon", "text", "content"};
        int[] to = new int[] { R.id.row_icon, R.id.row_text, R.id.row_content };
        
        final SimpleAdapter adapter = new SimpleAdapter(
                this,
                entries,				// from
                R.layout.main_row,		// to
                from,
                to );
        
        setListAdapter(adapter);	// ListActivity提供的功能
        
        // 开启后台服务，这样不好，用户每次打开主界面就会开启一下！
        // 就让第一条指令去开启它吧！
//        Intent myIntent = new Intent(this, MobileSecService.class);
//        startService(myIntent);
    }
    
    protected void onListItemClick (ListView l, View v, int position, long id) {
    	super.onListItemClick(l, v, position, id);
    	
    	switch (position) {
    	case 0:		// backup
			Intent iBackup = new Intent( this, BackupActivity.class );
			startActivity(iBackup);
			finish();		// 关闭这个Activity
			break;
    	case 1:		// lock
//    		Intent myIntent = new Intent(this, MobileSecService.class);
//        	myIntent.putExtra("ID", "Activity");
//        	myIntent.putExtra("cmd", 6);
//        	startService(myIntent);
    		Intent lockIntent = new Intent(this, LockActivity.class);
    		startActivity(lockIntent);
    		finish();
			break;
    	case 2:		// wipe
    		Intent iWipe = new Intent( this, WipeActivity.class );
			startActivity(iWipe);
			finish();
			break;
		default:
			break;
    	}
    }
}




