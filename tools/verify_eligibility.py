# tools/verify_eligibility.py
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP

class EligibilityOutput(BaseModel):
    member_id: str
    plan_description: str
    eff_date: str
    pcp_name: str
    eligible: bool
    message: str

# Sample dataset with memberId
SAMPLE_ELIGIBILITY_DATA = [
    {
        "memberId": "1001",
        "PlanDescription": "Gold Health Plan",
        "effDate": "2026-01-01",
        "PcpName": "Dr. Anita Rao",
        "eligible": True,
        "primaryStatus":"Y"
    },
    {
        "memberId": "1002",
        "PlanDescription": "Silver Health Plan",
        "effDate": "2026-03-15",
        "PcpName": "Dr. John Smith",
        "eligible": False,
        "primaryStatus":"N"
    },
    {
        "memberId": "1009",
        "PlanDescription": "Bronze Health Plan",
        "effDate": "2026-02-01",
        "PcpName": "Dr. RASHMI NANDA",
        "eligible": True,
        "primaryStatus":"Y"
    },
    {
        "memberId": "1008",
        "PlanDescription": "Bronze Health Plan",
        "effDate": "2026-02-01",
        "PcpName": "Dr. APRIL ANGLEY",
        "eligible": True,
        "primaryStatus":"Y"
    }
]

def register(mcp: FastMCP): 
    @mcp.tool(description="Verify member eligibility using only memberId")
    def verify_eligibility(member_id: str) -> EligibilityOutput:
        for record in SAMPLE_ELIGIBILITY_DATA:
            if record["memberId"].lower() == member_id.lower():
                return EligibilityOutput(
                    member_id=record["memberId"],
                    plan_description=record["PlanDescription"],
                    eff_date=record["effDate"],
                    pcp_name=record["PcpName"],
                    eligible=record["eligible"],
                    primaryStatus=record["primaryStatus"],
                    message="Eligibility verified successfully." if record["eligible"] else "Member is not eligible."
                )
        return EligibilityOutput(
            member_id=member_id,
            plan_description="Unknown",
            eff_date="Unknown",
            pcp_name="Unknown",
            eligible=False,
            primaryStatus="Unknown",
            message="No matching record found for this memberId."
        )
 