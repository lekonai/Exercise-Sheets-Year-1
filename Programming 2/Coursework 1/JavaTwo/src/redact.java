public static String redact(String content, String[] redactWords) {
    // split alongside pattern with matcher
    // have to retain spaces or else it gets realllllyy finnicky to format later
    ArrayList<String> splitString = new ArrayList<>();
    Matcher cond = Pattern.compile("\\s|[\\w-']+|[.,!?;:\"()]").matcher(content);
    while (cond.find()) {
        splitString.add(cond.group());
    }

    System.out.println(splitString); // debug

    // find and replcae
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
