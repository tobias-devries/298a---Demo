`timescale 1ns / 1ps

module tb_counter;

    // Testbench stimulus signals (drive inputs as reg)
    reg       clk;
    reg       rst_n;
    reg       load;
    reg       oe;
    reg [7:0] in;

    // Output bus (monitor outputs as wire)
    wire [7:0] count;

    // Instantiate the Unit Under Test (UUT)
    counter uut (
        .clk(clk),
        .rst_n(rst_n),
        .oe(oe),
        .in(in),
        .load(load),
        .count(count)
    );

    // Clock Generation: 10ns period (100 MHz)
    always #5 clk = ~clk;

    // Test Sequence
    initial begin
        // 1. Initialize Signals
        clk   = 0;
        rst_n = 1;
        load  = 0;
        oe    = 1;
        in    = 8'd0;

        // Display monitor header in console
        $display("--------------------------------------------------");
        $display("Time | rst_n | load | oe |   in   |  count (hex / dec)");
        $display("--------------------------------------------------");
        $monitor("%4t |   %b   |  %b   | %b  | 8'h%h | 8'h%h (%3d)", 
                 $time, rst_n, load, oe, in, count, count);

        // 2. Assert Asynchronous Reset
        #2;
        rst_n = 0; // Trigger reset
        #10;
        rst_n = 1; // Release reset
        #8;

        // 3. Test Up-Counting (Load = 0)
        // Counter should increment on each rising clock edge
        #20;

        // 4. Test Synchronous Load
        // Load preset value (e.g., 8'd50) into counter
        in   = 8'd50;
        load = 1;
        #10;       // Wait for rising edge to load
        load = 0;  // Release load

        // 5. Test Up-Counting from Loaded Value
        #30;

        // 6. Test Tri-State Output Buffer Disable
        oe = 0;    // Output should float to High-Z (8'hzz)
        #20;

        // 7. Re-enable Output Buffer
        oe = 1;    // Output should drive valid counter value again
        #20;

        // 8. Test Asynchronous Reset Mid-Count
        rst_n = 0; // Immediately clears counter to 0 regardless of clk
        #10;
        rst_n = 1;
        #20;

        $display("--------------------------------------------------");
        $display("Simulation Finished Successfully.");
        $finish;
    end

endmodule
