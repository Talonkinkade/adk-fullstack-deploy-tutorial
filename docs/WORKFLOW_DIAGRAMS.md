# LearnQwest Workflow Diagrams
## Mermaid Flowcharts for All Agent Workflows

**Generated:** 2025-11-16
**System:** LearnQwest Multi-Agent Orchestration Platform

---

## Table of Contents

1. [Request Flow](#request-flow)
2. [Agent Lifecycle](#agent-lifecycle)
3. [Task Execution Workflow](#task-execution-workflow)
4. [Worklog Processing Pipeline](#worklog-processing-pipeline)
5. [Leaderboard Calculation](#leaderboard-calculation)
6. [Health Monitoring](#health-monitoring)
7. [Data Storage Flow](#data-storage-flow)
8. [Integration Bridges](#integration-bridges)

---

## 1. Request Flow

Complete request routing from user to agent execution:

```mermaid
graph TB
    Start[User Request] --> ADA[ADA Orchestrator]

    ADA --> Router{Request Router}
    Router --> TypeMap[Map Request Type<br/>to Capability]

    TypeMap --> FindAgents[Find Available Agents<br/>with Capability]

    FindAgents --> Strategy{Routing Strategy}

    Strategy -->|Least Loaded| SelectLL[Select Agent<br/>with Lowest Load]
    Strategy -->|Best Performance| SelectBP[Select Agent<br/>with Best Metrics]
    Strategy -->|Round Robin| SelectRR[Select Next<br/>in Rotation]

    SelectLL --> AgentSelected[Agent Selected]
    SelectBP --> AgentSelected
    SelectRR --> AgentSelected

    AgentSelected --> MarkBusy[Mark Agent as Busy]
    MarkBusy --> Execute[Execute Task on Agent]

    Execute --> Success{Success?}

    Success -->|Yes| UpdateSuccess[Update Agent Metrics<br/>Success + Response Time]
    Success -->|No| UpdateFailure[Update Agent Metrics<br/>Failure + Error]

    UpdateSuccess --> MarkAvailable[Mark Agent Available]
    UpdateFailure --> MarkAvailable

    MarkAvailable --> LogResult[Log to Worklog DB]
    LogResult --> ReturnResult[Return Result to User]

    ReturnResult --> End[End]
```

---

## 2. Agent Lifecycle

Agent registration, health monitoring, and deregistration:

```mermaid
stateDiagram-v2
    [*] --> Initializing: Register Agent

    Initializing --> Ready: Health Check Pass
    Initializing --> Error: Health Check Fail

    Ready --> Busy: Receive Task
    Busy --> Ready: Task Complete (Success)
    Busy --> Error: Task Complete (Failure)

    Error --> Maintenance: Auto-Recovery Triggered
    Maintenance --> Ready: Recovery Successful
    Maintenance --> Offline: Recovery Failed

    Ready --> Offline: Heartbeat Timeout
    Offline --> Ready: Heartbeat Restored

    Offline --> [*]: Deregister
    Error --> [*]: Deregister
    Ready --> [*]: Deregister
```

---

## 3. Task Execution Workflow

Detailed task execution through the 8-tier hierarchy:

```mermaid
graph TB
    subgraph "TIER 1: ADA Orchestration"
        Task[Task Request] --> ADA[ADA Orchestrator]
        ADA --> Validate[Validate Request]
    end

    subgraph "TIER 2: Strategic Planning"
        Validate --> GoalPlanner[Goal Planning Agent]
        GoalPlanner --> Decompose[Task Decomposer]
        Decompose --> Allocate[Resource Allocator]
        Allocate --> Prioritize[Priority Engine]
    end

    subgraph "TIER 3: Execution Coordinators"
        Prioritize --> DetermineType{Task Type}

        DetermineType -->|Code| CodeCoord[Code Execution<br/>Coordinator]
        DetermineType -->|Test| TestCoord[Test Execution<br/>Coordinator]
        DetermineType -->|Deploy| DeployCoord[Deployment<br/>Coordinator]
        DetermineType -->|Data| DataCoord[Data Processing<br/>Coordinator]
    end

    subgraph "TIER 4: Worker Agents"
        CodeCoord --> PythonAgent[Python Agent]
        CodeCoord --> TSAgent[TypeScript Agent]

        TestCoord --> PyTestAgent[PyTest Agent]
        TestCoord --> JestAgent[Jest Agent]

        DeployCoord --> DockerAgent[Docker Agent]
        DeployCoord --> K8sAgent[Kubernetes Agent]

        DataCoord --> WorklogParser[Worklog Parser]
        DataCoord --> AnalyticsAgent[Analytics Agent]
    end

    subgraph "TIER 5: Data Layer"
        PythonAgent --> LogToDB[(Log to PostgreSQL)]
        TSAgent --> LogToDB
        PyTestAgent --> LogToDB
        JestAgent --> LogToDB

        WorklogParser --> ParsedData[(Parsed Data Storage)]

        LogToDB --> Metrics[(Metrics to BigQuery)]
        ParsedData --> Metrics
    end

    subgraph "TIER 6: Intelligence"
        Metrics --> Scorer[Agent Scorer]
        Scorer --> UpdateLeaderboard[Update Leaderboard]
        UpdateLeaderboard --> GenerateSummary[Auto-Summarizer]
    end

    GenerateSummary --> Result[Task Result]
    Result --> End[Return to User]
```

---

## 4. Worklog Processing Pipeline

Parsing and analytics workflow:

```mermaid
graph LR
    subgraph "Input Sources"
        RawLogs[Raw Log Files]
        ADKEvents[ADK Session Events]
        AgentDiaries[Agent Work Diaries]
    end

    subgraph "Parsing Layer"
        RawLogs --> WorklogParser[Worklog Parser<br/>Regex + Pattern Matching]
        ADKEvents --> EventParser[Event Parser<br/>JSON Processing]
        AgentDiaries --> DiaryParser[Diary Parser<br/>LLM Extraction]
    end

    subgraph "Entity Extraction"
        WorklogParser --> Entities[Entity Extractor]
        EventParser --> Entities
        DiaryParser --> Entities

        Entities --> ExtractAgents[Extract: Agents]
        Entities --> ExtractTasks[Extract: Tasks]
        Entities --> ExtractFiles[Extract: Files]
        Entities --> ExtractErrors[Extract: Errors]
    end

    subgraph "Structured Storage"
        ExtractAgents --> PostgreSQL[(PostgreSQL<br/>Worklogs Table)]
        ExtractTasks --> PostgreSQL

        ExtractAgents --> Neo4j[(Neo4j<br/>Agent Graph)]
        ExtractTasks --> Neo4j

        ExtractAgents --> BigQuery[(BigQuery<br/>Time-Series)]
        ExtractTasks --> BigQuery
    end

    subgraph "Analytics"
        PostgreSQL --> Aggregator[Metrics Aggregator]
        Neo4j --> GraphAnalyzer[Graph Analyzer]
        BigQuery --> TrendAnalyzer[Trend Analyzer]

        Aggregator --> Leaderboard[Leaderboard]
        GraphAnalyzer --> Insights[Collaboration Insights]
        TrendAnalyzer --> Predictions[Performance Predictions]
    end

    Leaderboard --> Dashboard[Analytics Dashboard]
    Insights --> Dashboard
    Predictions --> Dashboard
```

---

## 5. Leaderboard Calculation

Scoring and ranking workflow:

```mermaid
graph TB
    Start[Trigger: Scheduled/On-Demand] --> FetchAgents[Fetch All Active Agents<br/>from Registry]

    FetchAgents --> Loop{For Each Agent}

    Loop --> CalcPerf[Calculate Performance Score<br/>Success Rate + Response Time]
    CalcPerf --> CalcRel[Calculate Reliability Score<br/>Uptime + Consistency]
    CalcRel --> CalcEff[Calculate Efficiency Score<br/>Resource Usage]
    CalcEff --> CalcCollab[Calculate Collaboration Score<br/>Team Interactions]

    CalcCollab --> Weighted[Apply Weighted Average<br/>40% Perf + 30% Rel + 20% Eff + 10% Collab]

    Weighted --> StoreScore[Store Agent Score]
    StoreScore --> NextAgent{More Agents?}

    NextAgent -->|Yes| Loop
    NextAgent -->|No| SortScores[Sort by Total Score<br/>Descending]

    SortScores --> AssignRanks[Assign Ranks<br/>1, 2, 3...]

    AssignRanks --> CalcChanges[Calculate Rank Changes<br/>vs Previous Period]

    CalcChanges --> AwardBadges[Award Achievement Badges]

    AwardBadges --> SaveLeaderboard[(Save to PostgreSQL<br/>Leaderboard Table)]

    SaveLeaderboard --> PublishDashboard[Publish to Dashboard UI]

    PublishDashboard --> End[End]

    style CalcPerf fill:#e1f5e1
    style CalcRel fill:#e1f5e1
    style CalcEff fill:#e1f5e1
    style CalcCollab fill:#e1f5e1
    style Weighted fill:#fff4e1
    style AwardBadges fill:#ffe1e1
```

---

## 6. Health Monitoring

Continuous health check and auto-recovery:

```mermaid
graph TB
    Start[Health Monitor Start] --> Schedule[Schedule Check<br/>Every 30 seconds]

    Schedule --> FetchAgents[Fetch All Registered Agents]

    FetchAgents --> CheckAgent{For Each Agent}

    CheckAgent --> Heartbeat{Heartbeat<br/>Recent?}

    Heartbeat -->|Yes, <60s| CheckMetrics[Check Performance Metrics]
    Heartbeat -->|No, >60s| Unresponsive[Mark as Unresponsive]

    CheckMetrics --> ErrorRate{Error Rate<br/>>50%?}

    ErrorRate -->|Yes| HighErrors[Alert: High Error Rate]
    ErrorRate -->|No| LoadCheck{Current Load<br/>< Max?}

    LoadCheck -->|Yes| Healthy[Mark as Healthy]
    LoadCheck -->|No| Overloaded[Alert: Overloaded]

    Unresponsive --> TriggerRecovery[Trigger Auto-Recovery]
    HighErrors --> LogAlert[Log Alert]
    Overloaded --> LogAlert

    Healthy --> NextAgent{More Agents?}

    TriggerRecovery --> Restart{Can Restart?}

    Restart -->|Yes| RestartAgent[Restart Agent Instance]
    Restart -->|No| MarkOffline[Mark Agent Offline]

    RestartAgent --> NextAgent
    MarkOffline --> NextAgent
    LogAlert --> NextAgent

    NextAgent -->|Yes| CheckAgent
    NextAgent -->|No| GenerateReport[Generate Health Report]

    GenerateReport --> SystemHealth{System Health<br/>>90%?}

    SystemHealth -->|Yes| StatusHealthy[Overall Status: Healthy]
    SystemHealth -->|No| StatusDegraded[Overall Status: Degraded]

    StatusHealthy --> Wait[Wait 30 seconds]
    StatusDegraded --> Wait

    Wait --> Schedule

    style Healthy fill:#e1f5e1
    style StatusHealthy fill:#e1f5e1
    style Unresponsive fill:#ffe1e1
    style HighErrors fill:#ffe1e1
    style StatusDegraded fill:#fff4e1
```

---

## 7. Data Storage Flow

Multi-backend data routing:

```mermaid
graph TB
    subgraph "Data Sources"
        AgentMetrics[Agent Metrics]
        TaskData[Task Execution Data]
        Worklogs[Worklog Entries]
        Collaborations[Agent Collaborations]
    end

    subgraph "Decision Layer"
        AgentMetrics --> DecisionMetrics{Data Type?}
        TaskData --> DecisionTask{Data Type?}
        Worklogs --> DecisionLogs{Data Type?}
        Collaborations --> DecisionCollab{Data Type?}
    end

    subgraph "PostgreSQL - Structured"
        DecisionMetrics -->|Session Data| PG1[(Sessions Table)]
        DecisionTask -->|Task Metadata| PG2[(Tasks Table)]
        DecisionLogs -->|Worklog Entries| PG3[(Worklogs Table)]
        DecisionCollab -->|User Profiles| PG4[(Users Table)]
    end

    subgraph "Neo4j - Relationships"
        DecisionCollab -->|Agent Network| Neo1[(Agent Nodes)]
        DecisionTask -->|Dependencies| Neo2[(Task Dependencies)]
        DecisionCollab -->|Workflow Graph| Neo3[(Workflow Nodes)]
    end

    subgraph "BigQuery - Analytics"
        DecisionMetrics -->|Time-Series| BQ1[(Metrics Timeseries)]
        DecisionTask -->|Aggregated Stats| BQ2[(Task Analytics)]
        DecisionLogs -->|Daily Summaries| BQ3[(Daily Summaries)]
    end

    subgraph "GCS - Storage"
        DecisionLogs -->|Large Logs| GCS1[/logs//]
        DecisionTask -->|Artifacts| GCS2[/artifacts//]
        DecisionMetrics -->|Trace Overflow| GCS3[/traces//]
    end

    subgraph "Query Layer"
        PG1 --> Queries[Query Service]
        PG2 --> Queries
        Neo1 --> Queries
        BQ1 --> Queries

        Queries --> API[REST API Endpoints]
        API --> Dashboard[Analytics Dashboard]
        API --> Reports[Report Generator]
    end

    style PG1 fill:#e1e8f5
    style PG2 fill:#e1e8f5
    style Neo1 fill:#f5e1e8
    style Neo2 fill:#f5e1e8
    style BQ1 fill:#e8f5e1
    style BQ2 fill:#e8f5e1
    style GCS1 fill:#f5f5e1
    style GCS2 fill:#f5f5e1
```

---

## 8. Integration Bridges

External system integration:

```mermaid
graph LR
    subgraph "LearnQwest Core"
        ADA[ADA Orchestrator]
        Registry[Agent Registry]
        Leaderboard[Leaderboard System]
    end

    subgraph "TeamLink_MasterControl Bridge"
        ADA --> TeamLinkBridge[TeamLink Bridge]
        TeamLinkBridge --> Sync[State Synchronization]
        TeamLinkBridge --> Messaging[Cross-System Messaging]

        Sync --> TeamLinkAPI[TeamLink API]
        Messaging --> TeamLinkAPI
    end

    subgraph "Comet Workflow Integration"
        ADA --> CometBridge[Comet Integration]
        CometBridge --> WorkflowChain[Workflow Chaining]
        CometBridge --> EventBus[Event Bus]

        WorkflowChain --> CometAPI[Comet Workflows API]
        EventBus --> CometAPI
    end

    subgraph "Vertex AI Agent Engine"
        Registry --> ADKSession[ADK Session Manager]
        ADKSession --> CloudDeploy[Cloud Deployment]

        CloudDeploy --> VertexAI[Vertex AI<br/>Agent Engine]
    end

    subgraph "External Tools"
        ADA --> Aider[Aider<br/>Code Modification]
        Leaderboard --> Slack[Slack<br/>Notifications]
        Registry --> Prometheus[Prometheus<br/>Metrics Export]
    end

    style TeamLinkBridge fill:#e1f5e1
    style CometBridge fill:#f5e1e8
    style CloudDeploy fill:#e1e8f5
```

---

## 9. Agent Conversion Pipeline

Batch conversion of features to agents:

```mermaid
graph TB
    Start[Input: Feature/Program List] --> Analyze[Feature Analyzer]

    Analyze --> Extract{For Each Feature}

    Extract --> ExtractInputs[Extract Inputs/Outputs]
    ExtractInputs --> ExtractDeps[Extract Dependencies]
    ExtractDeps --> ExtractLogic[Extract Core Logic]

    ExtractLogic --> Template[Generate Agent Template<br/>from ADK Base Class]

    Template --> Scaffold[Code Scaffolder<br/>Generate Python Code]

    Scaffold --> Wrap[ADK Integration Wrapper<br/>Add Orchestration Hooks]

    Wrap --> Manifest[Create Agent Manifest<br/>Capabilities, Tier, Config]

    Manifest --> Register[Register with ADA<br/>Agent Registry]

    Register --> Deploy{Deployment Mode}

    Deploy -->|Local| LocalPool[Add to Local Agent Pool]
    Deploy -->|Cloud| CloudDeploy[Deploy to Vertex AI<br/>Agent Engine]

    LocalPool --> HealthCheck[Initial Health Check]
    CloudDeploy --> HealthCheck

    HealthCheck --> Success{Health OK?}

    Success -->|Yes| Activate[Activate Agent<br/>Mark as Ready]
    Success -->|No| Rollback[Rollback Deployment<br/>Log Error]

    Activate --> NextFeature{More Features?}
    Rollback --> NextFeature

    NextFeature -->|Yes| Extract
    NextFeature -->|No| Summary[Generate Conversion Summary]

    Summary --> End[End: Report Successes/Failures]

    style Analyze fill:#e1f5e1
    style Scaffold fill:#e1f5e1
    style Activate fill:#e1f5e1
    style Rollback fill:#ffe1e1
```

---

## 10. End-to-End System Flow

Complete system integration:

```mermaid
graph TB
    subgraph "User Interface - TIER 8"
        User[User] --> Dashboard[Analytics Dashboard]
        User --> Leaderboard[Leaderboard UI]
        User --> ChatInterface[Chat Interface]
    end

    subgraph "API Layer"
        Dashboard --> API[REST/GraphQL API]
        Leaderboard --> API
        ChatInterface --> SSE[SSE Streaming Endpoint]
    end

    subgraph "ADA Orchestration - TIER 1"
        API --> ADA[ADA Master Orchestrator]
        SSE --> ADA

        ADA --> Router[Request Router]
        ADA --> HealthMon[Health Monitor]
        ADA --> ConfigMgr[Config Manager]
    end

    subgraph "Strategic Planning - TIER 2"
        Router --> GoalPlanner[Goal Planning Agent]
        Router --> TaskDecomp[Task Decomposer]
        Router --> ResourceAlloc[Resource Allocator]
    end

    subgraph "Execution - TIER 3 & 4"
        GoalPlanner --> Coordinators[Execution Coordinators]
        Coordinators --> Workers[60+ Worker Agents]
    end

    subgraph "Data Layer - TIER 5"
        Workers --> PostgreSQL[(PostgreSQL)]
        Workers --> Neo4j[(Neo4j)]
        Workers --> BigQuery[(BigQuery)]
        Workers --> GCS[(GCS)]
    end

    subgraph "Intelligence - TIER 6"
        PostgreSQL --> Scorer[Agent Scorer]
        BigQuery --> TrendAnalyzer[Trend Analyzer]
        Neo4j --> GraphAnalyzer[Collaboration Analyzer]

        Scorer --> LeaderboardMgr[Leaderboard Manager]
        Scorer --> Summarizer[Auto-Summarizer]
    end

    subgraph "Integration - TIER 7"
        ADA --> TeamLink[TeamLink Bridge]
        ADA --> Comet[Comet Integration]
        ADA --> VertexAI[Vertex AI Engine]
    end

    LeaderboardMgr --> API
    Summarizer --> API
    HealthMon --> API

    style ADA fill:#ffe1e1
    style Workers fill:#e1f5e1
    style LeaderboardMgr fill:#f5e1e8
    style Dashboard fill:#e1e8f5
```

---

## Notes

- All workflows support async/parallel execution where possible
- Error handling and retry logic implemented at each tier
- Telemetry and tracing integrated throughout
- Auto-scaling triggered based on load thresholds
- Real-time monitoring via SSE streaming

**END OF WORKFLOW DIAGRAMS**
