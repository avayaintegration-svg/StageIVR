import os
import httpx


def register(mcp):
    @mcp.tool()
    async def transfer_call(call_sid: str) -> str:
        """
        Transfer the active Twilio call to a human agent.
        call_sid: the Twilio CallSid for the active call.
        """
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token  = os.getenv("TWILIO_AUTH_TOKEN")
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
