import weechat
import os.path

userlist = '~/.weechat/userlist'
debug = True

weechat.register('hal', 'hal9000', '6.6.6', 'GPL3', 'HAL Script', '', '')

users = []

def timer_cb(data, remaining_calls):
    current = weechat.current_buffer()
    if os.path.isfile(userlist):
        weechat.prnt(current, 'HAL\tReading ' + userlist + '.')
        file = open(userlist, 'r') 
        users = file.readlines()
    else:
        weechat.prnt(current, "HAL\tuserlist doesn't exists.")
        users = [
            '*!*@82-197-212-247.dsl.cambrium.nl',
            '*!*80-101-145-252.ip.xs4all.nl',
            '*!*2a01:238:4350:ff00:c53e:c819:422a:2511'
        ]
    if debug:
        for u in users:
            weechat.prnt(current, 'user\t' + u)
    weechat.prnt(current, '%s' % data)
    return weechat.WEECHAT_RC_OK

weechat.hook_timer(2000, 0, 1, 'timer_cb', 'HAL\tSystem fully operational.')

def priv_cb(data, signal, signal_data):

    buffer = weechat.current_buffer()

    args = signal_data.split(' ')[0:3]
    nick = args[0][1:].split('!')[0]
    user = args[0][1:].split('!')[1].split('@')[0]
    host = args[0][1:].split('!')[1].split('@')[1]
    target = args[2]
    message = signal_data[1:]
    message = message[message.find(':') + 1:]

    if debug:
        weechat.prnt(buffer, '===\t========== Debug ==========')
        weechat.prnt(buffer, 'raw\t' + signal_data)
        weechat.prnt(buffer, 'vars\tnick=' + nick + ', user=' + user + ', host=' + host + ', target=' + target)

    if any(host in s for s in users):
        if message[0] == '/':
            weechat.command(buffer, 'On behalf of *' + nick + '*')
            weechat.command(buffer, message)
        if debug:
            weechat.prnt(buffer, 'match\t' + host)
            weechat.prnt(buffer, 'msg\t' + message)
    
    return weechat.WEECHAT_RC_OK

weechat.hook_signal('*,irc_in2_privmsg', 'priv_cb', '')