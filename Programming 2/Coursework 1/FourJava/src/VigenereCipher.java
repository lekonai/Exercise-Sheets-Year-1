import java.util.ArrayList;
import java.nio.file.Files;
import java.util.HashSet;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.io.IOException;

public class VigenereCipher implements Cipher {
    // realistically this is a static class ?
    private final String vigSquareText = """
            A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
            B C D E F G H I J K L M N O P Q R S T U V W X Y Z A
            C D E F G H I J K L M N O P Q R S T U V W X Y Z A B
            D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
            E F G H I J K L M N O P Q R S T U V W X Y Z A B C D
            F G H I J K L M N O P Q R S T U V W X Y Z A B C D E
            G H I J K L M N O P Q R S T U V W X Y Z A B C D E F
            H I J K L M N O P Q R S T U V W X Y Z A B C D E F G
            I J K L M N O P Q R S T U V W X Y Z A B C D E F G H
            J K L M N O P Q R S T U V W X Y Z A B C D E F G H I
            K L M N O P Q R S T U V W X Y Z A B C D E F G H I J
            L M N O P Q R S T U V W X Y Z A B C D E F G H I J K
            M N O P Q R S T U V W X Y Z A B C D E F G H I J K L
            N O P Q R S T U V W X Y Z A B C D E F G H I J K L M
            O P Q R S T U V W X Y Z A B C D E F G H I J K L M N
            P Q R S T U V W X Y Z A B C D E F G H I J K L M N O
            Q R S T U V W X Y Z A B C D E F G H I J K L M N O P
            R S T U V W X Y Z A B C D E F G H I J K L M N O P Q
            S T U V W X Y Z A B C D E F G H I J K L M N O P Q R
            T U V W X Y Z A B C D E F G H I J K L M N O P Q R S
            U V W X Y Z A B C D E F G H I J K L M N O P Q R S T
            V W X Y Z A B C D E F G H I J K L M N O P Q R S T U
            W X Y Z A B C D E F G H I J K L M N O P Q R S T U V
            X Y Z A B C D E F G H I J K L M N O P Q R S T U V W
            Y Z A B C D E F G H I J K L M N O P Q R S T U V W X
            Z A B C D E F G H I J K L M N O P Q R S T U V W X Y""";
    private final ArrayList<ArrayList<String>> mainGrid = reformatTo2D(vigSquareText.split("\\s+"));
    // maybe would be more sensible to be using regular list rather than arraylist as it doesn't vary too much?

    // debug
    public ArrayList<ArrayList<String>> retrieveGrid(){
        return mainGrid;
    }
    // debug

    public String accessGrid(int a, int b){
        return mainGrid.get(a).get(b);
    }

    public int charToIndex(String s){
        HashSet<String> alphabet = new HashSet<>(mainGrid.getFirst());

        // make sure to return a funky ass number if what's given's not in the alphabet.
        // then it'll signal not to change the plaintext

        return alphabet.contains(s) || alphabet.contains((s.toUpperCase())) ? s.toUpperCase().toCharArray()[0] - 65 : -1;
    }

    public int charToIndex(char c){
        HashSet<String> alphabet = new HashSet<>(mainGrid.getFirst());
        // make sure to return a funky ass number if what's given's not in the alphabet.
        // then it'll signal not to change the plaintext
        String actualCharacter = String.valueOf(c).toUpperCase();
        boolean indexable;
        if (alphabet.contains(actualCharacter)){
            indexable = true;
        }
        else {
            indexable = false;

            System.out.println("False spotted"); // debug
        }
        return indexable ? actualCharacter.toCharArray()[0] - 65 : -1;
    }


    public ArrayList<ArrayList<String>> reformatTo2D(String[] arr){
//        ArrayList<ArrayList<String>> returnArray = new ArrayList<>();
//        for (int i = 0; i < 26; i++){
//            ArrayList<String> current = new ArrayList<>(i * 26, (i * 26) + 26);
//        }
//        return returnArray;
    }

    public String encryptionProcess(String plaintext, String key){
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < plaintext.length(); i++){
            int num1 = charToIndex(plaintext.charAt(i));
            System.out.println(String.valueOf(plaintext.charAt(i)) + num1);
            int num2 = charToIndex(key.charAt(i));
            System.out.println(String.valueOf(plaintext.charAt(i)) + num2);
            if (num1 != -1 || num2 != -1){
                sb.append(accessGrid(num1, num2));
            }
            else {
                sb.append(plaintext.toCharArray()[i]);
            }
        }
        return sb.toString();
    }
    @Override // makes sure its all okay ! :)
    public String encrypt(String message_filename, String key_filename) {
        StringBuilder finalString = new StringBuilder();
        Path msgPath = Paths.get(message_filename);
        Path keyPath = Paths.get(key_filename);
//        String toEncrypt = "", keys = "";
//        try {
//            toEncrypt = new String(Files.readAllBytes(msgPath));
//        } catch (IOException e) {
//            System.out.println("DONE");
//        }
//        try {
//            keys = new String(Files.readAllBytes(keyPath));
//        } catch (IOException e) {
//            System.out.println("DONE");
//        }
//        System.out.println(toEncrypt);
//        System.out.println(keys);
//        for (int i = 0; i < toEncrypt.size(); i++) {
//
//            // ideally some error checks should be made before this, some basic ones like checking
//            // the lengths and the keyPath
//            // there should also be a KEY WRAPPER.
//            // keep that in mind
//            finalString.append(encryptionProcess(toEncrypt.get(i), keys.get(i)));
//        }

//        return finalString.toString();

        return " ";
    }

    @Override
    public String decrypt(String message_filename, String key_filename) {
//        StringBuilder finalString = new StringBuilder();
//        List<String> toDecrypt = Files.readAllLines(Path.of(message_filename));
//        List<String> keys = Files.readAllLines(key_filename);


        return "";
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

//    ArrayList<ArrayList<String>> curr = vCi.retrieveGrid();
    System.out.println(vCi.accessGrid(0,25));
    System.out.println(vCi.retrieveGrid());
    System.out.println(vCi.accessGrid(11,15));

//    System.out.println(vCi.retrieveGrid().getFirst());
//    System.out.println(vCi.charToIndex("a"));
    vCi.encrypt("encrypt_check.txt","key_check.txt");
    vCi.encryptionProcess("HEllo", "KEv1n");
}
