module sim ();

    reg clk = 0;
	reg [15:0]sw = 0;
	wire [15:0]LED;
    top top_inst
    (
		.CLK(clk),
		.sw(sw),
		.LED(LED)
	);

    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    initial begin
		#4000
        $finish;
    end

endmodule

