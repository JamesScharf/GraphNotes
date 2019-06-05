gn or GraphNotes is a simple program that lets you manage your knowledge base on the command line.
It's based on the idea of Directed Graphs.


*Recommended Software and Settings:*
You must have Graph::Easy installed to view your connections.

You can edit your notes with any editor you like, just change the settings on startup [implement!!].
I am a fan of `nano` and `micro`.

Move the executable to /bin to run it like any other program.

Here are some command line shortcuts if you don't want to open the whole program:

	- To create a new note: gn edit [name]
			or gn -e [note]

	- To delete a note: gn del [name]
			or gn -d [note]

	- To view a note: gn view [note]
			or gn -v [note]

	- To view the graph: gn graph
	        or gn -g




**TODO List:**

    - Make parseable configuration file (using json)

    - Make notes linkeable automatically from within a note.
        So, if I have [some_note] in my txt file, then GraphNotes will try to automatically
        connect/create a new note. This allows for quick linking.

        ...Maybe add a short method in node?


    - Correct corrupted knowledgebase file/reconstruct it based on available .nd files