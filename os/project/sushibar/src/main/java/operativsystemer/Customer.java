package operativsystemer;

import java.util.Random;

/**
 * This class implements a customer, which is used for holding data and update
 * the statistics
 */
public class Customer {

    private int id;
    private Random random;

    /**
     * Creates a new Customer. Each customer should be given a unique ID
     * 
     * @throws InterruptedException
     */
    public Customer() throws InterruptedException {
        id = SushiBar.ids.take();
        random = new Random();
    }

    /**
     * Here you should implement the functionality for ordering food as described in
     * the assignment.
     */
    public void order() {
        try {
            // generate orders
            // +1 to omit the case where it is 0, since nextInt(0) throws an exception
            int totalOrders = random.nextInt(SushiBar.maxOrder) + 1;
            int eatenOrders = random.nextInt(totalOrders) + 1;
            int takeawayOrders = totalOrders - eatenOrders;
            SushiBar.statistics.addOrders(totalOrders, eatenOrders, takeawayOrders);

            // spend time eating
            Thread.sleep(SushiBar.customerWait);    

        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    /**
     *
     * @return customerID as UUID
     */
    public int getCustomerID() {
        return id;
    }
    // Add more methods as you see fit.
}
