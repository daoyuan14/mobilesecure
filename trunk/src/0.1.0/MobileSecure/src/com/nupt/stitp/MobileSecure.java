/*
 * Author: 	clzqwdy@gmail.com
 * 
 * Logs:
 * 2010-04-10:	1. ��TestLogin���Ͻ���������д��LoginActivity�У�
 * 				ע���¼���������ص�������MobileSecure�У�ע�������Ӧ��Ȩ��
 * 				Success!
 * 				2. LoginActivityһ���ɹ�ע�������Ҳ���������ˣ�
 * 				���˸�����ķ����㶨�ˣ�һ��isLogined���true�󣬾���Ҳ�����������ˣ�
 * 				3. ��TestUI���Ͻ������޸���һ��arrays.xml��success!
 * 				4. ��TestPostXml���Ͻ�����
 * 				5. ��onCreate()�����ӿ�����̨������ȥ���ˣ�Ӧ������BootUpReceiver�п����������.
 * 				6. ��ȡ�ֻ��е�SIM����
 * 
 * ToDo:
 * 1. layout�ļ������ǲ����е�xmlû�õ��������ܳ�
 * 2. delete smsʱ������һ��ָ����ţ����ҲҪɾ��
 * 3. Ӧ���ټӸ�[׷��]����track SIM���Ĺ��ܣ�
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
    	
    	if (!isLogined) {		// �û���ûע��
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
         * ����Щdataӳ����ͳһ�ı�ǣ�����������ȡ��
         */
        List< Map<String, Object> > entries = new ArrayList< Map<String, Object> >();
        for (i = 0; i < N; i++) {
        	// Object�����ܰ���
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
        
        setListAdapter(adapter);	// ListActivity�ṩ�Ĺ���
        
        // ������̨�����������ã��û�ÿ�δ�������ͻῪ��һ�£�
        // ���õ�һ��ָ��ȥ�������ɣ�
//        Intent myIntent = new Intent(this, MobileSecService.class);
//        startService(myIntent);
    }
    
    protected void onListItemClick (ListView l, View v, int position, long id) {
    	super.onListItemClick(l, v, position, id);
    	
    	switch (position) {
    	case 0:		// backup
			Intent iBackup = new Intent( this, BackupActivity.class );
			startActivity(iBackup);
			finish();		// �ر����Activity
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




