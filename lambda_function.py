### 2. `lambda_function.py`
```python
import boto3
import json

iam = boto3.client('iam')

def lambda_handler(event, context):
    # Extract the compromised username and access key ID from the leak alert event
    username = event.get('username')
    access_key_id = event.get('access_key_id')
    
    if not username or not access_key_id:
        print("[-] Missing vital threat telemetry parameters (username/access_key_id).")
        return {"status": "SKIPPED"}
        
    print(f"[!] EMERGENCY: Deactivating leaked credential {access_key_id} for user {username}")
    
    try:
        # 1. Invalidate the access key immediately
        iam.update_access_key(
            UserName=username,
            AccessKeyId=access_key_id,
            Status='Inactive'
        )
        print(f"[+] Access key {access_key_id} status successfully flipped to INACTIVE.")
        
        # 2. Attach an immediate explicit global deny policy to the user as a backstop
        nuclear_deny_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "EmergencyIncidentResponseKillSwitch",
                    "Effect": "Deny",
                    "Action": "*",
                    "Resource": "*"
                }
            ]
        }
        
        iam.put_user_policy(
            UserName=username,
            PolicyName="EmergencyIRKillSwitch",
            PolicyDocument=json.dumps(nuclear_deny_policy)
        )
        print(f"[+] Emergency explicit global Deny applied successfully to user account {username}.")
        
        return {"status": "CONTAINED", "user": username}
        
    except Exception as e:
        print(f"[-] Critical failure during identity isolation sequence: {str(e)}")
        raise e
