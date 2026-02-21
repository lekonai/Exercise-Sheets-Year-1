public class SortedLinkedList implements SortedList {
    boolean asc = false; // this is inherent, so maybe it should be inherently true.
    boolean dsc = false;
    Node initNode = new Node ("initNodeEmpty");

    @Override
    public int size() {
        // number of nodes in a linked list
        String initialName = "";
        int counter = 1; // there'll always be one
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

        return counter == 0 && initNode.getString().equals("initNodeEmpty") ? 0 : counter;
    }

    @Override
    public void add(String string) {
        // add a node with a string to the linked list (in the appropriate order)
        if (size() == 1 && initNode.getString().equals("initNode")){
            initNode.setString(string);
        }



        // to be implemented
    }

    @Override
    public void add(Node node) {
        if (size() == 1 && initNode.getString().equals("initNode")){
            initNode = node;
        }
        Node curNode = initNode;
        else {

        }

        // to be implemented
    }

    // overload!
    // -2 = go a node previous
    // -1 = place on previous pointer
    // 0 = equivalence, so just swap out the pointers.
    // 1 = place on next pointer
    // 2 = go a node next
    public int lowerOrUpper(Node n, String i){
        if (n.getString().toCharArray()[0] > i.toCharArray()[0]){
            if (n.getPrev() != null){
                return -2;
            }
            else {
                return -1;
            }
        }
    }

    public int lowerOrUpper(Node n, Node i){

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

        return null;
    }

    @Override
    public boolean isPresent(String string) {
        // is the node present? given a string

        return false;
    }

    @Override
    public boolean removeFirst() {
        // as it says

        return false;
    }

    @Override
    public boolean removeLast() {
        // as it says

        return false;
    }

    @Override
    public boolean remove(int index) {
        // as it says

        return false;
    }

    @Override
    public boolean remove(String string) {
        // as it says

        return false;
    }

    @Override
    public void orderAscending() {
        // as it says

    }

    @Override
    public void orderDescending() {
        // as it says

    }

    @Override
    public void print() {
        // prints the ocntents of hte linked list in the specified alphabetical order
        // each node's string on a new line
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
    Node zee = new Node ("Z");
    Node ayy = new Node("A");
    Node bee = new Node("B");
    ayy.setPrev(zee); // bit tedious that it doesnt set both ways, you've to manually do it
    zee.setNext(ayy);
    ayy.setNext(bee);
    bee.setPrev(ayy);

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