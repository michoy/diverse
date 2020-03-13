package operativsystemer;

import java.util.concurrent.ArrayBlockingQueue;

/**
 * This class implements a waiting area used as the bounded buffer, in the
 * producer/consumer problem.
 */
public class WaitingArea {

    private ArrayBlockingQueue<Customer> buffer;

    /**
     * Creates a new waiting area.
     * It uses a local buffer that is implemented via a synchronous array que 
     * with fixed size and fairness set to true.
     * Fairness ensures that accessing threads get access in a FIFO manner and 
     * it prevents starvation. 
     *
     * @param size The maximum number of Customers that can be waiting.
     */
    public WaitingArea(int size) {
        buffer = new ArrayBlockingQueue<>(size, true); 
    }

    /**
     * This method should put the customer into the waitingArea
     *
     * @param customer A customer created by Door, trying to enter the waiting area
     * @throws InterruptedException if interrupted while waiting
     */
    public void enter(Customer customer) throws InterruptedException {
        SushiBar.write(Thread.currentThread(), customer, "waiting");
        buffer.put(customer);
        SushiBar.statistics.customerVisited();
    }

    /**
     * @return The customer that is first in line.
     * @throws InterruptedException if interrupted while waiting
     */
    public Customer next() throws InterruptedException {
        return buffer.take();
    }

    public boolean isEmpty() {
        return buffer.isEmpty();
    }
}
