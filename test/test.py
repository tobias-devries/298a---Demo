import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge


@cocotb.test()
async def test_counter_full(dut):
    """Test all features of the 8-bit programmable counter."""

    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut._log.info("Starting Counter Cocotb Test...")

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 2)

    assert dut.uo_out.value == 0, (
        f"Reset failed! Expected 0, got {dut.uo_out.value}"
    )

    # Release reset
    dut.rst_n.value = 1

    # Wait until we're safely away from a rising edge
    await FallingEdge(dut.clk)

    # Load 50
    test_load_val = 50
    dut._log.info(f"Loading parallel value: {test_load_val}")

    dut.ui_in.value = test_load_val
    dut.uio_in.value = 1

    # Rising edge samples the load signal
    await ClockCycles(dut.clk, 1)

    # Disable load
    dut.uio_in.value = 0

    # Verify loaded value
    assert dut.uo_out.value == test_load_val, (
        f"Load failed! Expected {test_load_val}, got {dut.uo_out.value}"
    )

    # Up-counting
    dut._log.info("Testing sequential up-counting...")

    await ClockCycles(dut.clk, 5)

    expected_val = test_load_val + 5

    assert dut.uo_out.value == expected_val, (
        f"Counting failed! Expected {expected_val}, got {dut.uo_out.value}"
    )

    # Overflow
    dut._log.info("Testing overflow wrap-around...")

    # Change inputs away from the sampling edge
    await FallingEdge(dut.clk)

    dut.ui_in.value = 255
    dut.uio_in.value = 1

    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value == 255, (
        f"255 load failed! Expected 255, got {dut.uo_out.value}"
    )

    dut.uio_in.value = 0

    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value == 0, (
        f"Overflow failed! Expected 0, got {dut.uo_out.value}"
    )

    dut._log.info("All counter tests passed successfully!")
