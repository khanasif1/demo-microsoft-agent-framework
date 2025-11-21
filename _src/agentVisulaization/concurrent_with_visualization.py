# Copyright (c) Microsoft. All rights reserved.

import asyncio
from dataclasses import dataclass

from agent_framework import (
    AgentExecutor,
    AgentExecutorRequest,
    AgentExecutorResponse,
    AgentRunEvent,
    ChatMessage,
    Executor,
    Role,
    WorkflowBuilder,
    WorkflowContext,
    WorkflowOutputEvent,
    WorkflowViz,
    handler,
)
from agent_framework.azure import AzureAIAgentClient
from azure.identity import AzureCliCredential
from typing_extensions import Never
from dotenv import load_dotenv
import os

"""
Sample: Concurrent (Fan-out/Fan-in) with Agents + Visualization

What it does:
- Fan-out: dispatch the same prompt to multiple domain agents (research, marketing, legal).
- Fan-in: aggregate their responses into one consolidated output.
- Visualization: generate Mermaid and GraphViz representations via `WorkflowViz` and optionally export SVG.

Prerequisites:
- Azure AI/ Azure OpenAI for `AzureOpenAIChatClient` agents.
- Authentication via `azure-identity` — uses `AzureCliCredential()` (run `az login`).
- For visualization export: `pip install agent-framework[viz] --pre` and install GraphViz binaries.
"""
# Load environment variables
load_dotenv()

class DispatchToExperts(Executor):
    """Dispatches the incoming prompt to all expert agent executors (fan-out)."""

    def __init__(self, expert_ids: list[str], id: str | None = None):
        super().__init__(id=id or "dispatch_to_experts")
        self._expert_ids = expert_ids

    @handler
    async def dispatch(self, prompt: str, ctx: WorkflowContext[AgentExecutorRequest]) -> None:
        # Wrap the incoming prompt as a user message for each expert and request a response.
        initial_message = ChatMessage(Role.USER, text=prompt)
        for expert_id in self._expert_ids:
            await ctx.send_message(
                AgentExecutorRequest(messages=[initial_message], should_respond=True),
                target_id=expert_id,
            )


@dataclass
class AggregatedInsights:
    """Structured output from the aggregator."""

    research: str
    marketing: str
    legal: str


class AggregateInsights(Executor):
    """Aggregates expert agent responses into a single consolidated result (fan-in)."""

    def __init__(self, expert_ids: list[str], id: str | None = None):
        super().__init__(id=id or "aggregate_insights")
        self._expert_ids = expert_ids

    @handler
    async def aggregate(self, results: list[AgentExecutorResponse], ctx: WorkflowContext[Never, str]) -> None:
        # Map responses to text by executor id for a simple, predictable demo.
        by_id: dict[str, str] = {}
        for r in results:
            # AgentExecutorResponse.agent_run_response.text contains concatenated assistant text
            by_id[r.executor_id] = r.agent_run_response.text

        research_text = by_id.get("researcher", "")
        marketing_text = by_id.get("marketer", "")
        legal_text = by_id.get("legal", "")

        aggregated = AggregatedInsights(
            research=research_text,
            marketing=marketing_text,
            legal=legal_text,
        )

        # Provide a readable, consolidated string as the final workflow result.
        consolidated = (
            "Consolidated Insights\n"
            "====================\n\n"
            f"Research Findings:\n{aggregated.research}\n\n"
            f"Marketing Angle:\n{aggregated.marketing}\n\n"
            f"Legal/Compliance Notes:\n{aggregated.legal}\n"
        )

        await ctx.yield_output(consolidated)


async def main() -> None:

    print(f"Setting up agents and workflow...{os.getenv('AZURE_AI_PROJECT_ENDPOINT')}")   

    # 1) Create agent executors for domain experts
    # Current approach using environment variables (recommended)
    
    async with (
         
        AzureAIAgentClient(
            async_credential=AzureCliCredential(),
            # project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
            # model_deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
            endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
            deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
        ) as agentClient
    ):

        researcher = AgentExecutor(
        agentClient.create_agent(
            instructions=(
                "You're an expert market and product researcher. Given a prompt, provide concise, factual insights,"
                " opportunities, and risks."
            ),
        ),
        id="researcher",
    )
    marketer = AgentExecutor(
        agentClient.create_agent(
            instructions=(
                "You're a creative marketing strategist. Craft compelling value propositions and target messaging"
                " aligned to the prompt."
            ),
        ),
        id="marketer",
    )
    legal = AgentExecutor(
        agentClient.create_agent(
            instructions=(
                "You're a cautious legal/compliance reviewer. Highlight constraints, disclaimers, and policy concerns"
                " based on the prompt."
            ),
        ),
        id="legal",
    )

    expert_ids = [researcher.id, marketer.id, legal.id]

    dispatcher = DispatchToExperts(expert_ids=expert_ids, id="dispatcher")
    aggregator = AggregateInsights(expert_ids=expert_ids, id="aggregator")

    # 2) Build a simple fan-out/fan-in workflow
    workflow = (
        WorkflowBuilder()
        .set_start_executor(dispatcher)
        .add_fan_out_edges(dispatcher, [researcher, marketer, legal])
        .add_fan_in_edges([researcher, marketer, legal], aggregator)
        .build()
    )

    # 2.5) Generate workflow visualization
    print("Generating workflow visualization...")
    viz = WorkflowViz(workflow)
    mermaid_code = viz.to_mermaid()
    # Print out the mermaid string.
    print("Mermaid string: \n=======")
    print(viz.to_mermaid())
     # Save Mermaid to file
    try:
        mermaid_file = "workflow_diagram.mmd"
        with open(mermaid_file, "w") as f:
            f.write(mermaid_code)
        print(f"✅ Mermaid diagram saved to: {mermaid_file}")
        print(f"   View it at: https://mermaid.live")
    except Exception as e:
        print(f"⚠️  Could not save Mermaid file: {e}")
    print("=======")
    # Print out the DiGraph string.
    print("DiGraph string: \n=======")
    print(viz.to_digraph())
    print("=======")
    try:
        # Export the DiGraph visualization as SVG.
        svg_file = viz.export(format="svg")
        print(f"SVG file saved to: {svg_file}")
    except ImportError:
        print("Tip: Install 'viz' extra to export workflow visualization: pip install agent-framework[viz] --pre")

    # 3) Run with a single prompt
    async for event in workflow.run_stream("We are launching a new budget-friendly electric bike for urban commuters."):
        if isinstance(event, AgentRunEvent):
            # Show which agent ran and what step completed.
            print(event)
        elif isinstance(event, WorkflowOutputEvent):
            print("===== Final Aggregated Output =====")
            print(event.data)


if __name__ == "__main__":
    asyncio.run(main())