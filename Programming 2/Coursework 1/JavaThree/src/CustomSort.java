import java.util.ArrayList; // this is redundant but include it in the submission

public class CustomSort implements SortingInterface {
    private ArrayList<Double> values = new ArrayList<>();

    public void setValues(ArrayList<Double> values){
        // sets and sorts the values provided in ascending order
        if (values == null){
            return;
        }
        this.values = values; // remember its setting it not adding them all on
        sort();
    }

    public ArrayList<Integer> getGaps(){
        // returns the gaps used by the sorting algorithm
        // what is a gap ?
        // values are already defined within the class

        // can't edit. remember

        ArrayList<Integer> temp = new ArrayList<>();
        ArrayList<Integer> gaps = new ArrayList<>();
        int n = values.size();
        int gap = 1;
        int i = 2;
        while (gap < n){
            temp.add(gap);
            gap = (int)(Math.pow(2, i) - 1);
            i++;
        }
        for (i = (temp.size() - 1); i >= 0; i--){
            gaps.add(temp.get(i));
        }
        return gaps;
    }

    public void add(Double value){
        // adds a value to the sorted arraylist ! ! in ascending order ! !
        if (value == null){
            return;
        }
        values.add(value);
        sort();
    }

    public void remove(int index){
        // removes a value at the specified index from the sorted arraylist
        if (index < 0 || index >= values.size()){
            // silently ignore the edge case whatever
            return;
        }
        values.remove(index);
        sort();
    }

    public void sort(){
        // sorts arraylist in ascending order
        // can't edit. remember
        int n = values.size();
        ArrayList<Integer> gaps = getGaps();
        for (Integer gap : gaps){
            for (int i = gap; i < n; i++){
                Double temp = values.get(i);
                int j = 0;
                for (j = i; j >= gap; j -= gap){
                    if (values.get(j - gap) <= temp){
                        break;
                    }
                    values.set(j, values.get(j - gap));
                }
                values.set(j, temp);
            }
        }
    }

    // there's no print function? how on earth is the automarker going to know what's right or not??

    // debug function
    public void print(){ System.out.println(values); }
    // debug function

}

void main(){
    CustomSort listy = new CustomSort();
    listy.setValues(new ArrayList<Double>(Arrays.asList(4.2,5.6,2.4,9.2)));
    listy.print();
    listy.add(-3.2);
    listy.print();
}
/*
    The values contained in the array lists should be sorted in ascending order OK
    You are only allowed to use the above pseudoalgorithm for sorting - failure to do so will result in 0 marks OK
    You are only allowed to use the following import statement: import java.util.ArrayList; OK
    You are not allowed to use any other import statements or fully-qualified names of additional classes OK

// PSEUDOCODE IS AS FOLLOWS:

function calculate_gaps(values):
    temp = [], gaps = []
    n = length_of(values)
    gap = 1, i = 2
    while gap is less than n:
        add gap to temp
        gap = (2 to the power of i) - 1
        i+=1
    for i from (length_of(temp) - 1) to 0 in decrements of 1: // the semantics here is infuriating
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