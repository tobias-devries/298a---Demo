`default_nettype none


module counter(
    input wire clk,
    input wire rst_n,
    input oe,
    input wire [7:0] in,
    input wire load,
    output reg [7:0] count
);
  reg [7:0] count_reg;
  
  always @(posedge clk and negedge rst_n) begin
      if(!rst_n) begin
        count_reg <= 8'd0;
      end else begin
      if(load)begin
         count_reg <= in;
      end else begin
        count_reg <= count_reg + 1'b1;
      end
    end
  end
  assign count = oe ? count_reg : 8'bzzzzzzz;
endmodule
