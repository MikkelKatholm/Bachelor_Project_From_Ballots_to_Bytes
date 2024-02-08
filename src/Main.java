public class test {

    private String text;

    public test(String text) {
        this.text = text;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public void main(String[] args){
        setText("hej");
        System.out.println(getText());
    }

}
