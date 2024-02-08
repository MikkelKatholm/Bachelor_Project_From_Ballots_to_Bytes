import java.util.ArrayList;

public class Parti {
    private int vote;
    private ArrayList<Integer> sharesOfOwnSecret;
    private ArrayList<ArrayList<Integer>> sharesOfOtherSecret;
    private int Z = 5080;
    private int P = 5081;

    public ArrayList<Integer> getSharesOfOwnSecret() {
        return sharesOfOwnSecret;
    }

    public ArrayList<ArrayList<Integer>> getSharesOfOtherSecret() {
        return sharesOfOtherSecret;
    }

    public void addSharesOfOtherSecret(ArrayList<Integer> shares){
        this.sharesOfOtherSecret.add(shares);
    }

    public int getP() {
        return P;
    }

    public Parti(int vote){
        this.vote = vote;
        this.sharesOfOwnSecret = new ArrayList<>();
        this.sharesOfOtherSecret = new ArrayList<>();
    }


    // Split the secret into n shares
    public void splitSecret(int n){
        // pick a random number between 0 and Z
        int preliminaryR = 0;
        for (int i = 0; i < n-1; i++) {
            int r = (int) (Math.random() * Z);
            sharesOfOwnSecret.add(r);
            preliminaryR -= r;
        }
        int rn = ((vote + preliminaryR) % P+P) % P; // (vote - r1 - r2) % P is not enough, because it can be negative
        sharesOfOwnSecret.add(rn);
    }

    public ArrayList<Integer> calculateS(ArrayList<ArrayList<Integer>> sharesOfOtherSecret){
        ArrayList<Integer> s = new ArrayList<Integer>();
        for (int i = 0; i < sharesOfOtherSecret.size(); i++){
            int sum = 0;
            for (int j = 0; j < sharesOfOtherSecret.size(); j++){
                sum += sharesOfOtherSecret.get(j).get(i);
            }
            s.add(sum % P);
        }
        return s;
    }

}
