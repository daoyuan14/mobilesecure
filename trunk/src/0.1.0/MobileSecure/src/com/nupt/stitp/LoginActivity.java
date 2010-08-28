/*
 * Author: 	clzqwdy@gmail.com
 * 
 * Logs:
 * 2010-04-10:	1. 从TestLogin移植过来，strKey将来要在后台服务中获取；
 * 				2. sendLoginData()由void型改为boolean，增加登录成功的Toast；
 * 				3. 删掉了onStop()，把get SharedPreferences移到了onClick中；
 * 				4. 在onClick中增加了jump to MobileSecure Activity
 * 				5. 把SIM卡号也一并传过去！
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
	// 改成https，它是不是就会自动请求443端口了，而不是80端口了？
	public static final String loginURL = "https://nupter-cn.appspot.com/rpc/login";
	
	// tag of SharedPreferences
	public static final String PREF = "MOBILESECURE";
	public static final String PREF_KEY = "KEY";
	public static final String PREF_PSWD = "PASSWORD";
	public static final String PREF_LOGIN = "isLogined";
	
	private String strKey;
	private String strSimNum;
	// 声明控件变量
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
    
    // 定义控件变量
    private void findViews() {
    	button_login = (Button) findViewById(R.id.submit);
        field_email = (EditText) findViewById(R.id.email);
        field_pswd = (EditText) findViewById(R.id.pswd);	
    }
    
    private void initButtons() {
    	
    	button_login.setOnClickListener(new OnClickListener() {  
            public void onClick(View arg0) {
            	if ( sendLoginData() ) {
            		Toast.makeText(LoginActivity.this, "你已经成功注册，现在跳到主界面！", Toast.LENGTH_SHORT)	// LoginActivity.this
           		 		 .show();
            		
            		// get a SharedPreferences object
            		SharedPreferences settings = getSharedPreferences(PREF, 0);
            		settings.edit()			// 处于可编辑状态
            			.putString( PREF_KEY, strKey )		// 服务端返回的KEY
            			.putString( PREF_PSWD, field_pswd.getText().toString() )
            			.putBoolean( PREF_LOGIN, true )
            			.commit();			// 保存SharedPreferences
            		
            		// jump to MobileSecure Activity
            		Intent intent = new Intent(LoginActivity.this, MobileSecure.class);
    				startActivity(intent);
    				finish();
    				
            	} else {
            		Toast.makeText(LoginActivity.this, "你没有注册成功，请重新尝试！", Toast.LENGTH_SHORT)
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
        	// UrlEncodedFormEntity()最重要的功能，就是幫你加上 setContentType("application/x-www-form-urlencoded")。
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
				// 释放连接
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






