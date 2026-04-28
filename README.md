# IVRAgent
```mermaid
graph TB
    subgraph Customer_Zone [User Interaction]
        Customer((Customer))
        Twilio_Gateway[Twilio Telephony Gateway]
    end

    subgraph IVR [IVR - Voice AI Agent]
        direction TB
        subgraph ECS [ECS Fargate]
            CoreApp[Core App Service - FastAPI]
        end
        subgraph Bedrock_Voice [Bedrock]
            NovaSonic[Nova 2 Sonic - Voice AI Model]
        end
        subgraph MCP [MCP Server]
            T1[Member Tool]
            T2[Provider Tool]
            T3[ID Card Tool]            
            T4[Transfer to human]
        end
    end 

    subgraph Integrations [Database & External System Integrations]
        DB[(RDS Postgres)]
        TwilioAPI[Twilio API]
        Onvida[Onvida API]
        Qnxt[Qnxt API]
    end

    %% Connections
    Customer <--> Twilio_Gateway
    Twilio_Gateway <--> CoreApp
    CoreApp <-->|Bidirectional Stream| NovaSonic
    NovaSonic <-->|I/O transport| MCP
    
    %% Connections to Integrations
    MCP <--> Integrations
    
    %% Internal Logic flows (Optional: specifically linking tools to APIs)
    T1 -.-> Qnxt
    T2 -.-> Onvida
    T3 -.-> DB
