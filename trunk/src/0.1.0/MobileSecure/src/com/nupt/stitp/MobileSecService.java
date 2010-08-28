/*
 * 	Author: clzqwdy@gmail.com
 * 
 * 	Logs:
 * 	2010-04-10:	1. 从TestPostXml中移植过来！
 * 				2. 增加从SharedPreferences中获取strKEY的部分
 * 				3. 对于来自Activity和Receiver的指令的不同处理
 * 				4. 解决了backupXML等xml中的nid为null的错误
 * 				5. 增加Lock部分的处理和传输，TestPostXml中的MainActivity.java中有写一部分
 * 				6. 在service中启动一个activity遇到了问题
 * 				7. 从主界面lock，则不用跑到service里面来处理了！
 *  2010-04-12:	1. 使用了unlockIntent.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
 *  			从service关闭了一个Activity
 *  			2. 增加了if (DEBUG)
 *  2010-05-01:	1. add HTTPS
 * 
 * 	ToDo:
 * 	done! 1. 线程何时进行垃圾回收呢？！
 * 	应该是run()方法执行完，它就结束了。
 *  2. delect的时候为啥count总是0呢？只有Contacts deleted: 4是正常的
 * 
 */
package com.nupt.stitp;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.HTTP;
import android.app.Service;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.os.IBinder;
import android.provider.CallLog.Calls;
import android.provider.Contacts.People;
import android.telephony.TelephonyManager;
import android.util.Log;

public class MobileSecService extends Service {
	
	private static final boolean DEBUG = false;
	private static final String TAG = "MobileSecService";
	public static String strEncode = "key";
	
	String strID = "";
	
	/*	all KEYs	*/
//	String strKEY = "agludXB0ZXItY25yDQsSBUxvZ2luGIH6AQw";	// clzqwdy@gmail.com
	String strKEY;
	
	// all XMLs
	String headXML   	=	"<?xml version='1.0' encoding='UTF-8'?>";
	String backupXML, calllogXML, smsXML, lockXML;
    
    // all URLs
	String lockURL		= 	"https://nupter-cn.appspot.com/rpc/lock";
    String calllogURL	= 	"https://nupter-cn.appspot.com/rpc/calllog";
    String backupURL 	= 	"https://nupter-cn.appspot.com/rpc/backup";
    String smsURL 		= 	"https://nupter-cn.appspot.com/rpc/sms";
    String cmdURL 		= 	"https://nupter-cn.appspot.com/rpc/cmd";		// 反馈指令执行情况的
    
    // 创建URI
    Uri allPeople = People.CONTENT_URI;
    Uri allCall = Calls.CONTENT_URI;
    Uri allSmsInbox = Uri.parse("content://sms/inbox");
    Uri delSms = Uri.parse("content://sms/");
    Uri oneName;		// 动态的

	@Override
	public IBinder onBind(Intent intent) {
		if (DEBUG)	Log.i(TAG, "============> InfoSecService.onBind");
		return null;
	}
	
	@Override
	public void onCreate() {
		if (DEBUG)	Log.i(TAG, "============> InfoSecService.onCreate");
		
		// strKEY is right, but in XML it is 'null'
		// 知道为什么了，因为你虽然修改了strKEY，但是smsXML并没有马上跟着修改！
		SharedPreferences sharedData = getSharedPreferences(LoginActivity.PREF, 0);
		strKEY = sharedData.getString(LoginActivity.PREF_KEY, "");
		Log.i(TAG, "strKEY = " + strKEY);
		
		// 再次赋下值
		backupXML	= 	headXML + "<contact nid='" + strKEY + "'>";
		Log.i(TAG, "backupXML = " + backupXML);
		calllogXML 	= 	headXML + "<calllog nid='" + strKEY + "'>";
		Log.i(TAG, "calllogXML = " + calllogXML);
		smsXML 		= 	headXML + "<sms nid='" + strKEY + "'>";
		Log.i(TAG, "smsXML = " + smsXML);
		lockXML 	= 	headXML + "<phone nid='" + strKEY + "'>";
		Log.i(TAG, "lockXML = " + lockXML);
	}
	
	// if remove 'Intent intent, int startId'
	/**
	 * 要好好利用这两个参数啊：Intent intent, int startId
	 * startId对于我们是没什么用的
	 */
	@Override
	public void onStart(Intent intent, int startId) {
		super.onStart(intent, startId);		// 要写否？		
		if (DEBUG)	Log.i(TAG, "============> InfoSecService.onStart");
		
		// strKEY is right, but in XML it is 'null'
//		SharedPreferences sharedData = getSharedPreferences(LoginActivity.PREF, 0);
//		strKEY = sharedData.getString(LoginActivity.PREF_KEY, "");
//		Log.i(TAG, strKEY);
		
		Bundle bundle = intent.getExtras();
		
		if (bundle != null) {
			int nCmd;
			nCmd = intent.getIntExtra("cmd", -1);

			strID = intent.getStringExtra("ID");
			if (DEBUG)	Log.i(TAG, "strID = " + strID);	// test: Success!
			
			if (nCmd != -1) {
				
				switch(nCmd) {
				case 0:						// backup Contacts
					if (DEBUG)	Log.i(TAG, "nCmd == 0");

					new Thread(){
						@Override
						public void run () {
							ContentResolver cr = getContentResolver();
							Cursor curContact = cr.query(allPeople, null, null, null, null);
							getContactData(curContact);
							if ( sendData(backupXML, backupURL) ) {
								if ( strID.equals("Activity") ) {
									if (DEBUG)	Log.v(TAG, "Backup Contacts: Success!");
									// 最好给Activity一个反馈
								} else {
									sendCmdData(strID, cmdURL);
								}
							}
							// 最好是当出现失败，也返回一个错误信息。
						}
					}.start();
					
					break;
				case 1:						// backup Sms
					if (DEBUG)	Log.i(TAG, "nCmd == 1");
					
					new Thread(){
						@Override
						public void run () {
							// get Sms
							ContentResolver cr = getContentResolver();
							Cursor curSms = cr.query(allSmsInbox,							// 相当于table
									// "address"就是发信人
									new String[] { "address", "person", "date", "body" },	// 相当于select
									null,													// 相当于where
									null,
									"date DESC");
							getSmsData(curSms);
							if ( sendData(smsXML, smsURL) ) {								
								if ( strID.equals("Activity") ) {
									// 最好给Activity一个反馈
									if (DEBUG)	Log.v(TAG, "Backup Sms: Success!");
								} else {
									sendCmdData(strID, cmdURL);
								}
							}
						}
					}.start();
					
					break;
				case 2:						// backup CallLogs
					if (DEBUG)	Log.i(TAG, "nCmd == 2");
					
					new Thread(){
						@Override
						public void run () {
							// get call log data
							ContentResolver cr = getContentResolver();
							Cursor curCallLog = cr.query(allCall, null, null, null, Calls.DATE + " DESC");
							getCallLogData(curCallLog);
							if ( sendData(calllogXML, calllogURL) ) {
								if ( strID.equals("Activity") ) {
									// 最好给Activity一个反馈
									if (DEBUG)	Log.v(TAG, "Backup CallLogs: Success!");
								} else {
									sendCmdData(strID, cmdURL);
								}
							}
						}
					}.start();
					
					break;
				case 3:						// delete Contacts
					if (DEBUG)	Log.i(TAG, "nCmd == 3");
					
					new Thread(){
						@Override
						public void run () {
							ContentResolver cr = getContentResolver();
							int nCount = cr.delete(allPeople, null, null);
							// 能不能显示出nCount的值啊？怎么老是0呢？！
							if (DEBUG)	Log.v(TAG, "Contacts deleted:" + nCount);
							
							if ( strID.equals("Activity") ) {
								// 最好给Activity一个反馈
								if (DEBUG)	Log.v(TAG, "Delete Contacts: Success!");
							} else {
								sendCmdData(strID, cmdURL);
							}
						}
					}.start();
					
					break;
				case 4:						// delete Sms
					if (DEBUG)	Log.i(TAG, "nCmd == 4");
					
					new Thread(){
						@Override
						public void run () {
							ContentResolver cr = getContentResolver();
							int nCount = cr.delete(delSms, null, null);
							if (DEBUG)	Log.v(TAG, "Sms deleted:" + nCount);;
							
							if ( strID.equals("Activity") ) {
								// 最好给Activity一个反馈
								if (DEBUG)	Log.v(TAG, "Delete Sms: Success!");
							} else {
								sendCmdData(strID, cmdURL);
							}
						}
					}.start();
					
					break;
				case 5:						// delete CallLogs
					if (DEBUG)	Log.i(TAG, "nCmd == 5");
					
					new Thread(){
						@Override
						public void run () {
							ContentResolver cr = getContentResolver();
							int nCount = cr.delete(allCall, null, null);
							if (DEBUG)	Log.v(TAG, "CallLogs deleted:" + nCount);
							
							if ( strID.equals("Activity") ) {
								// 最好给Activity一个反馈
								if (DEBUG)	Log.v(TAG, "Delete CallLogs: Success!");
							} else {
								sendCmdData(strID, cmdURL);
							}
						}
					}.start();
					
					break;
				case 6:						// lock, and in unlock, don't have to send XML
					if (DEBUG)	Log.i(TAG, "nCmd == 6");
					
					Intent lockIntent = new Intent(this, LockActivity.class);
					lockIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
					// need it? It will be wrong!
//					lockIntent.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
					startActivity(lockIntent);
					
					new Thread(){
						@Override
						public void run () {
							// send xml
							getLockData("true");
							if ( sendData(lockXML, lockURL) ) {
								sendCmdData(strID, cmdURL);
							}
						}
					}.start();
					
					break;
				case 7:						// unlock
					if (DEBUG)	Log.i(TAG, "nCmd == 6");
					
					// {这个不用了}比对传进来的pswd，只需在LockActivity中做
					// 让LockActivity消失, hard!
					Intent unlockIntent = new Intent("com.nupt.stitp.action.UNLOCK");	
//					try {
//						IntentSender intentSender = null;
//						// int code怎么用？
//						intentSender.sendIntent(this, 3, unlockIntent, null, null);
//					} catch (SendIntentException e) {
//						e.printStackTrace();
//					}
					unlockIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
					unlockIntent.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
					startActivity(unlockIntent);
					
					new Thread(){
						@Override
						public void run () {
							// send xml
							getLockData("false");
							if ( sendData(lockXML, lockURL) ) {
								sendCmdData(strID, cmdURL);
							}
						}
					}.start();
					
					break;
				default:
					if (DEBUG)	Log.e(TAG, "nCmd == unExpected error!");
					break;
				}
			}			
		} else {							// do nothing, just start
			if (DEBUG)	Log.i(TAG, "No cmd is here, and InfoSecService is started!");
		}
	}
	
	@Override
	public void onDestroy () {
		if (DEBUG)	Log.i(TAG, "============> InfoSecService.onDestroy");
	}
	
	private void getLockData(String strBoolean) {
    	TelephonyManager telephonyManager = 
        	(TelephonyManager)getSystemService( Context.TELEPHONY_SERVICE );
    	
    	String strSimNum = telephonyManager.getLine1Number();
        if( DEBUG )	Log.i(TAG, "Line1Number = " + strSimNum);
        
        lockXML +=
        	"<num>" + strSimNum + "</num>" +
        	"<lock>" + strBoolean + "</lock>" +
        	"</phone>";
    }

	private void getContactData(Cursor cur){ 
		if (DEBUG)	Log.i(TAG, "in InfoSecService.getContactData");
		
	    if (cur.moveToFirst()) {

	        String name; 
	        String phoneNumber;
	        int nameColumn = cur.getColumnIndex(People.NAME); 
	        int phoneColumn = cur.getColumnIndex(People.NUMBER);
	        
	        //int nCounter = 0;		// 循环计数器
	        	    
	        do {
	            // Get the field values
	            name = cur.getString(nameColumn);
	            phoneNumber = cur.getString(phoneColumn);
	           
	            // Do something with the values.
	            
	            /*
	            Log.i("Contact", name);
	            Log.i("Contact", phoneNumber);
	            */
	            
	            // produce XML data
	            backupXML += 
	            		"<entity>" +
	            		"<name>" + name + "</name>" +
	            		"<phone>" + phoneNumber +"</phone>" +
	            		"</entity>";
	            
	            //nCounter++;		// 一条记录则nCounter==1	            
	            // test 'strXML'
	            //Log.i("Contact", backupXML);
	            
	        } while (cur.moveToNext());
	        
	        // add </contact> to 'backupXML'
	        backupXML += "</contact>";
	        // log the count
	        // 需要把整型转为字符型吗？ 
	        //backupXML += "<log>" + nCounter +"</log>";
	    }
	}
	
	private void getCallLogData(Cursor cur){ 
		if (DEBUG)	Log.i(TAG, "============> in InfoSecService.getCallLogData()");
		
		if (cur.moveToFirst()) {
					
	        String strNumber, strDate, strType, strName, strDuration;
	        
	        long nDate;
	        int nType;
	        
	        // Retrieve the column-indexes: 
	        // phoneNumber, date, type, name and duration
	        // all return String type
	        int numberColumn = cur.getColumnIndex(Calls.NUMBER);
	        int dateColumn = cur.getColumnIndex(Calls.DATE);
	        int typeColumn = cur.getColumnIndex(Calls.TYPE);	// type can be: Incoming, Outgoing or Missed
	        int nameColumn = cur.getColumnIndex(Calls.CACHED_NAME);
	        int durationColumn = cur.getColumnIndex(Calls.DURATION);
	        
	        do {
	        	// number
	        	strNumber = cur.getString(numberColumn);
	        	// date
	        	nDate = cur.getLong(dateColumn);
	        	strDate = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date(nDate));
	        	// type
	        	nType = cur.getInt(typeColumn);
	        	switch (nType)
	        	{
	        	case Calls.INCOMING_TYPE:
	        		strType = "Incoming";
	        		break;			// 千万别忘加break哈，否则肯定会变成Error的！
	        	case Calls.MISSED_TYPE:
	        		strType = "Missed";
	        		break;
	        	case Calls.OUTGOING_TYPE:
	        		strType = "Outgoing";
	        		break;
	        	default:
	        		strType = "Error";
	        		break;
	        	}
	        	// name
	            strName = cur.getString(nameColumn);
	            // duration
	            //nDuration = cur.getLong(durationColumn);
	            // 在服务端再把" seconds"加上去，客户端应该尽可能少地传输数据。服务端的网页显示部分来添加，数据库还是只要数字就可以了
	            strDuration = cur.getString(durationColumn);
	            
	            // produce call log XML data
	            calllogXML += 
	            		"<entity>" +
	            		"<name>" + strName + "</name>" +
	            		"<number>" + strNumber +"</number>" +
	            		"<type>" + strType + "</type>" +
	            		"<date>" + strDate + "</date>" +
	            		"<duration>" + strDuration + "</duration>" +
	            		"</entity>";
	            
	        } while (cur.moveToNext());
	        
	        calllogXML += "</calllog>";
	        if (DEBUG)	Log.i(TAG, calllogXML);
		}
	}
	
	private void getSmsData(Cursor cur) {
		if (DEBUG)	Log.i(TAG, "============> in " + TAG + ".getSmsData()");
		
		if (cur.moveToFirst()) {
			
			long nDate;
			long nName;
			String strBody, strName, strNumber, strDate;
			ContentResolver oneCR = getContentResolver();
			
			do {
				// get Number from "address"
				strNumber = cur.getString(0);		// 手机号
				// get Name from "person"
//                strName = cur.getString(1);		// 直接用getString得到的是字符型数字
//				nName = cur.getLong(1);
//				nName = String.valueOf(nName);	// still is ID, not Name
				
				nName = cur.getLong(1);
				/*	get query in People	*/
				// Use the ContentUris method to produce the base URI for the contact with _ID == nName.
				oneName = ContentUris.withAppendedId(People.CONTENT_URI, nName);
				// Then query for this specific record
				Cursor curName = oneCR.query( oneName,
						new String[] { People.NAME },
						null, null, null);
				if (curName.moveToFirst()) {
					strName = curName.getString(0);
				} else {
					strName = "";
				}
				
				// get Date from "date"
                nDate = cur.getLong(2);              
                strDate = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date(nDate));
                // get Body from "body"
                strBody = cur.getString(3);
                
                // produce sms XML data
                smsXML += 
            		"<entity>" +
            		"<name>" + strName + "</name>" +
            		"<number>" + strNumber +"</number>" +
            		"<date>" + strDate + "</date>" +
            		"<body>" + strBody + "</body>" +
            		"</entity>";
                
			} while (cur.moveToNext());
			
			smsXML += "</sms>";
			if (DEBUG)	Log.i(TAG, smsXML);
		}
	}
	
//	private void deleteContactData(Cursor cur){
//		Log.i(TAG, "in InfoSecService.deleteContactData");
//	}
	
	// send XML data to server
	private boolean sendData(String strXML, String strURL) {
		if (DEBUG)	Log.i(TAG, strXML + "\n============> in InfoSecService.sendData");
		
		HttpClient httpClient = new DefaultHttpClient();
        HttpPost httpPost = new HttpPost(strURL);
        
        try {
			StringEntity entityXML;
	        
	        entityXML = new StringEntity(strXML, "utf-8");
	        entityXML.setContentEncoding("utf-8");
			entityXML.setContentType("text/xml");
			
			httpPost.setEntity(entityXML);		
			
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
			return false;
		}
				
		try {
			// Execute HTTP Post Request 
			HttpResponse response = httpClient.execute(httpPost);
			
			// if 201, return and also log the response
			if (response.getStatusLine().getStatusCode() == HttpStatus.SC_CREATED) {				
				// 释放连接
		        httpClient.getConnectionManager().shutdown();
		        return true;
			} else {
				return false;
			}
			
		} catch (ClientProtocolException e) {
			e.printStackTrace();
			return false;
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}
	}
	
	private void sendCmdData(String strID, String strURL) {
		if (DEBUG)	Log.i(TAG, "============> in InfoSecService.sendCmdData");
		
		HttpClient httpClient = new DefaultHttpClient();
        HttpPost httpPost = new HttpPost(strURL);
        
        List<NameValuePair> nvPair = new ArrayList<NameValuePair>();
//        nvPair.add( new BasicNameValuePair("key", strKey) );
        nvPair.add( new BasicNameValuePair("ID", strID) );
        
        try {
			httpPost.setEntity(new UrlEncodedFormEntity(nvPair, HTTP.UTF_8));
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
		
		try {
			HttpResponse response = httpClient.execute(httpPost);
			
			if (response.getStatusLine().getStatusCode() == HttpStatus.SC_CREATED) {
		        httpClient.getConnectionManager().shutdown();    
			}
			
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}







