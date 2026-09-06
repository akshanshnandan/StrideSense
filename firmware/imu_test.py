from machine import Pin, I2C
import time
import struct


# ---------------------------------------------------------
# StrideSense - MPU-6050 IMU Test
#
# Raspberry Pi Pico WH + Adafruit MPU-6050
#
# Default wiring:
#   Pico GP0  -> SDA
#   Pico GP1  -> SCL
#   Pico 3V3  -> VIN
#   Pico GND  -> GND
#
# Change SDA_PIN / SCL_PIN below if your wiring is different.
# ---------------------------------------------------------

SDA_PIN = 0
SCL_PIN = 1

MPU6050_ADDR = 0x68

# MPU-6050 register addresses
PWR_MGMT_1 = 0x6B
WHO_AM_I = 0x75

ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43


# Create I2C connection
i2c = I2C(
    0,
    sda=Pin(SDA_PIN),
    scl=Pin(SCL_PIN),
    freq=400000
)


def read_word(register):
    """
    Read a signed 16-bit value from two consecutive MPU-6050 registers.
    """

    data = i2c.readfrom_mem(MPU6050_ADDR, register, 2)

    value = struct.unpack(">h", data)[0]

    return value


def read_acceleration():
    """
    Read acceleration from the X, Y, and Z axes.

    The default MPU-6050 range is +/- 2g.
    At this range, the sensitivity is 16384 LSB per g.
    """

    ax_raw = read_word(ACCEL_XOUT_H)
    ay_raw = read_word(ACCEL_XOUT_H + 2)
    az_raw = read_word(ACCEL_XOUT_H + 4)

    ax = ax_raw / 16384.0
    ay = ay_raw / 16384.0
    az = az_raw / 16384.0

    return ax, ay, az


def read_gyroscope():
    """
    Read angular velocity from the X, Y, and Z axes.

    The default MPU-6050 range is +/- 250 degrees per second.
    At this range, the sensitivity is 131 LSB per degree/second.
    """

    gx_raw = read_word(GYRO_XOUT_H)
    gy_raw = read_word(GYRO_XOUT_H + 2)
    gz_raw = read_word(GYRO_XOUT_H + 4)

    gx = gx_raw / 131.0
    gy = gy_raw / 131.0
    gz = gz_raw / 131.0

    return gx, gy, gz


def initialize_mpu6050():

    print("Scanning I2C bus...")

    devices = i2c.scan()

    if not devices:
        raise RuntimeError("No I2C devices found.")

    print("Devices found:", [hex(device) for device in devices])

    if MPU6050_ADDR not in devices:
        raise RuntimeError(
            "MPU-6050 not detected at address 0x68."
        )

    # Wake the MPU-6050.
    # The sensor starts in sleep mode after power-up.
    i2c.writeto_mem(
        MPU6050_ADDR,
        PWR_MGMT_1,
        bytes([0])
    )

    time.sleep(0.1)

    identity = i2c.readfrom_mem(
        MPU6050_ADDR,
        WHO_AM_I,
        1
    )[0]

    print("WHO_AM_I:", hex(identity))

    if identity != 0x68:
        print(
            "Warning: unexpected WHO_AM_I value:",
            hex(identity)
        )

    print("MPU-6050 initialized.\n")


def main():

    initialize_mpu6050()

    print("Starting sensor readings...")
    print("Press Ctrl+C to stop.\n")

    start_time = time.ticks_ms()

    try:

        while True:

            timestamp = (
                time.ticks_diff(
                    time.ticks_ms(),
                    start_time
                )
                / 1000
            )

            ax, ay, az = read_acceleration()
            gx, gy, gz = read_gyroscope()

            print(
                "t={:.2f}s | "
                "Accel: X={:.3f}g Y={:.3f}g Z={:.3f}g | "
                "Gyro: X={:.2f} Y={:.2f} Z={:.2f} deg/s"
                .format(
                    timestamp,
                    ax,
                    ay,
                    az,
                    gx,
                    gy,
                    gz
                )
            )

            time.sleep(0.1)

    except KeyboardInterrupt:

        print("\nSensor test stopped.")


main()