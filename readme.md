
writing a lexical analyser (scanner).
===================================

the list of terminals the scanner should be able to recognize is at the end of this text.

your program gets a file as an argument.

we run it as:

```
./compiler0 program.txt
```

please include readme (or better a makefile) that describes how to compile the program.

DO NOT include binaries in the git repository.
git repository should only contain the plain text files.

program.txt may have a look like this:

```
var
  a, b: integer;
begin
  a:=23;b:=42;
end.
```

it is expected of a `compiler0` program to emit the following:

```
var
a
,
b
:
integer
;
begin
a
:=
23
;
b
:=
42
;
end
.
```

please test your program with

`make test`

to test if it works.

do not consider the homework done before you get `(:` symbol on the as the output of `make test`.

even if you got `(:` as the output of `make test` it does not mean your compiler will pass other tests successfully.

or it may contain the program that doesn't look gramatically correct:

```
23 var a:=begin if for b: integer = "i don't know"
```

it is expected then of compiler0 to emit the following:

```
number: 23
var
a
:=
begin
if
for
b
:
integer
=
string: "i don't know"
```

however, the following input file:

```
module aaa;
ooo;
2a;
eee;
```

should produce:

```
module
aaa
;
ooo
;
2a: error, invalid lexem
;
eee
;
```

the lexical analyser doesn't care about correct grammar, but only recognizes known lexems.

in case it finds the unknown lexem, it throws an error.

you also want to have the maxLexemLength constant to be able to stop the scanning process, for example in case the string is opened with quote and never closed.


your program consists of two parts:

* the actual scanner. may contain a function GetSym() which returns a next terminal.
* the function that calls GetSym() in a loop, unless there is no remaining symbols in the file.

the known lexems are:

identifier

identifier is a string, first character of which is a letter, other characters can be letters or numbers.

in EBNF we would write it as
```
    letter   = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" .
    digit    = "0123456789".
 identifier  =  letter { letter | digit } .
```

number

number is a string that only consists of digits.

in EBNF we can represent the number as follows:
```
 number  =  digit { digit }
```

literal string

that is a string enclosed with double quote symbol.

in EBNF we can represent the string as follows:

```
noQuote  = ANY - '"' - eol  .
 string  =  '"' { noQuote } '"' .
```

rest of the lexems, one per line:
```
*
&
+
-
=
#
<
<=
>
>=
:
:=
;
:
,
.
or
div
mod
char
integer
boolean
false
true
not
(
)
while
repeat
until
do
loop
end
if
else
elsif
procedure
const
type
var
module
import
```

