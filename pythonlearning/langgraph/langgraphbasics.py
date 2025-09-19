# pip install langgraph 

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


# State is just a dict of inputs/outputs
class State(dict):
    pass

# collecting all the execution log of all the task in the nodes 
# Define nodes
def step1(state: State):
    print("Step 1 running")
    state["step1"] = "Hello"
    return state

def step2(state: State):
    print("Step 2 running")
    state["step2"] = state["step1"] + " World"
    return state

# Build 
graph = StateGraph(State)

graph.add_node("first", step1)
graph.add_node("second", step2)
graph.add_edge(START, "first")
graph.add_edge("first", "second")
graph.add_edge("second", END)

# Compile and run
app = graph.compile()
final_state = app.invoke({})
print(final_state)

# def router(state: State):
#     if "error" in state:
#         return "error_node"
#     return "success_node"

# graph.add_conditional_edges("first", router, {
#     "error_node": "error_handler",
#     "success_node": "second"
# })

# graph.set_entry_point("first")