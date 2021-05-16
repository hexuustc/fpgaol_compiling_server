module top
(
	input CLK,
	input [15:0]sw,
	output [15:0]LED
);
	assign LED[0] = sw[0];
	wire clk1, clk2, clk3;
	clk_wiz_0 clk_wiz_0_inst
	(
		.clk_in1(CLK),
		.clk_out1(clk1),
		.clk_out2(clk2),
		.clk_out3(clk3)
	);

	reg [31:0]cnt1 = 0;
	reg [31:0]cnt2 = 0;
	reg [31:0]cnt3 = 0;
	always @ (posedge clk1) begin
		cnt1 <= cnt1 + 1;
	end
	always @ (posedge clk2) begin
		cnt2 <= cnt2 + 1;
	end
	always @ (posedge clk3) begin
		cnt3 <= cnt3 + 1;
	end
	assign LED[1] = cnt1[22];
	assign LED[2] = cnt2[22];
	assign LED[3] = cnt3[22];
	assign LED[4] = cnt1[20];
	assign LED[5] = cnt2[20];
	assign LED[6] = cnt3[20];
endmodule
