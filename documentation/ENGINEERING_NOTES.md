# Engineering Concepts
## Concept 1: What is the architecture of our application?

The architecture of the application is a monolithic layered architecture. It means separating the each functionality into different modules/layers for maintainability, scalability, and reusability.

### Monolithic Architecture
A monolithic architecture is a software design pattern in which all the components of an application are tightly coupled and run as a single process. It is a traditional approach to software development and is well-suited for small to medium-sized applications. It is also easy to deploy as it involves deploying a single artifact.

### Layered Architecture
A layered architecture is a software design pattern in which the components of an application are organized into layers, each with a specific responsibility. The layers are organized in a hierarchical manner, with each layer having access to the layers below it. 

## Concept 2 : Separation of Concern

This refers to each module having its own concern(functionality). In other words , it means dividing the application into different modules based on the functionality they provide.
A concern simply means a particular responsibility or job that the software needs to handle.
For my project :
    - Scanning files       → one concern
    - Analyzing storage    → another concern
    - Moving files         → another concern
    - Finding duplicates   → another concern
    - Generating reports   → another concern
    - User interaction     → another concern

## Concept 3: Layered Architecture
Now that you understand separation of concerns, we can introduce one additional idea: how those separate responsibilities are organized and allowed to interact.

My implementation plan is to implement this application using Layered Architecture.

Think of it as arranging our modules into levels.

Q. What does "layer" mean?

A. A layer is basically a level of responsibility.

For example, the top layer is concerned with:

1. "What does the user want?"

The service layer is concerned with:

2. "How do I perform that operation?"

And the filesystem is concerned with:

3. "How do I actually read/write/move files?" 

## Concept 4: What is a Data Model?
A defined structure that represents an entity in an application by specifying the information it contains and how that information is organized. In this project, FileInfo provides a standardized representation of a file, allowing different services to work with consistent file data instead of relying on loosely structured dictionaries.
    file_info = {
    "path": "...",
    "name": "resume.pdf",
    "extension": ".pdf",
    "size_bytes": 245000,
    "category": "Documents",
    "modified_time": "...",
    "sha256": None
}