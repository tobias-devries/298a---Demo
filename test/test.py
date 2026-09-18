import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Start clock (10us period)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset phase
    dut._log.info("Reset")
    dut.ena.value = 1       # Ensure power enable is set high
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    dut._log.info("Test project behavior")

    # Load 50 into counter:
    # ui_in holds value 50 (0x32)
    # uio_in[0] holds load bit = 1
    dut.ui_in.value = 50
    dut.uio_in.value = 1
    await ClockCycles(dut.clk, 1)

    # Disable load to resume up-counting
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 1)

    # Check loaded output
    assert dut.uo_out.value == 50
