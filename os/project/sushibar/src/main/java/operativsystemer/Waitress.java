package operativsystemer;

/**
 * This class implements the consumer part of the producer/consumer problem.
 * One waitress instance corresponds to one consumer.
 */
public class Waitress implements Runnable {

    private WaitingArea waitingArea;

    /**
     * Creates a new waitress. Make sure to save the parameter in the class
     *
     * @param waitingArea The waiting area for customers
     */
    Waitress(WaitingArea waitingArea) {
        this.waitingArea = waitingArea;
    }

    /**
     * This is the code that will run when a new thread is
     * created for this instance
     */
    @Override
    public void run() {
        
        try {
            while (SushiBar.isOpen && !waitingArea.isEmpty()) {
                Customer customer = waitingArea.next();
                Thread.sleep(SushiBar.waitressWait);
                customer.order();
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }


}

