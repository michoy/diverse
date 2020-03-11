package operativsystemer;

import java.util.UUID;

/**
 * This class implements a customer, which is used for holding data and update
 * the statistics
 */
public class Customer {

    private UUID id;

    /**
     * Creates a new Customer. Each customer should be given a unique ID
     */
    public Customer() {
        id = UUID.randomUUID();
    }

    /**
     * Here you should implement the functionality for ordering food as described in
     * the assignment.
     */
    public void order() {
        try {
            Thread.sleep(SushiBar.customerWait);    // customer eats
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    /**
     *
     * @return customerID as UUID
     */
    public UUID getCustomerID() {
        return id;
    }
    // Add more methods as you see fit.
}
