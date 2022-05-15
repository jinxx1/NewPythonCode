// -*- coding: utf-8 -*-

// a = '123';
// a = 10 - 1;
// a = undefined;
// var a;


// var a = 11;
// var b = a;
// // a++;
// ++b;
// a = a++
// console.log(a)
// console.log(typeof a)
//
// console.log(b)
// console.log(typeof b)
// 逻辑判断
// js有三种逻辑运算符
// !非
// &&与
// ||或


// 条件运算符，也叫三元云悬浮
// 语法：
// 条件表达式?语句1:语句2;
// - 执行的流程：
// 条件运算符在执行时，首先对条件表达式进行求值。
// 如果该值为true，则执行语句1，并返回执行结果
// 如果该值为Falsh，则执行语句2，并且返回执行结果。

// var a = true;
//
// a ? console.log('语句1') : console.log('语句2');
// a = 10;
// b = 20;
// c = 50;
// a > b ? console.log('a大') : console.log('b大');
// var max = a > b ? a : b;
//
// console.log(max)
//
// max = max > c ? max : max;
// console.log(max)
//
// // 如果||or的有限极高，或者&&and两个一样高
// // 拿不准的话，用（）
// {
//     var result = (1 || 2) && 3;
//     console.log(result)
//     console.log('122')
//     console.log('iii')
//
// }
// var a = 1;
// var b = 2;
// var c = a + b;
// if 语句1

// if语句2
// if(条件=true){
//     语句
// }else{语句}

//
// if 语句3
//
//     if(条件){
//         语句..
//     }else if(条件){
//         语句...
//     }else if(条件){
//         语句...
//     }else{
//         语句
//     }

// if (c == 3) {
//     console.log('121212121212121212');
//     console.log("33333333333333333333333");
// }
//
// var num = 'aaa';
// switch (num) {
//     case 1:
//         console.log('yi');
//         break;
//     case 2:
//         console.log('er');
//         break;
//     case 3:
//         console.log('san');
//         break;
//     default:
//         console.log('非法数字');
// }

// var score = 67;
// switch (parseInt(score / 10)) {
//     case 10:
//     case 9:
//     case 8:
//     case 7:
//     case 6:
//         console.log('合格');
//         break;
//     default:
//         console.log('不合格');
// }
//
// switch (true) {
//     case score >= 60:
//         console.log('————合格');
//         break
//     default:
//         console.log('————不合格')
// }
//
// // 循环while
// var n = 1;
// while (true) {
//     console.log(n++);
//     if (n == 10) {
//         break;
//     }
// }
// console.log('------------------------------')
// do while 循环
// do{
//     语句...
// }while (条件表达式)
// do。。。while语句在执行时，会先执行循环体。
// 如果值为true，则继续执行循环体，执行完毕继续判断
// 以此类推。
// 如果结果为flash，则终止循环。


// 实际上do while 和while两个语句功能类似。
// 不同的是while是先判断后执行，
// 而do while会先执行后判断。
// var i = 11;
// do {
//     console.log(i++);
// } while (i <= 10)
// {
//     console.log(i)
// }
// ;
// console.log('---------------------')
// var rate = 0.05;
// var count = 1000;
//
// var year = 0;
//
// while (count <= 5000) {
//     count *= (1 + rate)
//     year++
//     // console.log(count)
// }
// console.log(year)
// console.log('---------------------------')

// for语句，也是一个循环语句。也成为for循环
// 在for循环中，为我们提供了专门的位置用来放三个表达式。
// 1.初始化表达式
// 2.条件表达式
// 3.更新表达式
// for循环的语法：
// for(初始化表达式；条件表达式；更新表达式){
//     语句。。。}

// for循环的执行流程：
// 1、限制性初始化表达式。
// 2、判断条件表达式，判断是否执行循环。如果true则执行循环，否则终止。
// 3、执行更新表达式，更新表达式执行完毕继续重复。
// for循环中的三个部分都可以省略，也可以写在外部
// 如果在for循环中不写任何表达式，只写两个 分号；
// 此时循环是一个死循环，会一直执行下去。
// for (var i = 0; i < 5; i++) {
//     console.log(i);
// }
// 打印1-100所有奇数之和
// var count = 0;
// var sum = 0;
// for (var i = 0; i <= 100; i++) {
//     // if (i % 2 != 0) {
//     //     count += i;
//     //     console.log(i)
//     // }
//     if (i % 7 == 0) {
//         count += i;
//         sum += 1;
//         console.log(i)
//
//     }
//
//
// }
// console.log(count)
// console.log(sum)
// console.log('----------------------[[')
// for (var i = 100; i < 1000; i++) {
//     var bai = parseInt(i / 100) ** 3;
//     var shi = parseInt((i - bai * 100) / 10) ** 3;
//     var ge = (i % 10) ** 3;
//     // bai = a1 ** 3;
//     // shi = b1 ** 3;
//     // ge = c1 ** 3;
//     // console.log(i,a1,b1,c1,bai,shi,ge,bai+shi+ge)
//     if (bai + shi + ge == i) {
//         console.log('get ---------' + i);
//     }
//
//
// }
// console.log('---------------------质数')

// for (var num1 = 2; num1 < 100; num1++) {
//     bb = num1 == 2 || num1 == 3 || num1 == 5 || num1 == 7
//     aa = num1 % 2 != 0 && num1 % 3 != 0 && num1 % 5 != 0 && num1 % 7 != 0;
//     switch (true) {
//         case bb:
//             console.log(num1 + '这是质数')
//             break
//         case aa:
//             console.log(num1 + '这是质数')
//     }


// ii = 0;
//
// var ss1 = '';
// for (var ii = 0; ii < 5; ii++) {
//     ss = '*';
//     for (var j = 0; j < 5 - ii; j++) {
//         ss1 = ss1 + ss
//         console.log(ss1);
//     }
//     console.log('\n');

// if (aa) {
//     console.log(num1 + '这是质数')
// }
// if (bb) {
//     console.log(num1 + '这是质数')
// }


// console.log('----------------乘法口诀表');
//
// for (var x = 1; x < 10; x++) {
//     var stat = ''
//     for (var y = 1; y <= x; y++) {
//
//         var strWord = y + 'X' + x + "=" + x * y
//         stat = stat + " " + strWord
//         console.log(stat);
//     }
//     console.log('\n');
//
// }
// console.log('----------------终止外部循环');
//
// outer:
//     for (q1 = 0; q1 < 5; q1++) {
//         console.log('外层循环' + q1);
//         for (q2 = 0; q2 < 5; q2++) {
//             break outer;
//             console.log('内层循环' + q2);
//         }
//
//     }
//
// for (var q1 = 0; q1 < 5; q1++) {
//
//     if (q1 == 2) {
//         continue;
//     }
//     console.log(q1);
// }
// var  obj = new Object();
// obj.name = '孙悟空';
// obj.gender='男';
// obj.age=18;
// console.log(obj);
// console.log(typeof obj);
//
// delete obj.name;
// console.log(obj);
//
// obj.var = 'hello';
// console.log(obj);
// obj['123'] = 123;
// console.log(obj);
// console.log(obj['123']);
var fun = new Function("console.log('你好');");
fun()

function fun2(){
    console.log('这是我第二个函数');

}

console.log(fun2);
fun2()