`data class` 提供了以下方法：
- equals()：可以用 `==`代替
- hashCode()
- toString()：打印数据的属性 "User(name=John, age=42)"
- componentN()：按顺序访问数据对象中的字段
- copy()：用于生成新的对象

```kotlin
data class User(var name: String, var age: Int)

data class Group(var user: User)

fun main(args: Array<String>){
    val tom = User("Tom", 2)
    println(tom.toString())  // User(name=Tom, age=2)
    println(tom.component1()) // Tom
    println(tom.component2())  // 2

    val tom2 = User("Tom", 2)
    println(tom == tom2) // true
    
    val (name, age) = tom
    println(name) // Tom
    println(age) // 2

    val group = Group(tom)
    println(group.toString()) // Group(user=User(name=Tom, age=2))

    val (tomInGroup) = group
    println(tomInGroup == tom) // True

    val olderTom = tom.copy(age=4)
    println(olderTom.toString()) // User(name=Tom, age=4)
}
```
