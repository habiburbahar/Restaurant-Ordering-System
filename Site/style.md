# Standards for frontend code style

## JAVASCRIPT

Javascript Naming Guide:
- Packages: `camelCase`
- Classes: `CapitalCamel`
- Methods: `camelCase`
- Enums: `CapitalCamel`
- Constants: `SCREAMING_SNAKE_CASE`
- Parameters: `camelCase`
- Local vars: `camelCase`

Other javascript standards:
- Use 'let' instead of 'var' for variable declaration
- One variable per declaration (don't do let a = 1, b = 2;)
- Terminate statements with a semicolon
- In object and array definitions, add trailing commas:
```js
// Example:
let arr = [
    123,
    333,
    555,
]
let ob = {
    val1: 123,
    val2: 333,
}
```
- Methods can be defined on object literals using the method shorthand ({method() {… }}) in place of a colon immediately followed by a function or arrow function literal.
```js
// Example:
class {
    someMethod() {
        console.log("hello");
    }
}
```
- Optional parameters must include spaces on both sides of the equals operator, and be named exactly like required parameters
```js
// Example:
function myCoolFunction(required, optional = "") {}
```
- No line continuations using a backslash


## HTML
- Tag names, attribute names, classes and IDs should be skewer-case-and-lowercase


## CSS
- Don't include units for 0 values (prefer 0 to 0px)
- Exclude properties with no effect
- Declare properties in alphabetical order
- Property declarations should end in a semicolon


## GENERAL
Indent standard for all files:
- Single tab per level
- No trailing whitespace
- Prefer double quotes in attribute values
- Use meaningful names


