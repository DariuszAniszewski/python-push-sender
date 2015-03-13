# Basic usage example #

```
ps = PushSender(PATH_TO_PEM_CERTIFICATE,USE_SANDBOX)
payload = {"aps":{"alert":"MESSAGE"}}  # as Python dict
ps.addNotification(payload,TOKEN)

payload = {"aps":{"alert":"MESSAGE2"}}
ps.addNotification(payload,TOKEN2)

....

payload = {"aps":{"alert":"MESSAGEN"}}
ps.addNotification(payload,TOKEN3)

ps.push()
```