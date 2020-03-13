package operativsystemer;

public class Statistics {

    private int totalOrders;
    private int eatenOrders;
    private int takeawayOrders;
    private int numOfCustomers;

    public synchronized void addOrders(int totalOrders, int eatenOrders, int takeawayOrders) {
        this.totalOrders += totalOrders;
        this.eatenOrders += eatenOrders;
        this.takeawayOrders += takeawayOrders;
    }

    public int getTotalOrders() {
        return totalOrders;
    }

    public int getEatenOrders() {
        return eatenOrders;
    }

    public int getTakeawayOrders() {
        return takeawayOrders;
    }

    public int getNumOfCustomers() {
        return numOfCustomers;
    }

    public synchronized void customerVisited() {
        this.numOfCustomers++;
    }

}