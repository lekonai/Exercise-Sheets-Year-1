public class SortedLinkedList implements SortedList {
    boolean asc = true; // this is inherent; the default. it is dsc when false
    Node initNode = new Node ("nullInitNode");
    /*
     considering you can't use lists etc. everything can be stored as a link to this one sole object.
     the initial variable will always be changed to the first item added to a list, and as its sorted,
     it should be changed to the first item, for convenience, but always making sure the initial node is this can
     be a bit finicky.

     wondering if it'd be lazy yet convenient to just make sure the initnode is just the last item if its
     descending?
    */

    @Override
    public int size() {
        // number of nodes in a linked list
        int counter = 1; // there'll always be one
        Node curNode = initNode;
        if (asc){
            while (true){
                if (curNode.getNext() != null){
                    curNode = curNode.getNext();
                    counter += 1;
                }
                else {
                    break;
                }
                // forwards
            }
        }

        if (!asc){
            while (true){
                if (curNode.getPrev() != null){
                    curNode = curNode.getPrev();
                    counter += 1;
                }
                else {
                    break;
                }
                // backwards
            }
        }
        return counter == 1 && initNode.getString().equals("nullInitNode") ? 0 : counter;
    }

    @Override
    public void add(String string) {
        // add a node with a string to the linked list (in the appropriate order)
        if (string == null || string.equals("")){
            return;
        }
        if (size() == 0){ // if its just init node
            initNode.setString(string);
            return;
        }
        Node newNode = new Node(string);
        add(newNode);
        // to be implemented
    }

    public boolean filter(Node node){
        if (node == null){
            return false;
        }
        char[] nameArray = node.getString().toUpperCase().toCharArray();
        for (char Char : nameArray){
            if (Char < 65 || Char > 90){
                return false;
            }
        }
        return true;
    }

    @Override
    public void add(Node node) {
        if (size() == 0){ // if its just init node
            initNode = node;
            return;
        }
        if (!filter(node)){
            return; // close the stack because then there's a non-alphabetic character within
        }
        if (node.getNext() != null || node.getPrev() != null){
            if (node.getNext() != null && node.getPrev() == null){
                node.getNext().setPrev(null);

                add(node.getNext());
                node.setNext(null);
            }
            else if (node.getPrev() != null && node.getNext() == null){
                node.getPrev().setNext(null);

                add(node.getPrev());
                node.setPrev(null);
            }
            else {
                node.getPrev().setNext(null);
                node.getNext().setPrev(null);

                add(node.getPrev());
                add(node.getNext());
                node.setPrev(null);
                node.setNext(null);
            }
        }
        else {
            Node curNode = initNode;
            boolean brk = false;
            while (!brk){
                // its ALWAYS working in ascending order, it just changes depending on where init node has been set
                int curEval = lowerOrUpper(curNode, node);
                switch (curEval){
                    case -3:
                        curNode = curNode.getPrev();
                        break;
                    case -2:
                        brk = true;
                        node.setPrev(curNode.getPrev());
                        curNode.getPrev().setNext(node);
                        node.setNext(node);
                        curNode.setPrev(node);
                        break;
                    case -1:
                        brk = true;
                        curNode.setPrev(node);
                        node.setNext(curNode);

                        if (asc){
                            initNode = node;
                        }
                        // dont forget to change initnode etc

                        break;
                    case 0:
                        brk = true;
                        // nothing should be done if an equivalent is spotted
                        break;
                    case 1:
                        brk = true;
                        curNode.setNext(node);
                        node.setPrev(curNode);
                        // dont forget to change initnode etc
                        if (!asc){
                            initNode = node;
                        }
                        break;
                    case 2:
                        brk = true;
                        node.setNext(curNode.getNext());
                        curNode.getNext().setPrev(node);
                        node.setPrev(curNode);
                        curNode.setNext(node);
                        break;
                    case 3:
                        curNode = curNode.getNext();
                        break;
                }
            }
        }

        // to be implemented
    }

    // original
    public int lowerOrUpper(Node n, Node i){
//        int queryNode = n.getString().toUpperCase().toCharArray()[0]; // there must be a more intuitive way about this?
//        int subjectNode = i.getString().toUpperCase().toCharArray()[0];
        String queryNode = n.getString();
        String subjectNode = i.getString();
        // variables purely there for format + pretty
        return evaluate(n, queryNode, subjectNode);
    }

    // -3 = go a node previous
    // -2 = place on previous pointer, but the pointer's not null
    // -1 = place on previous pointer
    // 0 = equivalence, so just swap out the pointers.
    // 1 = place on next pointer
    // 2 = place on next pointer, but the pointer's not null
    // 3 = go a node next

    // there is an issue here with the fact that a case where if there are two nodes
    //
    public int evaluate(Node n, String q, String s){
        if (q.compareToIgnoreCase(s) > 0){
            if (n.getPrev() != null && n.getPrev().getString().compareToIgnoreCase(s) > 0) { return -3; }
            else if (n.getPrev() != null) { return -2; }
            else { return -1; }
        }
        else if (q.compareToIgnoreCase(s) < 0) {
            if (n.getNext() != null && n.getNext().getString().compareToIgnoreCase(s) < 0) { return 3; }
            else if (n.getNext() != null) { return 2; }
            else { return 1; }
        }
        else { return 0; }
    }

    @Override
    public Node getFirst() {
        // the first item, given an order
        if (size() == 0){
            return null;
        }
        return initNode;
    }

    @Override
    public Node getLast() {
        // the last item
        if (size() == 0){
            return null;
        }

        Node curNode = initNode;
        if (asc){
            while (true){
                if (curNode.getNext() == null){
                    return curNode;
                }
                curNode = curNode.getNext();
            }
        }

        else {
            while (true){
                if (curNode.getPrev() == null){
                    return curNode;
                }
                curNode = curNode.getPrev();
            }
        }
    }

    @Override
    public Node get(int index) {
        // get the node at a given index
        // im assuming its zero indexed
        // exception bait: too little or invalid
        if (initNode.getString().equals("nullInitNode")){
            return null;
        }
        if (size() <= index || index < 0){
            return null;
        }
        if (index == 0){
            return getFirst();
        }
        Node curNode = initNode;
        if (asc){
            while (true){
                index -= 1;
                curNode = curNode.getNext();
                if (index == 0){
                    return curNode;
                }
            }
        }

        else{
            while (true){
                index -= 1;
                curNode = curNode.getPrev();
                if (index == 0){
                    return curNode;
                }
            }
        }

        // TO BE IMPLEMENTED
    }

    @Override
    public boolean isPresent(String string) {
        // is the node present? given a string
        if (size() == 0) { return false; }

        Node curNode = initNode;
        while (true){
            if (asc){
                if (curNode.getString().equalsIgnoreCase(string)) { return true; }
                // ignore the case because case seems to only be for formatting here
                else{
                    if (curNode.getNext() != null){
                        curNode = curNode.getNext();
                    }
                    else { return false; }
                }
            }

            if (!asc){ // if descending
                if (curNode.getString().equalsIgnoreCase(string)) { return true; }
                else{
                    if (curNode.getPrev() != null){
                        curNode = curNode.getPrev();
                    }
                    else { return false; }
                }

            }
        }
    }

    @Override
    public boolean removeFirst() {
        // as it says
        // exception bait: empty
        if (size() == 0){
            return false;
        }
        if (size() == 1){
            initNode.setString("nullInitNode"); // default / empty state.
            return true;
        }

        if (asc){
            initNode = initNode.getNext();
            initNode.setPrev(null);
        }
        if (!asc){
            initNode = initNode.getPrev();
            initNode.setNext(null);
        }

        return true;
    }

    @Override
    public boolean removeLast() {
        // as it says
        // excception bait: empty
        Node curNode = initNode;
        if (size() == 0){
            return false;
        }
        if (size() == 1){
            initNode.setString("nullInitNode");
            return true;
        }

        while (true){
            if (asc){
                if (curNode.getNext() != null) {
                    curNode = curNode.getNext();
                }
                else{
                    curNode.getPrev().setNext(null);
                    return true;
                }
            }
            if (!asc){
                if (curNode.getPrev() != null){
                    curNode = curNode.getPrev();
                }
                else {
                    curNode.getNext().setPrev(null);
                    return true;
                }
            }
        }
    }

    @Override
    public boolean remove(int index) {
        // as it says
        // exception bait: not present
        if (get(index) == null){
            return false;
        }

        if (index == 0){
            initNode = asc ? initNode.getNext() : initNode.getPrev();
            if (asc){
                initNode.setPrev(null);
            }
            else{
                initNode.setNext(null);
            }
            return true;
        }

        Node removeNode = get(index);
        if (removeNode.getPrev() == null){
            removeNode.getNext().setPrev(null);
            return true;
        }

        else if (removeNode.getNext() == null) {
            removeNode.getPrev().setNext(null);
            return true;
        }

        else{
            Node ahead = removeNode.getNext();
            Node behind = removeNode.getPrev(); // these are here purely for clarity

            ahead.setPrev(behind);
            behind.setNext(ahead);

            return true;
        }
        // TO BE IMPLEMENTED
    }

    @Override
    public boolean remove(String string) {
        // as it says
        // exception bait: not present
        if (!isPresent(string)){
            return false;
        }
        int counter = 0;
        Node curNode = initNode;
        while (true){
            if (curNode.getString().equalsIgnoreCase(string)){
                return remove(counter);
            }
            curNode = asc ? curNode.getNext() : curNode.getPrev();
            counter++;
        }
    }

    // these are the two that determine the order in which everything else goes
    @Override
    public void orderAscending() {
        // as it says
        if (!asc){
            initNode = getLast();
            asc = true;
        }
        // TO BE IMPLEMENTED
    }

    @Override
    public void orderDescending() {
        // as it says
        // all this will do is set the initnode to the end and change a variable that'll treat
        // the list differently.
        if (asc){
            initNode = getLast();
            asc = false;
        }
        // TO BE IMPLEMENTED
    }

    @Override
    public void print() {
        // prints the ocntents of hte linked list in the specified alphabetical order
        // each node's string on a new line
        Node curNode = initNode;
        while (curNode != null){
            System.out.println(curNode.getString());
            if (asc){
                curNode = curNode.getNext();
            }
            else {
                curNode = curNode.getPrev();
            }
        }
    }
}

void main() {

    /*
    Possible exceptionbaits:
    - not an alphabetical character being entered.
     */
    // node has two pointers back and forth and a name
    // you link them via the constructor
    // set string and get string set and get the name
    // same with set/get next/prev

    Node jay = new Node("J");
    Node eff = new Node(jay, "F");
    Node emm = new Node("M", eff);
    jay.setNext(eff);
    jay.setPrev(emm);
    SortedLinkedList sLL = new SortedLinkedList();

    System.out.println(sLL.size());
    sLL.add("Z");
    sLL.add("L");
    sLL.add("what's uppppppp");
    sLL.add("hi!");
    sLL.add("hello");
    sLL.add("bartholomew");
    sLL.add("1");
    sLL.add("c");
    sLL.add("A");
    sLL.add("Burundi");
    sLL.add("a"); // this should not be added because of A
    sLL.add("B");
    sLL.add("j");
    sLL.add("Y");
    sLL.add(jay);
    sLL.print();
//    System.out.println(sLL.size());
    System.out.println();


}


/*
Store strings alphabetically in a doubly linked list. The SortedLinkedList class should store strings alphabetically
(by default this should be in ascending order) and should implement a SortedList interface (available here).

Rules:
    - Your implementation must use the doubly linked list structure using the Node class
    - Strings will only contain alphabetic characters (i.e., A-Z and a-z)
    - No duplicate words should be allowed (case insensitive), e.g., if "HELLO" is in the list "hello" would not be allowed
    - You are not allowed to modify the SortedList interface or the Node class
    - You are not allowed to import any libraries or fully-qualified names of additional classes for this question
    - You are not allowed to use any other underlying data structures (including but not limited to arrays, ArrayLists, LinkedList) for your linked list other than the Node class provided
    - Your code will be tested using methods from the SortedList interface
*/