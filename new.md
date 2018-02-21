# Sue 2.0

This is a VERY ambitious upgrade. I would like to make this an application whose design can be appreciated in all aspects. Here's an overlay of the design I am thinking of.

## Server
Written in Elixir. Has a web interface where you can view logs, and interface easily with the DB. Most important part is going to be the Queue of requests and messages that I have to send out, along with hot-swappable code features that allow me to load in new features.

## Database
Elasticsearch. Fully searchable text. May have to do something to resolve deltas with Message's sqlite database occasionally. Especially if it gets to the point where this has to scale across multiple computers.

## Logic
Done in Python. Called from Elixir through ErlPort. Going to have to automate testing somehow to decide when to hot-swap the code.

## Extensibility
Use some sort of containers (it seems to be that cloud9 uses Docker) to allow users to create their own functions. Maybe make its own package manager that users can install certain community-made functions in their group texts.