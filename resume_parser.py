# coding=utf-8
# Copyright 2018-2023 EvaDB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import numpy as np
import pandas as pd

from evadb.catalog.catalog_type import NdArrayType
from evadb.functions.abstract.abstract_function import AbstractFunction
from evadb.functions.decorators.decorators import forward, setup
from evadb.functions.decorators.io_descriptors.data_types import PandasDataframe
from evadb.functions.gpu_compatible import GPUCompatible
from evadb.utils.generic_utils import try_to_import_ultralytics

# this function takes the model and temperature as arguments from the user.

class Parser(AbstractFunction):
    @property
    def name(self):
        return "Parser"


    @setup(cacheable=True, function_type="chat-completion", batchable=True)
    def setup( self, model="gpt-3.5-turbo", temperature: float = 0,) -> None:
        # assert model in _VALID_CHAT_COMPLETION_MODEL, f"Unsupported ChatGPT {model}"
        self.model = model
        self.temperature = temperature

    @forward(
        input_signatures=[
            PandasDataframe(
                columns=["query", "content", "prompt"],
                column_types=[
                    NdArrayType.STR,
                    NdArrayType.STR,
                    NdArrayType.STR,
                ],
                column_shapes=[(1,), (1,), (None,)],
            )
        ],
        output_signatures=[
            PandasDataframe(
                columns=["response"],
                column_types=[
                    NdArrayType.STR,
                ],
                column_shapes=[(1,)],
            )
        ],
    )
    def forward(self, text_df):
        import openai

        #getting the data
        content = text_df[text_df.columns[0]]
        responses = []

        for prompt in content:
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", \
                                                    temperature=0.2, \
                                                    messages=[{"role": "user", "content": prompt}])
            response_text = response.choices[0].message.content
            responses.append(response_text)

        return_df = pd.DataFrame({"response": responses})
