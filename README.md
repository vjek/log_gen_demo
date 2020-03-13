# log_gen_demo
MMO log generator and parser demo in python3

Intended use for Windows would be:
- copy the scripts into the same folder
- open two command prompts in that folder
- then,in cmd1, log_gen_generator_1.py > outfile1.txt
- then,in cmd2, log_gen_gui_1.py and click on "Start monitoring.."

Intended use for Linux would be:
- copy the scripts into the same folder, cd to that folder
- ./log_gen_generator_1.py > outfile1.txt &
- ./log_gen_gui_1.py and click on "Start monitoring.."

Everything else should be pretty self explanatory from the comments in the code.
If not, feel free to email me.  Same goes for suggestions.

The overall point of this demo is to show how to parse MMO (or similar) log files, in real time.
The log_generator, by default, creates 1000 lines of logs, then exits.
The parser calculates total damage, per "class", per second.  Of course, it's reasonably straightforward to do much more, but you have to start somewhere. :)
