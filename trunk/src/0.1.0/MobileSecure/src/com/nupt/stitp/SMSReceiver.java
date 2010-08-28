/*
 * Author: 	clzqwdy@gmail.com
 * 
 * Logs:
 * 2010-04-10:	1. ��TestPostXml����ֲ������
 * 				2. Ϊɶready to backup sms!�������Σ���
 * 2010-04-11:	1. ���Ӷ�lock��unlockָ��Ĵ���
 * 2010-04-12:	1. add private static final boolean DEBUG = false;
 * 2010-05-22:	1. �ܲ��ܰ��յ���ָ�������ɾ������
 * 
 */
package com.nupt.stitp;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsMessage;
import android.util.Log;

public class SMSReceiver extends BroadcastReceiver {
	
	private static final boolean DEBUG = false;
	private static final String TAG = "SMSReceiver";
	
	@Override
	public void onReceive(Context context, Intent intent) {

		
		Bundle bundle = intent.getExtras();
		SmsMessage[] smsMsgs = null;
		
		if (bundle != null) {
			Object[] pdus = (Object[]) bundle.get("pdus");
			smsMsgs = new SmsMessage[pdus.length];

			for (int i=0; i<smsMsgs.length; i++){
				smsMsgs[i] = SmsMessage.createFromPdu( (byte[])pdus[i] );
			}
			
			// ���ܷ��������ѭ������������������
			Intent myIntent = new Intent(context, MobileSecService.class);
			
			//
			// �ж��Ƿ�������Ҫ�����ָ��
			// ���ݵ�����Ϣ������
			//
			for (SmsMessage message : smsMsgs) { 
				String strMsg = message.getMessageBody();
				
				if ( strMsg.startsWith("--") && strMsg.endsWith("--") ) {
					if (DEBUG)	Log.v(TAG, "It is our cmd!");
					
					String regexSplit = "--";
					String[] strMsgs = strMsg.split(regexSplit);
					String strCmd = strMsgs[1];			// "b1"
					String strID = strMsgs[2];			// "66001"
					
					myIntent.putExtra("ID", strID);
					
					// test Success!
					if (DEBUG)	Log.i(TAG, "strCmd = " + strCmd);
					if (DEBUG)	Log.i(TAG, "strID = " + strID);
					
					//-------------------------------
					// backup data
					//-------------------------------
					// backup Contacts
		            if ( strCmd.equals("b0") ) {
		            	if (DEBUG)	Log.i(TAG, "ready to backup contact!");
		            	
		            	myIntent.putExtra("cmd", 0);
		            	context.startService(myIntent);
		            }
		            // backup Sms
		            if ( strCmd.equals("b1") ) {
		            	if (DEBUG)	Log.i(TAG, "ready to backup sms!");
		            	
		            	myIntent.putExtra("cmd", 1);
		            	context.startService(myIntent);
		            }
		            // backup CallLogs
		            if ( strCmd.equals("b2") ) {
		            	if (DEBUG)	Log.i(TAG, "ready to backup calllog!");
		            	
		            	myIntent.putExtra("cmd", 2);
		            	context.startService(myIntent);
		            }
		            
		          	//-------------------------------
					// delete data
					//-------------------------------
		            // delete Contacts
		            if ( strCmd.equals("d0") ) {
		            	if (DEBUG)	Log.i(TAG, "ready to delete contact!");
		            	
		            	myIntent.putExtra("cmd", 3);
		            	context.startService(myIntent);
		            }
		            // delete Sms
		            if ( strCmd.equals("d1") ) {
		            	if (DEBUG)	Log.i(TAG, "ready to delete sms!");
		            	
		            	myIntent.putExtra("cmd", 4);
		            	context.startService(myIntent);
		            }
		            // delete CallLogs
		            if ( strCmd.equals("d2") ) {
		            	if (DEBUG)	Log.i(TAG, "ready to delete calllog!");
		            	
		            	myIntent.putExtra("cmd", 5);
		            	context.startService(myIntent);
		            }
		            //-------------------------------
					// lock and unlock
					//-------------------------------
		            // lock
		            if ( strCmd.equals("l0") ) {
		            	if (DEBUG)	Log.i(TAG, "ready to lock!");
		            	
		            	myIntent.putExtra("cmd", 6);
		            	context.startService(myIntent);
		            }
		            // unlock
		            if ( strCmd.equals("l1") ) {
		            	if (DEBUG)	Log.i(TAG, "ready to unlock!");
		            	
		            	myIntent.putExtra("cmd", 7);
		            	context.startService(myIntent);
		            }
				} else {
					if (DEBUG)	Log.v(TAG, "It's not our cmd!");
					// do nothing
				}
	        }
		}
	}
}






