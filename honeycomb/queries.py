"""
Evals for for Honeycomb Natural Langaguge Query generator from the Fine Tuning
LLMs course (https://maven.com/parlance-labs/fine-tuning)

Notebooks from the course: https://github.com/parlance-labs/ftcourse

The queries.csv dataset contains ~ 2,300 example queries (along with column
schemas generated offline via RAG). To evaluate a random subset of 200 queries
using a variety of models:

inspect eval queries.py --model openai/gpt-4-turbo --limit 200
inspect eval queries.py --model hf/google/gemma-2b --limit 200
inspect eval queries.py --model ollma/llama3 --limit 200

By default, scoring is done using the validity checker from the course (see
validate.py). You can instead use the critique prompt presented in the course
by specifying the 'critique' task parameter, for example:

inspect eval queries.py --model ollma/llama3 --limit 25 -T critique=true
"""

import json
import re

from inspect_ai import task, Task
from inspect_ai.dataset import csv_dataset, FieldSpec
from inspect_ai.model import get_model
from inspect_ai.scorer import accuracy, scorer, Score, CORRECT, INCORRECT
from inspect_ai.solver import system_message, generate, solver
from inspect_ai.util import resource

from validate import is_valid


@task
def queries(critique = False):

    # read dataset
    dataset = csv_dataset(
        csv_file="queries.csv",
        sample_fields=FieldSpec(
            input="user_input",
            metadata=["columns"]
        ),
        shuffle=True
    )

    # decide on the type of scorer to use
    scorer = critique_scorer() if critique else validation_scorer()

    # create task
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
def validation_scorer():

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


# sometimes models will enclose the JSON in markdown! (e.g. ```json)
# this function removes those delimiters should they be there
def json_completion(completion):
    import re
    completion = re.sub(r'^```json\n', '', completion.strip())
    completion = re.sub(r'\n```$', '', completion)
    return completion

comp = "```json\n{\"calculations\":[{\"op\":\"COUNT\"}],\"filters\":[{\"column\":\"name\",\"op\":\"=\",\"value\":\"p_cancela_grupos_nao_confirmado\"}],\"time_range\":7200}\n```"

