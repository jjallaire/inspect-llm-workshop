"""
Evals for for Honeycomb Natural Langaguge Query generator from the Fine Tuning
LLMs course (https://maven.com/parlance-labs/fine-tuning)

Notebooks from the course: https://github.com/parlance-labs/ftcourse

The queries.csv dataset contains ~ 2,300 example queries (along with column
schemas generated offline via RAG). There are two scoring methods supported
(corresponding to the two @task definitions below):

1. validate - score using the validity checker from the course (utils.py)
2. critique - score using the critique prompt from the course (critique.txt)
"""

import json

from inspect_ai import task, Task
from inspect_ai.dataset import csv_dataset, FieldSpec
from inspect_ai.model import get_model
from inspect_ai.scorer import accuracy, scorer, Score, CORRECT, INCORRECT
from inspect_ai.solver import system_message, generate, solver
from inspect_ai.util import resource

from utils import is_valid, json_completion


@task
def validate():
    return eval_task(scorer=validate_scorer())


@task
def critique():
    return eval_task(scorer=critique_scorer())


# shared task implementation parmaeterized by scorer
def eval_task(scorer):

    # read dataset
    dataset = csv_dataset(
        csv_file="queries.csv",
        sample_fields=FieldSpec(
            input="user_input",
            metadata=["columns"]
        ),
        shuffle=True
    )

    # create eval task
    return Task(
        dataset=dataset,
        plan=[
            system_message("Honeycomb AI suggests queries based on user input."),
            prompt_with_schema(),
            generate()
        ],
        scorer=scorer
    )


@solver
def prompt_with_schema():

    prompt_template = resource("prompt.txt")

    async def solve(state, generate):
        # build the prompt
        state.user_prompt.text = prompt_template.replace(
            "{{prompt}}", state.user_prompt.text
        ).replace(
            "{{columns}}", state.metadata["columns"]
        )
        return state

    return solve


@scorer(metrics=[accuracy()])
def validate_scorer():

    async def score(state, target):
       
        # check for valid query
        query = json_completion(state.output.completion)
        if is_valid(query, state.metadata["columns"]):
            value=CORRECT
        else: 
            value=INCORRECT
       
        # return score w/ query that was extracted
        return Score(value=value, answer=query)

    return score


@scorer(metrics=[accuracy()])
def critique_scorer(model = "openai/gpt-4-turbo"):

    async def score(state, target):
       
        # build the critic prompt
        query = state.output.completion.strip()
        critic_prompt = resource("critique.txt").replace(
            "{{prompt}}", state.user_prompt.text
        ).replace(
            "{{columns}}", state.metadata["columns"]
        ).replace(
            "{{query}}", query
        )
       
        # run the critique
        result = await get_model(model).generate(critic_prompt)
        try:
            parsed = json.loads(json_completion(result.completion))
            value = CORRECT if parsed["outcome"] == "good" else INCORRECT
            explanation = parsed["critique"]
        except (json.JSONDecodeError, KeyError):
            value = INCORRECT
            explanation = f"JSON parsing error:\n{result.completion}"
        
        # return value and explanation (critique text)
        return Score(value=value, explanation=explanation)

    return score

