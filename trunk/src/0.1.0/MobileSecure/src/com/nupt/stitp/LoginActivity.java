/*
 * Author: 	clzqwdy@gmail.com
 * 
 * Logs:
 * 2010-04-10:	1. ��TestLogin��ֲ������strKey����Ҫ�ں�̨�����л�ȡ��
 * 				2. sendLoginData()��void�͸�Ϊboolean�����ӵ�¼�ɹ���Toast��
 * 				3. ɾ����onStop()����get SharedPreferences�Ƶ���onClick�У�
 * 				4. ��onClick��������jump to MobileSecure Activity
 * 				5. ��SIM����Ҳһ������ȥ��
 * 
 */
package com.nupt.stitp;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.HTTP;
import org.apache.http.util.EntityUtils;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.telephony.TelephonyManager;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class LoginActivity extends Activity {
	
	private static final boolean DEBUG = false;
	private static final String TAG = "LoginActivity";
	
//	public static final String loginURL = "http://nupter-cn.appspot.com/rpc/login";
	// �ĳ�https�����ǲ��Ǿͻ��Զ�����443�˿��ˣ�������80�˿��ˣ�
	public static final String loginURL = "https://nupter-cn.appspot.com/rpc/login";
	
	// tag of SharedPreferences
	public static final String PREF = "MOBILESECURE";
	public static final String PREF_KEY = "KEY";
	public static final String PREF_PSWD = "PASSWORD";
	public static final String PREF_LOGIN = "isLogined";
	
	private String strKey;
	private String strSimNum;
	// �����ؼ�����
    private Button button_login;
    private EditText field_email;
    private EditText field_pswd;
    
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);     
        setTitle("MobileSecure :: Login");
        
        findViews();
        initButtons();
        getSimNum();
    }
    
    // ����ؼ�����
    private void findViews() {
    	button_login = (Button) findViewById(R.id.submit);
        field_email = (EditText) findViewById(R.id.email);
        field_pswd = (EditText) findViewById(R.id.pswd);	
    }
    
    private void initButtons() {
    	
    	button_login.setOnClickListener(new OnClickListener() {  
            public void onClick(View arg0) {
            	if ( sendLoginData() ) {
            		Toast.makeText(LoginActivity.this, "���Ѿ��ɹ�ע�ᣬ�������������棡", Toast.LENGTH_SHORT)	// LoginActivity.this
           		 		 .show();
            		
            		// get a SharedPreferences object
            		SharedPreferences settings = getSharedPreferences(PREF, 0);
            		settings.edit()			// ���ڿɱ༭״̬
            			.putString( PREF_KEY, strKey )		// ����˷��ص�KEY
            			.putString( PREF_PSWD, field_pswd.getText().toString() )
            			.putBoolean( PREF_LOGIN, true )
            			.commit();			// ����SharedPreferences
            		
            		// jump to MobileSecure Activity
            		Intent intent = new Intent(LoginActivity.this, MobileSecure.class);
    				startActivity(intent);
    				finish();
    				
            	} else {
            		Toast.makeText(LoginActivity.this, "��û��ע��ɹ��������³��ԣ�", Toast.LENGTH_SHORT)
      		 		 	 .show();
            	}
            }
        });
    }
    
    private void getSimNum() {
    	TelephonyManager telephonyManager = 
        	(TelephonyManager)getSystemService( Context.TELEPHONY_SERVICE );
    	
    	strSimNum = telephonyManager.getLine1Number();
        if( DEBUG )	Log.i(TAG, "Line1Number = " + strSimNum);
    }
    
    protected boolean sendLoginData() {
		HttpClient httpClient = new DefaultHttpClient();
        HttpPost httpPost = new HttpPost(loginURL);
        
        List<NameValuePair> nvPair = new ArrayList<NameValuePair>();
        nvPair.add(new BasicNameValuePair("email", field_email.getText().toString()));
        nvPair.add(new BasicNameValuePair("pswd", field_pswd.getText().toString()));
        // newly added!
        nvPair.add( new BasicNameValuePair("sim", strSimNum) );
        
        try {
        	// add data
        	// UrlEncodedFormEntity()����Ҫ�Ĺ��ܣ����ǎ������ setContentType("application/x-www-form-urlencoded")��
			httpPost.setEntity(new UrlEncodedFormEntity(nvPair, HTTP.UTF_8));
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
			return false;
		}
		
		try {
			HttpResponse response = httpClient.execute(httpPost);
			
			// if 201, return and also log the response
			if (response.getStatusLine().getStatusCode() == HttpStatus.SC_CREATED) {
				strKey = EntityUtils.toString(response.getEntity());
				if (DEBUG)	Log.i(TAG, strKey);				
				// �ͷ�����
		        httpClient.getConnectionManager().shutdown();    
		        return true;
			}
			return false;
			
		} catch (ClientProtocolException e) {
			e.printStackTrace();
			return false;
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}
	}
    
}






