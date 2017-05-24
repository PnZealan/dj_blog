#-*-coding:utf-8-*-
from django.shortcuts import render,render_to_response
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import reply
import receive
import robot_api
import url_anan

# Create your views here.
@csrf_exempt
def g_et(request):
    try:
        if request.method == 'GET':
            data = request.GET
            if data.has_key('signature') and data.has_key('timestamp') and data.has_key('nonce') and data.has_key('echostr'):
                signature = data.get('signature')
                timestamp = data.get('timestamp')
                nonce = data.get('nonce')
                echostr = data.get('echostr')
                token = 'n3NAhN3pwBgvv3a'
    
                list = [token, timestamp, nonce]
                list.sort()
                sha1 = hashlib.sha1()
                map(sha1.update, list)
                hashcode = sha1.hexdigest()
                if hashcode == signature:
                    return HttpResponse(echostr)
                else:
                    return HttpResponse('')
	    else:
		return HttpResponse('404')
	elif request.method == 'POST':
	    try:
		webData = request.body
		recMsg = receive.parse_xml(webData)
		if isinstance(recMsg, receive.Msg):
		    toUser = recMsg.FromUserName
		    fromUser = recMsg.ToUserName
		    if recMsg.MsgType == 'image':
			mediaId = recMsg.MediaId
			replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
			return HttpResponse(replyMsg.send())
		    elif recMsg.Content[0:6] == '转存' and len(recMsg.Content) > 7:
			content = url_anan.bdpanSpider().getbody(recMsg.Content[7:])
			replyMsg = reply.TextMsg(toUser, fromUser, content)
			return HttpResponse(replyMsg.send())
		    else:
			try:
			    content = robot_api.talk(recMsg.Content, recMsg.userid)
			    print content
			except:
			    content = 'error'
			replyMsg = reply.TextMsg(toUser, fromUser, content)
			return HttpResponse(replyMsg.send())
		else:
		    print 'pass'
		    return HttpResponse('success')
	    except Exception, e:
		return e
    except Exception, Argument:
             return Argument
def index(request):
    return HttpResponse('ok')
