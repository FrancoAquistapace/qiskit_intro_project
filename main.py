#Copyright 2023 Franco Aquistapace
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# This file launches the oracle_builder application

# Import app
from oracle_builder import build_oracle_from_string

# Ask user for initial input
input_msg = '\nInsert a bit string or press ENTER to exit: '
bit_in = input(input_msg,) 
# Define main loop
while not bit_in == '':
    # Check that the input is allowed
    test_in = bit_in
    test_in = test_in.replace('1','')
    test_in = test_in.replace('0','')
    if len(test_in) > 0:
        print('Input must only contain 1s and 0s.')
        # Ask for new input
        bit_in = input(input_msg,)
        continue
    
    # Ask for new input
    bit_in = input(input_msg,)

# Finish process
exit()