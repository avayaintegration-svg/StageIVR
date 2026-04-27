from mcp.server.fastmcp import FastMCP
from tools import member,  provider , verify_eligibility , transfer
 
 

mcp = FastMCP("HealthCare-Assistant")

member.register(mcp)
provider.register(mcp)
verify_eligibility.register(mcp)
transfer.register(mcp)
#search_knowledge_base.register(mcp)
 


if __name__ == "__main__":
    print("MCP RUN")
    mcp.run()