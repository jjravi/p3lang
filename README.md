# p3lang
General Purpose Language Preprocessor Using Perl and Python

**Purpose**: _p3lang_ (**P**reprocessor using **P**erl and **P**ython) 
was created to generate different levels of thread coarsened code for
a research project. However, it can be used to quickly replicate code
or even as a general purpose language preprocessor using embedded Perl code. 

## Example Usage
Let's say you have a file called 
`main.c`:
```
#include <stdio.h>

int main(int argc, char *argv[]) {
  printf("hello world\n");
  return 0;
}
```

You want hello world to be replicated at compile time instead of runtime. 
How would you do it? Perl has built-in string parsing capabilities 
and comes preinstalled in most systems. 

You can write some perl code inside your original file. But it is not a 
pure c code anymore, so we should rename the file so other developers do
not think this is part of the c standard. I define a very simple syntax 
to enable embedding perl code in any source code:  
`{.` _with perl code here_ `.}`

`note: If you are using vim, you can use modelines to force a particular syntax
to override vim's syntax highlighting from considering the file extension.`

[main.c.p3](main.c.p3):
```
# vim: set filetype=c:

#include <stdio.h>

int main(int argc, char *argv[]) {

{.
  my $gen_code='';
  for (my $i=0; $i < $argv1; $i++)
  {
    $gen_code .= "  printf(\"hello: \%s\\n\", argv[0]);\n"
  }
  $gen_code
.}

  return 0;
}
```

Now, you can create a perl file using `cperlcompile.py`.

```
$ python3 cperlcompile.py -i ./main.c.p3 -o ./main.c.pm
$ perl main.c.pm 4
$ gcc main.c -o main
$ ./main
hello: ./main
hello: ./main
hello: ./main
hello: ./main
```

## License & copyright
© John J Ravi, North Carolina State University

Licensed under the [Apache v2.0 License](LICENSE).
