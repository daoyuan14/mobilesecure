// 
//  Author: clzqwdy@gmail.com
//
//  Logs:
//  2010-04-08: 1. created!
//  2010-04-09: 1. basicly achieve!
//  2010-04-10: 1. �ĳ�ÿ��10��ˢ��һ�£�
//
//  Reference:
//  1. http://www.w3school.com.cn/ajax/ajax_server.asp
//
var xmlHttp;

//function isCmdFinish(url) {
function isCmdFinish() {
    
    xmlHttp = initXmlHttpReq();
    
    // �൱�ں���ָ�룬�ص�����
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4) {
            var result = xmlHttp.responseText;
            var timer;
            
            if ( result == 'NO' ) {
                // �ȴ�5�룬�ٴη�������
//                timer = setTimeout( "sendRequest(url)", 10000); // �ظ����û�զ������
                timer = setTimeout( "sendRequest()", 10000);
            } else {
                // �����ʱ��
                clearTimeout(timer);    // ���û�д�������ô��
                // ����responseText�ı�Html
                document.getElementById('wait_pic').innerHTML = "";
                document.getElementById('isFinished').innerHTML = 
                        "<textarea name='textarea' id='cmd-font2'>���ָ���Ѿ�ִ�����!</textarea>"
            }
        }
    }
    
//    sendRequest(url);
    sendRequest();
}

/**
 *  1. ���� XMLHttpRequest ����
 */
function initXmlHttpReq() {
    if (window.XMLHttpRequest) {
        return new XMLHttpRequest();
    } else if (window.ActiveXObject) {
        try {
            return new ActiveXObject('Msxml2.XMLHTTP');
        } catch(e) {
            return new ActiveXObject('Microsoft.XMLHTTP');
        }
    }
}

function sendRequest() {
//function sendRequest(url) {
    // �õ�Ҫ��������ӵ�ַ
    
    // test: Success! ��ʱ��̨�߼���������ȷ��AjaxЧ����OK�ģ�
    //var url = "http://nupter-cn.appspot.com/finish?id=71001";
    
    // test: Failed! 'undefined'
    //alert(url);
    
    // test: Failed, 'INPUT'
    //var url = document.getElementById('strURL').nodeName;
    //alert(url);
    
//    var url = document.getElementById('input_url').lastChild.nodeValue;
    var url = document.getElementById('input_url').value;
//    alert(url);   // test: success!
    
//    document.getElementById('wait_pic').className = 'processing';

    document.getElementById('wait_pic').innerHTML = 
            "<img src='static/images/bigloading.gif' alt='Waiting' />";
    document.getElementById('isFinished').innerHTML = 
            "<textarea name='textarea' id='cmd-font1'>���ָ�ûִ�����!</textarea>"
    
    xmlHttp.open("GET", url, true);
    xmlHttp.send(null);
}






