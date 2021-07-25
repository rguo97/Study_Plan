

# Go
## 语法
```
    "package" 包声明，声明自己当前属于哪个包
    import {
            "fmt"
            }  引用包
    对于输出

    Println、Fprintln、Sprintln 输出内容时会加上换行符；
    Print、Fprint、Sprint        输出内容时不加上换行符；
    Printf、Fprintf、Sprintf    按照指定格式化文本输出内容。
    Print、Printf、Println      输出内容到标准输出os.Stdout；
    Fprint、Fprintf、Fprintln  输出内容到指定的io.Writer；
    Sprint、Sprintf、Sprintln  输出内容到字符串。
```

## client
> go的内部会定义一个client，然后会自动生成对应的文件，调用的时候调用生成的文件就可以建立连接了

## flag包
> 当程序需要从外面指定参数的时候可以用flag定义一个全局变量，指定一个变量名例如：
```
name=flag.string("Name","Derek","please input your name")
#上面的解析是参数的名字是Name，默认值是Derek，提示信息是please input your name
```

## 函数
> 从格式上来说，看起来是和大多数的编程语言有所不同，
```
func 函数名（参数，参数类型）返回值类型{

    
}
```

## run和start的区别

> run表示阻塞，也就是不执行完启动的新进程或者新线程，就不会执行下面的程序
start表示非阻塞，也就是新启动的进程或者线程在没有执行完的情况下，也会执行下面的程序。

## 更新map值字段的方法



> 对于map类型的变量，如果他的值是结构体，那么就不能通过直接修改结构体中变量的值来达到更新的目的，这个时候会编译报错。
```
package main

type data struct {  
    name string
}

func main() {  
    m := map[string]data {"x":{"one"}}
    m["x"].name = "two" //error
}
```
> 
产生这个问题的原因就是map的值不能寻址（原因可能是当map的容量不断增加的时候，这个map中的 元素中hash结构可能会发生变化）。遇到这种情况，有下面两种解决办法
>*  使用临时变量
>>类似于值传递，将map中的value传递给一个临时变量，也就是说，临时变量就是一个struct类型，此时就可以通过修改结构体的值，然后再把修改后的变量struct传递给原map，这样就实现了更新的目的

```
package main

import "fmt"

type data struct {
    name string
}

func main() {
    m := map[string]data {"x":{"one"}}
    r := m["x"]
    fmt.Println(r)
    //{one}
    r.name = "two"
    m["x"] = r
    fmt.Printf("%v",m) //prints: map[x:{two}]
}
```
>* 使用指针映射
>> 使用指针指向map的value，此时map的值就变成了可寻址的，这样就可以直接修改指针的值来达到更新的目的
>> 同时要注意的是，map不能同时读写，必须要加锁
```
package main

import "fmt"

type data struct {  
    name 
}

func main() {  
    m := map[string]*data {"x":{"one"}}
    m["x"].name = "two" //ok
    fmt.Println(m["x"]) //prints: &{two}
}
```
> 运行下面的代码会出现问题，是因为是一个野指针。解决办法就是创建一个data类型的指针，然后在完成给map添加元素的操作
```
package main

type data struct {  
    name string
}

func main() {  
    m := map[string]*data {"x":{"one"}}
    //m["z"]=new(data)
    m["z"].name = "what?" //???
}
```


### 下面的x是可寻址的

>* 一个变量: &x
>* 指针引用(pointer indirection): &*x
>* slice索引操作(不管slice是否可寻址): &s[1]
>* 可寻址struct的字段: &point.X
>* 可寻址数组的索引操作: &a[0]
>* composite literal类型: &struct{ X int }{1}

### 下面的x是不可寻址的
>* 字符串中的字节:
>* map对象中的元素
>* 接口对象的动态值(通过type assertions获得)
>* 常数
>* literal值(非composite literal)
>* package 级别的函数
>* 方法method (用作函数值)
>* 中间值(intermediate value):
>* 函数调用
>* 显式类型转换
>* 各种类型的操作 （除了指针引用pointer dereference操作 *x):
>* channel receive operations
>* sub-string operations
>* sub-slice operations
>* 加减乘除等运算符

> 对于上面的内容，有以下几点解释：

>>* 常数为什么不可以寻址?： 如果可以寻址的话，我们可以通过指针修改常数的值，破坏了常数的定义。
>>* map的元素为什么不可以寻址？:两个原因，如果对象不存在，则返回零值，零值是不可变对象，所以不能寻址，如果对象存在，因为Go中map实现中元素的地址是变化的，这意味着寻址的结果是无意义的。
>>* 为什么slice不管是否可寻址，它的元素读是可以寻址的？:因为slice底层实现了一个数组，它是可以寻址的。
>>* 为什么字符串中的字符/字节又不能寻址呢：因为字符串是不可变的。

## “ nil”接口和“ nil”接口值



```

package main

import "fmt"

func main() {
    var data *byte
    var in interface{}
    fmt.Println(data,data == nil) //prints: <nil> true
    fmt.Println(in,in == nil)     //prints: <nil> true
	fmt.Printf("The type of data is %T, the value of data is %v\n",data,data)
	//The type of data is *uint8, the value of data is <nil>
	fmt.Printf("The type of in is %T, the value of in is %v\n",in,in)
    //The type of in is <nil>, the value of in is <nil>
    in = data
    fmt.Println(in,in == nil)     //prints: <nil> false

	fmt.Printf("The type of in is %T, the value of in is %v\n",in,in)
    //The type of in is *uint8, the value of in is <nil>
   
}
```

>* 对于接口变量，只有当接口的类型和值都为nil时，这个变量才是nil，对于其他变量，值为nil就是nil
>* 接口类型的变量是万能变量，它可以被其他各种类型的变量赋值，也就是说，当一个接口变量被其他变量赋值时，它的值和类型都会和这个变量相同

>所以在上面那个程序里，interface的in可以被data赋值，此时in的类型就是data的类型，值也是data的值


## 堆栈和堆变量


> 您并不总是知道您的变量是分配在堆栈还是堆上。在C++中，使用new运算符创建变量始终意味着您具有堆变量。在Go语言中，即使使用new()或make()函数，编译器也会决定将变量分配到的位置。编译器根据变量的大小和“转义分析”的结果来选择存储变量的位置。这也意味着可以返回对局部变量的引用，而在其他语言（如C或C ++）中则不行。可以通过这个 `-gcflags -m` 参数来查看变量的位置，例如`go run -gcflags -m main.go`或者`go build -gcflags -m main.go`
例如：

![avatar](C://Users//rguo//Desktop//aaa.JPG)

这里就能看出来到底是分配到栈上，还是堆上了
对于会逃逸的变量，无论大小都分配到堆上。对不不会逃逸的对象，如果需要分配的内存太大，则分配到堆上，如果分配内存小，则分配到栈上

## GOMAXPROCS，并发和并行

---
> 1.4及以下版本仅使用一个执行上下文/OS线程。这意味着在任何给定时间只能执行一个goroutine。这个时候就是一个并发，一个CPU同时处理过个任务，是逻辑上的同时发生。从1.5 Go开始，将执行上下文的数量设置为所返回的逻辑CPU内核的数量runtime.NumCPU()。该数字可能与系统上逻辑CPU内核的总数不匹配，具体取决于进程的CPU亲和力设置。您可以通过更改`GOMAXPROCS`环境变量或调用`runtime.GOMAXPROCS()`函数来调整此数字。这个时候就是并行，物理上真正的同时发生。

> 你可以设置`GOMAXPROCS`的数量超过CPU的数量，最开始`GOMAXPROCS`的最大值是256，在1.9版本最大值为1024，但是从1.10开始就没有限制了
```
package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Println(runtime.GOMAXPROCS(-1)) //4
	fmt.Println(runtime.NumCPU())       //4
	runtime.GOMAXPROCS(20)
	fmt.Println(runtime.GOMAXPROCS(-1)) //20
	runtime.GOMAXPROCS(300)
	fmt.Println(runtime.GOMAXPROCS(-1)) //300
	runtime.GOMAXPROCS(10000)
	fmt.Println(runtime.GOMAXPROCS(-1)) //10000
}
```

> 可以看到，在go1.15之后在默认情况下，go已经将`GOMAXPROCS`的值设置成了CPU的数量，这在大多数情况下都具有好的性能。但有些时候，比如在进行读写时，将`GOMAXPROCS`的值设置更大一点可以提高I/O的吞吐率。

## 读写操作重新排序

> Go可以对某些操作进行重新排序，但是可以确保goroutine中发生该行为的整体行为不会改变。但是，它不能保证跨多个goroutine的执行顺序。
```
package main

import (
	"runtime"
	"time"
)

var _ = runtime.GOMAXPROCS(4)

var a, b int

func u1() {
	a = 1
	b = 2
}

func u2() {
	a = 3
	b = 4
}
func u3(){
	a = 5
	b = 6
}

func p() {
	println(a)
	println(b)
}

func main() {
	go u1()
	go u2()
	go u3()
	go p()
	time.Sleep(1 * time.Second)
}
```
> 有一次的结果是3，4
## 抢占式调度

---
```
package main

import "fmt"
var _ = runtime.GOMAXPROCS(1)

func main() {  
    done := false

    go func(){
        done = true
    }()

    for !done {
    }
    fmt.Println("done!")
}
```
> 程序不会中断

---
```
package main

import "fmt"
var _ = runtime.GOMAXPROCS(1)

func main() {  
    done := false

    go func(){
        done = true
    }()

    for !done {
     fmt.Println("break!")
    }
    fmt.Println("done!")
}
```
>* 程序会中断

> 产生这个现象的原因是，一次Println()操作就是一次I/O操作，他会中断当前的for循环，此时go的调度机制会查询当前的程序中是否存在其他的等待协程，如果有先执行其他的。


> 对于上面的程序，在go1.13版本的时候程序，由于陷入for死循环中，程序没有办法退出。但是不设置`GOMAXPROCS`的值，他就会是系统默认的CPU数量，不会导致陷入死循环。或者，在for中加一个输出，也不会陷入死循环。而在1.15版本中，即使没有输出也会自动退出死循环

## 导入C和多行导入块

---
> 如果在go语言中想要调用c语言的函数，我们可以导入“C”这个模块，模块名就是“C”，要注意的是模块“C”必须被单独import，不能和其他模块被同一个import 导入
```
package main

/*
#include <stdlib.h>
*/
import (
  "C"
  "unsafe"
)

func main() {
  cs := C.CString("my go string")
  C.free(unsafe.Pointer(cs))
}
```
> 上面的导入会在编译时报错，正确的导入方式应该如下：
```
package main

/*
#include <stdlib.h>
*/
import (
  "C"
)

import (
  "unsafe"
)

func main() {
  cs := C.CString("my go string")
  C.free(unsafe.Pointer(cs))
}
```

## 导入C和Cgo注释之间没有空行

---
```
package main

/*
#include <stdlib.h>
*/

import "C"

import (
  "unsafe"
)

func main() {
  cs := C.CString("my go string")
  C.free(unsafe.Pointer(cs))
}
```
> import “C”之后，在上面注释一下要使用的C文件，这个时候就可以调用这个文件中的C函数了，要注意的是import "C"和注释之间不能有空行，否则会导致编译错误

## 无法使用可变参数调用C函数

---

> 比如
```
package main

/*
#include <stdio.h>
#include <stdlib.h>
*/
import "C"

import (
  "unsafe"
)

func main() {
  cstr := C.CString("go")
  C.printf("%s\n",cstr) //not ok
  C.free(unsafe.Pointer(cstr))
}
```
> printf()是一个参数不定的函数，不能通过C.printf()这种方式调用参数不定的函数。如果要使用的话，需要把这个函数进行封装

```
package main

/*
#include <stdio.h>
#include <stdlib.h>

void out(char* in) {
  printf("%s\n", in);
}
*/
import "C"

import (
  "unsafe"
)

func main() {
  cstr := C.CString("go")
  C.out(cstr) //ok
  C.free(unsafe.Pointer(cstr))
}
```

# 调试方法
> 1. linux环境中，可以用shell自带的time命令，进行性能测试。示例如下：
> `time go run main.go`
> 2. 通过go自带的调试工具pprof
> CPU profile：报告程序的 CPU 使用情况，按照一定频率去采集应用程序在 CPU 和寄存器上面的数据
Memory Profile（Heap Profile）：报告程序的内存使用情况
Block Profiling：报告 goroutines 不在运行状态的情况，可以用来分析和查找死锁等性能瓶颈
Goroutine Profiling：报告 goroutines 的使用情况，有哪些 goroutine，它们的调用关系是怎样的
> 首先是最基本的runtime/pprof这是官方提供的最基本的包。然后是`net/http/pprof`这个包是封装在`runtime/pprof`这个包基础上的

首先调用runtime/pprof这个包，将结果输出到一份文件中，通过执行go tool pprof <文件名>就可以进行查看，查看性能的消耗。

# 调试工具
## dlv
>dlv是一种专门来调试go代码的工具。首先使用方法，通过ps -ef 找到go运行的二进制文件，然后 dlv attach pid 来进行调试
查看帮助 help，bp，查看断点


# make 和 new
> 在声明一个普通变量的时候，不需要new或者make，只需要通过var声明就可以，但是对于指针类型的变量，在声明的时候要通过new来申请内存空间，但是对于普通的变量，`int`,`string`等变量就不需要new了，但是对于make来说，主要使用的地方有三出，chanel，slice，以及map，使用这三种类型的时候一定要提前通过make申请空间。

# 变量逃逸
> 在go中，变量申请的内存到底是放在堆上还是栈上，是通过go的runtime来自动调度的。一般来说，在某个函数中的临时变量都是分配到栈上的，但是在go中，当发现变量的作用域没有跑出函数范围，就可以在栈上，反之则必须分配在堆
> 所以说，Golang中一个函数内局部变量，不管是不是动态new出来的，它会被分配在堆还是栈，是由编译器做逃逸分析之后做出的决定。