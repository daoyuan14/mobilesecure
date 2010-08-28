// 
//  Author: clzqwdy@gmail.com
//
//  Logs:
//  2010-04-08: 1. created!
//  2010-04-09: 1. basicly achieve!
//  2010-04-10: 1. 改成每隔10秒刷新一下！
//
//  Reference:
//  1. http://www.w3school.com.cn/ajax/ajax_server.asp
//
var xmlHttp;

//function isCmdFinish(url) {
function isCmdFinish() {
    
    xmlHttp = initXmlHttpReq();
    
    // 相当于函数指针，回调函数
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4) {
            var result = xmlHttp.responseText;
            var timer;
            
            if ( result == 'NO' ) {
                // 等待5秒，再次发送请求
//                timer = setTimeout( "sendRequest(url)", 10000); // 重复设置会咋样？！
                timer = setTimeout( "sendRequest()", 10000);
            } else {
                // 清除定时器
                clearTimeout(timer);    // 如果没有创建会怎么样
                // 根据responseText改变Html
                document.getElementById('wait_pic').innerHTML = "";
                document.getElementById('isFinished').innerHTML = 
                        "<textarea name='textarea' id='cmd-font2'>你的指令已经执行完成!</textarea>"
            }
        }
    }
    
//    sendRequest(url);
    sendRequest();
}

/**
 *  1. 创建 XMLHttpRequest 对象
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
    // 得到要请求的链接地址
    
    // test: Success! 此时后台逻辑操作很正确！Ajax效果是OK的！
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
            "<textarea name='textarea' id='cmd-font1'>你的指令还没执行完成!</textarea>"
    
    xmlHttp.open("GET", url, true);
    xmlHttp.send(null);
}






