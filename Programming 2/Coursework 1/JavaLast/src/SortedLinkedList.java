public class SortedLinkedList implements SortedList {
    boolean asc = true; // this is inherent; the default. it is dsc when false
    Node initNode = new Node ("initNode");
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

        String initialName = initNode.getString();
        Node curNode = initNode;

        while (true){
            if (curNode.getNext() != null && !curNode.getNext().getString().equals(initialName)){
                curNode = curNode.getNext();
                counter += 1;
            }
            else {
                break;
            }
            // forwards
        }

        while (true){
            if (curNode.getPrev() != null && !curNode.getPrev().getString().equals(initialName)){
                curNode = curNode.getPrev();
                counter += 1;
            }
            else {
                break;
            }
            // backwards
        }

        return counter == 1 && initNode.getString().equals("initNode") ? 0 : counter;
    }

    @Override
    public void add(String string) {
        // add a node with a string to the linked list (in the appropriate order)
        if (size() == 0){ // if its just init node
            initNode.setString(string);
        }

        if (asc){

        }
        else{

        }


        // to be implemented
    }

    @Override
    public void add(Node node) {
        if (size() == 0){ // if its just init node
            initNode = node;
        }
        else {
            Node curNode = initNode;
            boolean brk = false;
            while (!brk){
                int curEval = lowerOrUpper(curNode, node);
                switch (curEval){
                    case -2:
                        curNode = curNode.getPrev();
                        break;
                    case -1:
                        brk = true;
                        break;
                    case 0:
                        brk = true;
                        // swap out the pointers


                        // ^^ here
                        break;
                    case 1:
                        brk = true;
                        break;
                    case 2:
                        curNode = curNode.getNext();
                        break;
                }
            }
        }

        // to be implemented
    }

    // overload!
    public int lowerOrUpper(Node n, String i){
        int queryNode = n.getString().toCharArray()[0]; // there must be a more intuitive way about this?
        int subjectNode = i.toCharArray()[0];
        // variables purely there for format + pretty
        return evaluate(n, queryNode, subjectNode);
    }


    public int lowerOrUpper(Node n, Node i){
        int queryNode = n.getString().toCharArray()[0]; // there must be a more intuitive way about this?
        int subjectNode = i.getString().toCharArray()[0];
        // variables purely there for format + pretty
        return evaluate(n, queryNode, subjectNode);
    }
    // -2 = go a node previous
    // -1 = place on previous pointer
    // 0 = equivalence, so just swap out the pointers.
    // 1 = place on next pointer
    // 2 = go a node next

    // there is an issue here with the fact that a case where if there are two nodes
    //
    public int evaluate(Node n, int q, int s){
        if (q > s){
            if (n.getPrev() != null) { return -2; }
            else { return -1; }
        }
        else {
            if (q < s) {
                if (n.getNext() != null) { return 2; }
                else { return 1; }
            }
            else { return 0; }
        }
    }

    @Override
    public Node getFirst() {
        // the first item, given an order

        return null;
    }

    @Override
    public Node getLast() {
        // the last item

        return null;
    }

    @Override
    public Node get(int index) {
        // get the node at a given index
        // exception bait: too little or invalid

        // TO BE IMPLEMENTED
        return null;
    }

    @Override
    public boolean isPresent(String string) {
        // is the node present? given a string
        if (size() == 0) { return false; }

        Node curNode = initNode;
        while (true){
            if (asc){ // if ascending
                if (curNode.getString().equals(string)) { return true; }
                else{
                    if (curNode.getNext() != null){
                        curNode = curNode.getNext();
                    }
                    else { return false; }
                }
            }

            if (!asc){ // if descending
                if (curNode.getString().equals(string)) { return true; }
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
            initNode.setString("initNode"); // default / empty state.
            return true;
        }

        // TO BE IMPLEMENTED
        return false;
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
            initNode.setString("initNode");
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


        // TO BE IMPLEMENTED



        return true; // a boolean ? really?? what is this lol
    }

    @Override
    public boolean remove(String string) {
        // as it says
        // exception bait: not present
        if (!isPresent(string)){
            return false;
        }

        // TO BE IMPLEMENTED

        return true;
    }

    // these are the two that determine the order in which everything else goes
    @Override
    public void orderAscending() {
        // as it says
        asc = true;

        // TO BE IMPLEMENTED
    }

    @Override
    public void orderDescending() {
        // as it says
        // all this will do is set the initnode to the end and change a variable that'll treat
        // the list differently.
        asc = false;

        // TO BE IMPLEMENTED
    }

    @Override
    public void print() {
        // prints the ocntents of hte linked list in the specified alphabetical order
        // each node's string on a new line



        // TO BE IMPLEMENTED
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

    /*
    // messing about
    Node zee = new Node ("Z");
    Node ayy = new Node("A");
    Node bee = new Node("B");
    ayy.setPrev(zee); // bit tedious that it doesnt set both ways, you've to manually do it
    zee.setNext(ayy);
    ayy.setNext(bee);
    bee.setPrev(ayy);
     */

    SortedLinkedList sLL = new SortedLinkedList();
    System.out.println(sLL.size());
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