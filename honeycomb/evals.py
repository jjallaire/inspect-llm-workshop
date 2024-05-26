import re

from inspect_ai import task, Task
from inspect_ai.scorer import accuracy, scorer, Score, CORRECT, INCORRECT
from inspect_ai.solver import system_message, generate, solver
from inspect_ai.util import resource

from utils.dataset import read_user_queries
from utils.validate import is_valid



@task
def validate_query():
    return Task(
        dataset=read_user_queries(),
        plan=[
            system_message("Honeycomb AI suggests queries based on user input."),
            prompt_with_schema(),
            generate()
        ],
        scorer=validation_scorer()
    )



@solver
def prompt_with_schema():

    prompt_template = resource("prompt.txt")

    async def solve(state, generate):
        state.user_prompt.text = prompt_template.replace(
            "{{prompt}}", state.user_prompt.text
        ).replace(
            "{{columns}}", state.metadata["columns"]
        )
        return state

    return solve

@scorer(metrics=[accuracy()])
def validation_scorer():

    async def score(state, target):
       
        answer = state.output.completion.strip()
        
        if is_valid(answer, state.metadata["columns"]):
            value=CORRECT
        else: 
            value=INCORRECT
       
        return Score(value=value, answer=answer)

    return score