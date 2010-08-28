/*
 * Logs:
 * 2010-04-10:	1. 从TestUI中移植过来！
 * 				2. 向MobileSecService发出相应的指令，success!
 * 
 */
package com.nupt.stitp;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import android.app.ListActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.Toast;

public class BackupActivity extends ListActivity{
	@Override
	public void onCreate(Bundle savedInstanceState){
		super.onCreate(savedInstanceState);
		setContentView(R.layout.backup);
		setTitle("MobileSecure :: Backup");
		
		int i;
		int icons[] = new int[]{
				R.drawable.sms,
				R.drawable.contacts,
				R.drawable.calllogs
		};
		final int N = icons.length;
		String[] texts = getResources().getStringArray(R.array.backup_row_texts);
		String[] contents = getResources().getStringArray(R.array.backup_row_contents);
		List<Map<String,Object>> entries = new ArrayList<Map<String,Object>>();
		for(i = 0;i < N;i++){
			Map<String,Object> entry = new HashMap<String,Object>();
			entry.put("icon",icons[i]);
			entry.put("text",texts[i] );
			entry.put("content", contents[i]);
			
			entries.add(entry);
		}
		String[] from = new String[]{"icon","text","content"};
		int[] to = new int[] {R.id.row_icon,R.id.row_text,R.id.row_content};
		final SimpleAdapter adapter = new SimpleAdapter(this,entries,R.layout.main_row,from,to);
		setListAdapter(adapter);
		
	}
	
	@Override
	public boolean onCreateOptionsMenu(Menu menu){
		menu.add(0, Menu.FIRST, 0, "Back");
		return true;
	}
	
	@Override
	public boolean onOptionsItemSelected(MenuItem item){
		super.onOptionsItemSelected(item);
		switch(item.getItemId()){
			case Menu.FIRST:
				Intent intent = new Intent(this, MobileSecure.class);
				// 跟finish()的区别，哪个好？问马哲超
				intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);//清除Activity栈顶的活动
				startActivity(intent);
		}
		return false;
	}

	protected void onListItemClick (ListView l, View v, int position, long id) {
    	super.onListItemClick(l, v, position, id);
    	
    	Intent myIntent = new Intent(this, MobileSecService.class);
    	myIntent.putExtra("ID", "Activity");
    	
    	switch (position) {
    	case 0:		// backup sms
    		myIntent.putExtra("cmd", 1);
    		startService(myIntent);  
    		
    		// 等待图标的显示：正在执行中
    		
    		// 执行完成后，给个Toast提示
    		Toast.makeText(this, "Backup sms, Success!", Toast.LENGTH_SHORT)
		 	 	 .show();
			break;
    	case 1:		// backup contacts
    		myIntent.putExtra("cmd", 0);
    		startService(myIntent);
    		
    		// 执行完成后，给个Toast提示
    		Toast.makeText(this, "Backup contacts, Success!", Toast.LENGTH_SHORT)
		 	 	 .show();
    		break;
    	case 2:		// backup call logs
    		myIntent.putExtra("cmd", 2);
    		startService(myIntent);
    		
    		// 执行完成后，给个Toast提示
    		Toast.makeText(this, "Backup call logs, Success!", Toast.LENGTH_SHORT)
		 	 	 .show();
    		break;
		default:
			break;
    	}
    }
}



