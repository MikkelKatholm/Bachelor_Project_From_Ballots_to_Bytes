import java.util.ArrayList;
import java.util.Collections;


public class Main {

    public static void main(String[] args) {
        int numberOfParties = 3;

        // make 3 parties
        ArrayList<Parti> partis = makeParties(numberOfParties);

        // generate and split the secret
        for (Parti parti : partis) {
            parti.splitSecret(numberOfParties);
        }

        // distribute shares of each party to all other parties
        distributeShares(partis);

        // calculate s
        ArrayList<Integer> s = calculateS(partis);

        // calculate final vote
        ArrayList<Integer> finalVotes = new ArrayList<>();
        for (Parti parti : partis) {
            finalVotes.add(parti.calculateFinalVote(s));
        }

        // Check if all voters agree
        boolean allEqual = finalVotes.stream().distinct().limit(2).count() <= 1;
        String msg = allEqual ? "All voters agree on " + finalVotes.get(0) : "Voters disagree";
        System.out.println(msg);
    }

    private static ArrayList<Parti> makeParties(int n){
        ArrayList<Parti> partis = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            int vote = (i % 2 == 0) ? 1 : 0; // 1 for even, 0 for odd
            partis.add(new Parti(vote));
        }
        return partis;
    }

    private static void distributeShares(ArrayList<Parti> partis){
        // i is parties that send shares
        for (int i = 0; i<partis.size(); i++){ //clients
            ArrayList<Integer> shares = partis.get(i).getSharesOfOwnSecret();
            // j is parties that receive shares
            for (int j = 0; j<partis.size(); j++){
                    //send all shares except jth share to jth party
                    ArrayList<Integer> sharesToSend = new ArrayList<>(shares);
                    sharesToSend.set(j,0);
                    partis.get(j).addSharesOfOtherSecret(sharesToSend);
            }
        }
    }

    private static ArrayList<Integer> calculateS(ArrayList<Parti> partis){
        int numOfParties = partis.size();
        ArrayList<ArrayList<Integer>> tempS = new ArrayList<>();
        ArrayList<Integer> sFromParti;

        for (int i = 0; i < numOfParties; i++) {
            ArrayList<ArrayList<Integer>> partiShares = partis.get(i).getSharesOfOtherSecret();
            System.out.println(partiShares);
            sFromParti = partis.get(i).calculateS(partiShares);
            tempS.add(sFromParti);
        }
        System.out.println(tempS);
        ArrayList<Integer> s = new ArrayList<>(Collections.nCopies(numOfParties,0));
        for (int i = 0; i<numOfParties; i++){
            for (int j = 0; j<s.size(); j++){
                int toAdd = Math.max(s.get(i),tempS.get(j).get(i));
                s.set(i,toAdd);
            }
        }
        return s;
    }
}
