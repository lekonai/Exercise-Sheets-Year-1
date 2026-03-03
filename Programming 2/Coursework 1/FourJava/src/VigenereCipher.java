import java.util.ArrayList;
import java.util.HashSet;
import java.util.Arrays;

public class VigenereCipher implements Cipher {
    // realistically this is a static class ?
    private final String vigSquareText = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z\n" +
            "B C D E F G H I J K L M N O P Q R S T U V W X Y Z A\n" +
            "C D E F G H I J K L M N O P Q R S T U V W X Y Z A B\n" +
            "D E F G H I J K L M N O P Q R S T U V W X Y Z A B C\n" +
            "E F G H I J K L M N O P Q R S T U V W X Y Z A B C D\n" +
            "F G H I J K L M N O P Q R S T U V W X Y Z A B C D E\n" +
            "G H I J K L M N O P Q R S T U V W X Y Z A B C D E F\n" +
            "H I J K L M N O P Q R S T U V W X Y Z A B C D E F G\n" +
            "I J K L M N O P Q R S T U V W X Y Z A B C D E F G H\n" +
            "J K L M N O P Q R S T U V W X Y Z A B C D E F G H I\n" +
            "K L M N O P Q R S T U V W X Y Z A B C D E F G H I J\n" +
            "L M N O P Q R S T U V W X Y Z A B C D E F G H I J K\n" +
            "M N O P Q R S T U V W X Y Z A B C D E F G H I J K L\n" +
            "N O P Q R S T U V W X Y Z A B C D E F G H I J K L M\n" +
            "O P Q R S T U V W X Y Z A B C D E F G H I J K L M N\n" +
            "P Q R S T U V W X Y Z A B C D E F G H I J K L M N O\n" +
            "Q R S T U V W X Y Z A B C D E F G H I J K L M N O P\n" +
            "R S T U V W X Y Z A B C D E F G H I J K L M N O P Q\n" +
            "S T U V W X Y Z A B C D E F G H I J K L M N O P Q R\n" +
            "T U V W X Y Z A B C D E F G H I J K L M N O P Q R S\n" +
            "U V W X Y Z A B C D E F G H I J K L M N O P Q R S T\n" +
            "V W X Y Z A B C D E F G H I J K L M N O P Q R S T U\n" +
            "W X Y Z A B C D E F G H I J K L M N O P Q R S T U V\n" +
            "X Y Z A B C D E F G H I J K L M N O P Q R S T U V W\n" +
            "Y Z A B C D E F G H I J K L M N O P Q R S T U V W X\n" +
            "Z A B C D E F G H I J K L M N O P Q R S T U V W X Y";
    private final ArrayList<ArrayList<String>> mainGrid = reformatTo2D(vigSquareText.split("\\s+"));
    // maybe would be more sensible to be using regular list rather than arraylist as it doesn't vary too much?

    public ArrayList<ArrayList<String>> retrieveGrid(){
        return mainGrid;
    }

    public String accessGrid(int a, int b){
        return mainGrid.get(a).get(b);
    }

    public ArrayList<ArrayList<String>> reformatTo2D(String[] arr){
        ArrayList<ArrayList<String>> finalGrid = new ArrayList<>();
        for (int i = 0; i < 26; i++){
            ArrayList<String> current = new ArrayList<>(new ArrayList<>(Arrays.asList(arr).subList(i * 26, (i * 26) + 26)));
            // lowkey so intuitive ???
            finalGrid.add(current);
        }
        return finalGrid;
    }

    @Override
    public String encrypt(String message_filename, String key_filename) {
        String toEncrypt = readFile(message_filename);
        String keys = readFile(key_filename);
        if (toEncrypt == null || keys == null) { return null; }
        return encryptionProcess(toEncrypt, keys).toUpperCase(); // added a touppercase because everything needs to be uppercase...
    }

    @Override
    public String decrypt(String message_filename, String key_filename) {
        String toDecrypt = readFile(message_filename);
        String keys = readFile(key_filename);
        if (toDecrypt == null || keys == null) { return null; }
        return decryptionProcess(toDecrypt, keys).toUpperCase();
    }

    // overload!
    public int charToIndex(char c){
        HashSet<String> alphabet = new HashSet<>(mainGrid.get(0));
        String actualCharacter = String.valueOf(c).toUpperCase();

        return alphabet.contains(actualCharacter) ? actualCharacter.toCharArray()[0] - 65 : -1;
    }

    public String readFile(String fileN){
        StringBuilder output = new StringBuilder();
        File theFile = new File(fileN);

        try (Scanner reader = new Scanner(theFile)) {
            while (reader.hasNextLine()) {
                String data = reader.nextLine() + "\n";
                output.append(data);
            }
        } catch (FileNotFoundException e) {
            return null;
        }
        output.delete(output.length() - 1, output.length()); // this is a really finnicky manner of avoiding a whitespace at the end
        // but there's not much more i can do about it, because java doesn't have a way to format your stringbuilders. java man...
        return output.toString();
    }

    public String formatKey(String key, int ptLength){
        StringBuilder wrap = new StringBuilder();
        for (int i = 0; i < ptLength; i++){
            wrap.append(key.toCharArray()[i % key.length()]);
        }
        // the uppercase technically isn't necessary for this but it'll be best if you're to view this method independently
        return reverse(wrap.toString()).toUpperCase();
    }

    private String reverse(String key){
        StringBuilder rev = new StringBuilder();
        for (int i = key.length() - 1; i >= 0; i--){
            rev.append(key.toCharArray()[i]);
        }
        return rev.toString();
    }

    public String encryptionProcess(String plaintext, String key){
        StringBuilder sb = new StringBuilder();
        if (key.isEmpty()){
            return null;
        }
        key = formatKey(key, plaintext.length());
        for (int i = 0; i < plaintext.length(); i++){
            int num1 = charToIndex(plaintext.charAt(i));

            int num2 = charToIndex(key.charAt(i));

            if (num1 != -1 && num2 != -1){
                sb.append(accessGrid(num1, num2));
            }
            else {
                sb.append(plaintext.toCharArray()[i]);
            }
        }
        return sb.toString();
    }

    public String decryptionProcess(String ciphertext, String key){
        StringBuilder dc = new StringBuilder();
        if (key.isEmpty()){
            return null;
        }
        key = formatKey(key, ciphertext.length());
        // main concern with this is that what if a fully formatted key's already been given?
        // probably unlikely because that's just not the key at that point
        for (int i = 0; i < ciphertext.length(); i++){

            char letter = ciphertext.charAt(i);

            int keyIndex = charToIndex(key.charAt(i));

            if (charToIndex(ciphertext.charAt(i)) != -1 && keyIndex != -1){
                dc.append(retrieveGrid().get(0).get(retrieveGrid().get(keyIndex).indexOf(String.valueOf(letter))));
                // very convoluted piece of code here let me break it down for you:
                /*
                - get the first row of the grid (the alphabet)
                - get the index of the letter of the cipher text on the row of the key's letter
                - that index is then used on the alphabet as the ciphertext's letter will be the column
                 */
            }
            else {
                dc.append(ciphertext.toCharArray()[i]);
            }
        }
        return dc.toString();
    }
}

void main() {
    /*
    Exceptionbaits to keep track of:
        - Key is an invalid length (so anything smaller or larger)
            - Recall that you cannot change the key yourself, that'd be against the principle of a cipher
        - Numeric characters and anything that isn't an alphabetic character's ignored.
        - Everything must be capitals
        - Insufficient amount of keys for amount of plaintexts and vice versa
     */

    VigenereCipher vCi = new VigenereCipher();

//    System.out.println(vCi.encrypt("src/encrypt_check.txt","src/key_check.txt"));

    System.out.println(vCi.encryptionProcess("I've a brave heart! And, I love to say numbers; even all of them. 1, 2 and even 3. Those are my favourites :)", "Omar"));
    System.out.println(vCi.decryptionProcess("W'VQ R NFRVQ YEMFK! OED, Z XCME HF EOP ZIDBQFJ; SMEZ RLX FF HYEY. 1, 2 MBU QJVN 3. FVFSQ RRQ DY TRVAIIIFSJ :) ", "Omar"));
    System.out.println(vCi.decryptionProcess("yo what's up", "-1230-';.';,]")); // this shouldn't return null as it's not... null, basically
    System.out.println(vCi.encryptionProcess("hello", ""));

}
