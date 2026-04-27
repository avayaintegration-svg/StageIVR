# tools/getmember_auth.py
from pydantic import BaseModel 
from mcp.server.fastmcp import FastMCP
from typing import Optional, Union
# Define the output schema
class getmember_authOutput(BaseModel):
    status: str
    member_name: Optional[str] = None
    member_address: Optional[str] = None
    userid: Optional[Union[str, int]] = None
    confirmation_prompt: Optional[str] = None

# Sample data (mock database)
MEMBER_DATA = [
    {"memberid": "1001", "dob": "1990-01-01", "name": "Dhinesh Kumar","Address":"123 Main Street at 4, B Springfield, Illinois. 62704","userid":1},
     {"memberid": "MA1001", "dob": "1990-01-01", "name": "Antonio Rubin","Address":"123 Main Street at 4, B Springfield, Illinois. 62704","userid":2},   
    {
		"memberid": "1008",
		"dob": "1977-06-13",
		"name": "Antonio Rubin",
		"Address": "2100 N Line Street Apt T201, Lansdale, PA 19446",
		"userid": 5
	},
    {
		"memberid": "1009","dob": "1977-06-13",
		"name": "Nina Duffy","Address": "2100 N Line Street Apt T201, Lansdale, PA 19446",
		"userid": 6
	}
]
def register(mcp: FastMCP):    
    def filter_by_memberid_and_dob(memberid: str, dob: str):
        for record in MEMBER_DATA:
            if record["memberid"] == memberid and record["dob"] == dob:
                return record   # return the dict, not a string
        return None

    @mcp.tool(description="Authenticate a member by ID and DOB, return confirmation prompt")
    def getmember_auth(memberid: str, dob: str) -> getmember_authOutput:
        result = filter_by_memberid_and_dob(memberid, dob)
        if result:
            return getmember_authOutput(
                status="success",
                member_name=result['name'],
                member_address=result['Address'],
                userid=result['userid'],
                confirmation_prompt=f"Please confirm that your name is {result['name']}."
            )
        else:
            return getmember_authOutput(
                status="failed",
                confirmation_prompt="Authentication failed. Please try again."
            )
        #return getmember_authOutput(result=result)
