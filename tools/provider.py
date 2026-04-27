# tools/get_provider_by_npi.py
from pydantic import BaseModel 
from mcp.server.fastmcp import FastMCP

# Define the output schema
class ProviderOutput(BaseModel):
    status: str
    provider_name: str | None
    specialty: str | None
    npi: str

# Sample NPI data (mock database)
PROVIDER_DATA = [
    {"npi": "1234567890", "provider_name": "Dr. Priya Kumar", "specialty": "Cardiology","userid":1},
    {"npi": "2345678901", "provider_name": "Dr. Arun Singh", "specialty": "Dermatology","userid":2},
    {"npi": "3456789012", "provider_name": "Dr. Meera Nair", "specialty": "Pediatrics","userid":3},
]
def register(mcp: FastMCP):    
    def filter_by_npi(npi: str):
        for record in PROVIDER_DATA:
            if record["npi"] == npi:
                return record
        return None

    @mcp.tool(description="Retrieve provider details by NPI number")
    def get_provider_by_npi(npi: str) -> ProviderOutput:
        record = filter_by_npi(npi)
        if record:
            return ProviderOutput(
                status="success",
                provider_name=record["provider_name"],
                specialty=record["specialty"],
                npi=record["npi"]
            )
        else:
            return ProviderOutput(
                status="failed",
                provider_name=None,
                specialty=None,
                npi=npi
            )
