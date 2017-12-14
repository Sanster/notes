## 指定 build apk 的名字
```groovy
      buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
            applicationVariants.all { variant ->
                variant.outputs.each { output ->
                    def newName = "" + ".apk"
                    output.outputFile = new File(output.outputFile.parent, newName)
                }
            }
        }
    }
```
