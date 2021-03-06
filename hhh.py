# -*- coding: utf-8 -*-
import weechat
import os.path
import datetime

userlist = './userlist'
debug = True

weechat.register('hal', 'hal9000', '6.6.6', 'GPL3', 'HAL Script', '', '')

users = []

def timer_cb(data, remaining_calls):

    current = weechat.current_buffer()
    global users

    if os.path.isfile(userlist):
        weechat.prnt(current, 'HAL\tReading ' + userlist)
        file = open(userlist, 'r') 
        users = file.readlines()
    else:
        weechat.prnt(current, "HAL\tUsing default user list")
        users = [
            '*!*@82-197-212-247.dsl.cambrium.nl',
            '*!*@80-101-145-252.ip.xs4all.nl',
            '*!*@2a01:238:4350:ff00:c53e:c819:422a:2511'
        ]

    if debug:
        for u in users:
            weechat.prnt(current, 'user\t' + u)

    weechat.prnt(current, '%s' % data)
    return weechat.WEECHAT_RC_OK

weechat.hook_timer(2000, 0, 1, 'timer_cb', 'HAL\tSystem fully operational')

def priv_cb(data, signal, signal_data):

    global users
    current = weechat.current_buffer()

    args = signal_data.split(' ')[0:3]
    nick = args[0][1:].split('!')[0]
    user = args[0][1:].split('!')[1].split('@')[0]
    host = args[0][1:].split('!')[1].split('@')[1]
    target = args[2]
    message = signal_data[1:]
    message = message[message.find(':') + 1:]

    if debug:
        weechat.prnt(current, '===\t========== Debug ==========')
        weechat.prnt(current, 'raw\t' + signal_data)
        weechat.prnt(current, 'vars\tnick=' + nick + ', user=' + user + ', host=' + host + ', target=' + target)

    if any(host in u for u in users):
        if message[0] == '/':
            if message[1:4] == 'say':
                weechat.command(current, 'Yo')
            if message[1:5] == 'quit':
                weechat.command(current, 'hihi')
            else:
                weechat.command(current, message)
        if debug:
            weechat.prnt(current, 'match\t' + host)
            weechat.prnt(current, 'msg\t' + message)
    
    if 'HAL900' in message.upper():
        if 'HOE LAAT' in message.upper() or 'TIME' in message.upper():
            weechat.command(current, str(datetime.datetime.now()))
    
    return weechat.WEECHAT_RC_OK

weechat.hook_signal('*,irc_in2_privmsg', 'priv_cb', '')

def join_cb(data, signal, signal_data):
    server = signal.split(",")[0]
    msg = weechat.info_get_hashtable("irc_message_parse", {"message": signal_data})
    buffer = weechat.info_get("irc_buffer", "%s,%s" % (server, msg["channel"]))
    if buffer:
        if debug:
            weechat.prnt(buffer, '%s (%s) has joined. Welcome!' % (msg['nick'], msg['host']))
        weechat.command(buffer, 'для здоровья!')
    return weechat.WEECHAT_RC_OK

weechat.hook_signal('*,irc_in2_join', 'join_cb', '')
