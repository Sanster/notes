调试 AsyncTask doInBackground 里的代码，添加以下代码才能命中断点：
```java
android.os.Debug.waitForDebugger();
```
参考：[Debug#waitForDebugger](https://developer.android.com/reference/android/os/Debug.html#waitForDebugger())
