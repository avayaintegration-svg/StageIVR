import os
import httpx

account_sid = os.getenv("TWILIO_ACCOUNT_SID") 
auth_token  = os.getenv("TWILIO_AUTH_TOKEN")
def register(mcp):
    @mcp.tool()
    async def transfer_call(call_sid: str) -> str:
        """
        Transfer the active Twilio call to a human agent.
        call_sid: the Twilio CallSid for the active call.
        """ 
        transfer_to = os.getenv("TRANSFER_PHONE_NUMBER") 


        twiml = f"<Response><Dial>{transfer_to}</Dial></Response>"

        async with httpx.AsyncClient(verify=False) as client:
            r = await client.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Calls/{call_sid}.json",
                data={"Twiml": twiml},
                auth=(account_sid, auth_token),
            )

        if r.status_code == 200:
            return "Call transferred successfully."
        return f"Transfer failed: {r.text}"

    @mcp.tool(description="Disconnect or call complete a Twilio call by calling Twilio REST API directly")
    async def call_complete_or_disconnect(call_sid: str) -> str: 
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Calls/{call_sid}.json"
        print(f"{account_sid} {auth_token} {url}")
       
        try:
            async with httpx.AsyncClient(verify=False) as client:
                r = await client.post(
                    url,
                    data={"Status": "completed"},
                    auth=(account_sid, auth_token),
                )
                print(f"{r} {r.status_code}")
            if r.status_code == 200:
                return "Call disconnected successfully via Twilio API." 
            else:
                return f"Failed to disconnect call. HTTP {r.status_code}: {r.text}" 
        except Exception as e:
             return  f"Exception occurred: {str(e)}" 
