import java.util.ArrayList; // this is redundant but include it in the submission

public class CustomSort implements SortingInterface {
    public void setValues(ArrayList<Double> values){
        // sets and sorts the values provided in ascending order.
    }

    public ArrayList<Integer> getGaps(){
        // returns the gaps used by the sorting algorithm
    }

    public void add(Double value){
        // adds a value to the sorted arraylist in ascending order
    }

    public void remove(int index){
        // removes a value at the specified index from the sorted arraylist
    }

    public void sort(){
        // sorts arraylist in ascending order
    }

}

void main(){

}
/*

    The values contained in the array lists should be sorted in ascending order
    You are only allowed to use the above pseudoalgorithm for sorting - failure to do so will result in 0 marks
    You are only allowed to use the following import statement: import java.util.ArrayList;
    You are not allowed to use any other import statements or fully-qualified names of additional classes

// PSEUDOCODE IS AS FOLLOWS:
function calculate_gaps(values):
    temp = [], gaps = []
    n = length_of(values)
    gap = 1, i = 2
    while gap is less than n:
        add gap to temp
        gap = (2 to the power of i) - 1
        i+=1
    for i from (length_of(temp) - 1) to 0 in decrements of 1:
        add temp[i] to gaps
    return gaps

function sort(values, gaps):

      n = length_of(values)
      gaps = calculate_gaps(values)
      for each gap in gaps:
          for i from gap to (n - 1) in increments of 1:
              temp = values[i]
              j = 0
              for j from i to gap in decrements of gap:
                  if values[j-gap] is less than or equal to temp:
                      break
                  values[j] = values[j - gap]
              values[j] = temp
 */