调试 AsyncTask doInBackground 里的代码，添加以下代码才能命中断点：
```java
// 最好加上这个判断，否则非调试模式就会 hang 住
if(android.os.Debug.isDebuggerConnected()) {  
    android.os.Debug.waitForDebugger();
}
```
参考：[Debug#waitForDebugger](https://developer.android.com/reference/android/os/Debug.html#waitForDebugger())
