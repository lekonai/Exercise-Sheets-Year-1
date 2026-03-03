public static String redact(String content, String[] redactWords) {
    // have to retain spaces or else it gets realllllyy finnicky to format later
    ArrayList<String> splitString = new ArrayList<>();
    // nvm can't use regex, had a nice solution and now no more.

    // split apart
    int ctr = 0;
    while (ctr < content.length()){
        char curChar = content.charAt(ctr);
        boolean wordCondition = Character.isLetterOrDigit(curChar);

        if (Character.isWhitespace(curChar)){
            splitString.add(String.valueOf(curChar));
            ctr++;
        }
        else if (wordCondition){ // word collation
            int wordStart = ctr;
            while (ctr < content.length()){
                char wordChar = content.charAt(ctr);
                if (Character.isLetterOrDigit(wordChar) || wordChar == '\'' || wordChar == '-'){
                    ctr++;
                }
                else { break; }
            }
            splitString.add(content.substring(wordStart, ctr));
        }

        else if (".,!?;:\\\"()".indexOf(curChar) != -1){
            splitString.add(String.valueOf(curChar));
            ctr++;
        }

        else { ctr++; }
    }

    // find and replace
    for (int i = 0; i < splitString.size(); i++){
        for (String word : redactWords) {
            if (splitString.get(i).equalsIgnoreCase(word)) {
                splitString.set(i, "#".repeat(splitString.get(i).length()));
                break;
            }
        }
    }

    // finish up and format properly
    StringBuilder firstFinalProduct = new StringBuilder();
    for (String item : splitString){
        firstFinalProduct.append(item);
    }
    return firstFinalProduct.toString();
}

void main(){
    System.out.println(redact("These's quick, Brown,,,, fox!! . Laz-y ass dog", new String[]{"fox", "laZY", "dog"}));
    System.out.println(redact("A B C, it's as easy as 1 2 3, as simple as do re mi, A B C, 1 2 3, baby you and me girl", new String[]{"1", "easy", "it's", "A", "a"}));
}
