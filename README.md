# NLVM Core
An open-source API to make programming in NoLimits2 easier and accessible!

### Table of Contents
- [Motivations](#motivations)
- [Coding Standard](#coding-standard)



## Motivations
As great the built in library is for NoLimits2, it lacks some helpful features to make certain tasks easier; custom trains, sequencing, block-logic etc. I found myself constantly having to re-make certain things over and over when programming, so why not create a comprehensive library of all those little things I've created over the years?

As well as creating classes I've also created snippets for VSCode to help speed up the process of developing NLVM scripts, and adopted a similar documentation style to Visual-Studio with their tag style documentation.


## Coding Standard
This is a more niche topic however I believe it helps make sharing and understanding others code easier, I personally come from a very C# heavy background and adopt a lot of their conventions in NLVM, sure its closer to Java but; Java.
> [!NOTE]
> Code however you like! But I do enforce this standard for any contributions to this library!

#### Braces
Braces should be placed on a new line, this can be configured in most IDEs, this goes for all brace use cases including empty methods(stubs).

Example of incorrect brace placement:
```java
public void MyMethod() {
  ...
}

if (statement) {
  ...
}
```
Example of correct brace placement:
```java
public void MyMethod()
{
  ...
}

if (statement)
{
  ...
}
```

#### Classes
- Classes should use Pascal case and should be marked ```final``` wherever possible, class names should be concise and explain what the class will do.
- Classes that do not extend any classes should extend from ```Object```, this shows intention with the class structure.
- When importing types try to directly import the type rather than the package the type is part of, an exception is if you intend to use many types from that package; com.nolimitscoaster package is a common one to import.

#### Interfaces
- Interfaces should use Pascal case and use an I prefix before the name; ```IQueue``` or ```ISetable```.
  
#### Methods
- Methods should use Pascal case and marked with the least scope wherever possible, the name should be concise and explain what the function will do.
- Methods that should not be overriden in extending classes should be marked ```final```, an exception being if the class is already marked ```final```.
- Try to keep arguments to a minimum, more than 5 should be turned into a container and passed as a single argument.
- Arguments should have concise names and explain what they do.
- Arguements should use lower-Camel case.
- Local members of methods should use lower-Camel case.

#### Members
- Members should use Pascal case and marked with the least scope wherever possible, member names should be concise and explain what the member is representing.
- Members that should not be overriden in extending classes should be marked ```final```, an exception being if the class is already marked ```final```.
- Members with scopes: ```private``` or ```protected``` should use an m_ prefix before the member name.
- Boolean member names should be formatted as a question; ```IsRunning``` or ```CanPlay```.
- Minimise use of single character variables, they create obsurity and can be hard to understand their uses, exception being for loop iterators.

#### Documenting
- Use comments in code wherever possible, tab indent the comments to make them stand out from code.
- Classes, Interfaces, Methods, Members and Constructors with a scope accessible outside of the encompassing type should include [documentation tags](#documenting-code).

## Documenting Code
Code documentation is incredibly important for you and others viewing your code, it helps make understanding new code faster and point out important information you might need. I've been working on a system to make code documentation easier and provide a good basis to develop syntax tools.
