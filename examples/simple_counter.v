module simple_counter (
    input clk,
    input rst,
    output [3:0] count
);

    // Standard cells (simulated)
    DFF inst_0 (.D(n1), .CLK(clk), .Q(count[0]));
    DFF inst_1 (.D(n2), .CLK(clk), .Q(count[1]));
    DFF inst_2 (.D(n3), .CLK(clk), .Q(count[2]));
    DFF inst_3 (.D(n4), .CLK(clk), .Q(count[3]));

    AND inst_gate_0 (.A(count[0]), .B(rst), .Y(n1));
    OR  inst_gate_1 (.A(count[1]), .B(n1), .Y(n2));

endmodule
