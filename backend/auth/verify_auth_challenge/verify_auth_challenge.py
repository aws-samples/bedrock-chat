import json
from typing import Dict

def handler(event: Dict, context: Dict) -> Dict:
    # TODO Remove this line after testing
    print(json.dumps(event))

    try:
        challenge = event['request']['privateChallengeParameters']['challenge']
    except:
        event['response']['answerCorrect'] = False
        return event
    
    # check if challenge is correct
    if event['request']['challengeAnswer'] == challenge:
        event['response']['answerCorrect'] = True
        return event
    
    event['response']['answerCorrect'] = False
    return event 

