`default_nettype none


module tt_um_counter(
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);
  reg [7:0] count_reg;
    wire load = uio_in [0];
  
    always @(posedge clk or negedge rst_n) begin
      if(!rst_n) begin
        count_reg <= 8'd0;
      end else begin
      if(load)begin
         count_reg <= ui_in;
      end else begin
        count_reg <= count_reg + 1'b1;
      end
    end
  end
  assign uo_out = ena ? count_reg : 8'bz;

    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;
endmodule
