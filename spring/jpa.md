## findOne 和 getOne 的区别
getOne 是 lazy load, findOne 是获得实体或者 null
```java
public static String NON_EXISTING_ID = -1;
...
MyEntity getEnt = myEntityRepository.getOne(NON_EXISTING_ID);
MyEntity findEnt = myEntityRepository.findOne(NON_EXISTING_ID);

if(findEnt != null) {
     findEnt.getText(); // findEnt is null - this code is not executed
}

if(getEnt != null) {
     getEnt.getText(); // Throws exception - no data found, BUT getEnt is not null!!!
}
```
