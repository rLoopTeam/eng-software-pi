Note:
This is a very basic implementation mostly for experimentation purposes and getting my head around it.

Requirements
============
1.supervisor (as described in the CANVAS git readme)

How to use
==========
1. Run this: supervisord -n in the supervisord.conf directory
2. In another terminal, call the send_command script with any of the following arguments:
	a. get_engine_status
	a. start - pod initialisation sequence. Starts hover engines, checks statuses etc
	c. move - x is the speed you want. set it to whatever, and the hover engines will tilt to the required angle to achieve said speed
	b. stop
These are the commands we use to control the pod. THe functions are sent over the CAN network. The pod responds with a status which also travels over CAN.
	

Instructions
============
IDs.py is the file where messages are defined. Each message has a unique id which also acts like a priority.
You can add more messages (and corresponding functions within the nodes) to this file but you need to ensure the ids numbers and node filter variables are updated as needed.

To make the code more modular and easier to use, the message ids are referenced in the code by a human readable name. 
The id itself(the one that gets trasmitted over CAN) is just a number.

Improvements needed
===================
MEssage ids are repeated many times in the code which is not great because they need to be updated individually if changes are made. 
Ideally there should be a variable per message id in the node's code so its easier to reference the id.


Based on CANVAS
===============
https://github.com/rLoopTeam/eng-software-canvas




