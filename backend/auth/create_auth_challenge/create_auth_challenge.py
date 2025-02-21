import json
from typing import Dict

def handler(event: Dict, context: Dict) -> Dict:
    # TODO Remove this line after testing
    print(json.dumps(event))

    # We can pass aribtrary value to client by using publicChallengeParameters. 
    # Use a hard-coded challenge for now
    event['response']['publicChallengeParameters'] = { "challenge": "opensesame"}
    event['response']['privateChallengeParameters'] = { "challenge": "opensesame"}
    return event

