package operativsystemer;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashSet;
import java.util.concurrent.ArrayBlockingQueue;


public class SushiBar {
    // SushiBar settings.
    private static int waitingAreaCapacity = 20;
    private static int waitressCount = 7;
    private static int duration = 5;
    public static int maxOrder = 15;
    public static int waitressWait = 60;    // Used to calculate the time the waitress spends before taking the order
    public static int customerWait = 2500;  // Used to calculate the time the customer spends eating
    public static int doorWait = 120;       // Used to calculate the interval at which the door tries to create a customer
    public static boolean isOpen = true;
    public static ArrayBlockingQueue<Integer> ids;

    // Creating log file.
    private static File log;
    private static String path = "./";

    // Variables related to statistics.
    public static Statistics statistics;


    public static void main(String[] args) {

        log = new File(path + "log.txt");
        statistics = new Statistics();

        // initialize pool of ids
        int limit = 10000;
        ids = new ArrayBlockingQueue<>(limit);  // risky: if emptied, door will be waiting indefinetly
        for (int i=1; i<limit; i++) ids.add(i);

        // initialize waiting area
        WaitingArea waitingArea = new WaitingArea(waitingAreaCapacity);

        // create threads
        HashSet<Thread> waitressThreads = new HashSet<>();
        for (int i=0; i<waitressCount; i++) {
            waitressThreads.add(new Thread(new Waitress(waitingArea)));
        }
        Thread doorThread = new Thread(new Door(waitingArea));
        
        // start threads and the clock
        for (Thread waitressThread : waitressThreads) {
            waitressThread.start();
        }
        new Clock(duration);  // start clock timer right before door opens
        doorThread.start();

        // wait for all threads to finish
        try {
            doorThread.join();
            SushiBar.write("**** DOOR CLOSED ****");

            for (Thread thread : waitressThreads) {
                thread.join();
            }
            
            SushiBar.write("**** NO MORE CUSTOMERS - SHOP IS CLOSED ****");
            SushiBar.write("Total orders: " + String.valueOf(statistics.getTotalOrders()));
            SushiBar.write("Takeaway orders: " + String.valueOf(statistics.getTakeawayOrders()));
            SushiBar.write("Eaten orders: " + String.valueOf(statistics.getEatenOrders()));
            SushiBar.write("Customers served: " + String.valueOf(statistics.getNumOfCustomers()));
            SushiBar.write("Time open: " + String.valueOf(duration) + " seconds");
            
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    // Writes actions in the log file and console.
    public static void write(String str) {
        try {
            FileWriter fw = new FileWriter(log.getAbsoluteFile(), true);
            BufferedWriter bw = new BufferedWriter(fw);
            bw.write(Clock.getTime() + ", " + str + "\n");
            bw.close();
            System.out.println(Clock.getTime() + ", " + str);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void write(Thread thread, Customer customer, String activity) {

        String id = String.valueOf(customer.getCustomerID());
        String str = thread.getName() + ": Customer " + id + " is now " + activity;

        try {
            FileWriter fw = new FileWriter(log.getAbsoluteFile(), true);
            BufferedWriter bw = new BufferedWriter(fw);
            bw.write(Clock.getTime() + ", " + str + "\n");
            bw.close();
            System.out.println(Clock.getTime() + ", " + str);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
