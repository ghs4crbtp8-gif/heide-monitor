import os, json, urllib.request, urllib.error, datetime, uuid, pathlib

API='https://ecomm.api.meg-eu.accessoticketing.com/api/request/getmerchantpackageeventdates'
STATE=pathlib.Path('state.json')

def telegram(msg):
    token=os.environ['TELEGRAM_BOT_TOKEN']; chat=os.environ['TELEGRAM_CHAT_ID']
    data=json.dumps({'chat_id':chat,'text':msg}).encode()
    req=urllib.request.Request(f'https://api.telegram.org/bot{token}/sendMessage',data=data,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=25) as r: r.read()

def fetch():
    today=datetime.date.today()
    start=os.getenv('START_DATE') or today.isoformat()
    end=os.getenv('END_DATE') or (today+datetime.timedelta(days=30)).isoformat()
    payload={'request_type':'GetMerchantPackageEventDates','application_id':'1500','merchant_id':'6500','machine_id':'500','agent_id':'5','user_id':'5','request_token':str(uuid.uuid4()),'P':[{'id':'84326','event_id':'2579','CT':[{'id':'1283','qty':'1'}]}],'extra_movie':'SnapWizardDE','identify_customer_types':'1','min_capacity':'1','version':'2','display_zero_capacity':'1','start_date':start,'end_date':end}
    headers={'Origin':'https://me-hpgermany.tickets.heide-park.de','Content-Type':'application/json','com-accessopassport-app-id':'1500','com-accessopassport-language':'de-de','com-accessopassport-merchant-id':'6500','com-accessopassport-client':'accesso26'}
    req=urllib.request.Request(API,data=json.dumps(payload).encode(),headers=headers)
    with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)

def main():
    result=fetch()
    # The response schema has not been verified. Do not claim availability from arbitrary JSON changes.
    # Save the response for inspection; alert on differences, explicitly labeled as unverified.
    previous=json.loads(STATE.read_text()) if STATE.exists() else None
    if previous is None:
        telegram('✅ Heide-Park-Monitor gestartet. Erste API-Antwort gespeichert. Verfügbarkeitsauswertung muss noch anhand der echten API-Struktur geprüft werden.')
    elif result != previous:
        telegram('🔔 Die Heide-Park-API-Antwort hat sich geändert. Das bedeutet NICHT zwingend, dass Tickets verfügbar sind. Bitte im offiziellen Ticketshop prüfen.')
    STATE.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__': main()
