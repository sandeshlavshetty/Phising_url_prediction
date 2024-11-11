<table>
<tr>
<td>

### C++

1. **For Loop:**
   ```cpp
   #include <iostream>

   int main() {
       for (int i = 0; i < 5; i++) {
           std::cout << i << std::endl;
       }
       return 0;
   }
   ```

2. **Range-Based For Loop (for iterating through arrays or vectors):**
   ```cpp
   #include <iostream>
   #include <vector>

   int main() {
       std::vector<std::string> array = {"apple", "banana", "cherry"};
       for (const std::string& value : array) {
           std::cout << value << std::endl;
       }
       return 0;
   }
   ```

3. **While Loop:**
   ```cpp
   #include <iostream>

   int main() {
       int i = 0;
       while (i < 5) {
           std::cout << i << std::endl;
           i++;
       }
       return 0;
   }
   ```

</td>
<td>

### Java

1. **For Loop:**
   ```java
   public class Main {
       public static void main(String[] args) {
           for (int i = 0; i < 5; i++) {
               System.out.println(i);
           }
       }
   }
   ```

2. **Enhanced For Loop (for iterating through arrays or collections):**
   ```java
   public class Main {
       public static void main(String[] args) {
           String[] array = {"apple", "banana", "cherry"};
           for (String value : array) {
               System.out.println(value);
           }
       }
   }
   ```

3. **While Loop:**
   ```java
   public class Main {
       public static void main(String[] args) {
           int i = 0;
           while (i < 5) {
               System.out.println(i);
               i++;
           }
       }
   }
   ```

4. **Do-While Loop:**
   ```java
   public class Main {
       public static void main(String[] args) {
           int i = 0;
           do {
               System.out.println(i);
               i++;
           } while (i < 5);
       }
   }
   ```

</td>
</tr>
</table>
