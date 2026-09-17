`default_nettype none


module tt_um_counter(
    input wire clk,
    input wire rst_n,
    input wire oe,
    input wire [7:0] in,
    input wire load,
    output wire [7:0] count
);
  reg [7:0] count_reg;
  
    always @(posedge clk or negedge rst_n) begin
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
  assign count = oe ? count_reg : 8'bz;
endmodule
