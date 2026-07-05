module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/phoenix_gpu.fst");
    $dumpvars(0, phoenix_gpu);
end
endmodule
