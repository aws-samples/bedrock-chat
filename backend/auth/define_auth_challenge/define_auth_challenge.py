import json
from typing import Dict

def handler(event: Dict, context: Dict) -> Dict:
    # TODO Remove this line after testing
    print(json.dumps(event))

    if (('userNotFound' in event['request']) and event['request']['userNotFound']):
        print('user not found')
        event['response']['failAuthentication'] = True
        event['response']['issueTokens'] = False
        return event
    
    session = ''
    if 'session' in event['request']:
        session = event['request']['session']

    if (len(session) > 0 and session[-1]['challengeResult'] == True):
        print('session challenge')
        event['response']['failAuthentication'] = False
        event['response']['issueTokens'] = True
        return event
    
    event['response']['failAuthentication'] = False
    event['response']['issueTokens'] = False
    event['response']['challengeName'] = 'CUSTOM_CHALLENGE'
    return event
