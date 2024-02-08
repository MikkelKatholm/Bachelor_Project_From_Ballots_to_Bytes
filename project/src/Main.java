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

        // print shares of each party
        for (Parti parti : partis) {
            System.out.println(parti.getSharesOfOwnSecret());
            System.out.println(parti.getSharesOfOtherSecret() + "\n");
        }

        // calculate s
        ArrayList<Integer> s = calculateS(partis);
        System.out.println(s);


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
        for (int i = 0; i<partis.size(); i++){
            ArrayList<Integer> shares = partis.get(i).getSharesOfOwnSecret();
            // j is parties that receive shares
            for (int j = 0; j<partis.size(); j++){
                    //send all shares except jth share to jth party
                    ArrayList<Integer> sharesToSend = new ArrayList<>(shares);
//                    sharesToSend.remove(j);
                    sharesToSend.set(j,0);
                    partis.get(j).addSharesOfOtherSecret(sharesToSend);
            }
        }
    }

    private static ArrayList<Integer> calculateS(ArrayList<Parti> partis){
        ArrayList<Integer> s = new ArrayList<>(Collections.nCopies(partis.size(), 0));

        for (int i = 0; i < partis.size(); i++) {
            ArrayList<Integer> sFromParti = partis.get(i).calculateS(partis.get(i).getSharesOfOtherSecret());
            System.out.println(sFromParti);

        }
        return s;
    }

}
