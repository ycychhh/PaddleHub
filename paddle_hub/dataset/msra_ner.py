#   Copyright (c) 2019  PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
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

from paddle_hub.tools.downloader import default_downloader
from paddle_hub.dir import DATA_HOME

import os
import csv
import json
from collections import namedtuple

DATA_URL = "https://paddlehub-dataset.bj.bcebos.com/msra_ner.tar.gz"


class MSRA_NER(object):
    def __init__(self):
        ret, tips, self.dataset_dir = default_downloader.download_file_and_uncompress(
            url=DATA_URL, save_path=DATA_HOME, print_progress=True)

        print(self.dataset_dir)
        self._load_label_map()
        self._load_train_examples()

    def _load_label_map(self):
        self.label_map_file = os.path.join(self.dataset_dir, "label_map.json")
        with open(self.label_map_file) as fi:
            self.label_map = json.load(fi)

    def _load_train_examples(self):
        train_file = os.path.join(self.dataset_dir, "train.tsv")
        self.train_examples = self._read_tsv(train_file)

    def get_train_examples(self):
        return self.train_examples

    def _read_tsv(self, input_file, quotechar=None):
        """Reads a tab separated value file."""
        with open(input_file, "r") as f:
            reader = csv.reader(f, delimiter="\t", quotechar=quotechar)
            headers = next(reader)
            Example = namedtuple('Example', headers)

            examples = []
            for line in reader:
                example = Example(*line)
                examples.append(example)

            return examples


if __name__ == "__main__":
    ds = MSRA_NER()
    for e in ds.get_train_examples():
        print(e)
